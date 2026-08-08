# Should I go to Lumbini for three months?
#
# One file, four stages, no intermediate artefacts:
#
#	1. segment data/meditations.csv into practice periods	(was periods.jl)
#	2. fit the cessation survival model on those + the web	(was se_survival.jl)
#	3. carry the posterior into the estimation model	(was posterior.sq)
#	4. price a practice period (h, d) in dollars		(was analysis.sq)
#
# Stage 3 used to be a code generator: se_survival.jl wrote `posterior.sq` full
# of `SampleSet.fromList([...])` literals, and analysis.sq read them. That step
# only existed because Squiggle is a language rather than a library, and it
# failed the way generated files always fail — the checked-in posterior.sq
# carries a "!! VOID -- generated from the pre-chunking fit" banner because
# nobody could rerun it in place. Here the posterior is a Julia value:
#
#	post_a = gek(vec(chain[:a]))
#
# and staleness is not representable.
#
# The Gekrakel half is otherwise a fairly literal transcription of analysis.sq.
# The one substantive change is that p(stream entry | h, d) now comes from the
# fitted hazard rather than from analysis.sq's hand-guessed `seParams`
# dose-response, which was always marked STUB. That is the whole point of
# putting the two halves in one language.
#
#	julia full.jl			fit and price
#	julia full.jl --prior		price off the prior, skipping the fit
#	julia full.jl --quick		400 draws, for checking the plumbing
#	julia full.jl --synthetic	parameter-recovery check on the fit

push!(LOAD_PATH, joinpath(homedir(), "proj/Gekrakel.jl"))

using CSV, DataFrames, Dates, Turing, Distributions, Random, Statistics, Printf
using Gekrakel

Random.seed!(20260808)

const MEDITATIONS = joinpath(homedir(), "proj/site/data/meditations.csv")
const INTERVIEWS = joinpath(@__DIR__, "interviews.csv")
const WEB = joinpath(@__DIR__, "web_periods.csv")

const QUICK = "--quick" in ARGS
const SYNTHETIC = "--synthetic" in ARGS
const DRAWS = QUICK ? 400 : 1500

# --prior draws from the priors and never touches the likelihood, so nothing
# in web_periods.csv can reach the hazard. Use it while the fitted b_L is
# negative: the prior at least has the sign right, being an assertion that
# dose helps rather than an inference that it does not.
#
# This is a prior predictive check and should be read as one. The priors are
# also frankly optimistic — a ~ Normal(log 0.1, 1), b_L ~ Normal(1.2, 0.5) —
# so p(cessation | 12 hr/day for 90 days) comes out near certainty, which is
# a statement about the priors and not about meditation.
const PRIOR = "--prior" in ARGS

# ============================================================================
# 1. Practice periods
# ============================================================================
#
# A practice period is a maximal run of retreat-intensity days, or a calendar
# quarter of home practice. Quarters, because a "period" that spans years of
# drifting intensity is not a dose.

const RT_MIN_H = 4.0		# hr/day for a day to count as retreat-intensity
const RT_MIN_D = 5		# days for a run to count as a retreat
const RT_GAP = 2		# sub-threshold days tolerated inside a run

function daily_hours(path)
	df = CSV.read(path, DataFrame)
	h = Dict{Date,Float64}()
	for r in eachrow(df)
		ismissing(r.meditation_start) && continue
		d = Date(first(string(r.meditation_start), 10))
		s = ismissing(r.meditation_duration) ? 0.0 : Float64(r.meditation_duration)
		h[d] = get(h, d, 0.0) + s / 3600
	end
	ks = sort(collect(keys(h)))
	return [(d, get(h, d, 0.0)) for d in ks[1]:Day(1):ks[end]]
end

