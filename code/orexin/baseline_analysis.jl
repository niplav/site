#!/usr/bin/env julia
#=
Placebo vs. Baseline analysis.
Manipulation check: does the 5-6h sleep constraint produce measurable impairment?
Only participants with dedicated baseline days (currently: Nomagicpill) contribute data.
Pairs placebo ↔ baseline sessions by greedy nearest-neighbor within MAX_PAIR_GAP_DAYS.
=#

using CSV, DataFrames, JSON, Statistics, HypothesisTests, Dates, XLSX, Printf
using Plots; gr()

include(joinpath(@__DIR__, "orexin_data.jl"))

const OUT_DIR = @__DIR__

const METRIC_NAMES = Dict(
	"PVT_mean_rt"           => ("PVT Mean RT (ms)",      1),
	"PVT_median_rt"         => ("PVT Median RT (ms)",    1),
	"PVT_slowest_10pct"     => ("PVT Slowest 10% (ms)",  1),
	"DSST_correct_count"    => ("DSST Correct",          1),
	"DigitSpan_forward_span"  => ("Digit Span Fwd",      2),
	"DigitSpan_backward_span" => ("Digit Span Bwd",      2),
	"DigitSpan_total_span"    => ("Digit Span Total",    1),
	"SSS_rating"            => ("SSS Rating",            2),
)

const PLOT_NAMES = Dict(
	"PVT_mean_rt"             => "Mean RT (ms)",
	"PVT_median_rt"           => "Median RT (ms)",
	"PVT_slowest_10pct"       => "Slowest 10% (ms)",
	"DSST_correct_count"      => "Correct count",
	"DigitSpan_forward_span"  => "Fwd",
	"DigitSpan_backward_span" => "Bwd",
	"DigitSpan_total_span"    => "Total",
	"SSS_rating"              => "SSS Rating",
)

# --- Metric extraction (reuses match_to_condition from orexin_data.jl) ---

function load_json_entries(participant, filename)
	path = joinpath(BASE_DIR, participant, "orexin_data", filename)
	load_json_safe(path)
end

function extract_pvt(tracking)
	rows = []
	for p in PARTICIPANTS
		entries = load_json_entries(p, "pvt.json")
		for m in match_to_condition(entries, tracking, p)
			rts = get(m.entry, "reaction_times_ms", [])
			isempty(rts) && continue
			push!(rows, (
				participant = p,
				condition   = m.condition,
				date        = m.date,
				datetime    = m.datetime,
				mean_rt     = mean(rts),
				median_rt   = median(rts),
				slowest_10pct = quantile(rts, 0.9),
			))
		end
	end
	DataFrame(rows)
end

function extract_dsst(tracking)
	rows = []
	for p in PARTICIPANTS
		entries = load_json_entries(p, "dsst.json")
		for m in match_to_condition(entries, tracking, p)
			cc = get(m.entry, "correct_count", get(m.entry, "completed_trials", nothing))
			isnothing(cc) && continue
			push!(rows, (
				participant   = p,
				condition     = m.condition,
				date          = m.date,
				datetime      = m.datetime,
				correct_count = cc,
			))
		end
	end
	DataFrame(rows)
end

function extract_digit_span(tracking)
	rows = []
	for p in PARTICIPANTS
		entries = load_json_entries(p, "digit_span.json")
		for m in match_to_condition(entries, tracking, p)
			e = m.entry
			fs = get(e, "forward_span",  nothing)
			bs = get(e, "backward_span", nothing)
			ts = get(e, "total_span",    nothing)
			(isnothing(fs) && isnothing(bs)) && continue
			push!(rows, (
				participant  = p,
				condition    = m.condition,
				date         = m.date,
				datetime     = m.datetime,
				forward_span  = something(fs, missing),
				backward_span = something(bs, missing),
				total_span    = something(ts, missing),
			))
		end
	end
	DataFrame(rows)
end

function extract_sss(tracking)
	rows = []
	for p in PARTICIPANTS
		entries = load_json_entries(p, "sss.json")
		for m in match_to_condition(entries, tracking, p)
			r = get(m.entry, "rating", get(m.entry, "score", nothing))
			isnothing(r) && continue
			push!(rows, (
				participant = p,
				condition   = m.condition,
				date        = m.date,
				datetime    = m.datetime,
				rating      = r,
			))
		end
	end
	DataFrame(rows)
end

# --- Paired extraction (placebo vs baseline) ---

