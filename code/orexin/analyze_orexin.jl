#!/usr/bin/env julia
#=
Orexin-A Experiment Analysis
Pools data from all participants, runs:
- Welch's t-test for continuous metrics (PVT, DSST)
- Mann-Whitney U for ordinal metrics (SSS, Digit Span)
=#

using CSV, DataFrames, JSON, Statistics, HypothesisTests, Dates, XLSX, Printf
using Plots; gr()

const BASE_DIR = expanduser("~/down/Orexin")
const PARTICIPANTS = ["Niplav", "Sam", "Nomagicpill"]

# Display names with Wikipedia links and per-metric decimal places
const VARIABLE_NAMES = Dict(
	"PVT_mean_rt" => ("**[PVT](https://en.wikipedia.org/wiki/Psychomotor_vigilance_task) Mean RT (ms)**", 1),
	"PVT_median_rt" => ("**[PVT](https://en.wikipedia.org/wiki/Psychomotor_vigilance_task) Median RT (ms)**", 1),
	"PVT_slowest_10pct" => ("**[PVT](https://en.wikipedia.org/wiki/Psychomotor_vigilance_task) Slowest 10% (ms)**", 1),
	"DSST_correct_count" => ("**[DSST](https://en.wikipedia.org/wiki/Wechsler_Adult_Intelligence_Scale#Coding_and_Symbol_Search) Correct**", 1),
	"DigitSpan_forward_span" => ("**[Digit Span](https://en.wikipedia.org/wiki/Memory_span#Digit-span) Forward**", 2),
	"DigitSpan_backward_span" => ("**[Digit Span](https://en.wikipedia.org/wiki/Memory_span#Digit-span) Backward**", 2),
	"DigitSpan_total_span" => ("**[Digit Span](https://en.wikipedia.org/wiki/Memory_span#Digit-span) Total**", 1),
	"SSS_rating" => ("**[SSS](https://en.wikipedia.org/wiki/Stanford_Sleepiness_Scale) Rating**", 2),
	"Sleep_duration_h" => ("**Sleep Duration (hrs)**", 2),
	"Sleep_minutes_asleep" => ("**Sleep Time Asleep (min)**", 0),
	"Sleep_efficiency" => ("**Sleep Efficiency (%)**", 1),
	"Sleep_deep_min" => ("**Sleep Deep (min)**", 1),
	"Sleep_light_min" => ("**Sleep Light (min)**", 0),
	"Sleep_rem_min" => ("**Sleep [REM](https://en.wikipedia.org/wiki/Rapid_eye_movement_sleep) (min)**", 1),
	"Sleep_wake_min" => ("**Sleep Wake (min)**", 1),
)

const SUPP_VARIABLE_NAMES = Dict(
	"HRV_daily_rmssd" => ("**HRV Daily RMSSD (ms)**", 1),
	"HRV_deep_rmssd" => ("**HRV Deep RMSSD (ms)**", 1),
	"SpO2_avg" => ("**SpO2 Avg (%)**", 1),
	"SpO2_min" => ("**SpO2 Min (%)**", 1),
	"Breathing_rate" => ("**Breathing Rate (breaths/min)**", 1),
	"Skin_temp_rel" => ("**Skin Temp Δ (°C)**", 2),
	"Steps" => ("**Steps**", 0),
)

const SUPP_PLOT_NAMES = Dict(
	"HRV_daily_rmssd" => "HRV Daily RMSSD (ms)",
	"HRV_deep_rmssd" => "HRV Deep RMSSD (ms)",
	"SpO2_avg" => "SpO2 Avg (%)",
	"SpO2_min" => "SpO2 Min (%)",
	"Breathing_rate" => "Breathing Rate",
	"Skin_temp_rel" => "Skin Temp Δ (°C)",
	"Steps" => "Steps",
)

# --- Tracking data loaders ---

function load_niplav_tracking()
	rows = []
	path = joinpath(BASE_DIR, "Niplav", "tracking.csv")
	isfile(path) || return rows
	for line in eachline(path)
		parts = split(line, ',')
		length(parts) < 2 && continue
		ts, substance = parts[1], parts[2]
		date_str = split(ts, 'T')[1]
		cond = if substance == "water"
			"placebo"
		elseif substance == "orexin-a"
			"orexin"
		else
			continue
		end
		push!(rows, (participant="Niplav", date=Date(date_str), condition=cond))
	end
	rows
end

function load_xlsx_tracking(participant, xlsx_path, cond_col, cond_map)
	rows = []
	isfile(xlsx_path) || return rows
	xf = XLSX.readxlsx(xlsx_path)
	sn = XLSX.sheetnames(xf)[1]
	data = XLSX.readtable(xlsx_path, sn)

	dates = data.data[1]
	conds = data.data[cond_col]

	for i in eachindex(dates)
		d = dates[i]
		c = conds[i]
		ismissing(d) && continue
		ismissing(c) && continue

		dt = if d isa DateTime
			Date(d)
		elseif d isa Date
			d
		else
			continue
		end

		cond_str = string(c)
		mapped = get(cond_map, cond_str, nothing)
		isnothing(mapped) && continue
		push!(rows, (participant=participant, date=dt, condition=mapped))
	end
	rows
