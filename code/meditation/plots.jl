# Bar plots of daily meditation hours from data/meditations.csv.
#
# Writes into this directory:
#	meditation_home.png	everyday practice, retreat spans shaded out
#	meditation_retreats.png	one panel per retreat
#
#	julia plots.jl

include(joinpath(@__DIR__, "periods.jl"))
using Statistics, Plots

gr()

# Not the model's segmentation (4 hr/day, >= 4 days, gap 2): stricter on
# intensity, looser on length, so weekend intensives get a panel too.
const MIN_H = 6.0
const MIN_D = 2
const GAP = 1

const ROLL = 30		# window of the trailing mean on the home-practice plot
const W = 850		# max image width in px

trailing_mean(xs, w) = [mean(@view xs[max(1, i - w + 1):i]) for i in eachindex(xs)]

days, hours = daily_hours()
runs = retreat_runs(hours; min_h = MIN_H, min_d = MIN_D, gap = GAP)

# ------------------------------------------------------------
# home practice: retreat days blanked, their spans shaded
# ------------------------------------------------------------

home = copy(hours)
foreach(r -> home[r] .= 0.0, runs)

p = plot(size = (W, 340), legend = :topleft, legendfontsize = 6, titlefontsize = 9,
	xtickfontsize = 6, ytickfontsize = 6, guidefontsize = 7,
	left_margin = 4Plots.mm, bottom_margin = 3Plots.mm,
	ylabel = "hours/day", title = "everyday meditation (retreats shaded out)",
	ylims = (0, ceil(maximum(home)) + 0.5), grid = :y)

for (k, r) in enumerate(runs)
	vspan!(p, [days[first(r)] - Day(1), days[last(r)] + Day(1)],
		color = :grey70, alpha = 0.45, linewidth = 0, label = k == 1 ? "retreat" : "")
end

bar!(p, days, home, linewidth = 0, bar_width = 1.0, color = :steelblue,
	label = "daily hours")
plot!(p, days, trailing_mean(home, ROLL), color = :firebrick, linewidth = 1.5,
	label = "$(ROLL)-day trailing mean")

savefig(p, joinpath(@__DIR__, "meditation_home.png"))

# ------------------------------------------------------------
# retreats: one panel each, on a shared y scale
# ------------------------------------------------------------

ymax = ceil(maximum(hours)) + 0.5
panels = map(runs) do r
	d, h = days[r], hours[r]
	q = bar(d, h, linewidth = 0, bar_width = 0.8, color = :seagreen, label = "",
		title = "$(d[1])  $(length(d))d  $(round(Int, sum(h)))h", titlefontsize = 7,
		ylims = (0, ymax), xticks = ([d[1], d[end]], string.([d[1], d[end]])),
		xtickfontsize = 5, ytickfontsize = 5, grid = :y)
	hline!(q, [MIN_H], color = :grey40, linestyle = :dash, linewidth = 1, label = "")
end

cols = 3
rows = cld(length(panels), cols)
r = plot(panels..., layout = (rows, cols),
	size = (W, (W ÷ cols) * 3 ÷ 4 * rows + 30),
	plot_title = "retreats (>= $(Int(MIN_H)) h/day), dashed line = threshold",
	plot_titlefontsize = 10)

savefig(r, joinpath(@__DIR__, "meditation_retreats.png"))

println("wrote meditation_home.png and meditation_retreats.png")
for r in runs
	println("  ", days[first(r)], " .. ", days[last(r)], "  ", length(r), "d  ",
		round(sum(hours[r]), digits = 1), "h")
end
