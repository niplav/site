#!/usr/bin/env julia
#=
Learning effects visualization for orexin experiment cognitive tests.
Layout: rows = metrics, columns = participants.
Per-subplot: x = chronological session index, y = metric value,
color = condition (blue=orexin, orange=placebo),
marker = day-slot (●=1st session, ◆=2nd session of the day).
Dashed lines: per-condition OLS trend.
=#

using CSV, DataFrames, JSON, Statistics, Dates, XLSX, Printf
using Plots; gr()

include(joinpath(@__DIR__, "orexin_data.jl"))

const METRIC_SPECS = [
	("PVT mean RT (ms)",    "pvt.json",        e -> begin
		rts = get(e, "reaction_times_ms", [])
		isempty(rts) ? nothing : mean(rts)
	end),
	("PVT slowest 10% (ms)", "pvt.json",       e -> begin
		rts = get(e, "reaction_times_ms", [])
		isempty(rts) ? nothing : quantile(rts, 0.9)
	end),
	("DSST correct",        "dsst.json",        e -> begin
		cc = get(e, "correct_count", get(e, "completed_trials", nothing))
		isnothing(cc) ? nothing : Float64(cc)
	end),
	("Digit Span total",    "digit_span.json",  e -> begin
		ts = get(e, "total_span", nothing)
		isnothing(ts) ? nothing : Float64(ts)
	end),
	("SSS rating",          "sss.json",         e -> begin
		r = get(e, "rating", get(e, "score", nothing))
		isnothing(r) ? nothing : Float64(r)
	end),
]

function ols(x, y)
	length(x) < 2 && return (NaN, NaN)
	xm, ym = mean(x), mean(y)
	denom = sum((xi - xm)^2 for xi in x)
	denom == 0.0 && return (NaN, NaN)
	b = sum((x[i] - xm) * (y[i] - ym) for i in eachindex(x)) / denom
	(ym - b * xm, b)
end

function load_sessions(tracking)
	rows = []
	for p in PARTICIPANTS
		data_dir = joinpath(BASE_DIR, p, "orexin_data")
		isdir(data_dir) || continue

		for (label, filename, fn) in METRIC_SPECS
			entries = load_json_safe(joinpath(data_dir, filename))
			for m in match_to_condition(entries, tracking, p)
				val = fn(m.entry)
				isnothing(val) && continue
				push!(rows, (
					participant = p,
					condition   = m.condition,
					date        = m.date,
					datetime    = m.datetime,
					metric      = label,
					value       = Float64(val),
				))
			end
		end
	end

	df = DataFrame(rows)
	df[!, :session_n] = zeros(Int, nrow(df))
	df[!, :slot]      = zeros(Int, nrow(df))

	for p in PARTICIPANTS, m in unique(df.metric)
		mask = (df.participant .== p) .& (df.metric .== m)
		idx  = findall(mask)
		isempty(idx) && continue

		# Chronological rank across all sessions
		for (rank, i) in enumerate(sort(idx, by = i -> df[i, :datetime]))
			df[i, :session_n] = rank
		end

		# Slot within each dosing day (1 = earlier, 2 = later)
		for d in unique(df[mask, :date])
			day_idx = findall(mask .& (df.date .== d))
			for (s, i) in enumerate(sort(day_idx, by = i -> df[i, :datetime]))
				df[i, :slot] = s
			end
		end
	end

	df
end

function make_subplot(sub, metric, participant, show_legend)
	orx_color = colorant"#264d99"
	plc_color = colorant"#e07040"
	slot_shapes = [:circle, :diamond]

	sp = plot(;
		xlabel      = "Session №",
		ylabel      = metric,
		title       = participant,
		titlefontsize = 9,
		legend      = show_legend ? :topright : false,
		legendfontsize = 7,
		left_margin = 4Plots.mm,
		bottom_margin = 6Plots.mm,
	)

	for (cond, col) in [("orexin", orx_color), ("placebo", plc_color)]
		csub = sub[sub.condition .== cond, :]
		isempty(csub) && continue

		for s in [1, 2]
			ss = csub[csub.slot .== s, :]
			isempty(ss) && continue
			lbl = (s == 1 && show_legend) ? uppercasefirst(cond) : ""
			scatter!(sp, ss.session_n, ss.value;
				color            = col,
				markershape      = slot_shapes[s],
				markeralpha      = 0.8,
				markerstrokewidth = 0.5,
				markersize       = 5,
				label            = lbl,
			)
		end

		# Per-condition OLS trend
		a, b = ols(Float64.(csub.session_n), csub.value)
		if !isnan(a)
			xs = Float64[minimum(csub.session_n), maximum(csub.session_n)]
			plot!(sp, xs, a .+ b .* xs;
				color     = col,
				lw        = 1.5,
				linestyle = :dash,
				label     = "",
			)
		end
	end

	sp
end

function plot_learning(df, out_dir)
	metrics = [spec[1] for spec in METRIC_SPECS]
	subplots = []

	for (mi, metric) in enumerate(metrics)
		for (pi, p) in enumerate(PARTICIPANTS)
			sub = df[(df.participant .== p) .& (df.metric .== metric), :]
			show_legend = (mi == 1 && pi == length(PARTICIPANTS))
			push!(subplots, make_subplot(sub, metric, p, show_legend))
		end
	end

	n_cols = length(PARTICIPANTS)
	n_rows = length(metrics)

	fig = plot(subplots...;
		layout      = (n_rows, n_cols),
		size        = (360 * n_cols, 270 * n_rows),
		plot_title  = "Learning Effects: Cognitive Tests Over Sessions",
		dpi         = 150,
	)

	path = joinpath(out_dir, "learning.png")
	savefig(fig, path)
	println("Saved to $path")
end

function main()
	tracking = load_all_tracking()
	df = load_sessions(tracking)

	println("Sessions per participant × metric:")
	for p in PARTICIPANTS
		pdf = df[df.participant .== p, :]
		isempty(pdf) && continue
		for m in [spec[1] for spec in METRIC_SPECS]
			n = nrow(pdf[pdf.metric .== m, :])
			n > 0 && @printf("  %-14s / %-24s %d sessions\n", p, m, n)
		end
	end

	plot_learning(df, dirname(@__FILE__))
end

main()
