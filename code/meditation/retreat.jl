# Should I go to Lumbini for three months? Shared by full.jl (script) and
# notebook.jl (Pluto).
#
#	1. practice periods from data/meditations.csv		periods.jl
#	2. a cessation survival model on those plus the web data
#	3. its posterior carried into Gekrakel, draw by draw
#	4. a practice period (h hr/day, d days) priced in dollars
#
# The posterior is a Gekrakel value (`gek(vec(chain[:a]))`), not a generated
# file, so it cannot go stale.

for p in ("proj/Gekrakel.jl", "proj/PredictionPlatforms.jl")
	p = joinpath(homedir(), p)
	p in LOAD_PATH || push!(LOAD_PATH, p)
end

module Retreat

using CSV, DataFrames, Dates, Turing, Distributions, Random, Statistics, Printf
using Markdown
using Gekrakel
using PredictionPlatforms: manifold, cdf_points, distribution

include("periods.jl")
include(joinpath(homedir(), "proj/shared/world.jl"))	# timelines, doom, away cost

export own_periods, load_data, synthetic, fit_se, PARS, posterior, WALES
export World, value, p_cess, cost, mundane
export dose_warning, dose_table, scenario_table, sensitivity_table, money, ci
export p_grid, net_grid, net_sweep

const INTERVIEWS = joinpath(@__DIR__, "interviews.csv")
const WEB = joinpath(@__DIR__, "web_periods.csv")

# ============================================================================
# Survival model
# ============================================================================
#
#	log L = base + b_d*log1p(D/1000) + b_h*x + b_L*l + b_hL*x*l
#	base = a + b_src*web + u_person,  x = log(h/8),  l = log(days/10)
#	p(event in a period) = 1 - exp(-L)
#
# D is the formal hours practised before. b_hL is the container effect, and it
# has to be an interaction: with separable terms the model concludes that a
# year at 2 hr/day beats a month-long retreat, because length is length. Days
# compound only when intense *and* unbroken.
#
# Periods longer than CHUNK days are split into chunks whose hazards add, so
# that a 10-day retreat and a 30-year era are commensurable. b_L is thereby
# superadditivity *within* 90 days; beyond that, exposure is additive.
#
# 45% of web periods state no hours/day, so h is latent there, with a
# type-level prior learned from the periods where it is stated. b_src absorbs
# the attainer over-representation of public practice logs into the intercept,
# so web data informs the shape without dragging the level up; predictions use
# `a` alone.

const H_REF = 8.0
const L_REF = 10.0
const CHUNK = 90.0
const P_UNRECOGNISED = 0.1	# niplav may have attained and not classified it

"""
	period_hazard(c, lg, days, acc) -> (L, acc')

Cumulative hazard of one practice period at log-intensity `lg`, summed over
its chunks, with `acc` formal hours practised before it. Returns `acc`
advanced past the period. `c` is anything with fields `base, b_d, b_h, b_L,
b_hL`: a NamedTuple of Turing parameters in the fit, a `Post` of Gekrakel
values when predicting, plain numbers in the simulator. All three must agree
on this, which is why there is exactly one copy.
"""
function period_hazard(c, lg, days, acc)
	x = lg - log(H_REF)
	h = exp(lg)
	lam = sum(1:ceil(Int, days / CHUNK)) do k
		d = min(CHUNK, days - (k - 1) * CHUNK)
		l = log(d / L_REF)
		exp(c.base + c.b_d * log1p((acc + (k - 1) * CHUNK * h) / 1000) +
			c.b_h * x + c.b_L * l + c.b_hL * x * l)
	end
	return lam, acc + days * h
end

log1mexp(x) = x < -0.693 ? log1p(-exp(x)) : log(-expm1(x))

