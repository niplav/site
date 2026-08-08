### A Pluto.jl notebook ###
# v1.0.3

using Markdown
using InteractiveUtils

# ╔═╡ 0d3adf68-934e-11f1-9e6f-d9c933bf00f8
push!(LOAD_PATH, joinpath(homedir(), "proj/Gekrakel.jl"))

# ╔═╡ c4fa1fee-d7c4-4b43-92bb-a17f94e822c4
using CSV, DataFrames, Dates, Turing, Distributions, Random, Statistics, Printf

# ╔═╡ cc88334c-1e90-4cd0-b4ef-d672a5851f52
using Gekrakel

# ╔═╡ 5975f055-85eb-4769-9723-417e4b33e071
Random.seed!(20260808)

# ╔═╡ d7f65c1b-8e4e-4f35-bbe4-6ad1bfe768cd
begin
	const MEDITATIONS = joinpath(homedir(), "proj/site/data/meditations.csv")
	const INTERVIEWS = joinpath(@__DIR__, "interviews.csv")
	const WEB = joinpath(@__DIR__, "web_periods.csv")
	
	const QUICK = "--quick" in ARGS
	const SYNTHETIC = "--synthetic" in ARGS
	const DRAWS = QUICK ? 400 : 1500
	const PRIOR = "--prior" in ARGS
end

# ╔═╡ fcd964a1-9618-40b1-9ebe-aec48b1ae200
begin
	const RT_MIN_H = 4.0            # hr/day for a day to count as retreat-intensity
	const RT_MIN_D = 5              # days for a run to count as a retreat
	const RT_GAP = 2                # sub-threshold days tolerated inside a run
end

# ╔═╡ 1cee9b79-41fd-46da-ab1d-d8311e12aa26
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

# ╔═╡ 41b573a9-37e2-41be-af63-52226b95f633

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

# ╔═╡ 07102747-a4fc-46a0-879a-322c7fc88d7c
function quarter_cuts(series, lo, hi)
        cuts = Int[lo]
        for k in (lo + 1):hi
                d, prev = series[k][1], series[k - 1][1]
                (month(d) - 1) ÷ 3 != (month(prev) - 1) ÷ 3 && push!(cuts, k)
        end
        push!(cuts, hi + 1)
        return cuts
end

# ╔═╡ ec8a72cc-44df-4fcc-b419-6c493d181e4b
function period_row(series, a, b, retreat)
        days = b - a + 1
        hours = sum(series[k][2] for k in a:b)
        return (start = series[a][1], stop = series[b][1], days = days,
                hours = round(hours, digits = 2),
                h_per_day = round(hours / days, digits = 3), retreat = retreat)
end

# ╔═╡ 8d31adbd-794f-4bec-b193-bb6c7f931cd6
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

# ╔═╡ 39ca740d-b79c-4834-bdd1-fca3f19450d0
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

# ╔═╡ 22354df2-39f6-46f0-9407-94850b1f6f8d
function own_periods()
        df = DataFrame(build_periods(daily_hours(MEDITATIONS)))
        # the July 2026 retreat postdates the log; become.md dates it to that month
        push!(df, (start = Date(2026, 7, 5), stop = Date(2026, 8, 1), days = 28,
                hours = 280.0, h_per_day = 10.0, retreat = true))
        return df
end

# ╔═╡ 3c4f05e4-787b-45eb-8b29-3491149a9c39
begin
    const H_REF = 8.0
    const L_REF = 10.0
    const P_UNRECOGNISED = 0.1      # niplav may have attained and not classified it
    const CHUNK = 90.0              # days; makes a 10-day retreat and a 30-year era commensurable
    
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
end

# ╔═╡ 3a1b0630-6994-4150-b34e-bf4c79766254
begin
         mutable struct Build
                pers::Vector{Int}; ptype::Vector{Int}; days::Vector{Float64}
                logh::Vector{Float64}; miss::Vector{Int}
                rows::Vector{Vector{Int}}; block::Vector{Int}; event::Vector{Int}
                known::Vector{Bool}; soft::Vector{Bool}; web::Vector{Bool}
                types::Dict{String,Int}; n_miss::Int; n_block::Int
        end
            Build() = Build(Int[], Int[], Float64[], Float64[], Int[], Vector{Int}[], Int[], Int[], Bool[], Bool[], Bool[], Dict{String,Int}(), 0, 0)
end

# ╔═╡ 0ab7bf98-251f-45f7-b874-b23a90f9ebb1
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

# ╔═╡ b9cc819e-da09-4897-a1b0-2777cbf8bf2d
finish_data(b::Build) = Data(b.pers, b.ptype, b.days, b.logh, b.miss, b.rows,
        b.block, b.event, b.known, b.soft, b.web, length(b.types), b.n_miss)

# ╔═╡ af6ce65e-e412-4a75-b83d-97dc4ef0dd8b
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

# ╔═╡ c2f55dce-f1f1-4b47-899a-dfe2f6287d78
log1mexp(x) = x < -0.693 ? log1p(-exp(x)) : log(-expm1(x))

# ╔═╡ 45bd1537-c1d9-4661-ba1f-3c5704627ee7
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
                blam = zero(a)          # hazard accumulated within the current block
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

# ╔═╡ 0084c677-9ff1-49fe-9b88-2f81aa555ef0
struct Post
        a::Node
        u::Node
        b_d::Node
        b_h::Node
        b_L::Node
        b_hL::Node
        acc0::Float64           # formal hours logged before the decision point
end

# ╔═╡ 43c59e15-e9a0-436c-b947-7a4c06d35b1b
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

# ╔═╡ f28819d1-4c3b-47c6-be7a-c09b3330ec66
function p_cess(P::Post, h, d)
        lh = log(h / H_REF)
        ll = log(d / L_REF)
        lam = exp(P.a + P.u + P.b_d * log1p(P.acc0 / 1000) +
                P.b_h * lh + P.b_L * ll + P.b_hL * lh * ll)
        return 1 - exp(-lam)
end

# ╔═╡ 6290ebf3-7d95-49db-9d13-777dd0c76eca
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

# ╔═╡ 0d842ccc-717e-4199-93a4-c0814ec2e9e8
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

# ╔═╡ 5cbbc465-8448-400e-9fb6-12c2972607f2
function mundane(M::Model, h, d)
        eh = d * h              # raw dose; the shape parameters are the stubs here
        upside = M.upside_scale * (1 - exp(-eh / 2000))
        return upside - M.dark_night_cost * (eh / 3000)
end

# ╔═╡ 6d1b2eb1-4a1a-4487-b721-c1bc23576011
function value(M::Model, P::Post, h, d; cost_mult = 1.0)
        p = p_cess(P, h, d)
        supra = p * M.value_se_per_year * M.window
        mund = mundane(M, h, d)
        c = cost(M, h, d) * cost_mult
        return (supramundane = supra, mundane = mund, cost = c,
                net = supra + mund - c, p = p)
end

# ╔═╡ 6f4d54e6-00f5-4bb5-a16c-5462c4f62be4
function money(x)
        out = ""
        for (i, c) in enumerate(reverse(string(round(Int, abs(x)))))
                i > 1 && (i - 1) % 3 == 0 && (out = "," * out)
                out = c * out
        end
        return (x < 0 ? "-\$" : "\$") * out
end

# ╔═╡ 7234534c-372c-4604-b939-6142651b24f4
begin
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
    const SENSITIVITY = [
            ("as specified", 1.0),
            ("split the difference", 0.7),
            ("bottom-up cost", 0.4),
            ("lodging and travel only", 0.1),
    ]
end

# ╔═╡ f426a9fc-bbd1-4d9e-a300-682ad63c16d9


# ╔═╡ 3dca1448-f6e1-4591-9c5a-fea17528748c
begin
    ci(x) = string(money(quantile(x, 0.05)), " – ", money(quantile(x, 0.95)))
    yrs(x) = string(round(quantile(x, 0.05), digits = 1), " – ",
            round(quantile(x, 0.95), digits = 1))
end

# ╔═╡ bb08a3d4-6a1c-40e7-b885-e0d449e95d8d
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

# ╔═╡ 61f3e8c6-86a4-437a-990e-062b9cfbcf75
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

# ╔═╡ cfc60c21-8fce-4154-bda6-581913ff6a62
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
                for i in eachindex(hpd)         # match the 45% real missingness rate
                        rand() < 0.45 && (hpd[i] = missing)
                end
                add_person!(b, days, hpd, ty, ei)
        end
        println("synthetic: $nev/$n attained, $(b.n_miss)/$(length(b.days)) blanked")
        println("truth: a=$(round(th.a, digits=3)) b_d=$(th.b_d) b_h=$(th.b_h) " *
                "b_L=$(th.b_L) b_hL=$(th.b_hL) sigma_u=0.6")
        return finish_data(b)
end

# ╔═╡ f5caf6f4-328c-4227-a090-484b2bdb81ba
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

# ╔═╡ 9f01bfce-31e2-47f3-b95c-acd8dbbb4897
main()

# ╔═╡ 00000000-0000-0000-0000-000000000001
PLUTO_PROJECT_TOML_CONTENTS = """
[deps]
CSV = "336ed68f-0bac-5ca0-87d4-7b16caf5d00b"
DataFrames = "a93c6f00-e57d-5684-b7b6-d8193f3e46c0"
Dates = "ade2ca70-3891-5945-98fb-dc099432e06a"
Distributions = "31c24e10-a181-5473-b8eb-7969acd0382f"
Printf = "de0858da-6303-5e67-8744-51eddeeeb8d7"
Random = "9a3f8284-a2c9-5f02-9a11-845980a1fd5c"
Statistics = "10745b16-79ce-11e8-11f9-7d13ad32a3b2"
Turing = "fce5fe82-541a-59a6-adf8-730c64b5f9a0"

[compat]
CSV = "~0.10.16"
DataFrames = "~1.8.2"
Distributions = "~0.25.130"
Turing = "~0.44.5"
"""

