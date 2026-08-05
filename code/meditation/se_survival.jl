# Survival model for first path / cessation.
#
# Unit of observation: a practice period. A person contributes an ordered
# sequence of them and either attains during one of them or is censored.
#
#	log L_i = a + b_src*web_p + u_p + b_d*log1p(D_i/1000)
#		+ b_h*lh + b_L*ll + b_hL*lh*ll
#	lh = log(h_i/8), ll = log(L_i/10)
#	p(event in period i) = 1 - exp(-L_i)
#
# b_hL is the container effect. It has to be an interaction rather than a main
# effect: with separable log-linear terms the model concludes that a year at
# 2 hr/day beats a month-long retreat, because length is length. Days only
# compound when they are intense and unbroken, which is exactly h x L.
#
# Three further things:
#
# 1. LATENT INTENSITY. 45% of the web-scraped rows have no hours/day. Rather
#    than dropping them or writing in a guess, h is a latent variable with a
#    type-level prior (sesshin, monastic, mahasi, ...) learned from the rows
#    where h *is* stated, partially pooled across types. Uncertainty in h then
#    propagates into b_hL, which matters because b_hL is an interaction in h.
#
# 2. SOURCE OFFSET. Web practice logs over-represent attainers no matter how
#    carefully the sampling frame is drawn -- people who quietly stop logging
#    after four fruitless years leave no legible endpoint. b_src absorbs that
#    into the intercept, so the web data informs the SHAPE (b_h, b_L, b_hL)
#    without dragging the LEVEL up. Predictions for niplav use a alone.
#    With web-only data a and b_src are confounded and b_src is just its
#    prior; it becomes identified once interview rows arrive.
#
# 3. Soft censoring for niplav: he may have attained and not classified it.
#
#
# OUTSTANDING, as of 2026-08-03 (see git log / notes for the reasoning):
#
# - MIXTURE-CURE. Add a susceptible fraction pi: with probability 1-pi a person
#   never attains at any dose. Without it the "plateau at Equanimity" population
#   has nowhere to go and leaks into b_d, which is why b_d fits at -0.61
#   (more prior practice -> lower hazard, which is dynamic selection, not
#   ripening).
# - DO NOT FIT SLOPES TO web_periods.csv. Narrated practice periods have
#   boundaries endogenous to the outcome, and the highest-dose traditions have
#   the strongest taboo on claiming attainment, so the long/intense arm is
#   almost all non-events. Give web rows their own b_h/b_L/b_hL or exclude them.
#   Interview rows collected on a fixed calendar grid are exempt.
# - sigma_u is biased toward zero (0.24 recovered against 0.60 truth), so the
#   model understates between-person variation.
# - No passing recovery check for the latent-intensity version; the n=120
#   synthetic timed out twice. Do not trust b_hL until it passes.
#
#	julia se_survival.jl				fit
#	julia se_survival.jl --synthetic [--n=120]	recovery check

using CSV, DataFrames, Turing, Distributions, Random, Statistics

Random.seed!(20260803)

const PERIODS = joinpath(@__DIR__, "periods_niplav.csv")
const INTERVIEWS = joinpath(@__DIR__, "interviews.csv")
const WEB = joinpath(@__DIR__, "web_periods.csv")

const H_REF = 8.0
const L_REF = 10.0
const P_UNRECOGNISED = 0.1

# Exposure periods are chunked to at most this many days so that a 10-day
# retreat and a 30-year daily-practice era are commensurable. Without it the
# sampler is forced to make b_L negative to stop multi-decade rows predicting
# certain attainment, which flips the whole dose-response. periods.jl already
# chunks niplav's home practice quarterly; the web rows did not get that
# treatment, which is what made the two sources incomparable.
const CHUNK = 90.0

# ===== flat dataset =====

struct Data
	pers::Vector{Int}
	ptype::Vector{Int}
	days::Vector{Float64}
	logh::Vector{Float64}		# observed log h, 0.0 when latent
	miss::Vector{Int}		# 0 if observed, else index into latents
	rows::Vector{Vector{Int}}	# chunk rows per person, chronological
	block::Vector{Int}		# reported-period id, per chunk row
	event::Vector{Int}		# block id of the event, 0 = censored
	known::Vector{Bool}
	soft::Vector{Bool}
	web::Vector{Bool}
	n_type::Int
	n_miss::Int