end

function load_sam_tracking()
	load_xlsx_tracking(
		"Sam",
		joinpath(BASE_DIR, "Sam", "sh ox notes.xlsx"),
		3,  # column C: "placebo or real"
		Dict("real" => "orexin", "placebo" => "placebo", "BASELINE DAY" => "baseline")
	)
end

function load_nomagicpill_tracking()
	load_xlsx_tracking(
		"Nomagicpill",
		joinpath(BASE_DIR, "Nomagicpill", "Orexin Tracking.xlsx"),
		6,  # column F: "Syringe Taken?"
		Dict("Orexin" => "orexin", "Placebo" => "placebo", "Baseline day" => "baseline")
	)
end

function load_all_tracking()
	tracking = vcat(load_niplav_tracking(), load_sam_tracking(), load_nomagicpill_tracking())
	# Filter to only orexin/placebo (drop baseline for now)
	filter(r -> r.condition in ("orexin", "placebo"), tracking)
end

# --- JSON data loaders ---

function load_json_safe(path)
	isfile(path) || return []
	content = read(path, String)
	# Fix trailing commas (Ethan's digit_span.json)
	content = replace(content, r",\s*\]" => "]")
	content = replace(content, r",\s*\}" => "}")
	JSON.parse(content)
end

function match_to_condition(entries, tracking, participant; window_h=24)
	matched = []
	p_tracking = filter(r -> r.participant == participant, tracking)
	for entry in entries
		ts_str = get(entry, "timestamp", get(entry, "date", nothing))
		isnothing(ts_str) && continue
		# Parse timestamp to Date
		entry_date = Date(split(ts_str, 'T')[1])
		entry_dt = DateTime(split(ts_str, '.')[1], dateformat"yyyy-mm-ddTHH:MM:SS")

		for t in p_tracking
			dose_dt = DateTime(t.date)  # midnight of dosing day
			# Test must be on dosing day or within window
			if entry_date == t.date || (entry_dt >= dose_dt && entry_dt <= dose_dt + Hour(window_h))
				push!(matched, (entry=entry, condition=t.condition, participant=participant, date=t.date))
				break
			end
		end
	end
	matched
end

# --- Sleep data ---

function load_sleep_data(participant)
	sleep_dir = joinpath(BASE_DIR, participant, "fitbit", "sleep")
	isdir(sleep_dir) || return Dict{String, Any}()

	# Index all sleep records by dateOfSleep
	by_date = Dict{String, Any}()
	for f in readdir(sleep_dir, join=true)
		endswith(f, ".json") || continue
		records = load_json_safe(f)
		for r in records
			# Only main sleep
			get(r, "isMainSleep", false) || continue
			dos = get(r, "dateOfSleep", nothing)
			isnothing(dos) && continue
			by_date[dos] = r
		end
	end
	by_date
end

function extract_sleep_metrics(tracking)
	rows = []
	for p in PARTICIPANTS
		sleep_by_date = load_sleep_data(p)
		isempty(sleep_by_date) && continue

		p_tracking = filter(r -> r.participant == p, tracking)
		for t in p_tracking
			# Sleep on the night after dosing: dateOfSleep = dose_date + 1
			next_day = string(t.date + Day(1))
			r = get(sleep_by_date, next_day, nothing)
			isnothing(r) && continue

			levels = get(get(r, "levels", Dict()), "summary", Dict())
			push!(rows, (
				participant = p,
				condition = t.condition,
				date = t.date,
				duration_h = get(r, "duration", 0) / 3.6e6,
				minutes_asleep = get(r, "minutesAsleep", missing),
				efficiency = get(r, "efficiency", missing),
				deep_min = get(get(levels, "deep", Dict()), "minutes", missing),
				light_min = get(get(levels, "light", Dict()), "minutes", missing),
				rem_min = get(get(levels, "rem", Dict()), "minutes", missing),
				wake_min = get(get(levels, "wake", Dict()), "minutes", missing),
			))
		end
	end
	DataFrame(rows)
end

# --- Supplementary Fitbit data ---

function load_fitbit_daily(participant, subdir)
	dir = joinpath(BASE_DIR, participant, "fitbit", subdir)
	isdir(dir) || return Dict{String, Any}()
	by_date = Dict{String, Any}()
	for f in readdir(dir, join=true)
		endswith(f, ".json") || continue
		records = load_json_safe(f)
		for r in records
			dt = get(r, "dateTime", nothing)
			isnothing(dt) && continue
			by_date[dt] = r
		end
	end
	by_date
end

