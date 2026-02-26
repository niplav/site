#!/usr/bin/env julia
#=
Bayesian analysis of Orexin-A experiment data.
Hierarchical model with participant random intercepts.
Prior on standardized treatment effect: N(0,1).
=#

using CSV, DataFrames, JSON, Statistics, Dates, XLSX, Printf
using Turing, MCMCChains, Random
using Plots, KernelDensity; gr()

Random.seed!(42)

include(joinpath(@__DIR__, "orexin_data.jl"))

# --- Extract a single metric from matched data ---

function extract_metric(matched, metric_fn)
	rows = []
	for m in matched
		val = metric_fn(m.entry)
		isnothing(val) && continue
		push!(rows, (
			participant = m.participant,
			condition = m.condition,
			value = Float64(val)
		))
	end
	DataFrame(rows)
end

# --- Bayesian model ---

@model function treatment_effect(y, treatment, participant_idx, n_participants)
	# Priors
	μ ~ Normal(0, 10)         # grand mean (on raw scale, vague)
	σ ~ truncated(Normal(0, 10); lower=0)  # residual SD
	δ ~ Normal(0, 1)          # standardized treatment effect (N(0,1) prior)

	# Participant random intercepts
	τ ~ truncated(Normal(0, 5); lower=0)   # between-participant SD
	α ~ filldist(Normal(0, τ), n_participants)

	# Likelihood
	for i in eachindex(y)
		y[i] ~ Normal(μ + δ * σ * treatment[i] + α[participant_idx[i]], σ)
	end
end

function run_bayesian_analysis(df, label; n_samples=2000, n_chains=4)
	nrow(df) < 4 && return nothing

	# Encode treatment: orexin=1, placebo=0
	treat = [r.condition == "orexin" ? 1.0 : 0.0 for r in eachrow(df)]

	# Encode participants as integers
	p_names = unique(df.participant)
	p_map = Dict(p => i for (i, p) in enumerate(p_names))
	p_idx = [p_map[r.participant] for r in eachrow(df)]

	y = df.value

	model = treatment_effect(y, treat, p_idx, length(p_names))
	chain = sample(model, NUTS(), MCMCThreads(), n_samples, n_chains; progress=false)

	# Extract δ posterior
	δ_samples = vec(chain[:δ].data)
	δ_mean = mean(δ_samples)
	δ_std = std(δ_samples)
	δ_q = quantile(δ_samples, [0.025, 0.25, 0.5, 0.75, 0.975])
	p_positive = mean(δ_samples .> 0)
	p_negative = mean(δ_samples .< 0)

	# Effective sample size and Rhat for δ
	δ_summary = summarize(chain[[:δ]])
	ess_val = δ_summary[1, :ess_tail]
	rhat_val = δ_summary[1, :rhat]

	Dict(
		"metric" => label,
		"n" => nrow(df),
		"n_orexin" => count(==(1.0), treat),
		"n_placebo" => count(==(0.0), treat),
		"δ_mean" => δ_mean,
		"δ_std" => δ_std,
		"δ_median" => δ_q[3],
		"ci_025" => δ_q[1],
		"ci_25" => δ_q[2],
		"ci_75" => δ_q[4],
		"ci_975" => δ_q[5],
		"p_positive" => p_positive,
		"p_negative" => p_negative,
		"ess" => ess_val,
		"rhat" => rhat_val,
		"δ_samples" => δ_samples,
	)
end

function extract_sleep_metric(tracking, metric_fn)
	rows = []
	for p in PARTICIPANTS
		sleep_by_date = load_sleep_data(p)
		isempty(sleep_by_date) && continue
		p_tracking = filter(r -> r.participant == p, tracking)
		for t in p_tracking
			next_day = string(t.date + Day(1))
			r = get(sleep_by_date, next_day, nothing)
			isnothing(r) && continue
			val = metric_fn(r)
			isnothing(val) && continue
			push!(rows, (participant=p, condition=t.condition, value=Float64(val)))
		end
	end
	DataFrame(rows)
end