function retreat_runs(series)
	runs = Tuple{Int,Int}[]
	i, n = 1, length(series)
	while i <= n
		if series[i][2] >= RT_MIN_H
			last = i
			j = i
			gap = 0
			while j < n
				j += 1
				if series[j][2] >= RT_MIN_H
					last = j
					gap = 0
				else
					gap += 1
					gap > RT_GAP && break
				end
			end
			last - i + 1 >= RT_MIN_D && push!(runs, (i, last))
			i = last + 1
		else
			i += 1
		end
	end
	return runs
end

function quarter_cuts(series, lo, hi)
	cuts = Int[lo]
	for k in (lo + 1):hi
		d, prev = series[k][1], series[k - 1][1]
		(month(d) - 1) ÷ 3 != (month(prev) - 1) ÷ 3 && push!(cuts, k)
	end
	push!(cuts, hi + 1)
	return cuts
end

function period_row(series, a, b, retreat)
	days = b - a + 1
	hours = sum(series[k][2] for k in a:b)
	return (start = series[a][1], stop = series[b][1], days = days,
		hours = round(hours, digits = 2),
		h_per_day = round(hours / days, digits = 3), retreat = retreat)
end

function home_periods(series, lo, hi)
	out = NamedTuple[]
	cuts = quarter_cuts(series, lo, hi)
	for k in 1:(length(cuts) - 1)
		a, b = cuts[k], cuts[k + 1] - 1
		b < a && continue
		r = period_row(series, a, b, false)
		r.hours > 0 && push!(out, r)
	end
	return out
end

function build_periods(series)
	rows = NamedTuple[]
	pos = 1
	for (a, b) in retreat_runs(series)
		a > pos && append!(rows, home_periods(series, pos, a - 1))
		push!(rows, period_row(series, a, b, true))
		pos = b + 1
	end
	pos <= length(series) && append!(rows, home_periods(series, pos, length(series)))
	return rows
end

function own_periods()
	df = DataFrame(build_periods(daily_hours(MEDITATIONS)))
	# the July 2026 retreat postdates the log; become.md dates it to that month
	push!(df, (start = Date(2026, 7, 5), stop = Date(2026, 8, 1), days = 28,
		hours = 280.0, h_per_day = 10.0, retreat = true))
	return df
end

# ============================================================================
# 2. Survival model
# ============================================================================
#
#	log L_i = a + b_src*web + u_p + b_d*log1p(D_i/1000)
#		+ b_h*lh + b_L*ll + b_hL*lh*ll
#	lh = log(h_i/8), ll = log(L_i/10),  p(event in period i) = 1 - exp(-L_i)
#
# b_hL is the container effect, and it has to be an interaction: with separable
# log-linear terms the model concludes a year at 2 hr/day beats a month-long
# retreat, because length is length. Days compound only when intense *and*
# unbroken, which is h × L.
#
# 45% of web rows state no hours/day, so h is latent with a type-level prior
# learned from the rows where it is stated. b_src absorbs the attainer
# over-representation of public practice logs into the intercept, so web data
# informs the shape without dragging the level up; predictions use `a` alone.

const H_REF = 8.0
const L_REF = 10.0
const P_UNRECOGNISED = 0.1	# niplav may have attained and not classified it
const CHUNK = 90.0		# days; makes a 10-day retreat and a 30-year era commensurable

struct Data
	pers::Vector{Int}
	ptype::Vector{Int}
	days::Vector{Float64}
	logh::Vector{Float64}
	miss::Vector{Int}
	rows::Vector{Vector{Int}}
	block::Vector{Int}
	event::Vector{Int}
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
		# one latent intensity per reported period, shared by its chunks --
		# the source stated at most one number, not one per 90 days
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

finish_data(b::Build) = Data(b.pers, b.ptype, b.days, b.logh, b.miss, b.rows,
	b.block, b.event, b.known, b.soft, b.web, length(b.types), b.n_miss)

function load_all()
	b = Build()
	df = own_periods()
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
	return finish_data(b)
end

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
		# first chunk of the block only, else long eras count 100x
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