function extract_supplementary_metrics(tracking)
	rows = []
	for p in PARTICIPANTS
		hrv_data = load_fitbit_daily(p, "hrv")
		spo2_data = load_fitbit_daily(p, "spo2")
		br_data = load_fitbit_daily(p, "breathing_rate")
		temp_data = load_fitbit_daily(p, "temperature_skin")
		steps_data = load_fitbit_daily(p, "steps")

		p_tracking = filter(r -> r.participant == p, tracking)
		for t in p_tracking
			ds = string(t.date)
			ds_next = string(t.date + Day(1))

			# HRV (same day)
			hrv_daily = nothing
			hrv_deep = nothing
			hrv_rec = get(hrv_data, ds, nothing)
			if !isnothing(hrv_rec)
				v = get(hrv_rec, "value", Dict())
				hrv_daily = get(v, "dailyRmssd", nothing)
				hrv_deep = get(v, "deepRmssd", nothing)
			end

			# SpO2 (same day — measured during preceding night)
			spo2_avg = nothing
			spo2_min = nothing
			spo2_rec = get(spo2_data, ds, nothing)
			if !isnothing(spo2_rec)
				v = get(spo2_rec, "value", Dict())
				spo2_avg = get(v, "avg", nothing)
				spo2_min = get(v, "min", nothing)
			end

			# Breathing rate (same day)
			br_val = nothing
			br_rec = get(br_data, ds, nothing)
			if !isnothing(br_rec)
				v = get(br_rec, "value", Dict())
				br_val = get(v, "breathingRate", nothing)
			end

			# Skin temperature (following night)
			temp_val = nothing
			temp_rec = get(temp_data, ds_next, nothing)
			if !isnothing(temp_rec)
				v = get(temp_rec, "value", Dict())
				temp_val = get(v, "nightlyRelative", nothing)
			end

			# Steps (same day)
			steps_val = nothing
			steps_rec = get(steps_data, ds, nothing)
			if !isnothing(steps_rec)
				sv = get(steps_rec, "value", nothing)
				if !isnothing(sv)
					steps_val = tryparse(Float64, string(sv))
				end
			end

			push!(rows, (
				participant = p,
				condition = t.condition,
				date = t.date,
				hrv_daily_rmssd = something(hrv_daily, missing),
				hrv_deep_rmssd = something(hrv_deep, missing),
				spo2_avg = something(spo2_avg, missing),
				spo2_min = something(spo2_min, missing),
				breathing_rate = something(br_val, missing),
				skin_temp_rel = something(temp_val, missing),
				steps = something(steps_val, missing),
			))
		end
	end
	DataFrame(rows)
end

# --- Metric extraction ---

function extract_pvt_metrics(matched)
	rows = []
	for m in matched
		e = m.entry
		rts = get(e, "reaction_times_ms", [])
		isempty(rts) && continue
		push!(rows, (
			participant = m.participant,
			condition = m.condition,
			date = m.date,
			mean_rt = mean(rts),
			median_rt = median(rts),
			slowest_10pct = quantile(rts, 0.9),
			false_starts = get(e, "false_starts", 0)
		))
	end
	DataFrame(rows)
end

function extract_dsst_metrics(matched)
	rows = []
	for m in matched
		e = m.entry
		cc = get(e, "correct_count", get(e, "completed_trials", nothing))
		isnothing(cc) && continue
		push!(rows, (
			participant = m.participant,
			condition = m.condition,
			date = m.date,
			correct_count = cc,
			accuracy = get(e, "accuracy", missing)
		))
	end
	DataFrame(rows)
end

function extract_digit_span_metrics(matched)
	rows = []
	for m in matched
		e = m.entry
		fs = get(e, "forward_span", nothing)
		bs = get(e, "backward_span", nothing)
		ts = get(e, "total_span", nothing)
		(isnothing(fs) && isnothing(bs)) && continue
		push!(rows, (
			participant = m.participant,
			condition = m.condition,
			date = m.date,
			forward_span = something(fs, missing),
			backward_span = something(bs, missing),
			total_span = something(ts, missing)
		))
	end
	DataFrame(rows)
end

function extract_sss_metrics(matched)
	rows = []
	for m in matched
		e = m.entry
		rating = get(e, "rating", get(e, "score", nothing))
		isnothing(rating) && continue
		push!(rows, (
			participant = m.participant,
			condition = m.condition,
			date = m.date,
			rating = rating
		))
	end
	DataFrame(rows)
end

# --- Statistical tests ---

function cohens_d(a, b)
	pooled_std = sqrt((var(a) + var(b)) / 2)
	pooled_std == 0 && return 0.0
	(mean(a) - mean(b)) / pooled_std
end

function rank_biserial(u, n1, n2)
	# r = 1 - 2U/(n1*n2)
	1.0 - 2.0 * u / (n1 * n2)
end

function run_welch_ttest(df, metric, label)
	orx = collect(skipmissing(df[df.condition .== "orexin", metric]))
	plc = collect(skipmissing(df[df.condition .== "placebo", metric]))
	(length(orx) < 2 || length(plc) < 2) && return nothing

	t = UnequalVarianceTTest(Float64.(orx), Float64.(plc))
	Dict(
		"metric" => label,
		"test" => "Welch's t",
		"orexin_mean" => mean(orx),
		"orexin_std" => std(orx),
		"orexin_n" => length(orx),
		"placebo_mean" => mean(plc),
		"placebo_std" => std(plc),
		"placebo_n" => length(plc),
		"statistic" => t.t,
		"p_value" => pvalue(t),
		"effect_size" => cohens_d(orx, plc),
		"effect_label" => "Cohen's d"
	)