function extract_supp_fitbit(tracking, metric_name, subdir, value_fn; use_next_day=false)
	rows = []
	for p in PARTICIPANTS
		by_date = load_fitbit_daily(p, subdir)
		isempty(by_date) && continue
		p_tracking = filter(r -> r.participant == p, tracking)
		for t in p_tracking
			ds = use_next_day ? string(t.date + Day(1)) : string(t.date)
			rec = get(by_date, ds, nothing)
			isnothing(rec) && continue
			val = value_fn(rec)
			isnothing(val) && continue
			push!(rows, (participant=p, condition=t.condition, value=Float64(val)))
		end
	end
	DataFrame(rows)
end

# --- Main ---

function main()
	println("Bayesian Orexin-A Analysis")
	println("Prior on δ (standardized effect): N(0, 1)")
	println("="^70)

	tracking = load_all_tracking()
	println("\n$(length(tracking)) dosing records loaded\n")

	# Define all metrics to analyze
	metrics = Pair{String, Any}[]

	# Cognitive tests
	cognitive_metrics = [
		("PVT_mean_rt", "pvt.json", e -> begin
			rts = get(e, "reaction_times_ms", [])
			isempty(rts) ? nothing : mean(rts)
		end),
		("PVT_median_rt", "pvt.json", e -> begin
			rts = get(e, "reaction_times_ms", [])
			isempty(rts) ? nothing : median(rts)
		end),
		("DSST_correct", "dsst.json", e -> get(e, "correct_count", get(e, "completed_trials", nothing))),
		("DigitSpan_forward", "digit_span.json", e -> get(e, "forward_span", nothing)),
		("DigitSpan_backward", "digit_span.json", e -> get(e, "backward_span", nothing)),
		("DigitSpan_total", "digit_span.json", e -> get(e, "total_span", nothing)),
		("SSS_rating", "sss.json", e -> get(e, "rating", get(e, "score", nothing))),
	]

	# Build cognitive DataFrames
	println("Loading cognitive data...")
	for (label, filename, metric_fn) in cognitive_metrics
		all_matched = []
		for p in PARTICIPANTS
			data_dir = joinpath(BASE_DIR, p, "orexin_data")
			isdir(data_dir) || continue
			entries = load_json_safe(joinpath(data_dir, filename))
			append!(all_matched, match_to_condition(entries, tracking, p))
		end
		df = extract_metric(all_matched, metric_fn)
		push!(metrics, label => df)
	end

	# Sleep metrics
	println("Loading sleep data...")
	sleep_extractors = [
		("Sleep_duration_h", r -> get(r, "duration", nothing) === nothing ? nothing : get(r, "duration", 0) / 3.6e6),
		("Sleep_efficiency", r -> get(r, "efficiency", nothing)),
		("Sleep_deep_min", r -> begin
			levels = get(get(r, "levels", Dict()), "summary", Dict())
			get(get(levels, "deep", Dict()), "minutes", nothing)
		end),
		("Sleep_rem_min", r -> begin
			levels = get(get(r, "levels", Dict()), "summary", Dict())
			get(get(levels, "rem", Dict()), "minutes", nothing)
		end),
		("Sleep_wake_min", r -> begin
			levels = get(get(r, "levels", Dict()), "summary", Dict())
			get(get(levels, "wake", Dict()), "minutes", nothing)
		end),
	]

	for (label, metric_fn) in sleep_extractors
		df = extract_sleep_metric(tracking, metric_fn)
		push!(metrics, label => df)
	end

	# Supplementary Fitbit metrics
	println("Loading supplementary Fitbit data...")
	supp_metrics = Pair{String, Any}[]

	push!(supp_metrics, "HRV_daily_rmssd" => extract_supp_fitbit(tracking, "HRV_daily_rmssd", "hrv",
		r -> get(get(r, "value", Dict()), "dailyRmssd", nothing)))
	push!(supp_metrics, "HRV_deep_rmssd" => extract_supp_fitbit(tracking, "HRV_deep_rmssd", "hrv",
		r -> get(get(r, "value", Dict()), "deepRmssd", nothing)))
	push!(supp_metrics, "SpO2_avg" => extract_supp_fitbit(tracking, "SpO2_avg", "spo2",
		r -> get(get(r, "value", Dict()), "avg", nothing)))
	push!(supp_metrics, "SpO2_min" => extract_supp_fitbit(tracking, "SpO2_min", "spo2",
		r -> get(get(r, "value", Dict()), "min", nothing)))
	push!(supp_metrics, "Breathing_rate" => extract_supp_fitbit(tracking, "Breathing_rate", "breathing_rate",
		r -> get(get(r, "value", Dict()), "breathingRate", nothing)))
	push!(supp_metrics, "Skin_temp_rel" => extract_supp_fitbit(tracking, "Skin_temp_rel", "temperature_skin",
		r -> get(get(r, "value", Dict()), "nightlyRelative", nothing); use_next_day=true))
	push!(supp_metrics, "Steps_kilosteps" => extract_supp_fitbit(tracking, "Steps_kilosteps", "steps",
		r -> begin
			sv = get(r, "value", nothing)
			isnothing(sv) && return nothing
			v = tryparse(Float64, string(sv))
			(isnothing(v) || v == 0.0) ? nothing : v / 1000.0
		end))

	# Run Bayesian analysis for each metric
	results = Dict[]
	println("\nRunning MCMC (this takes a while)...\n")

	for (label, df) in metrics
		norx = nrow(df) > 0 ? count(==("orexin"), df.condition) : 0
		nplc = nrow(df) > 0 ? count(==("placebo"), df.condition) : 0
		println("  $label (n=$norx orexin, $nplc placebo)...")

		r = run_bayesian_analysis(df, label)
		if !isnothing(r)
			push!(results, r)
			δm = @sprintf("%.3f", r["δ_mean"])
			ci = @sprintf("[%.3f, %.3f]", r["ci_025"], r["ci_975"])
			pp = @sprintf("%.1f%%", r["p_positive"] * 100)
			println("    δ = $δm, 95% CI = $ci, P(δ>0) = $pp")
		else
			println("    Skipped (insufficient data)")
		end
	end

	# Print summary table
	println("\n" * "="^70)
	println("POSTERIOR SUMMARY: δ ~ N(0,1) prior")
	println("δ > 0 means orexin > placebo on raw metric")
	println("="^70)
	println()
	@printf("%-22s %7s %18s %8s %8s\n", "Metric", "δ_mean", "95% CI", "P(δ>0)", "Rhat")
	println("-"^70)

	for r in results
		ci = @sprintf("[%+.3f, %+.3f]", r["ci_025"], r["ci_975"])
		@printf("%-22s %+7.3f %18s %7.1f%% %8.3f\n",
			r["metric"], r["δ_mean"], ci, r["p_positive"]*100, r["rhat"])
	end

	# Save CSV (exclude samples column)
	out_dir = dirname(@__FILE__)
	csv_results = [Dict(k => v for (k,v) in r if k != "δ_samples") for r in results]
	out_df = DataFrame(csv_results)
	csv_path = joinpath(out_dir, "bayesian_results.csv")
	CSV.write(csv_path, out_df)
	println("\nResults saved to $csv_path")

	# Markdown
	if "--markdown" in ARGS || "-m" in ARGS
		md_path = joinpath(out_dir, "bayesian_results.md")
		write_bayesian_markdown(results, md_path)
	end

	# Plots
	if "--plot" in ARGS || "-p" in ARGS
		plot_posteriors(results, out_dir)
	end

	# --- Supplementary Bayesian analysis ---
	supp_results = Dict[]
	println("\nRunning supplementary MCMC...\n")

	for (label, df) in supp_metrics
		norx = nrow(df) > 0 ? count(==("orexin"), df.condition) : 0
		nplc = nrow(df) > 0 ? count(==("placebo"), df.condition) : 0
		println("  $label (n=$norx orexin, $nplc placebo)...")

		r = run_bayesian_analysis(df, label)
		if !isnothing(r)
			push!(supp_results, r)
			δm = @sprintf("%.3f", r["δ_mean"])
			ci = @sprintf("[%.3f, %.3f]", r["ci_025"], r["ci_975"])
			pp = @sprintf("%.1f%%", r["p_positive"] * 100)
			println("    δ = $δm, 95% CI = $ci, P(δ>0) = $pp")
		else
			println("    Skipped (insufficient data)")
		end
	end

	if !isempty(supp_results)
		println("\n" * "="^70)
		println("SUPPLEMENTARY POSTERIOR SUMMARY: δ ~ N(0,1) prior")
		println("="^70)
		println()
		@printf("%-22s %7s %18s %8s %8s\n", "Metric", "δ_mean", "95% CI", "P(δ>0)", "Rhat")
		println("-"^70)

		for r in supp_results
			ci = @sprintf("[%+.3f, %+.3f]", r["ci_025"], r["ci_975"])
			@printf("%-22s %+7.3f %18s %7.1f%% %8.3f\n",
				r["metric"], r["δ_mean"], ci, r["p_positive"]*100, r["rhat"])
		end

		supp_csv = [Dict(k => v for (k,v) in r if k != "δ_samples") for r in supp_results]
		supp_csv_path = joinpath(out_dir, "bayesian_supplementary_results.csv")
		CSV.write(supp_csv_path, DataFrame(supp_csv))
		println("\nSupplementary results saved to $supp_csv_path")

		if "--markdown" in ARGS || "-m" in ARGS
			supp_md_path = joinpath(out_dir, "bayesian_supplementary_results.md")
			write_bayesian_markdown(supp_results, supp_md_path)
		end

		if "--plot" in ARGS || "-p" in ARGS
			plot_posteriors(supp_results, out_dir; filename="supplementary_posteriors.png", left=-2, right=2, legpos=:top)
		end
	end