# ╔═╡ 00000000-0000-0000-0000-000000000002
PLUTO_MANIFEST_TOML_CONTENTS = """
# This file is machine-generated - editing it directly is not advised

julia_version = "1.12.6"
manifest_format = "2.0"
project_hash = "dd7d356b4b2ec11fa892e64dddef88ba890b90b4"

[[deps.ADTypes]]
git-tree-sha1 = "9b38b82a9fe131f3d331a53b7203d9d1a2a4602c"
uuid = "47edcb42-4c32-4615-8424-f2b9edc5f35b"
version = "1.22.4"
weakdeps = ["ChainRulesCore", "ConstructionBase", "EnzymeCore"]

    [deps.ADTypes.extensions]
    ADTypesChainRulesCoreExt = "ChainRulesCore"
    ADTypesConstructionBaseExt = "ConstructionBase"
    ADTypesEnzymeCoreExt = "EnzymeCore"

[[deps.AbstractFFTs]]
deps = ["LinearAlgebra"]
git-tree-sha1 = "d92ad398961a3ed262d8bf04a1a2b8340f915fef"
uuid = "621f4979-c628-5d54-868e-fcf4e3e8185c"
version = "1.5.0"
weakdeps = ["ChainRulesCore", "Test"]

    [deps.AbstractFFTs.extensions]
    AbstractFFTsChainRulesCoreExt = "ChainRulesCore"
    AbstractFFTsTestExt = "Test"

[[deps.AbstractMCMC]]
deps = ["BangBang", "ConsoleProgressMonitor", "Dates", "Distributed", "LogDensityProblems", "Logging", "LoggingExtras", "ProgressLogging", "Random", "StatsBase", "TerminalLoggers", "UUIDs"]
git-tree-sha1 = "328c7d50f307c66308a915abb20d9889e5aab48b"
uuid = "80f14c24-f653-4e6a-9b94-39d6b0f70001"
version = "5.16.0"

    [deps.AbstractMCMC.extensions]
    AbstractMCMCOnlineStatsExt = "OnlineStats"
    AbstractMCMCTensorBoardLoggerExt = "TensorBoardLogger"

    [deps.AbstractMCMC.weakdeps]
    OnlineStats = "a15396b6-48d5-5d58-9928-6d29437db91e"
    TensorBoardLogger = "899adc3e-224a-11e9-021f-63837185c80f"

[[deps.AbstractPPL]]
deps = ["AbstractMCMC", "Accessors", "BangBang", "DensityInterface", "JSON", "LinearAlgebra", "MacroTools", "OrderedCollections", "Random", "StatsBase"]
git-tree-sha1 = "e7be2de9646c1f61332de9f1e32c7dedf1e00831"
uuid = "7a57a42e-76ec-4ea3-a279-07e840d6d9cf"
version = "0.14.2"
weakdeps = ["Distributions"]

    [deps.AbstractPPL.extensions]
    AbstractPPLDistributionsExt = ["Distributions", "LinearAlgebra"]

[[deps.AbstractTrees]]
git-tree-sha1 = "2d9c9a55f9c93e8887ad391fbae72f8ef55e1177"
uuid = "1520ce14-60c1-5f80-bbc7-55ef81b5835c"
version = "0.4.5"

[[deps.Accessors]]
deps = ["CompositionsBase", "ConstructionBase", "Dates", "InverseFunctions", "MacroTools"]
git-tree-sha1 = "7063ad1083578215c7c4bf410368150abe8d5524"
uuid = "7d9f7c33-5ae7-4f3b-8dc6-eff91059b697"
version = "0.1.45"

    [deps.Accessors.extensions]
    AxisKeysExt = "AxisKeys"
    IntervalSetsExt = "IntervalSets"
    LinearAlgebraExt = "LinearAlgebra"
    StaticArraysExt = "StaticArrays"
    StructArraysExt = "StructArrays"
    TestExt = "Test"
    UnitfulExt = "Unitful"

    [deps.Accessors.weakdeps]
    AxisKeys = "94b1ba4f-4ee9-5380-92f1-94cde586c3c5"
    IntervalSets = "8197267c-284f-5f27-9208-e0e47529a953"
    LinearAlgebra = "37e2e46d-f89d-539d-b4ee-838fcccc9c8e"
    StaticArrays = "90137ffa-7385-5640-81b9-e52037218182"
    StructArrays = "09ab397b-f2b6-538f-b94a-2f83cf4a842a"
    Test = "8dfed614-e22c-5e08-85e1-65c5234f0b40"
    Unitful = "1986cc42-f94f-5a68-af5c-568840ba703d"

[[deps.Adapt]]
deps = ["LinearAlgebra"]
git-tree-sha1 = "daa72978cd7a624246e894a4f4f067706d4e17e2"
uuid = "79e6a3ab-5dfb-504d-930d-738a2a938a0e"
version = "4.7.0"
weakdeps = ["SparseArrays", "StaticArrays"]

    [deps.Adapt.extensions]
    AdaptSparseArraysExt = "SparseArrays"
    AdaptStaticArraysExt = "StaticArrays"

[[deps.AdvancedHMC]]
deps = ["AbstractMCMC", "ArgCheck", "DocStringExtensions", "IrrationalConstants", "LinearAlgebra", "LogDensityProblems", "LogDensityProblemsAD", "LogExpFunctions", "ProgressMeter", "Random", "Setfield", "Statistics", "StatsBase"]
git-tree-sha1 = "877f5aa8559585d13429008116827ce4c37483fc"
uuid = "0bf59076-c3b1-5ca4-86bd-e02cd72cde3d"
version = "0.8.6"

    [deps.AdvancedHMC.extensions]
    AdvancedHMCADTypesExt = "ADTypes"
    AdvancedHMCCUDAExt = "CUDA"
    AdvancedHMCComponentArraysExt = "ComponentArrays"
    AdvancedHMCMCMCChainsExt = "MCMCChains"
    AdvancedHMCOrdinaryDiffEqSymplecticRKExt = "OrdinaryDiffEqSymplecticRK"

    [deps.AdvancedHMC.weakdeps]
    ADTypes = "47edcb42-4c32-4615-8424-f2b9edc5f35b"
    CUDA = "052768ef-5323-5732-b1bb-66c8b64840ba"
    ComponentArrays = "b0b7db55-cfe3-40fc-9ded-d10e2dbeff66"
    MCMCChains = "c7f686f2-ff18-58e9-bc7b-31028e88f75d"
    OrdinaryDiffEqSymplecticRK = "fa646aed-7ef9-47eb-84c4-9443fc8cbfa8"

[[deps.AdvancedMH]]
deps = ["AbstractMCMC", "Distributions", "DocStringExtensions", "FillArrays", "LinearAlgebra", "LogDensityProblems", "Random", "Requires"]
git-tree-sha1 = "62ddbccf0ce5c26f8ef3cebe4bedef6b1599d616"
uuid = "5b7e9947-ddc0-4b3f-9b55-0d8042f74170"
version = "0.8.10"

    [deps.AdvancedMH.extensions]
    AdvancedMHForwardDiffExt = ["DiffResults", "ForwardDiff"]
    AdvancedMHMCMCChainsExt = "MCMCChains"
    AdvancedMHStructArraysExt = "StructArrays"

    [deps.AdvancedMH.weakdeps]
    DiffResults = "163ba53b-c6d8-5494-b064-1a9d43ac40c5"
    ForwardDiff = "f6369f11-7733-5829-9624-2563aa707210"
    MCMCChains = "c7f686f2-ff18-58e9-bc7b-31028e88f75d"
    StructArrays = "09ab397b-f2b6-538f-b94a-2f83cf4a842a"

[[deps.AdvancedPS]]
deps = ["AbstractMCMC", "Distributions", "Random", "Random123", "Requires", "SSMProblems", "StatsFuns"]
git-tree-sha1 = "d92dd3fb4cc2748860ae8d5dd1d324cf0715a53b"
uuid = "576499cb-2369-40b2-a588-c64705576edc"
version = "0.7.2"
weakdeps = ["Libtask"]

    [deps.AdvancedPS.extensions]
    AdvancedPSLibtaskExt = "Libtask"

[[deps.AdvancedVI]]
deps = ["ADTypes", "Accessors", "ChainRulesCore", "DiffResults", "DifferentiationInterface", "Distributions", "DocStringExtensions", "FillArrays", "Functors", "LinearAlgebra", "LogDensityProblems", "Optimisers", "ProgressMeter", "Random", "StatsBase"]
git-tree-sha1 = "d69d7d9e1756fff9dd5d3fd26add46ee5ac62be4"
uuid = "b5ca4192-6429-45e5-a2d9-87aec30a685c"
version = "0.6.2"

    [deps.AdvancedVI.extensions]
    AdvancedVIBijectorsExt = ["Bijectors", "Optimisers"]
    AdvancedVIEnzymeExt = ["Enzyme", "ChainRulesCore"]
    AdvancedVIMooncakeExt = ["Mooncake", "ChainRulesCore"]
    AdvancedVIReverseDiffExt = ["ReverseDiff", "ChainRulesCore"]

    [deps.AdvancedVI.weakdeps]
    Bijectors = "76274a88-744f-5084-9051-94815aaf08c4"
    Enzyme = "7da242da-08ed-463a-9acd-ee780be4f1d9"
    Mooncake = "da2b9cff-9c12-43a0-ae48-6db2b0edb7d6"
    ReverseDiff = "37e2e3b7-166d-5795-8a7a-e32c996b4267"

[[deps.AliasTables]]
deps = ["PtrArrays", "Random"]
git-tree-sha1 = "9876e1e164b144ca45e9e3198d0b689cadfed9ff"
uuid = "66dad0bd-aa9a-41b7-9441-69ab47430ed8"
version = "1.1.3"

[[deps.ArgCheck]]
git-tree-sha1 = "f9e9a66c9b7be1ad7372bbd9b062d9230c30c5ce"
uuid = "dce04be8-c92d-5529-be00-80e4d2c0e197"
version = "2.5.0"

[[deps.ArgTools]]
uuid = "0dad84c5-d112-42e6-8d28-ef12dabb789f"
version = "1.1.2"

[[deps.ArrayInterface]]
deps = ["Adapt", "LinearAlgebra"]
git-tree-sha1 = "60f11b38ebeabd984f5535838d91e197d97202f0"
uuid = "4fba245c-0d91-5ea0-9b3e-6abc04ee57a9"
version = "7.28.1"

    [deps.ArrayInterface.extensions]
    ArrayInterfaceAMDGPUExt = "AMDGPU"
    ArrayInterfaceBandedMatricesExt = "BandedMatrices"
    ArrayInterfaceBlockBandedMatricesExt = "BlockBandedMatrices"
    ArrayInterfaceCUDAExt = "CUDA"
    ArrayInterfaceCUDSSExt = ["CUDSS", "CUDA"]
    ArrayInterfaceChainRulesCoreExt = "ChainRulesCore"
    ArrayInterfaceChainRulesExt = "ChainRules"
    ArrayInterfaceFillArraysExt = "FillArrays"
    ArrayInterfaceGPUArraysCoreExt = "GPUArraysCore"
    ArrayInterfaceMetalExt = "Metal"
    ArrayInterfaceReverseDiffExt = "ReverseDiff"
    ArrayInterfaceSparseArraysExt = "SparseArrays"
    ArrayInterfaceStaticArraysCoreExt = "StaticArraysCore"
    ArrayInterfaceTrackerExt = "Tracker"

    [deps.ArrayInterface.weakdeps]
    AMDGPU = "21141c5a-9bdb-4563-92ae-f87d6854732e"
    BandedMatrices = "aae01518-5342-5314-be14-df237901396f"
    BlockBandedMatrices = "ffab5731-97b5-5995-9138-79e8c1846df0"
    CUDA = "052768ef-5323-5732-b1bb-66c8b64840ba"
    CUDSS = "45b445bb-4962-46a0-9369-b4df9d0f772e"
    ChainRules = "082447d4-558c-5d27-93f4-14fc19e9eca2"
    ChainRulesCore = "d360d2e6-b24c-11e9-a2a3-2a2ae2dbcce4"
    FillArrays = "1a297f60-69ca-5386-bcde-b61e274b549b"
    GPUArraysCore = "46192b85-c4d5-4398-a991-12ede77f4527"
    Metal = "dde4c033-4e86-420c-a63e-0dd931031962"
    ReverseDiff = "37e2e3b7-166d-5795-8a7a-e32c996b4267"
    SparseArrays = "2f01184e-e22b-5df5-ae63-d93ebab69eaf"
    StaticArraysCore = "1e83bf80-4336-4d27-bf5d-d5a4f845583c"
    Tracker = "9f7883ad-71c0-57eb-9f7f-b5c9e6d3789c"

[[deps.Artifacts]]
uuid = "56f22d72-fd6d-98f1-02f0-08ddc0907c33"
version = "1.11.0"

[[deps.AxisAlgorithms]]
deps = ["LinearAlgebra", "Random", "SparseArrays", "WoodburyMatrices"]
git-tree-sha1 = "01b8ccb13d68535d73d2b0c23e39bd23155fb712"
uuid = "13072b0f-2c55-5437-9ae7-d433b7a33950"
version = "1.1.0"

[[deps.AxisArrays]]
deps = ["Dates", "IntervalSets", "IterTools", "RangeArrays"]
git-tree-sha1 = "4126b08903b777c88edf1754288144a0492c05ad"
uuid = "39de3d68-74b9-583c-8d2d-e117c070f3a9"
version = "0.4.8"

[[deps.BangBang]]
deps = ["Accessors", "ConstructionBase", "InitialValues", "LinearAlgebra"]
git-tree-sha1 = "cceb62468025be98d42a5dc581b163c20896b040"
uuid = "198e06fe-97b7-11e9-32a5-e1d131e6ad66"
version = "0.4.9"

    [deps.BangBang.extensions]
    BangBangChainRulesCoreExt = "ChainRulesCore"
    BangBangDataFramesExt = "DataFrames"
    BangBangStaticArraysExt = "StaticArrays"
    BangBangStructArraysExt = "StructArrays"
    BangBangTablesExt = "Tables"
    BangBangTypedTablesExt = "TypedTables"

    [deps.BangBang.weakdeps]
    ChainRulesCore = "d360d2e6-b24c-11e9-a2a3-2a2ae2dbcce4"
    DataFrames = "a93c6f00-e57d-5684-b7b6-d8193f3e46c0"
    StaticArrays = "90137ffa-7385-5640-81b9-e52037218182"
    StructArrays = "09ab397b-f2b6-538f-b94a-2f83cf4a842a"
    Tables = "bd369af6-aec1-5ad0-b16a-f7cc5008161c"
    TypedTables = "9d95f2ec-7b3d-5a63-8d20-e2491e220bb9"

[[deps.Base64]]
uuid = "2a0f44e3-6c83-55bd-87e4-b1978d98bd5f"
version = "1.11.0"

[[deps.Bijectors]]
deps = ["AbstractPPL", "ArgCheck", "ChainRulesCore", "ChangesOfVariables", "DifferentiationInterface", "Distributions", "DocStringExtensions", "EnzymeCore", "FillArrays", "Functors", "InverseFunctions", "IrrationalConstants", "LinearAlgebra", "LogExpFunctions", "MappedArrays", "Random", "Reexport", "Roots", "SparseArrays", "Statistics", "Test"]
git-tree-sha1 = "b425418b2644f826823e8ebd4b68a076e8d8d2ec"
uuid = "76274a88-744f-5084-9051-94815aaf08c4"
version = "0.15.24"

    [deps.Bijectors.extensions]
    BijectorsDistributionsADExt = "DistributionsAD"
    BijectorsForwardDiffExt = "ForwardDiff"
    BijectorsLazyArraysExt = "LazyArrays"
    BijectorsMooncakeExt = "Mooncake"
    BijectorsReverseDiffChainRulesExt = ["ChainRules", "ReverseDiff"]
    BijectorsReverseDiffExt = "ReverseDiff"

    [deps.Bijectors.weakdeps]
    ChainRules = "082447d4-558c-5d27-93f4-14fc19e9eca2"
    DistributionsAD = "ced4e74d-a319-5a8a-b0ac-84af2272839c"
    ForwardDiff = "f6369f11-7733-5829-9624-2563aa707210"
    LazyArrays = "5078a376-72f3-5289-bfd5-ec5146d43c02"
    Mooncake = "da2b9cff-9c12-43a0-ae48-6db2b0edb7d6"
    ReverseDiff = "37e2e3b7-166d-5795-8a7a-e32c996b4267"

[[deps.CSV]]
deps = ["CodecZlib", "Dates", "FilePathsBase", "InlineStrings", "Mmap", "Parsers", "PooledArrays", "PrecompileTools", "SentinelArrays", "Tables", "Unicode", "WeakRefStrings", "WorkerUtilities"]
git-tree-sha1 = "8d8e0b0f350b8e1c91420b5e64e5de774c2f0f4d"
uuid = "336ed68f-0bac-5ca0-87d4-7b16caf5d00b"
version = "0.10.16"

[[deps.ChainRulesCore]]
deps = ["Compat", "LinearAlgebra"]
git-tree-sha1 = "12177ad6b3cad7fd50c8b3825ce24a99ad61c18f"
uuid = "d360d2e6-b24c-11e9-a2a3-2a2ae2dbcce4"
version = "1.26.1"
weakdeps = ["SparseArrays"]

    [deps.ChainRulesCore.extensions]
    ChainRulesCoreSparseArraysExt = "SparseArrays"

[[deps.Chairmarks]]
deps = ["Printf", "Random"]
git-tree-sha1 = "9a49491e67e7a4d6f885c43d00bb101e6e5a434b"
uuid = "0ca39b1e-fe0b-4e98-acfc-b1656634c4de"
version = "1.3.1"
weakdeps = ["Statistics"]

    [deps.Chairmarks.extensions]
    StatisticsChairmarksExt = ["Statistics"]

[[deps.ChangesOfVariables]]
deps = ["LinearAlgebra"]
git-tree-sha1 = "83ee8183bd8c4a390ae178385e6c7b3aa4e468b2"
uuid = "9e997f8a-9a97-42d5-a9f1-ce6bfc15e2c0"
version = "0.1.11"
weakdeps = ["InverseFunctions", "Test"]

    [deps.ChangesOfVariables.extensions]
    ChangesOfVariablesInverseFunctionsExt = "InverseFunctions"
    ChangesOfVariablesTestExt = "Test"

[[deps.CodecZlib]]
deps = ["TranscodingStreams", "Zlib_jll"]
git-tree-sha1 = "962834c22b66e32aa10f7611c08c8ca4e20749a9"
uuid = "944b1d66-785c-5afd-91f1-9de20f533193"
version = "0.7.8"

[[deps.CommonSolve]]
git-tree-sha1 = "cf963add2340ad9960e5eb22844e61ad8f931fe1"
uuid = "38540f10-b2f7-11e9-35d8-d573e4eb0ff2"
version = "0.2.13"

[[deps.CommonSubexpressions]]
deps = ["MacroTools"]
git-tree-sha1 = "cda2cfaebb4be89c9084adaca7dd7333369715c5"
uuid = "bbf7d656-a473-5ed7-a52c-81e309532950"
version = "0.3.1"

[[deps.Compat]]
deps = ["TOML", "UUIDs"]
git-tree-sha1 = "9d8a54ce4b17aa5bdce0ea5c34bc5e7c340d16ad"
uuid = "34da2185-b29b-5c13-b0c7-acf172513d20"
version = "4.18.1"
weakdeps = ["Dates", "LinearAlgebra"]

    [deps.Compat.extensions]
    CompatLinearAlgebraExt = "LinearAlgebra"

[[deps.CompilerSupportLibraries_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "e66e0078-7015-5450-92f7-15fbd957f2ae"
version = "1.3.0+1"

[[deps.CompositionsBase]]
git-tree-sha1 = "802bb88cd69dfd1509f6670416bd4434015693ad"
uuid = "a33af91c-f02d-484b-be07-31d278c5ca2b"
version = "0.1.2"
weakdeps = ["InverseFunctions"]

    [deps.CompositionsBase.extensions]
    CompositionsBaseInverseFunctionsExt = "InverseFunctions"

[[deps.ConsoleProgressMonitor]]
deps = ["Logging", "ProgressMeter"]
git-tree-sha1 = "3ab7b2136722890b9af903859afcf457fa3059e8"
uuid = "88cd18e8-d9cc-4ea6-8889-5259c0d15c8b"
version = "0.1.2"

[[deps.ConstructionBase]]
git-tree-sha1 = "b4b092499347b18a015186eae3042f72267106cb"
uuid = "187b0558-2788-49d3-abe0-74a17ed4e7c9"
version = "1.6.0"
weakdeps = ["IntervalSets", "LinearAlgebra", "StaticArrays"]

    [deps.ConstructionBase.extensions]
    ConstructionBaseIntervalSetsExt = "IntervalSets"
    ConstructionBaseLinearAlgebraExt = "LinearAlgebra"
    ConstructionBaseStaticArraysExt = "StaticArrays"

[[deps.Crayons]]
git-tree-sha1 = "54b76cbb40d9a0f5368c880725b2f141da77c94f"
uuid = "a8cc5b0e-0ffa-5ad4-8c14-923d3ee1735f"
version = "4.2.0"

[[deps.DataAPI]]
git-tree-sha1 = "abe83f3a2f1b857aac70ef8b269080af17764bbe"
uuid = "9a962f9c-6df0-11e9-0e5d-c546b8b5ee8a"
version = "1.16.0"

[[deps.DataFrames]]
deps = ["Compat", "DataAPI", "DataStructures", "Future", "InlineStrings", "InvertedIndices", "IteratorInterfaceExtensions", "LinearAlgebra", "Markdown", "Missings", "PooledArrays", "PrecompileTools", "PrettyTables", "Printf", "Random", "Reexport", "SentinelArrays", "SortingAlgorithms", "Statistics", "TableTraits", "Tables", "Unicode"]
git-tree-sha1 = "5fab31e2e01e70ad66e3e24c968c264d1cf166d6"
uuid = "a93c6f00-e57d-5684-b7b6-d8193f3e46c0"
version = "1.8.2"

[[deps.DataStructures]]
deps = ["OrderedCollections"]
git-tree-sha1 = "b0bc6d2cad1fed8b7fd59a1551a991cb3d2809e6"
uuid = "864edb3b-99cc-5e75-8d2d-829cb0a9cfe8"
version = "0.19.6"

[[deps.DataValueInterfaces]]
git-tree-sha1 = "bfc1187b79289637fa0ef6d4436ebdfe6905cbd6"
uuid = "e2d170a0-9d28-54be-80f0-106bbe20a464"
version = "1.0.0"

[[deps.Dates]]
deps = ["Printf"]
uuid = "ade2ca70-3891-5945-98fb-dc099432e06a"
version = "1.11.0"

[[deps.DensityInterface]]
deps = ["InverseFunctions", "Test"]
git-tree-sha1 = "80c3e8639e3353e5d2912fb3a1916b8455e2494b"
uuid = "b429d917-457f-4dbc-8f4c-0cc954292b1d"
version = "0.4.0"

[[deps.DiffResults]]
deps = ["StaticArraysCore"]
git-tree-sha1 = "782dd5f4561f5d267313f23853baaaa4c52ea621"
uuid = "163ba53b-c6d8-5494-b064-1a9d43ac40c5"
version = "1.1.0"

[[deps.DiffRules]]
deps = ["IrrationalConstants", "LogExpFunctions", "NaNMath", "Random", "SpecialFunctions"]
git-tree-sha1 = "79a2aca180a85c690c58a020d47b426954b590f8"
uuid = "b552c78f-8df3-52c6-915a-8e097449b14b"
version = "1.16.0"

[[deps.DifferentiationInterface]]
deps = ["ADTypes", "LinearAlgebra"]
git-tree-sha1 = "dbd46a5cd0e79a97438b0ebbec42e744e8f436fe"
uuid = "a0c0ee7d-e4b9-4e03-894e-1c5f64a51d63"
version = "0.7.20"

    [deps.DifferentiationInterface.extensions]
    DifferentiationInterfaceChainRulesCoreExt = "ChainRulesCore"
    DifferentiationInterfaceDiffractorExt = "Diffractor"
    DifferentiationInterfaceEnzymeExt = ["EnzymeCore", "Enzyme"]
    DifferentiationInterfaceFastDifferentiationExt = "FastDifferentiation"
    DifferentiationInterfaceFiniteDiffExt = "FiniteDiff"
    DifferentiationInterfaceFiniteDifferencesExt = "FiniteDifferences"
    DifferentiationInterfaceForwardDiffExt = ["ForwardDiff", "DiffResults"]
    DifferentiationInterfaceGPUArraysCoreExt = ["GPUArraysCore", "Adapt"]
    DifferentiationInterfaceGTPSAExt = "GTPSA"
    DifferentiationInterfaceHyperHessiansExt = "HyperHessians"
    DifferentiationInterfaceMooncakeExt = "Mooncake"
    DifferentiationInterfacePolyesterForwardDiffExt = ["PolyesterForwardDiff", "ForwardDiff", "DiffResults"]
    DifferentiationInterfaceReverseDiffExt = ["ReverseDiff", "DiffResults"]
    DifferentiationInterfaceSparseArraysExt = "SparseArrays"
    DifferentiationInterfaceSparseConnectivityTracerExt = "SparseConnectivityTracer"
    DifferentiationInterfaceSparseMatrixColoringsExt = "SparseMatrixColorings"
    DifferentiationInterfaceStaticArraysExt = "StaticArrays"
    DifferentiationInterfaceSymbolicsExt = "Symbolics"
    DifferentiationInterfaceTrackerExt = "Tracker"
    DifferentiationInterfaceZygoteExt = ["Zygote", "ForwardDiff"]

    [deps.DifferentiationInterface.weakdeps]
    Adapt = "79e6a3ab-5dfb-504d-930d-738a2a938a0e"
    ChainRulesCore = "d360d2e6-b24c-11e9-a2a3-2a2ae2dbcce4"
    DiffResults = "163ba53b-c6d8-5494-b064-1a9d43ac40c5"
    Diffractor = "9f5e2b26-1114-432f-b630-d3fe2085c51c"
    Enzyme = "7da242da-08ed-463a-9acd-ee780be4f1d9"
    EnzymeCore = "f151be2c-9106-41f4-ab19-57ee4f262869"
    FastDifferentiation = "eb9bf01b-bf85-4b60-bf87-ee5de06c00be"
    FiniteDiff = "6a86dc24-6348-571c-b903-95158fe2bd41"
    FiniteDifferences = "26cc04aa-876d-5657-8c51-4c34ba976000"
    ForwardDiff = "f6369f11-7733-5829-9624-2563aa707210"
    GPUArraysCore = "46192b85-c4d5-4398-a991-12ede77f4527"
    GTPSA = "b27dd330-f138-47c5-815b-40db9dd9b6e8"
    HyperHessians = "06b494a0-c8e0-40cc-ad32-d99506a00a6c"
    Mooncake = "da2b9cff-9c12-43a0-ae48-6db2b0edb7d6"
    PolyesterForwardDiff = "98d1487c-24ca-40b6-b7ab-df2af84e126b"
    ReverseDiff = "37e2e3b7-166d-5795-8a7a-e32c996b4267"
    SparseArrays = "2f01184e-e22b-5df5-ae63-d93ebab69eaf"
    SparseConnectivityTracer = "9f842d2f-2579-4b1d-911e-f412cf18a3f5"
    SparseMatrixColorings = "0a514795-09f3-496d-8182-132a7b665d35"
    StaticArrays = "90137ffa-7385-5640-81b9-e52037218182"
    Symbolics = "0c5d862f-8b57-4792-8d23-62f2024744c7"
    Tracker = "9f7883ad-71c0-57eb-9f7f-b5c9e6d3789c"
    Zygote = "e88e6eb3-aa80-5325-afca-941959d7151f"

[[deps.Distributed]]
deps = ["Random", "Serialization", "Sockets"]
uuid = "8ba89e20-285c-5b6f-9357-94700520ee1b"
version = "1.11.0"

[[deps.Distributions]]
deps = ["AliasTables", "FillArrays", "LinearAlgebra", "PDMats", "Printf", "QuadGK", "Random", "Roots", "SpecialFunctions", "Statistics", "StatsAPI", "StatsBase", "StatsFuns"]
git-tree-sha1 = "d2facc77c08c1c2bfb1a77c148edd05b3db5410b"
uuid = "31c24e10-a181-5473-b8eb-7969acd0382f"
version = "0.25.130"

    [deps.Distributions.extensions]
    DistributionsChainRulesCoreExt = "ChainRulesCore"
    DistributionsDensityInterfaceExt = "DensityInterface"
    DistributionsSparseConnectivityTracerExt = "SparseConnectivityTracer"
    DistributionsTestExt = "Test"

    [deps.Distributions.weakdeps]
    ChainRulesCore = "d360d2e6-b24c-11e9-a2a3-2a2ae2dbcce4"
    DensityInterface = "b429d917-457f-4dbc-8f4c-0cc954292b1d"
    SparseConnectivityTracer = "9f842d2f-2579-4b1d-911e-f412cf18a3f5"
    Test = "8dfed614-e22c-5e08-85e1-65c5234f0b40"

[[deps.DocStringExtensions]]
git-tree-sha1 = "7442a5dfe1ebb773c29cc2962a8980f47221d76c"
uuid = "ffbed154-4ef7-542d-bbb7-c09d3a79fcae"
version = "0.9.5"

[[deps.Downloads]]
deps = ["ArgTools", "FileWatching", "LibCURL", "NetworkOptions"]
uuid = "f43a241f-c20a-4ad4-852c-f6b1247861c6"
version = "1.7.0"

[[deps.DynamicPPL]]
deps = ["ADTypes", "AbstractMCMC", "AbstractPPL", "Accessors", "BangBang", "Bijectors", "Chairmarks", "Compat", "ConstructionBase", "DifferentiationInterface", "Distributions", "DocStringExtensions", "FillArrays", "InteractiveUtils", "LinearAlgebra", "LogDensityProblems", "MacroTools", "OrderedCollections", "PartitionedDistributions", "PrecompileTools", "Preferences", "Printf", "Random", "Statistics", "Test"]
git-tree-sha1 = "ec00e9fd60e861925780a4d0bd001862747a8a73"
uuid = "366bfd00-2699-11ea-058f-f148b4cae6d8"
version = "0.41.8"

    [deps.DynamicPPL.extensions]
    DynamicPPLComponentArraysExt = ["ComponentArrays"]
    DynamicPPLEnzymeCoreExt = ["EnzymeCore"]
    DynamicPPLForwardDiffExt = ["ForwardDiff"]
    DynamicPPLMCMCChainsExt = ["MCMCChains"]
    DynamicPPLMarginalLogDensitiesExt = ["MarginalLogDensities"]
    DynamicPPLMooncakeExt = ["Mooncake", "DifferentiationInterface"]
    DynamicPPLReverseDiffExt = ["ReverseDiff"]

    [deps.DynamicPPL.weakdeps]
    ComponentArrays = "b0b7db55-cfe3-40fc-9ded-d10e2dbeff66"
    EnzymeCore = "f151be2c-9106-41f4-ab19-57ee4f262869"
    ForwardDiff = "f6369f11-7733-5829-9624-2563aa707210"
    KernelAbstractions = "63c18a36-062a-441e-b654-da1e3ab1ce7c"
    MCMCChains = "c7f686f2-ff18-58e9-bc7b-31028e88f75d"
    MarginalLogDensities = "f0c3360a-fb8d-11e9-1194-5521fd7ee392"
    Mooncake = "da2b9cff-9c12-43a0-ae48-6db2b0edb7d6"
    ReverseDiff = "37e2e3b7-166d-5795-8a7a-e32c996b4267"

[[deps.EllipticalSliceSampling]]
deps = ["AbstractMCMC", "ArrayInterface", "Distributions", "Random", "Statistics"]
git-tree-sha1 = "e611b7fdfbfb5b18d5e98776c30daede41b44542"
uuid = "cad2338a-1db2-11e9-3401-43bc07c9ede2"
version = "2.0.0"

[[deps.EnumX]]
git-tree-sha1 = "c49898e8438c828577f04b92fc9368c388ac783c"
uuid = "4e289a0a-7415-4d19-859d-a7e5c4648b56"
version = "1.0.7"

[[deps.EnzymeCore]]
git-tree-sha1 = "971d7831cc85f43bc9f51d615a3f7f21270c2f1d"
uuid = "f151be2c-9106-41f4-ab19-57ee4f262869"
version = "0.8.21"
weakdeps = ["Adapt", "ChainRulesCore"]

    [deps.EnzymeCore.extensions]
    AdaptExt = "Adapt"
    EnzymeCoreChainRulesCoreExt = "ChainRulesCore"

[[deps.ExprTools]]
git-tree-sha1 = "d2e49e7efd29719d6f28b891b0e0e159daa9d2b4"
uuid = "e2ba6199-217a-4e67-a87a-7c52f15ade04"
version = "0.1.11"

[[deps.ExproniconLite]]
git-tree-sha1 = "c13f0b150373771b0fdc1713c97860f8df12e6c2"
uuid = "55351af7-c7e9-48d6-89ff-24e801d99491"
version = "0.10.14"

[[deps.FFTA]]
deps = ["AbstractFFTs", "DocStringExtensions", "LinearAlgebra", "MuladdMacro", "Primes", "Random", "Reexport"]
git-tree-sha1 = "65e55303b72f4a567a51b174dd2c47496efeb95a"
uuid = "b86e33f2-c0db-4aa1-a6e0-ab43e668529e"
version = "0.3.1"

[[deps.FilePathsBase]]
deps = ["Compat", "Dates"]
git-tree-sha1 = "3bab2c5aa25e7840a4b065805c0cdfc01f3068d2"
uuid = "48062228-2e41-5def-b9a4-89aafe57970f"
version = "0.9.24"
weakdeps = ["Mmap", "Test"]

    [deps.FilePathsBase.extensions]
    FilePathsBaseMmapExt = "Mmap"
    FilePathsBaseTestExt = "Test"

[[deps.FileWatching]]
uuid = "7b1f6079-737a-58dc-b8bc-7a2ca5c1b5ee"
version = "1.11.0"

[[deps.FillArrays]]
deps = ["LinearAlgebra"]
git-tree-sha1 = "5bad39456d9f0166184fce2248783dd9862645c1"
uuid = "1a297f60-69ca-5386-bcde-b61e274b549b"
version = "1.17.0"
weakdeps = ["PDMats", "SparseArrays", "StaticArrays", "Statistics"]

    [deps.FillArrays.extensions]
    FillArraysPDMatsExt = "PDMats"
    FillArraysSparseArraysExt = "SparseArrays"
    FillArraysStaticArraysExt = "StaticArrays"
    FillArraysStatisticsExt = "Statistics"

[[deps.FiniteDiff]]
deps = ["ArrayInterface", "LinearAlgebra", "Setfield"]
git-tree-sha1 = "0a155bdf6f00bfe7f80adc3e7e5aae19851fbea1"
uuid = "6a86dc24-6348-571c-b903-95158fe2bd41"
version = "2.32.1"

    [deps.FiniteDiff.extensions]
    FiniteDiffBandedMatricesExt = "BandedMatrices"
    FiniteDiffBlockBandedMatricesExt = "BlockBandedMatrices"
    FiniteDiffSparseArraysExt = "SparseArrays"
    FiniteDiffStaticArraysExt = "StaticArrays"

    [deps.FiniteDiff.weakdeps]
    BandedMatrices = "aae01518-5342-5314-be14-df237901396f"
    BlockBandedMatrices = "ffab5731-97b5-5995-9138-79e8c1846df0"
    SparseArrays = "2f01184e-e22b-5df5-ae63-d93ebab69eaf"
    StaticArrays = "90137ffa-7385-5640-81b9-e52037218182"

[[deps.ForwardDiff]]
deps = ["CommonSubexpressions", "DiffResults", "DiffRules", "LinearAlgebra", "LogExpFunctions", "NaNMath", "Preferences", "Printf", "Random", "SpecialFunctions"]
git-tree-sha1 = "afb7c51ac63e40708a3071f80f5e84a752299d4f"
uuid = "f6369f11-7733-5829-9624-2563aa707210"
version = "0.10.39"
weakdeps = ["StaticArrays"]

    [deps.ForwardDiff.extensions]
    ForwardDiffStaticArraysExt = "StaticArrays"

[[deps.FunctionWrappers]]
git-tree-sha1 = "d62485945ce5ae9c0c48f124a84998d755bae00e"
uuid = "069b7b12-0de2-55c6-9aab-29f3d0a68a2e"
version = "1.1.3"

[[deps.FunctionWrappersWrappers]]
deps = ["FunctionWrappers"]
git-tree-sha1 = "b104d487b34566608f8b4e1c39fb0b10aa279ff8"
uuid = "77dc65aa-8811-40c2-897b-53d922fa7daf"
version = "0.1.3"

[[deps.Functors]]
deps = ["Compat", "ConstructionBase", "LinearAlgebra", "Random"]
git-tree-sha1 = "1ac2813982db52b974c9343124ca61adbf297316"
uuid = "d9f16b24-f501-4c13-a1f2-28368ffc5196"
version = "0.5.3"

[[deps.Future]]
deps = ["Random"]
uuid = "9fa8497b-333b-5362-9e8d-4d0656e87820"
version = "1.11.0"

[[deps.GPUArraysCore]]
deps = ["Adapt"]
git-tree-sha1 = "83cf05ab16a73219e5f6bd1bdfa9848fa24ac627"
uuid = "46192b85-c4d5-4398-a991-12ede77f4527"
version = "0.2.0"

[[deps.Gamma]]
git-tree-sha1 = "86f86b6168a016ed88e4ae4e64577b98c3b59e8e"
uuid = "a0844989-3bd2-4988-8bea-c9407ab0941b"
version = "1.1.0"

[[deps.HypergeometricFunctions]]
deps = ["Gamma", "LinearAlgebra"]
git-tree-sha1 = "31bb6c92405c084617facc1d7ed9eb6c402d061e"
uuid = "34004b35-14d8-5ef3-9330-4cdb6864b03a"
version = "0.3.30"

[[deps.InitialValues]]
git-tree-sha1 = "4da0f88e9a39111c2fa3add390ab15f3a44f3ca3"
uuid = "22cec73e-a1b8-11e9-2c92-598750a2cf9c"
version = "0.3.1"

[[deps.InlineStrings]]
git-tree-sha1 = "8f3d257792a522b4601c24a577954b0a8cd7334d"
uuid = "842dd82b-1e85-43dc-bf29-5d0ee9dffc48"
version = "1.4.5"

    [deps.InlineStrings.extensions]
    ArrowTypesExt = "ArrowTypes"
    ParsersExt = "Parsers"

    [deps.InlineStrings.weakdeps]
    ArrowTypes = "31f734f8-188a-4ce0-8406-c8a06bd891cd"
    Parsers = "69de0a69-1ddd-5017-9359-2bf0b02dc9f0"

[[deps.IntegerMathUtils]]
git-tree-sha1 = "c72458f1962faeb003bf23cbdb75164fe6280906"
uuid = "18e54dd8-cb9d-406c-a71d-865a43cbb235"
version = "0.1.4"

[[deps.InteractiveUtils]]
deps = ["Markdown"]
uuid = "b77e0a4c-d291-57a0-90e8-8db25a27a240"
version = "1.11.0"

[[deps.Interpolations]]
deps = ["Adapt", "AxisAlgorithms", "ChainRulesCore", "LinearAlgebra", "OffsetArrays", "Random", "Ratios", "SharedArrays", "SparseArrays", "StaticArrays", "WoodburyMatrices"]
git-tree-sha1 = "65d505fa4c0d7072990d659ef3fc086eb6da8208"
uuid = "a98d9a8b-a2ab-59e6-89dd-64a1c18fca59"
version = "0.16.2"

    [deps.Interpolations.extensions]
    InterpolationsForwardDiffExt = "ForwardDiff"
    InterpolationsUnitfulExt = "Unitful"

    [deps.Interpolations.weakdeps]
    ForwardDiff = "f6369f11-7733-5829-9624-2563aa707210"
    Unitful = "1986cc42-f94f-5a68-af5c-568840ba703d"

[[deps.IntervalSets]]
git-tree-sha1 = "79d6bd28c8d9bccc2229784f1bd637689b256377"
uuid = "8197267c-284f-5f27-9208-e0e47529a953"
version = "0.7.14"
weakdeps = ["Random", "RecipesBase", "Statistics"]

    [deps.IntervalSets.extensions]
    IntervalSetsRandomExt = "Random"
    IntervalSetsRecipesBaseExt = "RecipesBase"
    IntervalSetsStatisticsExt = "Statistics"

[[deps.InverseFunctions]]
git-tree-sha1 = "a779299d77cd080bf77b97535acecd73e1c5e5cb"
uuid = "3587e190-3f89-42d0-90ee-14403ec27112"
version = "0.1.17"
weakdeps = ["Dates", "Test"]

    [deps.InverseFunctions.extensions]
    InverseFunctionsDatesExt = "Dates"
    InverseFunctionsTestExt = "Test"

[[deps.InvertedIndices]]
git-tree-sha1 = "6da3c4316095de0f5ee2ebd875df8721e7e0bdbe"
uuid = "41ab1584-1d38-5bbf-9106-f11c6c58b48f"
version = "1.3.1"

[[deps.IrrationalConstants]]
git-tree-sha1 = "b2d91fe939cae05960e760110b328288867b5758"
uuid = "92d709cd-6900-40b7-9082-c6be49f344b6"
version = "0.2.6"

[[deps.IterTools]]
git-tree-sha1 = "42d5f897009e7ff2cf88db414a389e5ed1bdd023"
uuid = "c8e1da08-722c-5040-9ed9-7db0dc04731e"
version = "1.10.0"

[[deps.IteratorInterfaceExtensions]]
git-tree-sha1 = "a3f24677c21f5bbe9d2a714f95dcd58337fb2856"
uuid = "82899510-4779-5014-852e-03e436cf321d"
version = "1.0.0"

[[deps.JLLWrappers]]
deps = ["Artifacts", "Preferences"]
git-tree-sha1 = "7204148362dafe5fe6a273f855b8ccbe4df8173e"
uuid = "692b3bcd-3c85-4b1f-b108-f13ce0eb3210"
version = "1.8.0"

[[deps.JSON]]
deps = ["Dates", "Mmap", "Parsers", "Unicode"]
git-tree-sha1 = "31e996f0a15c7b280ba9f76636b3ff9e2ae58c9a"
uuid = "682c06a0-de6a-54ab-a142-c8b1cf79cde6"
version = "0.21.4"

[[deps.Jieko]]
deps = ["ExproniconLite"]
git-tree-sha1 = "2f05ed29618da60c06a87e9c033982d4f71d0b6c"
uuid = "ae98c720-c025-4a4a-838c-29b094483192"
version = "0.2.1"

[[deps.JuliaSyntaxHighlighting]]
deps = ["StyledStrings"]
uuid = "ac6e5ff7-fb65-4e79-a425-ec3bc9c03011"
version = "1.12.0"

[[deps.KernelDensity]]
deps = ["Distributions", "DocStringExtensions", "FFTA", "Interpolations", "StatsBase"]
git-tree-sha1 = "9eda8292dd3268b3b7ec9df21bbfac24e177ec52"
uuid = "5ab0869b-81aa-558d-bb23-cbf5423bbe9b"
version = "0.6.12"

[[deps.LBFGSB]]
deps = ["L_BFGS_B_jll"]
git-tree-sha1 = "e2e6f53ee20605d0ea2be473480b7480bd5091b5"
uuid = "5be7bae1-8223-5378-bac3-9e7378a2f6e6"
version = "0.4.1"

[[deps.L_BFGS_B_jll]]
deps = ["Artifacts", "CompilerSupportLibraries_jll", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "77feda930ed3f04b2b0fbb5bea89e69d3677c6b0"
uuid = "81d17ec3-03a1-5e46-b53e-bddc35a13473"
version = "3.0.1+0"

[[deps.LaTeXStrings]]
git-tree-sha1 = "dda21b8cbd6a6c40d9d02a73230f9d70fed6918c"
uuid = "b964fa9f-0449-5b57-a5c2-d3ea65f4040f"
version = "1.4.0"

[[deps.LeftChildRightSiblingTrees]]
deps = ["AbstractTrees"]
git-tree-sha1 = "d4816abce26971e3237b46a47b99991f306e4832"
uuid = "1d6d02ad-be62-4b6b-8a6d-2f90e265016e"
version = "0.3.0"

[[deps.LibCURL]]
deps = ["LibCURL_jll", "MozillaCACerts_jll"]
uuid = "b27032c2-a3e7-50c8-80cd-2d36dbcbfd21"
version = "0.6.4"

[[deps.LibCURL_jll]]
deps = ["Artifacts", "LibSSH2_jll", "Libdl", "OpenSSL_jll", "Zlib_jll", "nghttp2_jll"]
uuid = "deac9b47-8bc7-5906-a0fe-35ac56dc84c0"
version = "8.15.0+0"

[[deps.LibGit2]]
deps = ["LibGit2_jll", "NetworkOptions", "Printf", "SHA"]
uuid = "76f85450-5226-5b5a-8eaa-529ad045b433"
version = "1.11.0"

[[deps.LibGit2_jll]]
deps = ["Artifacts", "LibSSH2_jll", "Libdl", "OpenSSL_jll"]
uuid = "e37daf67-58a4-590a-8e99-b0245dd2ffc5"
version = "1.9.0+0"

[[deps.LibSSH2_jll]]
deps = ["Artifacts", "Libdl", "OpenSSL_jll"]
uuid = "29816b5a-b9ab-546f-933c-edad1886dfa8"
version = "1.11.3+1"

[[deps.Libdl]]
uuid = "8f399da3-3557-5675-b5ff-fb832c97cbdb"
version = "1.11.0"

[[deps.Libtask]]
deps = ["MistyClosures", "Test"]
git-tree-sha1 = "188e6364a7bb87f21e37b7545e13ab204614edf0"
uuid = "6f1fad26-d15e-5dc8-ae53-837a1d7b8c9f"
version = "0.9.18"

[[deps.LineSearches]]
deps = ["LinearAlgebra", "NLSolversBase", "NaNMath", "Parameters", "Printf"]
git-tree-sha1 = "4adee99b7262ad2a1a4bbbc59d993d24e55ea96f"
uuid = "d3d80556-e9d4-5f37-9878-2ab0fcc64255"
version = "7.4.0"

[[deps.LinearAlgebra]]
deps = ["Libdl", "OpenBLAS_jll", "libblastrampoline_jll"]
uuid = "37e2e46d-f89d-539d-b4ee-838fcccc9c8e"
version = "1.12.0"

[[deps.LogDensityProblems]]
deps = ["ArgCheck", "DocStringExtensions", "Random"]
git-tree-sha1 = "d9625f27ded4ad726ceca7819394a4cc77ed25b3"
uuid = "6fdf6af0-433a-55f7-b3ed-c6c6e0b8df7c"
version = "2.2.0"

[[deps.LogDensityProblemsAD]]
deps = ["DocStringExtensions", "LogDensityProblems"]
git-tree-sha1 = "7b83f3ad0a8105f79a067cafbfd124827bb398d0"
uuid = "996a588d-648d-4e1f-a8f0-a84b347e47b1"
version = "1.13.1"

    [deps.LogDensityProblemsAD.extensions]
    LogDensityProblemsADADTypesExt = "ADTypes"
    LogDensityProblemsADDifferentiationInterfaceExt = ["ADTypes", "DifferentiationInterface"]
    LogDensityProblemsADEnzymeExt = "Enzyme"
    LogDensityProblemsADFiniteDifferencesExt = "FiniteDifferences"
    LogDensityProblemsADForwardDiffBenchmarkToolsExt = ["BenchmarkTools", "ForwardDiff"]
    LogDensityProblemsADForwardDiffExt = "ForwardDiff"
    LogDensityProblemsADReverseDiffExt = "ReverseDiff"
    LogDensityProblemsADTrackerExt = "Tracker"
    LogDensityProblemsADZygoteExt = "Zygote"

    [deps.LogDensityProblemsAD.weakdeps]
    ADTypes = "47edcb42-4c32-4615-8424-f2b9edc5f35b"
    BenchmarkTools = "6e4b80f9-dd63-53aa-95a3-0cdb28fa8baf"
    DifferentiationInterface = "a0c0ee7d-e4b9-4e03-894e-1c5f64a51d63"
    Enzyme = "7da242da-08ed-463a-9acd-ee780be4f1d9"
    FiniteDifferences = "26cc04aa-876d-5657-8c51-4c34ba976000"
    ForwardDiff = "f6369f11-7733-5829-9624-2563aa707210"
    ReverseDiff = "37e2e3b7-166d-5795-8a7a-e32c996b4267"
    Tracker = "9f7883ad-71c0-57eb-9f7f-b5c9e6d3789c"
    Zygote = "e88e6eb3-aa80-5325-afca-941959d7151f"

[[deps.LogExpFunctions]]
deps = ["DocStringExtensions", "IrrationalConstants", "LinearAlgebra"]
git-tree-sha1 = "13ca9e2586b89836fd20cccf56e57e2b9ae7f38f"
uuid = "2ab3a3ac-af41-5b50-aa03-7779005ae688"
version = "0.3.29"
weakdeps = ["ChainRulesCore", "ChangesOfVariables", "InverseFunctions"]

    [deps.LogExpFunctions.extensions]
    LogExpFunctionsChainRulesCoreExt = "ChainRulesCore"
    LogExpFunctionsChangesOfVariablesExt = "ChangesOfVariables"
    LogExpFunctionsInverseFunctionsExt = "InverseFunctions"

[[deps.Logging]]
uuid = "56ddb016-857b-54e1-b83d-db4d58db5568"
version = "1.11.0"

[[deps.LoggingExtras]]
deps = ["Dates", "Logging"]
git-tree-sha1 = "f00544d95982ea270145636c181ceda21c4e2575"
uuid = "e6f89c97-d47a-5376-807f-9c37f3926c36"
version = "1.2.0"

[[deps.MCMCChains]]
deps = ["AbstractMCMC", "AxisArrays", "DataAPI", "Dates", "Distributions", "IteratorInterfaceExtensions", "KernelDensity", "LinearAlgebra", "MCMCDiagnosticTools", "MLJModelInterface", "NaturalSort", "OrderedCollections", "PrettyTables", "Random", "RecipesBase", "Statistics", "StatsBase", "StatsFuns", "TableTraits", "Tables"]
git-tree-sha1 = "060d6bc7cf60e621dfd056ed2c1a2db1e68db0fe"
uuid = "c7f686f2-ff18-58e9-bc7b-31028e88f75d"
version = "7.7.0"

[[deps.MCMCDiagnosticTools]]
deps = ["AbstractFFTs", "DataAPI", "DataStructures", "Distributions", "LinearAlgebra", "MLJModelInterface", "Random", "SpecialFunctions", "Statistics", "StatsBase", "StatsFuns", "Tables"]
git-tree-sha1 = "526c98cd41028da22c01cb8a203246799ad853a8"
uuid = "be115224-59cd-429b-ad48-344e309966f0"
version = "0.3.15"

[[deps.MLJModelInterface]]
deps = ["InteractiveUtils", "REPL", "Random", "ScientificTypesBase", "StatisticalTraits"]
git-tree-sha1 = "c275fae2e693206b4527dd9d2382aa15359ef3ed"
uuid = "e80e1ace-859a-464e-9ed9-23947d8ae3ea"
version = "1.12.1"

[[deps.MacroTools]]
git-tree-sha1 = "1e0228a030642014fe5cfe68c2c0a818f9e3f522"
uuid = "1914dd2f-81c6-5fcd-8719-6d5c9610ff09"
version = "0.5.16"

[[deps.MappedArrays]]
git-tree-sha1 = "0ee4497a4e80dbd29c058fcee6493f5219556f40"
uuid = "dbb5928d-eab1-5f90-85c2-b9b0edb7c900"
version = "0.4.3"

[[deps.Markdown]]
deps = ["Base64", "JuliaSyntaxHighlighting", "StyledStrings"]
uuid = "d6f4376e-aef5-505a-96c1-9c027394607a"
version = "1.11.0"

[[deps.Missings]]
deps = ["DataAPI"]
git-tree-sha1 = "ec4f7fbeab05d7747bdf98eb74d130a2a2ed298d"
uuid = "e1d29d7a-bbdc-5cf2-9ac0-f12de2c33e28"
version = "1.2.0"

[[deps.MistyClosures]]
git-tree-sha1 = "d1a692e293c2a0dc8fda79c04cad60582f3d4de3"
uuid = "dbe65cb8-6be2-42dd-bbc5-4196aaced4f4"
version = "2.1.0"

[[deps.Mmap]]
uuid = "a63ad114-7e13-5084-954f-fe012c677804"
version = "1.11.0"

[[deps.Moshi]]
deps = ["ExproniconLite", "Jieko"]
git-tree-sha1 = "60beb0717782a3bbe0f7df56decad0ef89048c23"
uuid = "2e0e35c7-a2e4-4343-998d-7ef72827ed2d"
version = "0.3.12"

[[deps.MozillaCACerts_jll]]
uuid = "14a3606d-f60d-562e-9121-12d972cd8159"
version = "2025.11.4"

[[deps.MuladdMacro]]
deps = ["PrecompileTools"]
git-tree-sha1 = "283bf85d4a767481dd924dff0eee1735e95f449e"
uuid = "46d2c3a1-f734-5fdb-9937-b9b9aeba4221"
version = "0.2.7"

[[deps.NLSolversBase]]
deps = ["ADTypes", "DifferentiationInterface", "Distributed", "FiniteDiff", "ForwardDiff"]
git-tree-sha1 = "25a6638571a902ecfb1ae2a18fc1575f86b1d4df"
uuid = "d41bc354-129a-5804-8e4c-c37616107c6c"
version = "7.10.0"

[[deps.NaNMath]]
deps = ["OpenLibm_jll"]
git-tree-sha1 = "9b8215b1ee9e78a293f99797cd31375471b2bcae"
uuid = "77ba4419-2d1f-58cd-9bb1-8ffee604a2e3"
version = "1.1.3"

[[deps.NaturalSort]]
git-tree-sha1 = "eda490d06b9f7c00752ee81cfa451efe55521e21"
uuid = "c020b1a1-e9b0-503a-9c33-f039bfc54a85"
version = "1.0.0"

[[deps.NetworkOptions]]
uuid = "ca575930-c2e3-43a9-ace4-1e988b2c1908"
version = "1.3.0"

[[deps.OffsetArrays]]
git-tree-sha1 = "117432e406b5c023f665fa73dc26e79ec3630151"
uuid = "6fe1bfb0-de20-5000-8ca7-80f57d26f881"
version = "1.17.0"
weakdeps = ["Adapt"]

    [deps.OffsetArrays.extensions]
    OffsetArraysAdaptExt = "Adapt"

[[deps.OpenBLAS_jll]]
deps = ["Artifacts", "CompilerSupportLibraries_jll", "Libdl"]
uuid = "4536629a-c528-5b80-bd46-f80d51c5b363"
version = "0.3.29+0"

[[deps.OpenLibm_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "05823500-19ac-5b8b-9628-191a04bc5112"
version = "0.8.7+0"

[[deps.OpenSSL_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "458c3c95-2e84-50aa-8efc-19380b2a3a95"
version = "3.5.4+0"

[[deps.OpenSpecFun_jll]]
deps = ["Artifacts", "CompilerSupportLibraries_jll", "JLLWrappers", "Libdl"]
git-tree-sha1 = "1346c9208249809840c91b26703912dff463d335"
uuid = "efe28fd5-8261-553b-a9e1-b2916fc3738e"
version = "0.5.6+0"

[[deps.Optim]]
deps = ["Compat", "EnumX", "FillArrays", "ForwardDiff", "LineSearches", "LinearAlgebra", "NLSolversBase", "NaNMath", "PositiveFactorizations", "Printf", "SparseArrays", "StatsBase"]
git-tree-sha1 = "61942645c38dd2b5b78e2082c9b51ab315315d10"
uuid = "429524aa-4258-5aef-a3af-852621145aeb"
version = "1.13.2"

    [deps.Optim.extensions]
    OptimMOIExt = "MathOptInterface"

    [deps.Optim.weakdeps]
    MathOptInterface = "b8f27783-ece8-5eb3-8dc8-9495eed66fee"

[[deps.Optimisers]]
deps = ["ChainRulesCore", "ConstructionBase", "Functors", "LinearAlgebra", "Random", "Statistics"]
git-tree-sha1 = "36b5d2b9dd06290cd65fcf5bdbc3a551ed133af5"
uuid = "3bd65402-5787-11e9-1adc-39752487f4e2"
version = "0.4.7"

    [deps.Optimisers.extensions]
    OptimisersAdaptExt = ["Adapt"]
    OptimisersEnzymeCoreExt = "EnzymeCore"
    OptimisersReactantExt = "Reactant"

    [deps.Optimisers.weakdeps]
    Adapt = "79e6a3ab-5dfb-504d-930d-738a2a938a0e"
    EnzymeCore = "f151be2c-9106-41f4-ab19-57ee4f262869"
    Reactant = "3c362404-f566-11ee-1572-e11a4b42c853"

[[deps.Optimization]]
deps = ["ADTypes", "ArrayInterface", "ConsoleProgressMonitor", "DocStringExtensions", "LBFGSB", "LinearAlgebra", "Logging", "LoggingExtras", "OptimizationBase", "Pkg", "Printf", "ProgressLogging", "Reexport", "SciMLBase", "SparseArrays", "TerminalLoggers"]
git-tree-sha1 = "81abd38353faaf0297a964fa6115a54c6a066cab"
uuid = "7f7a1694-90dd-40f0-9382-eb1efda571ba"
version = "3.26.3"

[[deps.OptimizationBase]]
deps = ["ADTypes", "ArrayInterface", "DocStringExtensions", "LinearAlgebra", "Reexport", "Requires", "SciMLBase", "SparseArrays"]
git-tree-sha1 = "dcb1f85b0da580e2363c0197b0366406031a69cd"
uuid = "bca83a33-5cc9-4baa-983d-23429ab6bcbb"
version = "1.2.0"

    [deps.OptimizationBase.extensions]
    OptimizationEnzymeExt = "Enzyme"
    OptimizationFiniteDiffExt = "FiniteDiff"
    OptimizationForwardDiffExt = "ForwardDiff"
    OptimizationMTKExt = "ModelingToolkit"
    OptimizationReverseDiffExt = "ReverseDiff"
    OptimizationSparseDiffExt = ["SparseDiffTools", "Symbolics", "ReverseDiff"]
    OptimizationTrackerExt = "Tracker"
    OptimizationZygoteExt = "Zygote"

    [deps.OptimizationBase.weakdeps]
    Enzyme = "7da242da-08ed-463a-9acd-ee780be4f1d9"
    FiniteDiff = "6a86dc24-6348-571c-b903-95158fe2bd41"
    ForwardDiff = "f6369f11-7733-5829-9624-2563aa707210"
    ModelingToolkit = "961ee093-0014-501f-94e3-6117800e7a78"
    ReverseDiff = "37e2e3b7-166d-5795-8a7a-e32c996b4267"
    SparseDiffTools = "47a9eef4-7e08-11e9-0b38-333d64bd3804"
    Symbolics = "0c5d862f-8b57-4792-8d23-62f2024744c7"
    Tracker = "9f7883ad-71c0-57eb-9f7f-b5c9e6d3789c"
    Zygote = "e88e6eb3-aa80-5325-afca-941959d7151f"

[[deps.OptimizationOptimJL]]
deps = ["Optim", "Optimization", "Reexport", "SparseArrays"]
git-tree-sha1 = "43870d726f883a47d158beebb1fc3c9fab1da9d6"
uuid = "36348300-93cb-4f02-beb5-3c3902f8871e"
version = "0.3.2"

[[deps.OrderedCollections]]
git-tree-sha1 = "94ba93778373a53bfd5a0caaf7d809c445292ff4"
uuid = "bac558e1-5e72-5ebc-8fee-abe8a469f55d"
version = "1.8.2"

[[deps.PDMats]]
deps = ["LinearAlgebra", "SparseArrays", "SuiteSparse"]
git-tree-sha1 = "123266c25174ef6c8d4718920abc206452cf8de6"
uuid = "90014a1f-27ba-587c-ab20-58faa44d9150"
version = "0.11.41"
weakdeps = ["StatsBase"]

    [deps.PDMats.extensions]
    StatsBaseExt = "StatsBase"

[[deps.Parameters]]
deps = ["OrderedCollections", "UnPack"]
git-tree-sha1 = "34c0e9ad262e5f7fc75b10a9952ca7692cfc5fbe"
uuid = "d96e819e-fc66-5662-9728-84c9c7592b0a"
version = "0.12.3"

[[deps.Parsers]]
deps = ["Dates", "PrecompileTools", "UUIDs"]
git-tree-sha1 = "3de8f5e6e90ebfa8d6d1f86997d6cdcd6a912ff3"
uuid = "69de0a69-1ddd-5017-9359-2bf0b02dc9f0"
version = "2.8.7"

[[deps.PartitionedDistributions]]
deps = ["Distributions", "FillArrays", "InvertedIndices", "IrrationalConstants", "LinearAlgebra", "LogExpFunctions", "PDMats", "SpecialFunctions", "StatsBase"]
git-tree-sha1 = "5ea8f2735c0daeba35af6b879487e98f4e797093"
uuid = "569bd051-8d7b-4221-bcb8-d78512b5866a"
version = "0.0.1"

[[deps.Pkg]]
deps = ["Artifacts", "Dates", "Downloads", "FileWatching", "LibGit2", "Libdl", "Logging", "Markdown", "Printf", "Random", "SHA", "TOML", "Tar", "UUIDs", "p7zip_jll"]
uuid = "44cfe95a-1eb2-52ea-b672-e2afdf69b78f"
version = "1.12.1"
weakdeps = ["REPL"]

    [deps.Pkg.extensions]
    REPLExt = "REPL"

[[deps.PooledArrays]]
deps = ["DataAPI", "Future"]
git-tree-sha1 = "36d8b4b899628fb92c2749eb488d884a926614d3"
uuid = "2dfb63ee-cc39-5dd5-95bd-886bf059d720"
version = "1.4.3"

[[deps.PositiveFactorizations]]
deps = ["LinearAlgebra"]
git-tree-sha1 = "17275485f373e6673f7e7f97051f703ed5b15b20"
uuid = "85a6dd25-e78a-55b7-8502-1745935b8125"
version = "0.2.4"

[[deps.PreallocationTools]]
deps = ["Adapt", "ArrayInterface", "PrecompileTools"]
git-tree-sha1 = "c05b4c6325262152483a1ecb6c69846d2e01727b"
uuid = "d236fae5-4411-538c-8e31-a6e3d9e00b46"
version = "0.4.34"

    [deps.PreallocationTools.extensions]
    PreallocationToolsForwardDiffExt = "ForwardDiff"
    PreallocationToolsReverseDiffExt = "ReverseDiff"
    PreallocationToolsSparseConnectivityTracerExt = "SparseConnectivityTracer"

    [deps.PreallocationTools.weakdeps]
    ForwardDiff = "f6369f11-7733-5829-9624-2563aa707210"
    ReverseDiff = "37e2e3b7-166d-5795-8a7a-e32c996b4267"
    SparseConnectivityTracer = "9f842d2f-2579-4b1d-911e-f412cf18a3f5"

[[deps.PrecompileTools]]
deps = ["Preferences"]
git-tree-sha1 = "edbeefc7a4889f528644251bdb5fc9ab5348bc2c"
uuid = "aea7be01-6a6a-4083-8856-8a6e6704d82a"
version = "1.3.4"

[[deps.Preferences]]
deps = ["TOML"]
git-tree-sha1 = "8b770b60760d4451834fe79dd483e318eee709c4"
uuid = "21216c6a-2e73-6563-6e65-726566657250"
version = "1.5.2"

[[deps.PrettyTables]]
deps = ["Crayons", "LaTeXStrings", "Markdown", "PrecompileTools", "Printf", "REPL", "Reexport", "StringManipulation", "Tables"]
git-tree-sha1 = "ca9385c2f2c93a9491c6c53d31e9c237fe21b232"
uuid = "08abe8d2-0d0c-5749-adfa-8a2ac140af0d"
version = "3.4.5"

    [deps.PrettyTables.extensions]
    PrettyTablesExcelExt = "XLSX"
    PrettyTablesTypstryExt = "Typstry"

    [deps.PrettyTables.weakdeps]
    Typstry = "f0ed7684-a786-439e-b1e3-3b82803b501e"
    XLSX = "fdbf4ff8-1666-58a4-91e7-1b58723a45e0"

[[deps.Primes]]
deps = ["IntegerMathUtils"]
git-tree-sha1 = "25cdd1d20cd005b52fc12cb6be3f75faaf59bb9b"
uuid = "27ebfcd6-29c5-5fa9-bf4b-fb8fc14df3ae"
version = "0.5.7"

[[deps.Printf]]
deps = ["Unicode"]
uuid = "de0858da-6303-5e67-8744-51eddeeeb8d7"
version = "1.11.0"

[[deps.ProgressLogging]]
deps = ["Logging", "SHA", "UUIDs"]
git-tree-sha1 = "f0803bc1171e455a04124affa9c21bba5ac4db32"
uuid = "33c8b6b6-d38a-422a-b730-caa89a2f386c"
version = "0.1.6"

[[deps.ProgressMeter]]
deps = ["Distributed", "Printf"]
git-tree-sha1 = "fbb92c6c56b34e1a2c4c36058f68f332bec840e7"
uuid = "92933f4c-e287-5a05-a399-4b506db050ca"
version = "1.11.0"

[[deps.PtrArrays]]
git-tree-sha1 = "4fbbafbc6251b883f4d2705356f3641f3652a7fe"
uuid = "43287f4e-b6f4-7ad1-bb20-aadabca52c3d"
version = "1.4.0"

[[deps.QuadGK]]
deps = ["DataStructures", "LinearAlgebra"]
git-tree-sha1 = "5e8e8b0ab68215d7a2b14b9921a946fee794749e"
uuid = "1fd47b50-473d-5c70-9696-f719f8f3bcdc"
version = "2.11.3"

    [deps.QuadGK.extensions]
    QuadGKEnzymeExt = "Enzyme"

    [deps.QuadGK.weakdeps]
    Enzyme = "7da242da-08ed-463a-9acd-ee780be4f1d9"

[[deps.REPL]]
deps = ["InteractiveUtils", "JuliaSyntaxHighlighting", "Markdown", "Sockets", "StyledStrings", "Unicode"]
uuid = "3fa0cd96-eef1-5676-8a61-b3b8758bbffb"
version = "1.11.0"

[[deps.Random]]
deps = ["SHA"]
uuid = "9a3f8284-a2c9-5f02-9a11-845980a1fd5c"
version = "1.11.0"

[[deps.Random123]]
deps = ["Random", "RandomNumbers"]
git-tree-sha1 = "dbe5fd0b334694e905cb9fda73cd8554333c46e2"
uuid = "74087812-796a-5b5d-8853-05524746bad3"
version = "1.7.1"

[[deps.RandomNumbers]]
deps = ["Random"]
git-tree-sha1 = "c6ec94d2aaba1ab2ff983052cf6a606ca5985902"
uuid = "e6cf234a-135c-5ec9-84dd-332b85af5143"
version = "1.6.0"

[[deps.RangeArrays]]
git-tree-sha1 = "b9039e93773ddcfc828f12aadf7115b4b4d225f5"
uuid = "b3c3ace0-ae52-54e7-9d0b-2c1406fd6b9d"
version = "0.3.2"

[[deps.Ratios]]
deps = ["Requires"]
git-tree-sha1 = "1342a47bf3260ee108163042310d26f2be5ec90b"
uuid = "c84ed2f1-dad5-54f0-aa8e-dbefe2724439"
version = "0.4.5"

    [deps.Ratios.extensions]
    RatiosFixedPointNumbersExt = "FixedPointNumbers"

    [deps.Ratios.weakdeps]
    FixedPointNumbers = "53c48c17-4a7d-5ca2-90c5-79b7896eea93"

[[deps.RecipesBase]]
deps = ["PrecompileTools"]
git-tree-sha1 = "5c3d09cc4f31f5fc6af001c250bf1278733100ff"
uuid = "3cdcf5f2-1ef4-517c-9805-6587b60abb01"
version = "1.3.4"

[[deps.RecursiveArrayTools]]
deps = ["Adapt", "ArrayInterface", "DocStringExtensions", "GPUArraysCore", "LinearAlgebra", "RecipesBase", "StaticArraysCore", "Statistics", "SymbolicIndexingInterface"]
git-tree-sha1 = "96bef5b9ac123fff1b379acf0303cf914aaabdfd"
uuid = "731186ca-8d62-57ce-b412-fbd966d074cd"
version = "3.37.1"

    [deps.RecursiveArrayTools.extensions]
    RecursiveArrayToolsFastBroadcastExt = "FastBroadcast"
    RecursiveArrayToolsForwardDiffExt = "ForwardDiff"
    RecursiveArrayToolsKernelAbstractionsExt = "KernelAbstractions"
    RecursiveArrayToolsMeasurementsExt = "Measurements"
    RecursiveArrayToolsMonteCarloMeasurementsExt = "MonteCarloMeasurements"
    RecursiveArrayToolsReverseDiffExt = ["ReverseDiff", "Zygote"]
    RecursiveArrayToolsSparseArraysExt = ["SparseArrays"]
    RecursiveArrayToolsStructArraysExt = "StructArrays"
    RecursiveArrayToolsTablesExt = ["Tables"]
    RecursiveArrayToolsTrackerExt = "Tracker"
    RecursiveArrayToolsZygoteExt = "Zygote"

    [deps.RecursiveArrayTools.weakdeps]
    FastBroadcast = "7034ab61-46d4-4ed7-9d0f-46aef9175898"
    ForwardDiff = "f6369f11-7733-5829-9624-2563aa707210"
    KernelAbstractions = "63c18a36-062a-441e-b654-da1e3ab1ce7c"
    Measurements = "eff96d63-e80a-5855-80a2-b1b0885c5ab7"
    MonteCarloMeasurements = "0987c9cc-fe09-11e8-30f0-b96dd679fdca"
    ReverseDiff = "37e2e3b7-166d-5795-8a7a-e32c996b4267"
    SparseArrays = "2f01184e-e22b-5df5-ae63-d93ebab69eaf"
    StructArrays = "09ab397b-f2b6-538f-b94a-2f83cf4a842a"
    Tables = "bd369af6-aec1-5ad0-b16a-f7cc5008161c"
    Tracker = "9f7883ad-71c0-57eb-9f7f-b5c9e6d3789c"
    Zygote = "e88e6eb3-aa80-5325-afca-941959d7151f"

[[deps.Reexport]]
git-tree-sha1 = "45e428421666073eab6f2da5c9d310d99bb12f9b"
uuid = "189a3867-3050-52da-a836-e630ba90ab69"
version = "1.2.2"

[[deps.Requires]]
deps = ["UUIDs"]
git-tree-sha1 = "62389eeff14780bfe55195b7204c0d8738436d64"
uuid = "ae029012-a4dd-5104-9daa-d747884805df"
version = "1.3.1"

[[deps.Rmath]]
deps = ["Random", "Rmath_jll"]
git-tree-sha1 = "5b3d50eb374cea306873b371d3f8d3915a018f0b"
uuid = "79098fc4-a85e-5d69-aa6a-4863f24498fa"
version = "0.9.0"

[[deps.Rmath_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl"]
git-tree-sha1 = "6d40b2fe70437b01397d2a4d5b020008da4e7019"
uuid = "f50d1b31-88e8-58de-be2c-1cc44531875f"
version = "0.5.2+0"

[[deps.Roots]]
deps = ["Accessors", "CommonSolve", "Printf"]
git-tree-sha1 = "7fb25a964849d90a0446366cdefca822e0e84900"
uuid = "f2b01f46-fcfa-551c-844a-d8ac1e96c665"
version = "3.0.6"

    [deps.Roots.extensions]
    RootsChainRulesCoreExt = "ChainRulesCore"
    RootsForwardDiffExt = "ForwardDiff"
    RootsIntervalRootFindingExt = "IntervalRootFinding"
    RootsSymPyExt = "SymPy"
    RootsSymPyPythonCallExt = "SymPyPythonCall"
    RootsUnitfulExt = "Unitful"

    [deps.Roots.weakdeps]
    ChainRulesCore = "d360d2e6-b24c-11e9-a2a3-2a2ae2dbcce4"
    ForwardDiff = "f6369f11-7733-5829-9624-2563aa707210"
    IntervalRootFinding = "d2bf35a9-74e0-55ec-b149-d360ff49b807"
    SymPy = "24249f21-da20-56a4-8eb1-6a02cf4ae2e6"
    SymPyPythonCall = "bc8888f7-b21e-4b7c-a06a-5d9c9496438c"
    Unitful = "1986cc42-f94f-5a68-af5c-568840ba703d"

[[deps.RuntimeGeneratedFunctions]]
deps = ["ExprTools", "SHA", "Serialization"]
git-tree-sha1 = "65c9e1142f0372bfc16ba14b9edd57737fe0039f"
uuid = "7e49a35a-f44a-4d26-94aa-eba1b4ca6b47"
version = "0.5.24"

[[deps.SHA]]
uuid = "ea8e919c-243c-51af-8825-aaa63cd721ce"
version = "0.7.0"

[[deps.SSMProblems]]
deps = ["AbstractMCMC", "Distributions", "Random"]
git-tree-sha1 = "cbf723e4c486375cf91236db53a7beefe8291951"
uuid = "26aad666-b158-4e64-9d35-0e672562fa48"
version = "0.6.1"

[[deps.SciMLBase]]
deps = ["ADTypes", "Accessors", "Adapt", "ArrayInterface", "CommonSolve", "ConstructionBase", "Distributed", "DocStringExtensions", "EnumX", "FunctionWrappersWrappers", "IteratorInterfaceExtensions", "LinearAlgebra", "Logging", "Markdown", "Moshi", "PreallocationTools", "PrecompileTools", "Preferences", "Printf", "RecipesBase", "RecursiveArrayTools", "Reexport", "RuntimeGeneratedFunctions", "SciMLOperators", "SciMLStructures", "StaticArraysCore", "Statistics", "SymbolicIndexingInterface"]
git-tree-sha1 = "16fa030fb4bd4df373a677eca0460c3eee791ab2"
uuid = "0bca4576-84f4-4d90-8ffe-ffa030f20462"
version = "2.120.0"

    [deps.SciMLBase.extensions]
    SciMLBaseChainRulesCoreExt = "ChainRulesCore"
    SciMLBaseDistributionsExt = "Distributions"
    SciMLBaseEnzymeExt = "Enzyme"
    SciMLBaseForwardDiffExt = "ForwardDiff"
    SciMLBaseMLStyleExt = "MLStyle"
    SciMLBaseMakieExt = "Makie"
    SciMLBaseMeasurementsExt = "Measurements"
    SciMLBaseMonteCarloMeasurementsExt = "MonteCarloMeasurements"
    SciMLBaseMooncakeExt = "Mooncake"
    SciMLBasePartialFunctionsExt = "PartialFunctions"
    SciMLBasePyCallExt = "PyCall"
    SciMLBasePythonCallExt = "PythonCall"
    SciMLBaseRCallExt = "RCall"
    SciMLBaseReverseDiffExt = "ReverseDiff"
    SciMLBaseTrackerExt = "Tracker"
    SciMLBaseZygoteExt = ["Zygote", "ChainRulesCore"]

    [deps.SciMLBase.weakdeps]
    ChainRules = "082447d4-558c-5d27-93f4-14fc19e9eca2"
    ChainRulesCore = "d360d2e6-b24c-11e9-a2a3-2a2ae2dbcce4"
    Distributions = "31c24e10-a181-5473-b8eb-7969acd0382f"
    Enzyme = "7da242da-08ed-463a-9acd-ee780be4f1d9"
    ForwardDiff = "f6369f11-7733-5829-9624-2563aa707210"
    MLStyle = "d8e11817-5142-5d16-987a-aa16d5891078"
    Makie = "ee78f7c6-11fb-53f2-987a-cfe4a2b5a57a"
    Measurements = "eff96d63-e80a-5855-80a2-b1b0885c5ab7"
    MonteCarloMeasurements = "0987c9cc-fe09-11e8-30f0-b96dd679fdca"
    Mooncake = "da2b9cff-9c12-43a0-ae48-6db2b0edb7d6"
    PartialFunctions = "570af359-4316-4cb7-8c74-252c00c2016b"
    PyCall = "438e738f-606a-5dbb-bf0a-cddfbfd45ab0"
    PythonCall = "6099a3de-0909-46bc-b1f4-468b9a2dfc0d"
    RCall = "6f49c342-dc21-5d91-9882-a32aef131414"
    ReverseDiff = "37e2e3b7-166d-5795-8a7a-e32c996b4267"
    Tracker = "9f7883ad-71c0-57eb-9f7f-b5c9e6d3789c"
    Zygote = "e88e6eb3-aa80-5325-afca-941959d7151f"

[[deps.SciMLOperators]]
deps = ["Accessors", "Adapt", "ArrayInterface", "DocStringExtensions", "LinearAlgebra", "SciMLPublic"]
git-tree-sha1 = "54333a8ba01ff383643b44d5a97a4bc2c07d4d2f"
uuid = "c0aeaf25-5076-4817-a8d5-81caf7dfa961"
version = "1.26.1"

    [deps.SciMLOperators.extensions]
    SciMLOperatorsLoopVectorizationExt = "LoopVectorization"
    SciMLOperatorsSparseArraysExt = "SparseArrays"

    [deps.SciMLOperators.weakdeps]
    LoopVectorization = "bdcacae8-1622-11e9-2a5c-532679323890"
    SparseArrays = "2f01184e-e22b-5df5-ae63-d93ebab69eaf"

[[deps.SciMLPublic]]
git-tree-sha1 = "cf9aaf8b9ed5db993259ea8b24cf2b7ba9bd3b79"
uuid = "431bcebd-1456-4ced-9d72-93c2757fff0b"
version = "1.2.4"

[[deps.SciMLStructures]]
deps = ["ArrayInterface", "PrecompileTools"]
git-tree-sha1 = "53bf620cb2c3763d41495b2a145611c6ca400dcd"
uuid = "53ae85a6-f571-4167-b2af-e1d143709226"
version = "1.10.4"

[[deps.ScientificTypesBase]]
deps = ["InteractiveUtils"]
git-tree-sha1 = "e785eaa35a0f5518a388f9010e66fda64ea95ede"
uuid = "30f210dd-8aff-4c5f-94ba-8e64358c1161"
version = "3.1.0"

[[deps.SentinelArrays]]
deps = ["Dates", "Random"]
git-tree-sha1 = "084c47c7c5ce5cfecefa0a98dff69eb3646b5a80"
uuid = "91c51154-3ec4-41a3-a24f-3f23e20d615c"
version = "1.4.10"

[[deps.Serialization]]
uuid = "9e88b42a-f829-5b0c-bbe9-9e923198166b"
version = "1.11.0"

[[deps.Setfield]]
deps = ["ConstructionBase", "Future", "MacroTools", "StaticArraysCore"]
git-tree-sha1 = "c5391c6ace3bc430ca630251d02ea9687169ca68"
uuid = "efcf1570-3423-57d1-acb7-fd33fddbac46"
version = "1.1.2"

[[deps.SharedArrays]]
deps = ["Distributed", "Mmap", "Random", "Serialization"]
uuid = "1a1011a3-84de-559e-8e89-a11a2f7dc383"
version = "1.11.0"

[[deps.Sockets]]
uuid = "6462fe0b-24de-5631-8697-dd941f90decc"
version = "1.11.0"

[[deps.SortingAlgorithms]]
deps = ["DataStructures"]
git-tree-sha1 = "13cd91cc9be159e3f4d95b857fa2aa383b53772a"
uuid = "a2af1166-a08f-5f64-846c-94a0d3cef48c"
version = "1.2.3"

[[deps.SparseArrays]]
deps = ["Libdl", "LinearAlgebra", "Random", "Serialization", "SuiteSparse_jll"]
uuid = "2f01184e-e22b-5df5-ae63-d93ebab69eaf"
version = "1.12.0"

[[deps.SpecialFunctions]]
deps = ["IrrationalConstants", "LogExpFunctions", "OpenLibm_jll", "OpenSpecFun_jll"]
git-tree-sha1 = "c3ac026e735264e9bdc6a9bcbd1b1e781b36e3bc"
uuid = "276daf66-3868-5448-9aa4-cd146d93841b"
version = "2.8.3"
weakdeps = ["ChainRulesCore"]

    [deps.SpecialFunctions.extensions]
    SpecialFunctionsChainRulesCoreExt = "ChainRulesCore"

[[deps.StaticArrays]]
deps = ["LinearAlgebra", "PrecompileTools", "Random", "StaticArraysCore"]
git-tree-sha1 = "246a8bb2e6667f832eea063c3a56aef96429a3db"
uuid = "90137ffa-7385-5640-81b9-e52037218182"
version = "1.9.18"
weakdeps = ["ChainRulesCore", "Statistics"]

    [deps.StaticArrays.extensions]
    StaticArraysChainRulesCoreExt = "ChainRulesCore"
    StaticArraysStatisticsExt = "Statistics"

[[deps.StaticArraysCore]]
git-tree-sha1 = "6ab403037779dae8c514bad259f32a447262455a"
uuid = "1e83bf80-4336-4d27-bf5d-d5a4f845583c"
version = "1.4.4"

[[deps.StatisticalTraits]]
deps = ["ScientificTypesBase"]
git-tree-sha1 = "89f86d9376acd18a1a4fbef66a56335a3a7633b8"
uuid = "64bff920-2084-43da-a3e6-9bb72801c0c9"
version = "3.5.0"

[[deps.Statistics]]
deps = ["LinearAlgebra"]
git-tree-sha1 = "ae3bb1eb3bba077cd276bc5cfc337cc65c3075c0"
uuid = "10745b16-79ce-11e8-11f9-7d13ad32a3b2"
version = "1.11.1"
weakdeps = ["SparseArrays"]

    [deps.Statistics.extensions]
    SparseArraysExt = ["SparseArrays"]

[[deps.StatsAPI]]
deps = ["LinearAlgebra"]
git-tree-sha1 = "178ed29fd5b2a2cfc3bd31c13375ae925623ff36"
uuid = "82ae8749-77ed-4fe6-ae5f-f523153014b0"
version = "1.8.0"

[[deps.StatsBase]]
deps = ["AliasTables", "DataAPI", "DataStructures", "IrrationalConstants", "LinearAlgebra", "LogExpFunctions", "Missings", "Printf", "Random", "SortingAlgorithms", "SparseArrays", "Statistics", "StatsAPI"]
git-tree-sha1 = "e4d7a1a0edc20af42689ea6f4f3587a2175d50ee"
uuid = "2913bbd2-ae8a-5f71-8c99-4fb6c76f3a91"
version = "0.34.12"

[[deps.StatsFuns]]
deps = ["HypergeometricFunctions", "IrrationalConstants", "LogExpFunctions", "Reexport", "Rmath", "SpecialFunctions"]
git-tree-sha1 = "91f091a8716a6bb38417a6e6f274602a19aaa685"
uuid = "4c63d2b9-4356-54db-8cca-17b64c39e42c"
version = "1.5.2"
weakdeps = ["ChainRulesCore", "InverseFunctions"]

    [deps.StatsFuns.extensions]
    StatsFunsChainRulesCoreExt = "ChainRulesCore"
    StatsFunsInverseFunctionsExt = "InverseFunctions"

[[deps.StringManipulation]]
deps = ["PrecompileTools"]
git-tree-sha1 = "8a90c1d77c3277a5d43b83927b3cbe2c70a37484"
uuid = "892a3eda-7b42-436c-8928-eab12a02cf0e"
version = "0.4.7"

[[deps.StyledStrings]]
uuid = "f489334b-da3d-4c2e-b8f0-e476e12c162b"
version = "1.11.0"

[[deps.SuiteSparse]]
deps = ["Libdl", "LinearAlgebra", "Serialization", "SparseArrays"]
uuid = "4607b0f0-06f3-5cda-b6b1-a6196a1729e9"

[[deps.SuiteSparse_jll]]
deps = ["Artifacts", "Libdl", "libblastrampoline_jll"]
uuid = "bea87d4a-7f5b-5778-9afe-8cc45184846c"
version = "7.8.3+2"

[[deps.SymbolicIndexingInterface]]
deps = ["Accessors", "ArrayInterface", "RuntimeGeneratedFunctions", "StaticArraysCore"]
git-tree-sha1 = "ae6fd46b22508c2dfcd0fabf144ce5e9d9d2e719"
uuid = "2efcf032-c050-4f8e-a9bb-153293bab1f5"
version = "0.3.53"
weakdeps = ["PrettyTables"]

    [deps.SymbolicIndexingInterface.extensions]
    SymbolicIndexingInterfacePrettyTablesExt = "PrettyTables"

[[deps.TOML]]
deps = ["Dates"]
uuid = "fa267f1f-6049-4f14-aa54-33bafae1ed76"
version = "1.0.3"

[[deps.TableTraits]]
deps = ["IteratorInterfaceExtensions"]
git-tree-sha1 = "c06b2f539df1c6efa794486abfb6ed2022561a39"
uuid = "3783bdb8-4a98-5b6b-af9a-565f29a5fe9c"
version = "1.0.1"

[[deps.Tables]]
deps = ["DataAPI", "DataValueInterfaces", "IteratorInterfaceExtensions", "OrderedCollections", "TableTraits"]
git-tree-sha1 = "0f38a06c83f0007bbab3cf911262841c9a0f07e0"
uuid = "bd369af6-aec1-5ad0-b16a-f7cc5008161c"
version = "1.13.0"

[[deps.Tar]]
deps = ["ArgTools", "SHA"]
uuid = "a4e569a6-e804-4fa4-b0f3-eef7a1d5b13e"
version = "1.10.0"

[[deps.TerminalLoggers]]
deps = ["LeftChildRightSiblingTrees", "Logging", "Markdown", "Printf", "ProgressLogging", "UUIDs"]
git-tree-sha1 = "81c9b4137edfe56a56efcdcb35d721b2ce3e2416"
uuid = "5d786b92-1e48-4d6f-9151-6b4477ca9bed"
version = "0.1.8"

[[deps.Test]]
deps = ["InteractiveUtils", "Logging", "Random", "Serialization"]
uuid = "8dfed614-e22c-5e08-85e1-65c5234f0b40"
version = "1.11.0"

[[deps.TranscodingStreams]]
git-tree-sha1 = "0c45878dcfdcfa8480052b6ab162cdd138781742"
uuid = "3bb67fe8-82b1-5028-8e26-92a6c54297fa"
version = "0.11.3"

[[deps.Turing]]
deps = ["ADTypes", "AbstractMCMC", "AbstractPPL", "Accessors", "AdvancedHMC", "AdvancedMH", "AdvancedPS", "AdvancedVI", "BangBang", "Bijectors", "Compat", "DataStructures", "DifferentiationInterface", "Distributions", "DocStringExtensions", "DynamicPPL", "EllipticalSliceSampling", "ForwardDiff", "Libtask", "LinearAlgebra", "LogDensityProblems", "MCMCChains", "Optimization", "OptimizationOptimJL", "OrderedCollections", "Printf", "Random", "Reexport", "SciMLBase", "SpecialFunctions", "Statistics", "StatsAPI", "StatsBase", "StatsFuns"]
git-tree-sha1 = "666a4c4a3758e5b25eb100bce144f378addd8697"
uuid = "fce5fe82-541a-59a6-adf8-730c64b5f9a0"
version = "0.44.5"

    [deps.Turing.extensions]
    TuringDynamicHMCExt = "DynamicHMC"

    [deps.Turing.weakdeps]
    DynamicHMC = "bbc10e6e-7c05-544b-b16e-64fede858acb"

[[deps.UUIDs]]
deps = ["Random", "SHA"]
uuid = "cf7118a7-6976-5b1a-9a39-7adc72f591a4"
version = "1.11.0"

[[deps.UnPack]]
git-tree-sha1 = "387c1f73762231e86e0c9c5443ce3b4a0a9a0c2b"
uuid = "3a884ed6-31ef-47d7-9d2a-63182c4928ed"
version = "1.0.2"

[[deps.Unicode]]
uuid = "4ec0a83e-493e-50e2-b9ac-8f72acf5a8f5"
version = "1.11.0"

[[deps.WeakRefStrings]]
deps = ["DataAPI", "InlineStrings", "Parsers"]
git-tree-sha1 = "0716e01c3b40413de5dedbc9c5c69f27cddfddfc"
uuid = "ea10d353-3f73-51f8-a26c-33c1cb351aa5"
version = "1.4.3"

[[deps.WoodburyMatrices]]
deps = ["LinearAlgebra", "SparseArrays"]
git-tree-sha1 = "c1a7aa6219628fcd757dede0ca95e245c5cd9511"
uuid = "efce3f68-66dc-5838-9240-27a6d6f5f9b6"
version = "1.0.0"

[[deps.WorkerUtilities]]
git-tree-sha1 = "cd1659ba0d57b71a464a29e64dbc67cfe83d54e7"
uuid = "76eceee3-57b5-4d4a-8e66-0e911cebbf60"
version = "1.6.1"

[[deps.Zlib_jll]]
deps = ["Libdl"]
uuid = "83775a58-1f1d-513f-b197-d71354ab007a"
version = "1.3.1+2"

[[deps.libblastrampoline_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "8e850b90-86db-534c-a0d3-1478176c7d93"
version = "5.15.0+0"

[[deps.nghttp2_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "8e850ede-7688-5339-a07c-302acd2aaf8d"
version = "1.64.0+1"

[[deps.p7zip_jll]]
deps = ["Artifacts", "CompilerSupportLibraries_jll", "Libdl"]
uuid = "3f19e933-33d8-53b3-aaab-bd5110c3b7a0"
version = "17.7.0+0"
"""