end

function run_mann_whitney(df, metric, label)
	orx = collect(skipmissing(df[df.condition .== "orexin", metric]))
	plc = collect(skipmissing(df[df.condition .== "placebo", metric]))
	(length(orx) < 2 || length(plc) < 2) && return nothing

	u = MannWhitneyUTest(Float64.(orx), Float64.(plc))
	u_stat = u.U
	Dict(
		"metric" => label,
		"test" => "Mann-Whitney U",
		"orexin_mean" => mean(orx),
		"orexin_std" => std(orx),
		"orexin_n" => length(orx),
		"placebo_mean" => mean(plc),
		"placebo_std" => std(plc),
		"placebo_n" => length(plc),
		"statistic" => u_stat,
		"p_value" => pvalue(u),
		"effect_size" => rank_biserial(u_stat, length(orx), length(plc)),
		"effect_label" => "rank-biserial r"
	)
end

# --- Markdown output ---

function fmt_val(v, decimals)
	ismissing(v) && return "N/A"
	isnan(v) && return "N/A"
	@sprintf("%.*f", decimals, v)
end

function fmt_diff(v, decimals)
	ismissing(v) && return "N/A"
	isnan(v) && return "N/A"
	sign = v >= 0 ? "+" : ""
	"$sign$(@sprintf("%.*f", decimals, v))"
end

function write_markdown(results, path; bonferroni=false)
	p_header = bonferroni ? "p-value | p-corrected" : "p-value"
	p_sep = bonferroni ? "---------|------------" : "--------"
	lines = [
		"| Variable | Effect Size | $p_header | Orexin | Placebo | Difference |",
		"|----------|------------|$p_sep|--------|---------|------------|",
	]

	for r in results
		metric = r["metric"]
		haskey(VARIABLE_NAMES, metric) || continue
		name, dec = VARIABLE_NAMES[metric]

		orx_str = "$(fmt_val(r["orexin_mean"], dec)) ± $(fmt_val(r["orexin_std"], dec)) (n=$(Int(r["orexin_n"])))"
		plc_str = "$(fmt_val(r["placebo_mean"], dec)) ± $(fmt_val(r["placebo_std"], dec)) (n=$(Int(r["placebo_n"])))"
		diff = r["orexin_mean"] - r["placebo_mean"]

		es_label = r["effect_label"] == "Cohen's d" ?
			"[Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)" :
			"[r](https://en.wikipedia.org/wiki/Rank-biserial_correlation)"
		es_str = "$(fmt_val(r["effect_size"], 3)) ($es_label)"

		p_col = if bonferroni
			"$(fmt_val(r["p_value"], 3)) | $(fmt_val(r["p_corrected"], 3))"
		else
			fmt_val(r["p_value"], 3)
		end

		push!(lines, "| $name | $es_str | $p_col | $orx_str | $plc_str | $(fmt_diff(diff, dec)) |")
	end

	open(path, "w") do f
		write(f, join(lines, "\n") * "\n")
	end
	println("Markdown table saved to $path")
end

function write_supp_markdown(results, path; bonferroni=false)
	p_header = bonferroni ? "p-value | p-corrected" : "p-value"
	p_sep = bonferroni ? "---------|------------" : "--------"
	lines = [
		"| Variable | Effect Size | $p_header | Orexin | Placebo | Difference |",
		"|----------|------------|$p_sep|--------|---------|------------|",
	]

	for r in results
		metric = r["metric"]
		haskey(SUPP_VARIABLE_NAMES, metric) || continue
		name, dec = SUPP_VARIABLE_NAMES[metric]

		orx_str = "$(fmt_val(r["orexin_mean"], dec)) ± $(fmt_val(r["orexin_std"], dec)) (n=$(Int(r["orexin_n"])))"
		plc_str = "$(fmt_val(r["placebo_mean"], dec)) ± $(fmt_val(r["placebo_std"], dec)) (n=$(Int(r["placebo_n"])))"
		diff = r["orexin_mean"] - r["placebo_mean"]

		es_str = "$(fmt_val(r["effect_size"], 3)) ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d))"

		p_col = if bonferroni && haskey(r, "p_corrected")
			"$(fmt_val(r["p_value"], 3)) | $(fmt_val(r["p_corrected"], 3))"
		else
			fmt_val(r["p_value"], 3)
		end

		push!(lines, "| $name | $es_str | $p_col | $orx_str | $plc_str | $(fmt_diff(diff, dec)) |")
	end

	open(path, "w") do f
		write(f, join(lines, "\n") * "\n")
	end
	println("Supplementary markdown saved to $path")
end

# --- Plotting ---