Base.@kwdef mutable struct Data
	# per reported period
	ptype::Vector{Int} = Int[]
	days::Vector{Float64} = Float64[]
	logh::Vector{Float64} = Float64[]	# log hr/day; 0.0 where latent
	miss::Vector{Int} = Int[]		# 0 if stated, else index into h_raw
	# per person
	span::Vector{UnitRange{Int}} = UnitRange{Int}[]	# their periods, in order
	event::Vector{Int} = Int[]		# index into span, 0 = censored
	known::Vector{Bool} = Bool[]		# false: declined the attainment question
	soft::Vector{Bool} = Bool[]		# censoring allows "had it, missed it"
	web::Vector{Bool} = Bool[]
	types::Dict{String,Int} = Dict{String,Int}()
	n_miss::Int = 0
end

function add_person!(D::Data, days, hpd, types, event; known = true,
		soft = false, web = false)
	lo = length(D.days) + 1
	for (d, h, t) in zip(days, hpd, types)
		stated = h isa Real && h > 0
		push!(D.ptype, get!(D.types, String(t), length(D.types) + 1))
		push!(D.days, max(Float64(d), 1.0))
		push!(D.logh, stated ? log(h) : 0.0)
		push!(D.miss, stated ? 0 : (D.n_miss += 1))
	end
	push!(D.span, lo:length(D.days))
	push!(D.event, event)
	push!(D.known, known)
	push!(D.soft, soft)
	push!(D.web, web)
	return D
end

# interviews.csv and web_periods.csv, one row per practice period:
#	person,idx,start_year,days,h_per_day,event,outcome_known[,ptype]
function load_data(; kw...)
	D = Data()
	own = own_periods(; kw...)
	add_person!(D, own.days, own.h_per_day, fill("own", nrow(own)), 0; soft = true)
	for (path, web) in ((INTERVIEWS, false), (WEB, true))
		isfile(path) || continue
		for g in groupby(CSV.read(path, DataFrame), :person)
			g = sort(g, :idx)
			ty = hasproperty(g, :ptype) ? coalesce.(g.ptype, "unknown") :
				fill("unknown", nrow(g))
			add_person!(D, coalesce.(g.days, 1), g.h_per_day, ty,
				something(findfirst(isequal(1), g.event), 0);
				known = !hasproperty(g, :outcome_known) ||
					all(!isequal(0), g.outcome_known),
				web)
		end
	end
	return D
end

@model function se_model(D)
	a ~ Normal(log(0.1), 1.0)
	b_src ~ Normal(1.0, 0.7)
	sigma_u ~ Exponential(0.5)
	b_d ~ Normal(0.0, 0.5)
	b_h ~ Normal(1.5, 0.7)
	b_L ~ Normal(1.2, 0.5)
	b_hL ~ Normal(0.5, 0.4)
	u_raw ~ filldist(Normal(0, 1), length(D.span))
	# niplav's own frailty, as a plain scalar: indexing `u_raw[1]` out of a
	# chain works for MCMCChains but not for FlexiChains (Turing >= 0.45)
	u_self := u_raw[1] * sigma_u

	mu0 ~ Normal(log(6.0), 0.7)
	tau_type ~ Exponential(0.5)
	sigma_h ~ Exponential(0.5)
	t_raw ~ filldist(Normal(0, 1), length(D.types))
	h_raw ~ filldist(Normal(0, 1), D.n_miss)

	mt = mu0 .+ t_raw .* tau_type

	# the stated intensities are what teach the type distributions
	for i in eachindex(D.days)
		D.miss[i] == 0 &&
			Turing.@addlogprob! logpdf(Normal(mt[D.ptype[i]], sigma_h), D.logh[i])
	end

	for p in eachindex(D.span)
		D.known[p] || continue
		c = (base = a + b_src * D.web[p] + u_raw[p] * sigma_u,
			b_d = b_d, b_h = b_h, b_L = b_L, b_hL = b_hL)
		logS = zero(a)
		acc = 0.0
		attained = false
		for (k, i) in enumerate(D.span[p])
			lg = D.miss[i] == 0 ? D.logh[i] :
				mt[D.ptype[i]] + h_raw[D.miss[i]] * sigma_h
			lam, acc = period_hazard(c, lg, D.days[i], acc)
			if k == D.event[p]
				Turing.@addlogprob! logS + log1mexp(-lam)
				attained = true
				break
			end
			logS -= lam
		end
		attained && continue
		Turing.@addlogprob! D.soft[p] ?
			log((1 - P_UNRECOGNISED) * exp(logS) + P_UNRECOGNISED) : logS
	end
