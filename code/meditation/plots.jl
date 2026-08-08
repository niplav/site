# Bar plots of daily meditation hours from data/meditations.csv.
#
# Writes two images into this directory:
#   meditation_home.png     -- everyday practice, retreat spans shaded out
#   meditation_retreats.png -- one panel per retreat
#
# deps: CSV, DataFrames, Dates, Plots
# run:  julia plots.jl

using CSV, DataFrames, Dates, Statistics, Plots

gr()

const SRC = joinpath(homedir(), "proj/site/data/meditations.csv")
const OUT = @__DIR__

# a retreat is >=RT_MIN_H h/day for >=RT_MIN_D days, tolerating RT_GAP
# consecutive days below threshold (travel, collapse, illness)
const RT_MIN_H = 6.0
const RT_MIN_D = 2
const RT_GAP = 1

const ROLL = 30 # window for the trailing mean on the home-practice plot
const W = 850 # max image width in px

# every calendar day between first and last log entry, zeroes included
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
	days = collect(ks[1]:Day(1):ks[end])
	return days, [get(h, d, 0.0) for d in days]
end

# maximal runs above threshold, merging across short gaps; index pairs
function retreat_runs(hours)
	runs = Tuple{Int,Int}[]
	i, n = 1, length(hours)
	while i <= n
		if hours[i] >= RT_MIN_H
			last, j, gap = i, i, 0
			while j < n
				j += 1
				if hours[j] >= RT_MIN_H
					last, gap = j, 0
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

function trailing_mean(xs, w)
	out = similar(xs)
	for i in eachindex(xs)
		out[i] = mean(@view xs[max(1, i - w + 1):i])
	end
	return out
end

days, hours = daily_hours(SRC)
runs = retreat_runs(hours)

# ------------------------------------------------------------
# home practice: retreat days blanked, their spans shaded
# ------------------------------------------------------------

home = copy(hours)
for (a, b) in runs
	home[a:b] .= 0.0
end

p = plot(
	size = (W, 340),
	legend = :topleft,
	legendfontsize = 6,
	titlefontsize = 9,
	xtickfontsize = 6,
	ytickfontsize = 6,
	guidefontsize = 7,
	left_margin = 4Plots.mm,
	bottom_margin = 3Plots.mm,
	xlabel = "",
	ylabel = "hours/day",
	title = "everyday meditation (retreats shaded out)",
	ylims = (0, ceil(maximum(home)) + 0.5),
	grid = :y,
)

for (k, (a, b)) in enumerate(runs)
	vspan!(p, [days[a] - Day(1), days[b] + Day(1)],
		color = :grey70, alpha = 0.45, linewidth = 0,
		label = k == 1 ? "retreat" : "")
end

bar!(p, days, home,
	linewidth = 0, bar_width = 1.0, color = :steelblue, label = "daily hours")
plot!(p, days, trailing_mean(home, ROLL),
	color = :firebrick, linewidth = 1.5, label = "$(ROLL)-day trailing mean")

savefig(p, joinpath(OUT, "meditation_home.png"))

# ------------------------------------------------------------
# retreats: one panel each, on a shared y scale
# ------------------------------------------------------------

ymax = ceil(maximum(hours)) + 0.5
panels = Plots.Plot[]
for (a, b) in runs
	d = days[a:b]
	h = hours[a:b]
	tot = sum(h)
	ttl = "$(d[1])  $(length(d))d  $(round(Int, tot))h"
	q = bar(d, h,
		linewidth = 0, bar_width = 0.8, color = :seagreen, label = "",
		title = ttl, titlefontsize = 7, ylims = (0, ymax),
		xticks = ([d[1], d[end]], string.([d[1], d[end]])),
		xtickfontsize = 5, ytickfontsize = 5, grid = :y)
	hline!(q, [RT_MIN_H], color = :grey40, linestyle = :dash, linewidth = 1, label = "")
	push!(panels, q)
end

cols = 3
rows = ceil(Int, length(panels) / cols)
r = plot(panels...,
	layout = (rows, cols),
	size = (W, (W ÷ cols) * 3 ÷ 4 * rows + 30),
	plot_title = "retreats (>= $(Int(RT_MIN_H)) h/day), dashed line = threshold",
	plot_titlefontsize = 10)

savefig(r, joinpath(OUT, "meditation_retreats.png"))

println("wrote meditation_home.png and meditation_retreats.png")
for (a, b) in runs
	println("  $(days[a]) .. $(days[b])  $(b - a + 1)d  $(round(sum(hours[a:b]), digits = 1))h")
end