# Short display names for plot labels (no markdown)
const PLOT_NAMES = Dict(
	"PVT_mean_rt" => "PVT Mean RT (ms)",
	"PVT_median_rt" => "PVT Median RT (ms)",
	"PVT_slowest_10pct" => "PVT Slowest 10% (ms)",
	"DSST_correct_count" => "DSST Correct",
	"DigitSpan_forward_span" => "Digit Span Fwd",
	"DigitSpan_backward_span" => "Digit Span Bwd",
	"DigitSpan_total_span" => "Digit Span Total",
	"SSS_rating" => "SSS Rating",
	"Sleep_duration_h" => "Duration",
	"Sleep_minutes_asleep" => "Asleep",
	"Sleep_efficiency" => "Efficiency (%)",
	"Sleep_deep_min" => "Deep",
	"Sleep_light_min" => "Light",
	"Sleep_rem_min" => "REM",
	"Sleep_wake_min" => "Wake",
)

function make_bar_subplot(group_results, title_str;
		ylabel_str="Value", to_min=Set{String}(), ymin=nothing, legend_pos=:topleft)
	n = length(group_results)
	labels = [get(PLOT_NAMES, r["metric"], r["metric"]) for r in group_results]
	# Convert hours→minutes for metrics in to_min
	scale = [r["metric"] in to_min ? 60.0 : 1.0 for r in group_results]
	orx_means = [r["orexin_mean"] * scale[i] for (i,r) in enumerate(group_results)]
	plc_means = [r["placebo_mean"] * scale[i] for (i,r) in enumerate(group_results)]
	orx_se = [r["orexin_std"] / sqrt(r["orexin_n"]) * scale[i] for (i,r) in enumerate(group_results)]
	plc_se = [r["placebo_std"] / sqrt(r["placebo_n"]) * scale[i] for (i,r) in enumerate(group_results)]
	p_vals = [r["p_value"] for r in group_results]

	# If ymin set, shift bars down and draw a break indicator
	offset = isnothing(ymin) ? 0.0 : Float64(ymin)
	orx_plot = orx_means .- offset
	plc_plot = plc_means .- offset

	xs = 1:n
	w = 0.35

	sp = bar(xs .- w/2, orx_plot, bar_width=w, yerr=orx_se,
		label="Orexin", color=colorant"#264d99", linecolor=:black, lw=0.5)
	bar!(sp, xs .+ w/2, plc_plot, bar_width=w, yerr=plc_se,
		label="Placebo", color=colorant"#ffb399", linecolor=:black, lw=0.5)

	# p-value annotations — compute ymax in plot coords, add headroom
	global_ymax = 0.0
	p_annot = []
	for i in 1:n
		ymax_plot = max(orx_plot[i] + orx_se[i], plc_plot[i] + plc_se[i])
		global_ymax = max(global_ymax, ymax_plot)
		pv = p_vals[i]
		p_str = pv < 0.001 ? @sprintf("p<.001") : @sprintf("p=%.3f", pv)
		push!(p_annot, (xs[i], ymax_plot, p_str))
	end

	# Set ylims with 20% headroom above tallest bar+error for labels
	ylim_top = global_ymax * 1.2
	for (x, y, s) in p_annot
		annotate!(sp, x, y + global_ymax * 0.05, text(s, 7, :center))
	end

	# Build y-axis tick labels that show the real values (with offset added back)
	if !isnothing(ymin)
		# Pick nice ticks in the plot range
		tick_step = nice_step(ylim_top)
		raw_ticks = collect(0:tick_step:ylim_top)
		real_labels = [@sprintf("%g", t + offset) for t in raw_ticks]
		plot!(sp, yticks=(raw_ticks, real_labels))
	end

	plot!(sp,
		xticks=(xs, labels), xrotation=25,
		ylabel=ylabel_str, title=title_str,
		ylims=(0, ylim_top),
		legend=legend_pos,
		bottom_margin=12Plots.mm, left_margin=5Plots.mm,
	)

	sp
end

function nice_step(range)
	# Pick a round tick step for ~5-8 ticks
	raw = range / 6
	mag = 10.0^floor(log10(raw))
	for m in [1, 2, 5, 10]
		s = m * mag
		s >= raw && return s
	end
	mag * 10
end