end

const PARS = [:a, :b_src, :sigma_u, :b_d, :b_h, :b_L, :b_hL, :mu0, :sigma_h, :tau_type]

"""
	fit_se(D; draws = 1500, prior = false, seed = 20260808, kw...)

`prior = true` samples the priors and never evaluates the likelihood, so no
observation reaches the hazard: a prior predictive check. Useful while the
fitted b_L is negative, since the prior at least asserts that dose helps.
The priors are frankly optimistic, so p(cessation | 12 hr/day, 90 days)
comes out near certainty, which is a statement about the priors.

`kw` goes to `sample`, e.g. `chain_type = MCMCChains.Chains` to get
`summarystats` back under Turing >= 0.45. Everything here reads the chain only
through `chain[:name]`, which both chain types support.
"""
fit_se(D::Data; draws = 1500, prior = false, seed = 20260808, kw...) =
	sample(Xoshiro(seed), se_model(D), prior ? Prior() : NUTS(0.8), draws;
		progress = false, kw...)

"""
	synthetic(; n = 40, seed = 20260808)

Simulated practitioners with known parameters, for checking that the fit
recovers them. 45% of intensities are blanked to match the real missingness.
"""
function synthetic(; n = 40, seed = 20260808)
	rng = Xoshiro(seed)
	th = (a = log(0.10), b_d = 0.2, b_h = 1.5, b_L = 1.3, b_hL = 0.5, sigma_u = 0.6)
	D = Data()
	for _ in 1:n
		np = rand(rng, 6:24)
		ret = rand(rng, np) .< 0.3
		days = [r ? rand(rng, 3:30) : rand(rng, 30:120) for r in ret]
		hpd = Any[r ? 4 + 8 * rand(rng) : 0.2 + 1.5 * rand(rng) for r in ret]
		c = merge(th, (base = th.a + rand(rng, Normal(0, th.sigma_u)),))
		ev, acc = 0, 0.0
		for i in 1:np
			lam, acc = period_hazard(c, log(hpd[i]), days[i], acc)
			if rand(rng) < 1 - exp(-lam)
				ev = i
				break
			end
		end
		hpd[rand(rng, np) .< 0.45] .= missing
		add_person!(D, days, hpd, ifelse.(ret, "retreat", "daily"), ev)
	end
	println("synthetic: $(count(>(0), D.event))/$n attained, ",
		"$(D.n_miss)/$(length(D.days)) intensities blanked\ntruth: $th")
	return D
end

# ============================================================================
# Posterior -> Gekrakel
# ============================================================================
#
# Carried across draw by draw, so a, u, b_h, b_L and b_hL stay correlated.
# That matters: b_h and b_hL are strongly anti-correlated, and marginalising
# them separately would widen p(cessation) by more than the data warrant.

# The 24-day Wales retreat postdates the log; the decision is priced as if it
# has been survived. Delete it once it is in meditations.csv, or it is counted
# twice: a hardcoded July retreat did exactly that from August to October 2026.
const WALES = [(days = 24, h_per_day = 10.0)]

struct Post
	base::Node	# a + niplav's own frailty; not b_src, see the header
	b_d::Node
	b_h::Node
	b_L::Node
	b_hL::Node
	acc0::Float64	# formal hours practised before the decision point
end

"""
	posterior(chain, D, extra = WALES)

Calls `setnsamp!`: MonteCarloMeasurements puts the particle count in the type,
so every node in a model must agree on it. Build `World()` *after* this.
"""
function posterior(chain, D::Data, extra = WALES)
	col(k) = vec(Array(chain[k]))
	setnsamp!(length(col(:a)))
	acc0 = sum(D.days[i] * exp(D.logh[i]) for i in D.span[1]) +
		sum(e.days * e.h_per_day for e in extra; init = 0.0)
	return Post(gek(col(:a) .+ col(:u_self)),
		gek(col(:b_d)), gek(col(:b_h)), gek(col(:b_L)), gek(col(:b_hL)), acc0)
