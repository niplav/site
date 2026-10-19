# Loading data/meditations.csv and cutting it into practice periods.
#
# Plain functions rather than a module, so that plots.jl can include this
# without dragging in Turing.

using CSV, DataFrames, Dates

const MEDITATIONS = joinpath(homedir(), "proj/site/data/meditations.csv")

# Every calendar day from the first log entry to the last, zeroes included.
function daily_hours(path = MEDITATIONS)
	df = CSV.read(path, DataFrame)
	h = Dict{Date,Float64}()
	for r in eachrow(df)
		ismissing(r.meditation_start) && continue
		d = Date(first(string(r.meditation_start), 10))
		h[d] = get(h, d, 0.0) + coalesce(r.meditation_duration, 0.0) / 3600
	end
	days = collect(minimum(keys(h)):Day(1):maximum(keys(h)))
	return days, [get(h, d, 0.0) for d in days]
end

# Maximal runs of days at >= min_h hours, bridging up to `gap` consecutive
# days below it (travel, collapse, illness). Runs shorter than min_d are
# dropped.
function retreat_runs(hours; min_h, min_d, gap)
	runs = UnitRange{Int}[]
	i = findfirst(>=(min_h), hours)
	while i !== nothing
		last = i
		for j in (i + 1):length(hours)
			j - last > gap + 1 && break
			hours[j] >= min_h && (last = j)
		end
		last - i + 1 >= min_d && push!(runs, i:last)
		i = findnext(>=(min_h), hours, last + 1)
	end
	return runs
end

# Cut a stretch of days at calendar-quarter boundaries.
function quarters(days, r)
	out = UnitRange{Int}[]
	isempty(r) && return out
	a = first(r)
	for k in (first(r) + 1):last(r)
		if firstdayofquarter(days[k]) != firstdayofquarter(days[k - 1])
			push!(out, a:(k - 1))
			a = k
		end
	end
	push!(out, a:last(r))
	return out
end

# A practice period is a retreat run, or a calendar quarter of the home
# practice between runs: a "period" spanning years of drifting intensity
# is not a dose.
function practice_periods(days, hours; min_h = 4.0, min_d = 4, gap = 2)
	out = DataFrame(start = Date[], days = Int[], h_per_day = Float64[],
		retreat = Bool[])
	add(r, retreat) = sum(hours[r]) > 0 &&
		push!(out, (days[first(r)], length(r), sum(hours[r]) / length(r), retreat))
	pos = 1
	for r in retreat_runs(hours; min_h, min_d, gap)
		foreach(q -> add(q, false), quarters(days, pos:(first(r) - 1)))
		add(r, true)
		pos = last(r) + 1
	end
	foreach(q -> add(q, false), quarters(days, pos:length(days)))
	return out
end

own_periods(; kw...) = practice_periods(daily_hours()...; kw...)