end

mutable struct Build
	pers::Vector{Int}; ptype::Vector{Int}; days::Vector{Float64}
	logh::Vector{Float64}; miss::Vector{Int}
	rows::Vector{Vector{Int}}; block::Vector{Int}; event::Vector{Int}
	known::Vector{Bool}; soft::Vector{Bool}; web::Vector{Bool}
	types::Dict{String,Int}; n_miss::Int; n_block::Int
end

Build() = Build(Int[], Int[], Float64[], Float64[], Int[], Vector{Int}[], Int[],
	Int[], Bool[], Bool[], Bool[], Dict{String,Int}(), 0, 0)

function add_person!(b::Build, days, hpd, types, ev_idx; known = true,
		soft = false, web = false)
	push!(b.rows, Int[])
	pid = length(b.rows)
	ev_block = 0
	for k in eachindex(days)
		b.n_block += 1
		k == ev_idx && (ev_block = b.n_block)
		tid = get!(b.types, String(types[k]), length(b.types) + 1)
		h = hpd[k]
		ok = !(h === missing || h === nothing) && h isa Number && h > 0
		total = max(Float64(days[k]), 1.0)
		# split into commensurable chunks; they stay grouped by block so an
		# event known only to the reported period is not pinned to a chunk
		# one latent intensity per reported period, shared by its chunks --
		# the source stated (at most) one number, not one per 90 days
		mid = 0
		if !ok
			b.n_miss += 1
			mid = b.n_miss
		end
		while total > 0
			d = min(total, CHUNK)
			total -= d
			push!(b.pers, pid)
			push!(b.ptype, tid)
			push!(b.days, d)
			push!(b.block, b.n_block)
			push!(b.logh, ok ? log(Float64(h)) : 0.0)
			push!(b.miss, mid)
			push!(b.rows[pid], length(b.pers))
		end
	end
	push!(b.event, ev_block)
	push!(b.known, known)
	push!(b.soft, soft)
	push!(b.web, web)
end

finish(b::Build) = Data(b.pers, b.ptype, b.days, b.logh, b.miss, b.rows,
	b.block, b.event, b.known, b.soft, b.web, length(b.types), b.n_miss)

function load_all()
	b = Build()
	df = CSV.read(PERIODS, DataFrame)
	add_person!(b, df.days, df.h_per_day, fill("own", nrow(df)), 0; soft = true)

	for (path, web) in ((INTERVIEWS, false), (WEB, true))
		isfile(path) || continue
		d = CSV.read(path, DataFrame)
		nrow(d) == 0 && continue
		for g in groupby(d, :person)
			g = sort(g, :idx)
			ev = findfirst(x -> !ismissing(x) && x == 1, g.event)
			kn = !hasproperty(g, :outcome_known) ||
				all(x -> ismissing(x) || x == 1, g.outcome_known)
			ty = hasproperty(g, :ptype) ?
				[ismissing(t) ? "unknown" : t for t in g.ptype] :
				fill("unknown", nrow(g))
			dy = [ismissing(x) ? 1 : x for x in g.days]
			add_person!(b, dy, g.h_per_day, ty,
				ev === nothing ? 0 : ev; known = kn, web = web)
		end
	end
	return finish(b)
end

# ===== model =====

log1mexp(x) = x < -0.693 ? log1p(-exp(x)) : log(-expm1(x))