# ============================================================================
# 3. Posterior -> Gekrakel
# ============================================================================
#
# The joint posterior is carried across draw-by-draw, so a, u, b_h, b_L and
# b_hL stay correlated. That matters a lot: b_h and b_hL are strongly
# anti-correlated in this fit, and marginalising them separately would widen
# p(cessation) by more than the data warrant.
#
# `setnsamp!` first: MonteCarloMeasurements puts the particle count in the
# type, so every node in a model must agree on it. Anything built before this
# call keeps the old count and cannot be combined with anything after.

struct Post
	a::Node
	u::Node
	b_d::Node
	b_h::Node
	b_L::Node
	b_hL::Node
	acc0::Float64		# formal hours logged before the decision point
end

function to_gekrakel(chain, D, extra = NamedTuple[])
	col(k) = vec(Array(chain[k]))
	n = length(col(:a))
	setnsamp!(n)
	acc0 = sum(D.days[r] * exp(D.logh[r]) for r in D.rows[1])
	for e in extra
		acc0 += e.days * e.h_per_day
	end
	u = col(Symbol("u_raw[1]")) .* col(:sigma_u)
	return Post(gek(col(:a)), gek(u), gek(col(:b_d)), gek(col(:b_h)),
		gek(col(:b_L)), gek(col(:b_hL)), acc0)
end

"""
	p_cess(post, h, d)

p(cessation | h hr/day sustained for d days), given the practice history and
no attainment yet. `d` may itself be a distribution — the counterfactual drip
runs for the accrual window, which is uncertain.

Uses `a` alone, not `a + b_src`: we want the hazard for someone who practises,
not for someone who posts about practising.
"""
function p_cess(P::Post, h, d)
	lh = log(h / H_REF)
	ll = log(d / L_REF)
	lam = exp(P.a + P.u + P.b_d * log1p(P.acc0 / 1000) +
		P.b_h * lh + P.b_L * ll + P.b_hL * lh * ll)
	return 1 - exp(-lam)
end

# ============================================================================
# 4. What a practice period is worth
# ============================================================================

Base.@kwdef struct Model
	# --- exogenous ---
	hourly_wage = 38
	natural_lifespan = 40…60
	# the spec says sub-2 hr/day practice costs "just my hourly wage", which
	# assumes every meditation hour is an unbilled one. Some of it eats
	# slack, sleep, or scrolling instead.
	work_displacement = truncateRight(0.55…0.98, 1.0)

	# --- TAI, the common cause of both the Enlightener and doom ---
	# median ~2031, with 75% on "the transitive closure of obvious things
	# for LLMs gets us there" and 25% on "needs a further insight".
	tai_years = mx([2…12, 8…60], [0.75, 0.25])

	# --- Automated Enlightener (STUB: wants a Manifold question) ---
	# "a protocol that gets a motivated person to >90% chance of stream
	# entry in <14 days for <$10k". Structured as TAI plus a diffusion lag
	# rather than as a free-standing date, so it inherits the timeline.
	diffusion_lag = 0.25…5
	p_enlightener = 0.9

	# --- doom, conditional on the same TAI draw ---
	# p(doom) = 65%. Doom as TAI times a ratio rather than plus a lag,
	# because a slower takeoff plausibly stretches the whole sequence; mass
	# below 1 is catastrophe during the run-up.
	p_doom = 0.65
	timing_ratio = 0.7…4

	# --- value of the attainment (STUB: wants practitioner interviews) ---
	# annual willingness-to-pay for the persistent shift, not a one-off.
	# The 5% arm reaching $1M/yr dominates the mean; prefer the median.
	value_se_per_year = mx([2e3…4e4, 3e4…1e6], [0.95, 0.05])

	# --- costs ---
	soft_lodging_daily = 25…60
	europe_travel = 150…700
	nepal_travel = 1.2e3…3e3

	# --- mundane benefits ---
	upside_scale = 3e3…25e3
	dark_night_cost = mx([500…8e3, 2e4…2e5], [0.92, 0.08])

	# --- derived ---
	#
	# How long a cessation attained *now* pays counterfactual rent: until the
	# Enlightener arrives (after which having got there early is worth
	# ~nothing), or doom, or death of old age — whichever comes first.
	#
	# Built here, once, rather than inside `value`: every scenario has to be
	# priced against the *same* draws or the rows are not comparable, and the
	# differences between them are swamped by resampling noise.
	#
	# `enlightener` and `doom` are both functions of the same `tai_years`
	# draws, so they are correlated and the minimum is taken sample-wise. An
	# independent-draws model puts that minimum systematically too low.
	enlightener = mx([tai_years + diffusion_lag, 200],
		[p_enlightener, 1 - p_enlightener])
	doom = mx([tai_years * timing_ratio, 500], [p_doom, 1 - p_doom])
	# clamped, not truncated: we want `max(x, 0.05)` pointwise, not
	# conditioning on `x > 0.05`, which renormalises away the short-window
	# mass that is exactly the interesting part
	window = max(over(min, enlightener, doom, natural_lifespan), 0.05)