end

"p(cessation | h hr/day for d days), given the history and no attainment yet."
p_cess(P::Post, h, d) = 1 - exp(-first(period_hazard(P, log(h), d, P.acc0)))

# ============================================================================
# What a practice period is worth
# ============================================================================

const ENLIGHTENER = "when-will-we-get-neurotechnologyaid"
const SNAPSHOT = joinpath(homedir(), "proj/shared/snapshots/manifold-enlightener.json")

"""
	enlightener_year(wv; refresh = false)

When a product gets ≥90% of people to stream entry in ≤14 days for ≤\$10k,
from niplav's Manifold market, read from its snapshot unless `refresh`.
Mass after 2050 that is not "never" spreads to 2100, a judgment the market
says nothing about; the date is coupled to TED-AGI, see `enlightener`.
"""
function enlightener_year(wv; refresh = false)
	c = cdf_points(manifold(ENLIGHTENER; snapshot = SNAPSHOT, refresh))
	return enlightener(wv, distribution(c; upper = 2100), c.never)
end

Base.@kwdef struct World
	hourly_wage = 38
	natural_lifespan = 40…60
	# "just my hourly wage" assumes every meditation hour is an unbilled one;
	# some of it eats slack, sleep or scrolling instead
	work_displacement = truncateRight(0.55…0.98, 1.0)

	# TED-AGI, doom and the cost of being away from Berlin, as in the career
	# model; ~/proj/shared/world.jl
	wv = worldview()
	t0 = 2027.0		# the decision point: Nepal would come after Wales
	enlightener = enlightener_year(wv)

	# value of the attainment (STUB, wants the interviews): annual WTP for the
	# persistent shift. The 5% arm reaching $1M/yr dominates the mean.
	value_se_per_year = mx([2e3…4e4, 3e4…1e6], [0.95, 0.05])

	soft_lodging_daily = 25…60
	europe_travel = 150…700
	nepal_travel = 1.2e3…3e3

	upside_scale = 3e3…25e3
	dark_night_cost = mx([500…8e3, 2e4…2e5], [0.92, 0.08])

	# How long a cessation attained at t0 pays counterfactual rent: until the
	# Enlightener, doom, or old age, whichever comes first. Built once here
	# so every scenario is priced against the same draws; and since the
	# Enlightener and doom both move with the same ted draws, the minimum is
	# taken sample-wise. Floored rather than truncated: truncating would
	# condition away the short-window mass, which is the interesting part.
	window = over(enlightener, wv.doomed, wv.ted, wv.doom_ratio, natural_lifespan) do e, dm, t, r, life
		doom = dm == 1 ? 2027 + t * r : Inf
		max(min(e, doom, t0 + life) - t0, 0.05)
	end
end

# m months away from Berlin, in dollar-equivalents (shared/world.jl)
away(W::World, months) = W.wv.away1 * over(k -> months^k, W.wv.away_k)

"""
	cost(W, h, d)

Below 2 hr/day practice fits into normal life and costs the displaced wage; to
8 hr/day it is a soft retreat with part-time work that degrades as h rises;
above that, full retreat at \$50 → \$80 → \$200 per meditation-hour. Travel is
Europe up to 28 days, Nepal beyond. Whenever there is travel there is also the
cost of being away from Berlin, priced as in the career model.

The \$50/hr rate is load-bearing and probably too high: 12 hr/day for 90 days
comes to \$54k against a ~\$23k bottom-up estimate (\$19k foregone wage, ~\$1.5k
dana lodging, ~\$2k travel). See `sensitivity_table`.
"""
function cost(W::World, h, d)
	daily = if h <= 2
		h * W.hourly_wage * W.work_displacement
	elseif h <= 8
		h * (1 + 0.4 * (h - 2) / 6) * W.hourly_wage + W.soft_lodging_daily
	else
		h * (h <= 12 ? 50.0 : h <= 18 ? 50 + 30 * (h - 12) / 6 : 80 + 120 * (h - 18) / 6)
	end
	h <= 2 && return daily * d
	travel = d <= 28 ? W.europe_travel : W.nepal_travel
	return daily * d + travel + away(W, d / 30.44)