@model function se_model(D)
	a ~ Normal(log(0.1), 1.0)
	b_src ~ Normal(1.0, 0.7)
	sigma_u ~ Exponential(0.5)
	b_d ~ Normal(0.0, 0.5)
	b_h ~ Normal(1.5, 0.7)
	b_L ~ Normal(1.2, 0.5)
	b_hL ~ Normal(0.5, 0.4)
	u_raw ~ filldist(Normal(0, 1), length(D.rows))

	mu0 ~ Normal(log(6.0), 0.7)
	tau_type ~ Exponential(0.5)
	sigma_h ~ Exponential(0.5)
	t_raw ~ filldist(Normal(0, 1), D.n_type)
	h_raw ~ filldist(Normal(0, 1), D.n_miss)

	mt = mu0 .+ t_raw .* tau_type

	# the stated intensities are what teach the type distributions
	for r in eachindex(D.days)
		D.miss[r] == 0 || continue
		# first chunk of the block only, else long eras get counted 100x
		(r == 1 || D.block[r - 1] != D.block[r]) || continue
		Turing.@addlogprob! logpdf(Normal(mt[D.ptype[r]], sigma_h), D.logh[r])
	end

	for p in eachindex(D.rows)
		D.known[p] || continue
		logS = zero(a)
		acc = zero(a)
		blam = zero(a)		# hazard accumulated within the current block
		cur = 0
		hit = false
		for r in D.rows[p]
			if D.block[r] != cur
				if cur == D.event[p] && cur != 0
					Turing.@addlogprob! logS + log1mexp(-blam)
					hit = true
					break
				end
				logS -= blam
				blam = zero(a)
				cur = D.block[r]
			end
			lg = D.miss[r] == 0 ? D.logh[r] :
				mt[D.ptype[r]] + h_raw[D.miss[r]] * sigma_h
			x = lg - log(H_REF)
			ll = log(D.days[r] / L_REF)
			blam += exp(a + b_src * D.web[p] + u_raw[p] * sigma_u +
				b_d * log1p(acc / 1000) +
				b_h * x + b_L * ll + b_hL * x * ll)
			acc += D.days[r] * exp(lg)
		end
		if !hit && cur == D.event[p] && cur != 0
			Turing.@addlogprob! logS + log1mexp(-blam)
			hit = true
		end
		hit && continue
		logS -= blam
		Turing.@addlogprob! D.soft[p] ?
			log((1 - P_UNRECOGNISED) * exp(logS) + P_UNRECOGNISED) : logS
	end
end

# ===== prediction =====

# niplav is person 1. Predictions use a, not a + b_src: we want the hazard for
# someone who actually practises, not for someone who posts about it.
function hours_before(D, extra)
	acc = sum(D.days[r] * exp(D.logh[r]) for r in D.rows[1])
	for e in extra
		acc += e.days * e.h_per_day
	end
	return acc
end

function predict(chain, D, cand, extra = NamedTuple[])
	acc0 = hours_before(D, extra)
	x = log(cand.h_per_day / H_REF)
	ll = log(cand.days / L_REF)
	return [1 - exp(-exp(
		chain[:a][s] + chain[Symbol("u_raw[1]")][s] * chain[:sigma_u][s] +
		chain[:b_d][s] * log1p(acc0 / 1000) +
		chain[:b_h][s] * x + chain[:b_L][s] * ll +
		chain[:b_hL][s] * x * ll)) for s in 1:size(chain, 1)]
end

# ===== export to squiggle =====

function export_squiggle(chain, D, extra, path)
	ns = size(chain, 1)
	take = round.(Int, range(1, ns, length = min(1000, ns)))
	acc0 = hours_before(D, extra)
	cols = Dict(
		"a" => [chain[:a][i] for i in take],
		"b_d" => [chain[:b_d][i] for i in take],
		"b_h" => [chain[:b_h][i] for i in take],
		"b_L" => [chain[:b_L][i] for i in take],
		"b_hL" => [chain[:b_hL][i] for i in take],
		"u" => [chain[Symbol("u_raw[1]")][i] * chain[:sigma_u][i] for i in take],
	)
	open(path, "w") do io
		println(io, "// Generated by se_survival.jl -- do not edit by hand.")
		println(io, "// Cessation hazard conditioned on niplav's practice history")
		println(io, "// ($(round(Int, acc0)) formal hours before the decision point).")
		println(io, "")
		println(io, "posterior = {")
		for k in sort(collect(keys(cols)))
			println(io, "\t$k: SampleSet.fromList([" *
				join((string(round(x, sigdigits = 7)) for x in cols[k]), ",") *
				"]),")
		end
		println(io, "}")
		println(io, "")
		println(io, "@name(\"p(cessation | h hr/day for d days)\")")
		println(io, "pCess(h: [0.1, 16], d: [1, 365]) = {")
		println(io, "\tlh = log(h / $H_REF)")
		println(io, "\tll = log(d / $L_REF)")
		println(io, "\tlam = exp(posterior.a + posterior.u +")
		println(io, "\t\tposterior.b_d * log(1 + $(round(acc0, digits=1)) / 1000) +")
		println(io, "\t\tposterior.b_h * lh + posterior.b_L * ll +")
		println(io, "\t\tposterior.b_hL * lh * ll)")
		println(io, "\t1 - exp(-lam)")
		println(io, "}")
	end
	println("wrote $path ($(length(take)) draws)")