function plot_results(results, out_dir)
	cog = filter(r -> !startswith(r["metric"], "Sleep_"), results)
	slp = filter(r -> startswith(r["metric"], "Sleep_"), results)

	# Cognitive plot: PVT | DSST | Digit Span + SSS
	if !isempty(cog)
		pvt = filter(r -> startswith(r["metric"], "PVT_"), cog)
		dsst = filter(r -> startswith(r["metric"], "DSST_"), cog)
		span = filter(r -> startswith(r["metric"], "DigitSpan_"), cog)
		sss = filter(r -> startswith(r["metric"], "SSS_"), cog)

		subplots = []
		!isempty(pvt) && push!(subplots, make_bar_subplot(pvt, "PVT"; ylabel_str="RT (ms)", ymin=200))
		!isempty(dsst) && push!(subplots, make_bar_subplot(dsst, "DSST"; ylabel_str="Correct count", ymin=60))
		!isempty(span) && push!(subplots, make_bar_subplot(span, "Digit Span"; ylabel_str="Span"))
		!isempty(sss) && push!(subplots, make_bar_subplot(sss, "SSS"; ylabel_str="Rating"))

		if !isempty(subplots)
			p = plot(subplots...,
				layout=(1, length(subplots)),
				size=(400*length(subplots), 450),
				plot_title="Orexin-A vs Placebo: Cognitive Tests",
			)
			savefig(p, joinpath(out_dir, "plot_cognitive.png"))
			println("Plot saved to $(joinpath(out_dir, "plot_cognitive.png"))")
		end
	end

	# Sleep plot: stages (min) | totals (min) | efficiency (%)
	if !isempty(slp)
		stage_metrics = ["Sleep_deep_min", "Sleep_light_min", "Sleep_rem_min", "Sleep_wake_min"]
		total_metrics = ["Sleep_duration_h", "Sleep_minutes_asleep"]
		eff_metrics = ["Sleep_efficiency"]

		stages = filter(r -> r["metric"] in stage_metrics, slp)
		totals = filter(r -> r["metric"] in total_metrics, slp)
		eff = filter(r -> r["metric"] in eff_metrics, slp)

		subplots = []
		!isempty(stages) && push!(subplots, make_bar_subplot(stages, "Sleep Stages"; ylabel_str="Minutes", ymin=30))
		if !isempty(totals)
			push!(subplots, make_bar_subplot(totals, "Sleep Totals";
				ylabel_str="Minutes", ymin=400,
				to_min=Set(["Sleep_duration_h"]),
				legend_pos=:topright))
		end
		!isempty(eff) && push!(subplots, make_bar_subplot(eff, "Sleep Efficiency"; ylabel_str="%", ymin=80))

		if !isempty(subplots)
			p = plot(subplots...,
				layout=(1, length(subplots)),
				size=(400*length(subplots), 450),
				plot_title="Orexin-A vs Placebo: Sleep",
			)
			savefig(p, joinpath(out_dir, "plot_sleep.png"))
			println("Plot saved to $(joinpath(out_dir, "plot_sleep.png"))")
		end
	end
end

function make_bar_subplot_custom(group_results, title_str, name_map;
		ylabel_str="Value", ymin=nothing, legend_pos=:topleft)
	n = length(group_results)
	labels = [get(name_map, r["metric"], r["metric"]) for r in group_results]
	orx_means = [r["orexin_mean"] for r in group_results]
	plc_means = [r["placebo_mean"] for r in group_results]
	orx_se = [r["orexin_std"] / sqrt(r["orexin_n"]) for r in group_results]
	plc_se = [r["placebo_std"] / sqrt(r["placebo_n"]) for r in group_results]
	p_vals = [r["p_value"] for r in group_results]

	offset = isnothing(ymin) ? 0.0 : Float64(ymin)
	orx_plot = orx_means .- offset
	plc_plot = plc_means .- offset

	xs = 1:n
	w = 0.35

	sp = bar(xs .- w/2, orx_plot, bar_width=w, yerr=orx_se,
		label="Orexin", color=colorant"#264d99", linecolor=:black, lw=0.5)
	bar!(sp, xs .+ w/2, plc_plot, bar_width=w, yerr=plc_se,
		label="Placebo", color=colorant"#ffb399", linecolor=:black, lw=0.5)

	global_ymax = 0.0
	p_annot = []
	for i in 1:n
		ymax_plot = max(orx_plot[i] + orx_se[i], plc_plot[i] + plc_se[i])
		global_ymax = max(global_ymax, ymax_plot)
		pv = p_vals[i]
		p_str = pv < 0.001 ? @sprintf("p<.001") : @sprintf("p=%.3f", pv)
		push!(p_annot, (xs[i], ymax_plot, p_str))
	end

	ylim_top = global_ymax * 1.2
	for (x, y, s) in p_annot
		annotate!(sp, x, y + global_ymax * 0.05, text(s, 7, :center))
	end

	if !isnothing(ymin)
		tick_step = nice_step(ylim_top)
		raw_ticks = collect(0:tick_step:ylim_top)
		real_labels = [@sprintf("%g", t + offset) for t in raw_ticks]
		plot!(sp, yticks=(raw_ticks, real_labels))
	end

	plot!(sp,
		xticks=(xs, labels), xrotation=25,
		ylabel=ylabel_str, title=title_str,
		ylims=(0, ylim_top),
		legend=legend_pos,
		bottom_margin=12Plots.mm, left_margin=5Plots.mm,
	)
	sp
end