# ╔═╡ Cell order:
# ╠═0d3adf68-934e-11f1-9e6f-d9c933bf00f8
# ╠═c4fa1fee-d7c4-4b43-92bb-a17f94e822c4
# ╠═cc88334c-1e90-4cd0-b4ef-d672a5851f52
# ╠═5975f055-85eb-4769-9723-417e4b33e071
# ╠═d7f65c1b-8e4e-4f35-bbe4-6ad1bfe768cd
# ╠═fcd964a1-9618-40b1-9ebe-aec48b1ae200
# ╠═1cee9b79-41fd-46da-ab1d-d8311e12aa26
# ╠═41b573a9-37e2-41be-af63-52226b95f633
# ╠═07102747-a4fc-46a0-879a-322c7fc88d7c
# ╠═ec8a72cc-44df-4fcc-b419-6c493d181e4b
# ╠═8d31adbd-794f-4bec-b193-bb6c7f931cd6
# ╠═39ca740d-b79c-4834-bdd1-fca3f19450d0
# ╠═22354df2-39f6-46f0-9407-94850b1f6f8d
# ╠═3c4f05e4-787b-45eb-8b29-3491149a9c39
# ╠═3a1b0630-6994-4150-b34e-bf4c79766254
# ╠═0ab7bf98-251f-45f7-b874-b23a90f9ebb1
# ╠═b9cc819e-da09-4897-a1b0-2777cbf8bf2d
# ╠═af6ce65e-e412-4a75-b83d-97dc4ef0dd8b
# ╠═c2f55dce-f1f1-4b47-899a-dfe2f6287d78
# ╠═45bd1537-c1d9-4661-ba1f-3c5704627ee7
# ╠═0084c677-9ff1-49fe-9b88-2f81aa555ef0
# ╠═43c59e15-e9a0-436c-b947-7a4c06d35b1b
# ╠═f28819d1-4c3b-47c6-be7a-c09b3330ec66
# ╠═6290ebf3-7d95-49db-9d13-777dd0c76eca
# ╠═0d842ccc-717e-4199-93a4-c0814ec2e9e8
# ╠═5cbbc465-8448-400e-9fb6-12c2972607f2
# ╠═6d1b2eb1-4a1a-4487-b721-c1bc23576011
# ╠═6f4d54e6-00f5-4bb5-a16c-5462c4f62be4
# ╠═7234534c-372c-4604-b939-6142651b24f4
# ╠═f426a9fc-bbd1-4d9e-a300-682ad63c16d9
# ╠═3dca1448-f6e1-4591-9c5a-fea17528748c
# ╠═bb08a3d4-6a1c-40e7-b885-e0d449e95d8d
# ╠═61f3e8c6-86a4-437a-990e-062b9cfbcf75
# ╠═cfc60c21-8fce-4154-bda6-581913ff6a62
# ╠═f5caf6f4-328c-4227-a090-484b2bdb81ba
# ╠═9f01bfce-31e2-47f3-b95c-acd8dbbb4897
# ╟─00000000-0000-0000-0000-000000000001
# ╟─00000000-0000-0000-0000-000000000002