end

function plot_posteriors(results, out_dir; filename="posteriors.png", left=-2, right=2, legpos=:topleft)
	n = length(results)
	ncols = 3
	nrows = ceil(Int, n / ncols)

	subplots = []
	# Prior shown only in [left, right] range
	prior_x = range(left, right, length=500)
	prior_y = @. exp(-prior_x^2 / 2) / sqrt(2π)  # N(0,1) density

	for r in results
		samples = r["δ_samples"]
		kd = kde(samples)

		# Clip KDE to [left, right]
		mask = kd.x .>= left .&& kd.x .<= right
		kd_x = kd.x[mask]
		kd_y = kd.density[mask]

		sp = plot(
			prior_x, prior_y,
			label="Prior N(0,1)",
			color=:gray,
			linestyle=:dash,
			lw=1.5,
			fill=0, fillalpha=0.1, fillcolor=:gray,
		)
		plot!(sp, kd_x, kd_y,
			label="Posterior",
			color=colorant"#264d99",
			lw=2,
			fill=0, fillalpha=0.25, fillcolor=colorant"#264d99",
		)
		# 95% CI shading
		ci_mask = kd_x .>= r["ci_025"] .&& kd_x .<= r["ci_975"]
		ci_xr = kd_x[ci_mask]
		ci_yr = kd_y[ci_mask]
		plot!(sp, ci_xr, ci_yr,
			label="", fill=0, fillalpha=0.3, fillcolor=colorant"#264d99",
			linewidth=0,
		)
		vline!(sp, [0], color=:black, linestyle=:dot, lw=1, label="")
		vline!(sp, [r["δ_mean"]], color=:red, lw=1, label="δ=$(round(r["δ_mean"], digits=2))")

		title!(sp, r["metric"], titlefontsize=9)
		xlabel!(sp, "δ (standardized effect)")
		ylabel!(sp, "Density")
		xlims!(sp, left, right)
		plot!(sp, legend=legpos, legendfontsize=6)

		push!(subplots, sp)
	end

	p = plot(subplots...,
		layout=(nrows, ncols),
		size=(450*ncols, 350*nrows),
		left_margin=5Plots.mm,
		bottom_margin=5Plots.mm,
		dpi=200,
	)
	path = joinpath(out_dir, filename)
	savefig(p, path)
	println("Posterior plot saved to $path")
end

function write_bayesian_markdown(results, path)
	lines = [
		"| Metric | δ (posterior mean) | 95% CI | P(δ>0) | P(δ<0) |",
		"|--------|-------------------|--------|--------|--------|",
	]
	for r in results
		ci = @sprintf("[%+.3f, %+.3f]", r["ci_025"], r["ci_975"])
		push!(lines, @sprintf("| %s | %+.3f | %s | %.1f%% | %.1f%% |",
			r["metric"], r["δ_mean"], ci, r["p_positive"]*100, r["p_negative"]*100))
	end
	open(path, "w") do f
		write(f, join(lines, "\n") * "\n")
	end
	println("Markdown saved to $path")
end

main()