function plot_supp_results(results, out_dir)
	isempty(results) && return

	cardio_metrics = ["HRV_daily_rmssd", "HRV_deep_rmssd"]
	resp_metrics = ["SpO2_avg", "SpO2_min", "Breathing_rate"]
	temp_metrics = ["Skin_temp_rel"]
	steps_metrics = ["Steps"]

	cardio = filter(r -> r["metric"] in cardio_metrics, results)
	resp = filter(r -> r["metric"] in resp_metrics, results)
	temp = filter(r -> r["metric"] in temp_metrics, results)
	steps = filter(r -> r["metric"] in steps_metrics, results)

	subplots = []
	!isempty(cardio) && push!(subplots, make_bar_subplot_custom(cardio, "HRV", SUPP_PLOT_NAMES; ylabel_str="RMSSD (ms)"))
	!isempty(resp) && push!(subplots, make_bar_subplot_custom(resp, "Respiratory", SUPP_PLOT_NAMES; ylabel_str="Value"))
	!isempty(temp) && push!(subplots, make_bar_subplot_custom(temp, "Skin Temperature", SUPP_PLOT_NAMES; ylabel_str="Δ °C"))
	!isempty(steps) && push!(subplots, make_bar_subplot_custom(steps, "Activity", SUPP_PLOT_NAMES; ylabel_str="Steps"))

	if !isempty(subplots)
		p = plot(subplots...,
			layout=(1, length(subplots)),
			size=(450*length(subplots), 450),
			plot_title="Orexin-A vs Placebo: Supplementary Fitbit Metrics",
		)
		savefig(p, joinpath(out_dir, "plot_supplementary.png"))
		println("Plot saved to $(joinpath(out_dir, "plot_supplementary.png"))")
	end
end

# --- Main ---