end

# Concentration, equanimity, the retreat qua vacation, minus dark-night
# territory that persists afterwards. The upside saturates; the downside grows
# with raw dose and has a nasty tail. Both shapes are stubs.
mundane(W::World, h, d) =
	W.upside_scale * (1 - exp(-h * d / 2000)) - W.dark_night_cost * (h * d / 3000)

"""
	value(W, P, h, d; cost_mult = 1)

Benefit minus cost in dollars. The counterfactual is no further practice, so
the supramundane term is the full conditional p(cessation), not an increment
over a baseline drip. Practice *history* is not zero: it is in `P.acc0`.
"""
function value(W::World, P::Post, h, d; cost_mult = 1.0)
	p = p_cess(P, h, d)
	supra = p * W.value_se_per_year * W.window
	mund = mundane(W, h, d)
	c = cost(W, h, d) * cost_mult
	return (; p, supramundane = supra, mundane = mund, cost = c, net = supra + mund - c)
end

# ============================================================================
# Tables
# ============================================================================
#
# Decision statistic: the median and P(net>0). E[net] is driven by the 5% tail
# of value_se_per_year, and Gekrakel's particle means of heavy tails are biased
# low besides.

money(x) = (x < 0 ? "-\$" : "\$") *
	replace(string(round(Int, abs(x))), r"(?<=\d)(?=(\d{3})+$)" => ",")
ci(x) = money(quantile(x, 0.05)) * " – " * money(quantile(x, 0.95))
pct(x; digits = 1) = string(round(100 * x; digits)) * "%"
p_pos(x) = pct(1 - cdf(x, 0); digits = 0)

const SCENARIOS = [
	("nothing extra (0.5 hr/day, 90d)", 0.5, 90),
	("daily discipline (2 hr/day, 90d)", 2.0, 90),
	("soft retreat with friend (5 hr/day, 60d)", 5.0, 60),
	("soft retreat, hard (8 hr/day, 90d)", 8.0, 90),
	("Europe retreat (12 hr/day, 28d)", 12.0, 28),
	("Lumbini, moderate (10 hr/day, 90d)", 10.0, 90),
	("Lumbini, standard (12 hr/day, 90d)", 12.0, 90),
	("Lumbini, hardcore (16 hr/day, 90d)", 16.0, 90),
	("ascetic maximum (20 hr/day, 90d)", 20.0, 90),
]

# 0.4 is roughly the ~$23k bottom-up estimate
const SENSITIVITY = [
	("as specified", 1.0),
	("split the difference", 0.7),
	("bottom-up cost", 0.4),
	("lodging and travel only", 0.1),
]

function dose_table(P::Post)
	hs = [1.0, 2.0, 8.0, 12.0, 16.0]
	df = DataFrame("hr/day" => hs)
	for d in (28, 60, 90, 365)
		df[!, string(d, "d")] = [pct(mean(p_cess(P, h, d))) for h in hs]
	end
	return df
end

"""
	dose_warning(P)

`nothing` if more practice buys more probability along both axes, else a
warning: then everything downstream is arithmetic on a broken model. The known
failure is b_h and b_L fitting negative on the web rows, whose period
boundaries are endogenous to the outcome and whose highest-dose traditions
have the strongest taboo on claiming attainment.
"""
function dose_warning(P::Post)
	p(h, d) = mean(p_cess(P, h, d))
	bad = String[]
	p(12, 90) > p(12, 28) || push!(bad, "longer retreats score lower (`b_L < 0`).")
	p(12, 90) > p(2, 90) || push!(bad, "more intense retreats score lower (`b_h < 0`).")
	isempty(bad) && return nothing
	msg = join(["**Not monotone:**"; bad; "Give the web rows their own " *
		"`b_h`/`b_L`/`b_hL` or exclude them. The tables are plumbing, not advice."], " ")
	return Markdown.MD(Markdown.Admonition("danger", "Broken dose-response",
		[Markdown.parse(msg)]))
end