end

"""
	cost(M, h, d)

Three regimes: below 2 hr/day it fits into normal life and costs the wage of
the displaced hours; to 8 hr/day it is a soft retreat with part-time work whose
productivity decays as h rises; above that it is full retreat on the
\$50 → \$80 → \$200 per meditation-hour schedule. Travel is Europe below 28
days, Nepal above.

The \$50/hr retreat rate is load-bearing and probably too high: at 12 hr/day
for 90 days it implies \$54k against a ~\$23k bottom-up estimate (\$19k
foregone wage for a quarter of full-time work, ~\$1.5k dana lodging, ~\$2k
travel). Either it prices in career discontinuity and reintegration, or it
double-counts. See the sensitivity table.
"""
function cost(M::Model, h, d)
	daily = if h <= 2
		h * M.hourly_wage * M.work_displacement
	elseif h <= 8
		friction = 1 + 0.4 * (max(h - 2, 0) / 6)
		h * friction * M.hourly_wage + M.soft_lodging_daily
	else
		rate = h <= 12 ? 50.0 :
			h <= 18 ? 50 + 30 * (h - 12) / 6 : 80 + 120 * (h - 18) / 6
		h * rate
	end
	travel = h <= 2 ? 0 : d <= 28 ? M.europe_travel : M.nepal_travel
	return daily * d + travel
end

"""
	mundane(M, h, d)

Concentration, equanimity, sleep, the retreat qua vacation — minus dark-night
territory that persists afterwards, depersonalisation, or rarely psychosis.
The upside saturates (most concentration gains come early); the downside grows
with dose and has a nasty tail. Net expectation is small and can be negative.
"""
function mundane(M::Model, h, d)
	eh = d * h		# raw dose; the shape parameters are the stubs here
	upside = M.upside_scale * (1 - exp(-eh / 2000))
	return upside - M.dark_night_cost * (eh / 3000)
end

"""
	value(M, P, h, d; cost_mult=1)

benefit − cost, in dollars.

The counterfactual is no further practice at all — not a continuing drip — so
the supramundane term is the *full* conditional p(cessation) from the period
rather than an increment over a baseline. That is niplav's stated decision
problem, and analysis.sq was cut down to match.

Note what the counterfactual is not: practice *history* is very much not zero.
The ~2.8k formal hours already logged are carried in `Post.acc0` and are what
puts the retreat far enough up the saturation curve to matter.
"""
function value(M::Model, P::Post, h, d; cost_mult = 1.0)
	p = p_cess(P, h, d)
	supra = p * M.value_se_per_year * M.window
	mund = mundane(M, h, d)
	c = cost(M, h, d) * cost_mult
	return (supramundane = supra, mundane = mund, cost = c,
		net = supra + mund - c, p = p)