end

# ===== synthetic check =====

function argn(default)
	k = findfirst(a -> startswith(a, "--n="), ARGS)
	return k === nothing ? default : parse(Int, split(ARGS[k], "=")[2])
end

function synthetic()
	n = argn(40)
	th = (a = log(0.10), b_d = 0.2, b_h = 1.5, b_L = 1.3, b_hL = 0.5)
	b = Build()
	nev = 0
	for _ in 1:n
		np = rand(6:24)
		days = Int[]; hpd = Any[]; ty = String[]
		for _ in 1:np
			r = rand() < 0.3
			push!(days, r ? rand(3:30) : rand(30:120))
			push!(hpd, r ? 4 + 8 * rand() : 0.2 + 1.5 * rand())
			push!(ty, r ? "retreat" : "daily")
		end
		u = rand(Normal(0, 0.6))
		ei = 0
		acc = 0.0
		for i in eachindex(days)
			x = log(hpd[i] / H_REF)
			ll = log(days[i] / L_REF)
			lam = exp(th.a + u + th.b_d * log1p(acc / 1000) +
				th.b_h * x + th.b_L * ll + th.b_hL * x * ll)
			if rand() < 1 - exp(-lam)
				ei = i
				break
			end
			acc += days[i] * hpd[i]
		end
		ei > 0 && (nev += 1)
		# blank 45% of intensities, matching the real missingness rate
		for i in eachindex(hpd)
			rand() < 0.45 && (hpd[i] = missing)
		end
		add_person!(b, days, hpd, ty, ei)
	end
	println("synthetic: $nev/$n attained, $(b.n_miss)/$(length(b.days)) blanked")
	println("truth: a=$(round(th.a, digits=3)) b_d=$(th.b_d) b_h=$(th.b_h) " *
		"b_L=$(th.b_L) b_hL=$(th.b_hL) sigma_u=0.6")
	return finish(b)
end

# ===== run =====

function main()
	syn = "--synthetic" in ARGS
	D = syn ? synthetic() : load_all()
	if !syn
		println("$(length(D.rows)) people, $(length(D.days)) periods, " *
			"$(sum(D.web)) web rows, $(sum(.!D.known)) outcome-unknown people")
		println("$(D.n_miss)/$(length(D.days)) intensities latent across " *
			"$(D.n_type) practice types")
	end

	pars = [:a, :sigma_u, :b_d, :b_h, :b_L, :b_hL, :mu0, :sigma_h, :tau_type]
	syn || push!(pars, :b_src)
	chain = sample(se_model(D), NUTS(0.8), 1500; progress = false)
	show(stdout, MIME("text/plain"), summarystats(chain[pars]))
	println()
	show(stdout, MIME("text/plain"), quantile(chain[pars]))
	println()

	syn && return chain

	wales = [(days = 24.0, h_per_day = 10.0)]
	println("\np(cessation | candidate, history, Wales survived, none yet)")
	println("")
	for (lab, c) in [
		("home 2h/day 1yr", (days = 365.0, h_per_day = 2.0)),
		("Nepal 28d @ 12h", (days = 28.0, h_per_day = 12.0)),
		("Nepal 60d @ 12h", (days = 60.0, h_per_day = 12.0)),
		("Nepal 90d @ 10h", (days = 90.0, h_per_day = 10.0)),
		("Nepal 90d @ 12h", (days = 90.0, h_per_day = 12.0)),
	]
		x = predict(chain, D, c, wales)
		println(rpad(lab, 18), " mean ", round(mean(x), digits = 3),
			"  90% CI ", round(quantile(x, 0.05), digits = 3),
			" - ", round(quantile(x, 0.95), digits = 3))
	end
	export_squiggle(chain, D, wales, joinpath(@__DIR__, "posterior.sq"))
	return chain
end

main()