function extract_paired_pb(df, metric_col, pairs)
	plc_vals  = Float64[]
	base_vals = Float64[]

	nrow(df) == 0 && return plc_vals, base_vals
	has_dt = :datetime in propertynames(df)

	for pr in pairs
		p  = pr.participant
		pd = pr.placebo_date
		bd = pr.baseline_date

		plc_rows  = df[(df.participant .== p) .& (df.date .== pd), :]
		base_rows = df[(df.participant .== p) .& (df.date .== bd), :]
		(nrow(plc_rows) == 0 || nrow(base_rows) == 0) && continue

		if has_dt
			plc_rows  = sort(plc_rows,  :datetime)
			base_rows = sort(base_rows, :datetime)
		end

		for slot in 1:min(nrow(plc_rows), nrow(base_rows))
			pv = plc_rows[slot,  metric_col]
			bv = base_rows[slot, metric_col]
			(ismissing(pv) || ismissing(bv)) && continue
			push!(plc_vals,  Float64(pv))
			push!(base_vals, Float64(bv))
		end
	end
	plc_vals, base_vals
end

# --- Statistics ---

function run_test(metric, plc_vals, base_vals)
	diffs = plc_vals .- base_vals
	length(diffs) < 2 && return nothing

	# Ordinal SSS → Wilcoxon; continuous → paired t
	if metric == "SSS_rating"
		w   = SignedRankTest(diffs)
		n   = length(diffs)
		n_pos = count(>(0), diffs)
		n_neg = count(<(0), diffs)
		n_nz  = n_pos + n_neg
		r_rb  = n_nz > 0 ? (n_pos - n_neg) / n_nz : 0.0
		return Dict(
			"metric"        => metric,
			"test"          => "Wilcoxon signed-rank",
			"placebo_mean"  => mean(plc_vals),
			"placebo_std"   => std(plc_vals),
			"baseline_mean" => mean(base_vals),
			"baseline_std"  => std(base_vals),
			"n_pairs"       => n,
			"mean_diff"     => mean(diffs),
			"std_diff"      => std(diffs),
			"statistic"     => w.W,
			"p_value"       => pvalue(w),
			"effect_size"   => r_rb,
			"effect_label"  => "rank-biserial r",
		)
	else
		t   = OneSampleTTest(diffs)
		d_z = std(diffs) == 0 ? 0.0 : mean(diffs) / std(diffs)
		return Dict(
			"metric"        => metric,
			"test"          => "Paired t",
			"placebo_mean"  => mean(plc_vals),
			"placebo_std"   => std(plc_vals),
			"baseline_mean" => mean(base_vals),
			"baseline_std"  => std(base_vals),
			"n_pairs"       => length(diffs),
			"mean_diff"     => mean(diffs),
			"std_diff"      => std(diffs),
			"statistic"     => t.t,
			"p_value"       => pvalue(t),
			"effect_size"   => d_z,
			"effect_label"  => "Cohen's d_z",
		)
	end
end

# --- CSV output ---

function write_csv(results, path)
	rows = []
	for r in results
		isnothing(r) && continue
		push!(rows, (
			metric        = r["metric"],
			test          = r["test"],
			placebo_mean  = r["placebo_mean"],
			placebo_std   = r["placebo_std"],
			baseline_mean = r["baseline_mean"],
			baseline_std  = r["baseline_std"],
			n_pairs       = r["n_pairs"],
			mean_diff     = r["mean_diff"],
			std_diff      = r["std_diff"],
			statistic     = r["statistic"],
			p_value       = r["p_value"],
			effect_size   = r["effect_size"],
			effect_label  = r["effect_label"],
		))
	end
	CSV.write(path, DataFrame(rows))
	println("CSV saved to $path")
end

# --- Plot ---

function nice_step(range)
	raw = range / 6
	mag = 10.0^floor(log10(raw))
	for m in [1, 2, 5, 10]
		s = m * mag
		s >= raw && return s
	end
	mag * 10
end