function scenario_table(W::World, P::Post)
	rows = map(SCENARIOS) do (name, h, d)
		v = value(W, P, h, d)
		(scenario = name, var"p(cess)" = pct(mean(v.p)), var"cost (90%)" = ci(v.cost),
			var"E[net]" = money(mean(v.net)), var"median net" = money(median(v.net)),
			var"P(net>0)" = p_pos(v.net))
	end
	return DataFrame(rows)
end

# ============================================================================
# The next practice period, as a function of (hr/day, days)
# ============================================================================
#
# `value` maps a point (h, d) to a distribution over dollars: ℝ² → Dist, not a
# distribution over two variables. So there are two honest pictures. A table
# keeps the whole distribution at a few points; a heatmap covers the box but
# can show only one summary per cell.

const GRID_H = [1, 2, 5, 8, 10, 12, 16, 20]
const GRID_D = [7, 14, 28, 60, 90]
const BOX_H = (0.5, 20.0)
const BOX_D = (5.0, 90.0)

"""
	dist_grid(f, caption; dens = true, hs = GRID_H, ds = GRID_D)

HTML table with a row per hr/day and a column per length in days, each cell
`caption(f(h, d))`, under the density of `f(h, d)` if `dens`. Every density
has its own x-axis, labelled at its ends. Compare cells by the captions; read
shape from the curves.
"""
function dist_grid(f, caption; dens = true, hs = GRID_H, ds = GRID_D)
	io = IOBuffer()
	print(io, "<table style='font-family:monospace;font-size:.75em'>",
		"<tr><th>hr/day \\ days</th>")
	foreach(d -> print(io, "<th>", d, "</th>"), ds)
	print(io, "</tr>")
	for h in hs
		print(io, "<tr><th>", h, "</th>")
		for d in ds
			x = f(float(h), d)
			print(io, "<td style='padding:4px 8px'>",
				dens ? svgdens(x; w = 150, h = 34) * "<br>" : "", caption(x), "</td>")
		end
		print(io, "</tr>")
	end
	print(io, "</table>")
	return HTML(String(take!(io)))
end

p_grid(P::Post) = dist_grid((h, d) -> p_cess(P, h, d),
	x -> string("median ", pct(median(x)), " · mean ", pct(mean(x))))

# Text only: the right tail of net value reaches millions (the 5% arm of
# value_se_per_year times a long window), which flattens any density drawn to
# the 99.5th percentile into a spike at its left edge.
net_grid(W::World, P::Post) = dist_grid((h, d) -> value(W, P, h, d).net,
	x -> string("<b>", money(median(x)), "</b><br>", money(quantile(x, 0.25)),
		" … ", money(quantile(x, 0.75)), "<br>P>0 ", p_pos(x)); dens = false)

"""
	net_sweep(W, P; n = (16, 16))

Heatmap of P(net > 0) − ½ over the (hr/day, days) box, by `sweep`. Shifted by
½ because sweep's colour scale is symmetric about zero: grey then means a coin
flip, red more likely to lose money than not.

Not the median: median > 0 exactly when P(net > 0) > ½, so its colours would
carry the same sign, with magnitudes crushed by the 20 hr/day corner. And the
dominance frontier is off: nearly every cell is first-order undominated, so
outlining them marks almost everything and says almost nothing.
"""
net_sweep(W::World, P::Post; n = (16, 16)) =
	sweep((h, d) -> value(W, P, h, d).net, BOX_H, BOX_D; n, xlab = "hr/day",
		ylab = "days", stat = x -> 1 - cdf(x, 0) - 0.5, slab = "P(net>0) − ½",
		frontier = false)

# Lumbini standard (12 hr/day, 90 days) under scaled cost schedules
function sensitivity_table(W::World, P::Post)
	rows = map(SENSITIVITY) do (label, cm)
		v = value(W, P, 12.0, 90; cost_mult = cm)
		(schedule = label, var"cost×" = cm, cost = money(mean(v.cost)),
			var"E[net]" = money(mean(v.net)), var"median net" = money(median(v.net)),
			var"P(net>0)" = p_pos(v.net))
	end
	return DataFrame(rows)
end

end # module