function main()
	println("Loading tracking data...")
	tracking = load_all_tracking()
	println("  $(length(tracking)) dosing records across $(length(unique(r.participant for r in tracking))) participants")

	# Count per participant
	for p in PARTICIPANTS
		n = count(r -> r.participant == p, tracking)
		norx = count(r -> r.participant == p && r.condition == "orexin", tracking)
		nplc = count(r -> r.participant == p && r.condition == "placebo", tracking)
		n > 0 && println("  $p: $norx orexin, $nplc placebo")
	end

	# Load and match cognitive tests
	println("\nLoading cognitive test data...")
	all_pvt = []
	all_dsst = []
	all_ds = []
	all_sss = []

	for p in PARTICIPANTS
		data_dir = joinpath(BASE_DIR, p, "orexin_data")
		isdir(data_dir) || continue

		pvt = load_json_safe(joinpath(data_dir, "pvt.json"))
		dsst = load_json_safe(joinpath(data_dir, "dsst.json"))
		ds = load_json_safe(joinpath(data_dir, "digit_span.json"))
		sss = load_json_safe(joinpath(data_dir, "sss.json"))

		append!(all_pvt, match_to_condition(pvt, tracking, p))
		append!(all_dsst, match_to_condition(dsst, tracking, p))
		append!(all_ds, match_to_condition(ds, tracking, p))
		append!(all_sss, match_to_condition(sss, tracking, p))

		println("  $p: $(length(pvt)) PVT, $(length(dsst)) DSST, $(length(ds)) DigitSpan, $(length(sss)) SSS entries loaded")
	end

	pvt_df = extract_pvt_metrics(all_pvt)
	dsst_df = extract_dsst_metrics(all_dsst)
	ds_df = extract_digit_span_metrics(all_ds)
	sss_df = extract_sss_metrics(all_sss)

	println("\nMatched to conditions:")
	println("  PVT: $(nrow(pvt_df)) observations")
	println("  DSST: $(nrow(dsst_df)) observations")
	println("  Digit Span: $(nrow(ds_df)) observations")
	println("  SSS: $(nrow(sss_df)) observations")

	# Run tests
	results = Dict[]

	# Continuous: Welch's t-test
	for metric in [:mean_rt, :median_rt, :slowest_10pct]
		r = run_welch_ttest(pvt_df, metric, "PVT_$metric")
		!isnothing(r) && push!(results, r)
	end

	r = run_welch_ttest(dsst_df, :correct_count, "DSST_correct_count")
	!isnothing(r) && push!(results, r)

	# Ordinal: Mann-Whitney U
	for metric in [:forward_span, :backward_span, :total_span]
		r = run_mann_whitney(ds_df, metric, "DigitSpan_$metric")
		!isnothing(r) && push!(results, r)
	end

	r = run_mann_whitney(sss_df, :rating, "SSS_rating")
	!isnothing(r) && push!(results, r)

	# Sleep data
	println("\nLoading sleep data...")
	sleep_df = extract_sleep_metrics(tracking)
	println("  Sleep: $(nrow(sleep_df)) observations")

	for metric in [:duration_h, :minutes_asleep, :efficiency, :deep_min, :light_min, :rem_min, :wake_min]
		r = run_welch_ttest(sleep_df, metric, "Sleep_$metric")
		!isnothing(r) && push!(results, r)
	end

	# Supplementary Fitbit metrics
	println("\nLoading supplementary Fitbit data...")
	supp_df = extract_supplementary_metrics(tracking)
	println("  Supplementary: $(nrow(supp_df)) observations")

	supp_results = Dict[]
	supp_metrics = [
		(:hrv_daily_rmssd, "HRV_daily_rmssd"),
		(:hrv_deep_rmssd, "HRV_deep_rmssd"),
		(:spo2_avg, "SpO2_avg"),
		(:spo2_min, "SpO2_min"),
		(:breathing_rate, "Breathing_rate"),
		(:skin_temp_rel, "Skin_temp_rel"),
		(:steps, "Steps"),
	]
	for (col, label) in supp_metrics
		r = run_welch_ttest(supp_df, col, label)
		!isnothing(r) && push!(supp_results, r)
	end

	# Bonferroni correction
	bonferroni = "--bonferroni" in ARGS || "-b" in ARGS
	n_tests = length(results)
	if bonferroni && n_tests > 0
		for r in results
			r["p_corrected"] = min(r["p_value"] * n_tests, 1.0)
		end
	end

	n_supp_tests = length(supp_results)
	if bonferroni && n_supp_tests > 0
		for r in supp_results
			r["p_corrected"] = min(r["p_value"] * n_supp_tests, 1.0)
		end
	end

	# Print results
	correction_str = bonferroni ? " [Bonferroni-corrected, k=$n_tests]" : ""
	println("\n" * "="^90)
	println("RESULTS: Orexin-A vs Placebo (pooled across participants)$correction_str")
	println("="^90)

	for r in results
		p_raw = r["p_value"]
		p_str = p_raw < 0.001 ? @sprintf("%.1e", p_raw) : @sprintf("%.4f", p_raw)

		if bonferroni
			p_corr = r["p_corrected"]
			p_corr_str = p_corr < 0.001 ? @sprintf("%.1e", p_corr) : @sprintf("%.4f", p_corr)
			sig = p_corr < 0.05 ? " *" : ""
			p_display = "p=$p_str, p_corrected=$p_corr_str$sig"
		else
			sig = p_raw < 0.05 ? " *" : ""
			p_display = "p=$p_str$sig"
		end

		println("\n$(r["metric"]) [$(r["test"])]")
		println("  Orexin:  M=$(round(r["orexin_mean"], digits=2)), SD=$(round(r["orexin_std"], digits=2)), n=$(r["orexin_n"])")
		println("  Placebo: M=$(round(r["placebo_mean"], digits=2)), SD=$(round(r["placebo_std"], digits=2)), n=$(r["placebo_n"])")
		println("  statistic=$(round(r["statistic"], digits=3)), $p_display, $(r["effect_label"])=$(round(r["effect_size"], digits=3))")
	end

	# Save CSV
	out_dir = dirname(@__FILE__)
	out_df = DataFrame(results)
	csv_path = joinpath(out_dir, "analysis_results.csv")
	CSV.write(csv_path, out_df)
	println("\n\nResults saved to $csv_path")

	# Markdown table
	if "--markdown" in ARGS || "-m" in ARGS
		md_path = joinpath(out_dir, "analysis_results.md")
		write_markdown(results, md_path; bonferroni)
	end

	# Plots
	if "--plot" in ARGS || "-p" in ARGS
		plot_results(results, out_dir)
	end

	# --- Supplementary output ---
	if !isempty(supp_results)
		println("\n" * "="^90)
		println("SUPPLEMENTARY: Physiological Fitbit Metrics$correction_str")
		println("="^90)

		for r in supp_results
			p_raw = r["p_value"]
			p_str = p_raw < 0.001 ? @sprintf("%.1e", p_raw) : @sprintf("%.4f", p_raw)

			if bonferroni
				p_corr = r["p_corrected"]
				p_corr_str = p_corr < 0.001 ? @sprintf("%.1e", p_corr) : @sprintf("%.4f", p_corr)
				sig = p_corr < 0.05 ? " *" : ""
				p_display = "p=$p_str, p_corrected=$p_corr_str$sig"
			else
				sig = p_raw < 0.05 ? " *" : ""
				p_display = "p=$p_str$sig"
			end

			println("\n$(r["metric"]) [$(r["test"])]")
			println("  Orexin:  M=$(round(r["orexin_mean"], digits=2)), SD=$(round(r["orexin_std"], digits=2)), n=$(r["orexin_n"])")
			println("  Placebo: M=$(round(r["placebo_mean"], digits=2)), SD=$(round(r["placebo_std"], digits=2)), n=$(r["placebo_n"])")
			println("  statistic=$(round(r["statistic"], digits=3)), $p_display, $(r["effect_label"])=$(round(r["effect_size"], digits=3))")
		end

		supp_csv_path = joinpath(out_dir, "supplementary_results.csv")
		CSV.write(supp_csv_path, DataFrame(supp_results))
		println("\n\nSupplementary results saved to $supp_csv_path")

		if "--markdown" in ARGS || "-m" in ARGS
			supp_md_path = joinpath(out_dir, "supplementary_results.md")
			write_supp_markdown(supp_results, supp_md_path; bonferroni)
		end

		if "--plot" in ARGS || "-p" in ARGS
			plot_supp_results(supp_results, out_dir)
		end
	end
end

main()
