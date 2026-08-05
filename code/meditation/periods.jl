# Segment data/meditations.csv into "practice periods": maximal runs of
# retreat-intensity days, with the gaps between them chunked into calendar
# quarters of home practice. Writes periods_niplav.csv.

using CSV, DataFrames, Dates, Statistics

const SRC = joinpath(homedir(), "proj/site/data/meditations.csv")
const OUT = joinpath(@__DIR__, "periods_niplav.csv")

# a retreat is >=RT_MIN_H h/day sustained for >=RT_MIN_D days, tolerating
# RT_GAP consecutive days below threshold (travel, collapse, illness)
const RT_MIN_H = 4.0
const RT_MIN_D = 5
const RT_GAP = 2

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
	span = ks[1]:Day(1):ks[end]
	return [(d, get(h, d, 0.0)) for d in span]
end

# maximal runs above threshold, merging across short gaps
function retreat_runs(series)
	runs = Tuple{Int,Int}[]
	i = 1
	n = length(series)
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

# home stretches get cut at quarter boundaries so that no single "period"
# spans years of drifting practice intensity
function quarter_cuts(series, lo, hi)
	cuts = Int[lo]
	for k in (lo + 1):hi
		d = series[k][1]
		prev = series[k - 1][1]
		(month(d) - 1) ÷ 3 != (month(prev) - 1) ÷ 3 && push!(cuts, k)
	end
	push!(cuts, hi + 1)
	return cuts
end

function build(series)
	runs = retreat_runs(series)
	rows = NamedTuple[]
	pos = 1
	for (a, b) in runs
		a > pos && append!(rows, home_periods(series, pos, a - 1))
		push!(rows, period_row(series, a, b, true))
		pos = b + 1
	end
	pos <= length(series) && append!(rows, home_periods(series, pos, length(series)))
	return rows
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

function period_row(series, a, b, retreat)
	days = b - a + 1
	hours = sum(series[k][2] for k in a:b)
	return (
		start = series[a][1],
		stop = series[b][1],
		days = days,
		hours = round(hours, digits = 2),
		h_per_day = round(hours / days, digits = 3),
		retreat = retreat,
	)
end

rows = build(daily_hours(SRC))
df = DataFrame(rows)

# the July 2026 retreat postdates the log; become.md dates it to that month.
# 28 days at an assumed 10 h/day, flagged so it is easy to revise.
push!(df, (
	start = Date(2026, 7, 5),
	stop = Date(2026, 8, 1),
	days = 28,
	hours = 280.0,
	h_per_day = 10.0,
	retreat = true,
))

df.person = fill("niplav", nrow(df))
df.idx = 1:nrow(df)
select!(df, :person, :idx, :start, :stop, :days, :hours, :h_per_day, :retreat)
CSV.write(OUT, df)

println("wrote $(nrow(df)) periods -> $OUT")
println("  retreats: $(sum(df.retreat))  home: $(sum(.!df.retreat))")
println("  total logged hours: $(round(sum(df.hours), digits=0))")
println()
show(df[df.retreat, :], allrows = true)
println()