end

# ============================================================================
# 5. Report
# ============================================================================

function money(x)
	out = ""
	for (i, c) in enumerate(reverse(string(round(Int, abs(x)))))
		i > 1 && (i - 1) % 3 == 0 && (out = "," * out)
		out = c * out
	end
	return (x < 0 ? "-\$" : "\$") * out
end
ci(x) = string(money(quantile(x, 0.05)), " – ", money(quantile(x, 0.95)))
yrs(x) = string(round(quantile(x, 0.05), digits = 1), " – ",
	round(quantile(x, 0.95), digits = 1))

const SCENARIOS = [
	("nothing extra (0.5 hr/day, 90d)", 0.5, 90),
	("daily discipline (2 hr/day, 90d)", 2.0, 90),
	("soft retreat w/ friend (5 hr/day, 60d)", 5.0, 60),
	("soft retreat, hard (8 hr/day, 90d)", 8.0, 90),
	("Europe retreat (12 hr/day, 28d)", 12.0, 28),
	("Lumbini, moderate (10 hr/day, 90d)", 10.0, 90),
	("Lumbini, standard (12 hr/day, 90d)", 12.0, 90),
	("Lumbini, hardcore (16 hr/day, 90d)", 16.0, 90),
	("ascetic maximum (20 hr/day, 90d)", 20.0, 90),
]

# The counterfactual-drip axis was retired upstream along with `baselineHours`,
# so what is left to vary is the cost schedule. It is the load-bearing one: at
# $50/hr for 12 hr/day over 90 days the schedule prices Lumbini at ~$56k, and
# 0.4 is roughly the bottom-up estimate of ~$23k.
const SENSITIVITY = [
	("as specified", 1.0),
	("split the difference", 0.7),
	("bottom-up cost", 0.4),
	("lodging and travel only", 0.1),
]

"""
	dose_response(P)

Read the fitted hazard back out along both axes and check it is increasing in
each. Print this before anything else: if more practice does not buy more
probability, everything below is arithmetic on a broken model, and the honest
response is to fix the fit rather than to read the tables.

The known failure mode is that `b_h` and `b_L` fit negative on the web rows,
whose period boundaries are endogenous to the outcome (a narrated period ends
*because* something happened) and whose highest-dose traditions have the
strongest taboo on claiming attainment. That puts almost all the long/intense
mass on non-events and flips the slope.
"""
function dose_response(P::Post)
	p(h, d) = 100 * mean(p_cess(P, h, d))
	println("\ndose-response, p(cess) in %:")
	@printf("  %-10s %8s %8s %8s %8s\n", "hr/day \\ d", "28", "60", "90", "365")
	for h in (1.0, 2.0, 8.0, 12.0, 16.0)
		@printf("  %-10.0f %7.1f%% %7.1f%% %7.1f%% %7.1f%%\n",
			h, p(h, 28), p(h, 60), p(h, 90), p(h, 365))
	end
	ok_len = p(12, 90) > p(12, 28)
	ok_int = p(12, 90) > p(2, 90)
	ok_len && ok_int && return
	println("  !! NOT monotone: ",
		ok_len ? "" : "longer retreats score lower (b_L < 0). ",
		ok_int ? "" : "more intense retreats score lower (b_h < 0). ")
	println("  !! Give the web rows their own b_h/b_L/b_hL or exclude them.",
		"\n  !! The tables below are plumbing, not advice.")
end