function make_subplot(group_results, title_str; ylabel_str="", ymin=nothing)
	n      = length(group_results)
	labels = [get(PLOT_NAMES, r["metric"], r["metric"]) for r in group_results]
	plc_means  = [r["placebo_mean"]  for r in group_results]
	base_means = [r["baseline_mean"] for r in group_results]
	plc_se     = [r["placebo_std"]  / sqrt(r["n_pairs"]) for r in group_results]
	base_se    = [r["baseline_std"] / sqrt(r["n_pairs"]) for r in group_results]
	p_vals     = [r["p_value"] for r in group_results]

	offset   = isnothing(ymin) ? 0.0 : Float64(ymin)
	plc_plot  = plc_means  .- offset
	base_plot = base_means .- offset

	xs = 1:n
	w  = 0.35

	sp = bar(xs .- w/2, plc_plot,  bar_width=w, yerr=plc_se,
		label="Placebo",  color=colorant"#ffb399", linecolor=:black, lw=0.5)
	bar!(sp, xs .+ w/2, base_plot, bar_width=w, yerr=base_se,
		label="Baseline", color=colorant"#aaccaa", linecolor=:black, lw=0.5)

	global_ymax = 0.0
	p_annot = []
	for i in 1:n
		ymax_i = max(plc_plot[i] + plc_se[i], base_plot[i] + base_se[i])
		global_ymax = max(global_ymax, ymax_i)
		pv = p_vals[i]
		push!(p_annot, (xs[i], ymax_i, pv < 0.001 ? "p<.001" : @sprintf("p=%.3f", pv)))
	end

	ylim_top = global_ymax * 1.2
	for (x, y, s) in p_annot
		annotate!(sp, x, y + global_ymax * 0.05, text(s, 7, :center))
	end

	if !isnothing(ymin)
		tick_step  = nice_step(ylim_top)
		raw_ticks  = collect(0:tick_step:ylim_top)
		real_labels = [@sprintf("%g", t + offset) for t in raw_ticks]
		plot!(sp, yticks=(raw_ticks, real_labels))
	end

	plot!(sp,
		xticks=(xs, labels), xrotation=25,
		ylabel=ylabel_str, title=title_str,
		ylims=(0, ylim_top),
		legend=:topleft,
		bottom_margin=12Plots.mm, left_margin=5Plots.mm,
	)
	sp
end

function plot_results(results, path)
	pvt  = filter(r -> startswith(r["metric"], "PVT_"),       results)
	dsst = filter(r -> startswith(r["metric"], "DSST_"),      results)
	span = filter(r -> startswith(r["metric"], "DigitSpan_"), results)
	sss  = filter(r -> startswith(r["metric"], "SSS_"),       results)

	subplots = []
	!isempty(pvt)  && push!(subplots, make_subplot(pvt,  "PVT";        ylabel_str="RT (ms)",      ymin=200))
	!isempty(dsst) && push!(subplots, make_subplot(dsst, "DSST";       ylabel_str="Correct count", ymin=60))
	!isempty(span) && push!(subplots, make_subplot(span, "Digit Span"; ylabel_str="Span"))
	!isempty(sss)  && push!(subplots, make_subplot(sss,  "SSS";        ylabel_str="Rating",       ymin=2))

	isempty(subplots) && return

	p = plot(subplots...,
		layout=(1, length(subplots)),
		size=(400 * length(subplots), 450),
		plot_title="Placebo vs. Baseline (Manipulation Check)",
	)
	savefig(p, path)
	println("Plot saved to $path")
end

# --- Main ---

tracking      = load_all_tracking()
tracking_wb   = load_all_tracking_with_baseline()
session_pairs = match_sessions(tracking)
pairs         = match_placebo_baseline_sessions(session_pairs, tracking_wb)
println("Placebo-baseline pairs: $(length(pairs))")

# Inject synthetic baseline entries so match_to_condition can find baseline-day data.
baseline_entries = [(participant=p.participant, date=p.baseline_date, condition="baseline")
                    for p in pairs]
tracking_aug = vcat(tracking, baseline_entries)

pvt_df  = extract_pvt(tracking_aug)
dsst_df = extract_dsst(tracking_aug)
ds_df   = extract_digit_span(tracking_aug)
sss_df  = extract_sss(tracking_aug)

metrics = [
	("PVT_mean_rt",            pvt_df,  :mean_rt),
	("PVT_median_rt",          pvt_df,  :median_rt),
	("PVT_slowest_10pct",      pvt_df,  :slowest_10pct),
	("DSST_correct_count",     dsst_df, :correct_count),
	("DigitSpan_forward_span", ds_df,   :forward_span),
	("DigitSpan_backward_span",ds_df,   :backward_span),
	("DigitSpan_total_span",   ds_df,   :total_span),
	("SSS_rating",             sss_df,  :rating),
]

results = filter(!isnothing, [
	run_test(name, extract_paired_pb(df, col, pairs)...)
	for (name, df, col) in metrics
])

write_csv(results, joinpath(OUT_DIR, "baseline_results.csv"))
plot_results(results, joinpath(OUT_DIR, "baseline.png"))