function report(M::Model, P::Post)
	println("\npractice history: $(round(Int, P.acc0)) formal hours before the decision point")
	dose_response(P)

	println("\naccrual window (years)")
	println("  ", spark(M.window), "  median ", round(median(M.window), digits = 1),
		"   90% ", yrs(M.window))

	println("\nscenarios")
	@printf("  %-40s %7s %23s %12s %12s %8s\n",
		"", "p(cess)", "cost (90%)", "E[net]", "median net", "P(net>0)")
	for (name, h, d) in SCENARIOS
		v = value(M, P, h, d)
		@printf("  %-40s %6.1f%% %23s %12s %12s %7.0f%%\n", name,
			100 * mean(v.p), ci(v.cost), money(mean(v.net)),
			money(median(v.net)), 100 * (1 - cdf(v.net, 0)))
	end

	println("\nsensitivity, Lumbini standard (12 hr/day, 90 days)")
	@printf("  %-34s %6s %12s %12s %12s %8s\n",
		"", "cost×", "cost", "E[net]", "median net", "P(net>0)")
	for (label, cm) in SENSITIVITY
		v = value(M, P, 12.0, 90; cost_mult = cm)
		@printf("  %-34s %6.1f %12s %12s %12s %7.0f%%\n", label, cm,
			money(mean(v.cost)), money(mean(v.net)),
			money(median(v.net)), 100 * (1 - cdf(v.net, 0)))
	end

	v = value(M, P, 12.0, 90)
	println("\nLumbini, 3 months, 12 hr/day — net value")
	println("  ", spark(v.net))
	println("  90% ", ci(v.net), "   median ", money(median(v.net)),
		"   mean ", money(mean(v.net)))
	println("  supramundane ", money(mean(v.supramundane)),
		"   mundane ", money(mean(v.mundane)),
		"   cost ", money(mean(v.cost)))
	# the mean is dominated by the 5% arm of value_se_per_year reaching
	# $1M/yr, so it moves between runs; the median and P(net>0) do not
	println("\nDecision statistic: prefer the median and P(net>0). E[net] is " *
		"driven by the\n5% tail of value_se_per_year and is not stable across runs.")
end

# ============================================================================
# Synthetic recovery check
# ============================================================================

function synthetic(n = 40)
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
		for i in eachindex(hpd)		# match the 45% real missingness rate
			rand() < 0.45 && (hpd[i] = missing)
		end
		add_person!(b, days, hpd, ty, ei)
	end
	println("synthetic: $nev/$n attained, $(b.n_miss)/$(length(b.days)) blanked")
	println("truth: a=$(round(th.a, digits=3)) b_d=$(th.b_d) b_h=$(th.b_h) " *
		"b_L=$(th.b_L) b_hL=$(th.b_hL) sigma_u=0.6")
	return finish_data(b)
end

# ============================================================================

function main()
	D = SYNTHETIC ? synthetic() : load_all()
	SYNTHETIC || println("$(length(D.rows)) people, $(length(D.days)) chunks, " *
		"$(sum(D.web)) web rows, $(sum(.!D.known)) outcome-unknown people\n" *
		"$(D.n_miss)/$(length(D.days)) intensities latent across " *
		"$(D.n_type) practice types")

	pars = [:a, :sigma_u, :b_d, :b_h, :b_L, :b_hL, :mu0, :sigma_h, :tau_type]
	SYNTHETIC || push!(pars, :b_src)
	# `Prior()` draws the parameters and ignores the likelihood entirely, so
	# no observation reaches the hazard. The data are still loaded: the model
	# needs their shape, and the prediction needs niplav's own history.
	chain = sample(se_model(D), PRIOR ? Prior() : NUTS(0.8), DRAWS; progress = false)
	PRIOR && println("\n!! PRIOR MODE: the likelihood was not evaluated. " *
		"Everything below is a\n!! prior predictive check.")
	show(stdout, MIME("text/plain"), summarystats(chain[pars]))
	println()
	SYNTHETIC && return chain

	# the 24-day Wales retreat postdates the fitted log and is survived
	wales = [(days = 24.0, h_per_day = 10.0)]
	# order matters: to_gekrakel calls setnsamp!, and Model()'s fields are
	# particle-backed, so they have to be built after the count is fixed
	P = to_gekrakel(chain, D, wales)
	report(Model(), P)
	return chain
end

main()
