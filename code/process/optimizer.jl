#!/usr/local/etc/julia/bin/julialauncher
"""
Supplement Stack Optimizer — GP + Thompson Sampling (Julia version)

Fits a Gaussian Process over the binary space {0,1}^n of supplement stacks
and recommends stacks via Thompson Sampling.

Usage:
    julia optimizer.jl init happy
    julia optimizer.jl recommend happy
    julia optimizer.jl stats happy
"""

using CSV, DataFrames, Dates, JSON3, Statistics, TimeZones
using AbstractGPs, KernelFunctions, LinearAlgebra
using Distributions: MvNormal
using JLD2

include(joinpath(@__DIR__, "..", "load.jl"))

# Configuration
const SCRIPT_DIR = @__DIR__
const DATA_DIR = joinpath(SCRIPT_DIR, "..", "..", "data")
const STATE_DIR = joinpath(SCRIPT_DIR, "state")

const SUBSTANCES_FILE = joinpath(DATA_DIR, "substances.csv")
const MOOD_FILE = joinpath(DATA_DIR, "mood.csv")
const MENTAL_FILE = joinpath(DATA_DIR, "mental.csv")
const MEDITATIONS_FILE = joinpath(DATA_DIR, "meditations.csv")
const LIGHT_FILE = joinpath(DATA_DIR, "light.csv")
const MASTURBATIONS_FILE = joinpath(DATA_DIR, "masturbations.csv")

const MOOD_VARIABLES = ["happy", "content", "relaxed", "horny"]
const MENTAL_VARIABLES = ["productivity", "creativity", "sublen", "meaning"]
const ALL_VARIABLES = vcat(MOOD_VARIABLES, MENTAL_VARIABLES)
const MIN_SUPPLEMENT_COUNT = 10

const MORNING_SUBSTANCES = ["caffeine", "creatine", "l-theanine", "nicotine", "omega3", "sugar", "vitaminb12", "vitamind3", "l-glycine", "magnesium"]
const EVENING_SUBSTANCES = ["creatine", "magnesium", "melatonin", "l-glycine"]

const MORNING_CUTOFF_HOUR = 4
const EVENING_CUTOFF_HOUR = 16
const MEDITATION_THRESHOLD_MIN = 20
const LUMENATOR_THRESHOLD_MIN = 120
const MIN_TRAINING_DATE = Date("2022-07-06")  # Substance tracking start

const MORNING_INTERVENTIONS = ["meditation", "lumenator", "masturbation"]
const EVENING_INTERVENTIONS = ["meditation", "masturbation"]

const EXCLUDED_SUBSTANCES = String[]

mkpath(STATE_DIR)

# Data loading
function parse_datetime_robust(s)
	# Try multiple formats, return missing if all fail
	# Strip timezone info if present
	s_clean = replace(string(s), r"[+-]\d{2}:\d{2}$" => "")

	formats = [
		dateformat"yyyy-mm-dd HH:MM:SS",
		dateformat"yyyy-mm-ddTHH:MM:SS",
		dateformat"yyyy-mm-dd HH:MM:SS.s",
		dateformat"yyyy-mm-ddTHH:MM:SS.s"
	]
	for fmt in formats
		try
			return DateTime(s_clean, fmt)
		catch
			continue
		end
	end
	return missing
end

function assign_period(dt::DateTime)
	"""
	Assign datetime to (date, period) based on hour.
	- 04:00-15:59: (date, "morning")
	- 16:00-23:59: (date+1, "evening")
	- 00:00-03:59: (date, "evening")
	"""
	h = hour(dt)
	d = Date(dt)

	if h >= MORNING_CUTOFF_HOUR && h < EVENING_CUTOFF_HOUR
		return d, "morning"
	elseif h >= EVENING_CUTOFF_HOUR
		return d + Day(1), "evening"
	else  # 00:00-03:59
		return d, "evening"
	end
end

function load_substances()
	df = CSV.read(SUBSTANCES_FILE, DataFrame)
	df.datetime = parse_datetime_robust.(df.datetime)
	# Drop rows with unparseable dates
	df = df[.!ismissing.(df.datetime), :]
	# Shift evening substances to next day
	df.date = Date.(df.datetime)
	evening_mask = hour.(df.datetime) .>= EVENING_CUTOFF_HOUR
	df.date[evening_mask] .+= Day(1)
	return df
end

function load_mood()
	df = CSV.read(MOOD_FILE, DataFrame)
	df.datetime = parse_datetime_robust.(df.alarm)
	df = df[.!ismissing.(df.datetime), :]
	df.date = Date.(df.datetime)
	return df
end

function load_mental()
	df = CSV.read(MENTAL_FILE, DataFrame)
	df.datetime = parse_datetime_robust.(df.datetime)
	df = df[.!ismissing.(df.datetime), :]
	df.date = Date.(df.datetime)
	return df
end

function load_meditations()
	df = get_meditations()
	df.datetime = DateTime.(df.meditation_start)
	df = df[.!ismissing.(df.datetime), :]
	df = df[.!ismissing.(df.meditation_duration), :]

	period_data = assign_period.(df.datetime)
	df.date = [p[1] for p in period_data]
	df.period = [p[2] for p in period_data]

	return df
end

function load_lumenator()
	df = CSV.read(LIGHT_FILE, DataFrame)
	df.start_dt = parse_datetime_robust.(df.start)
	df.stop_dt = parse_datetime_robust.(df.stop)
	df = df[.!ismissing.(df.start_dt) .& .!ismissing.(df.stop_dt), :]

	df.duration = Second.(df.stop_dt .- df.start_dt) .|> x -> x.value
	df = df[df.duration .> 0, :]

	period_data = assign_period.(df.start_dt)
	df.date = [p[1] for p in period_data]
	df.period = [p[2] for p in period_data]

	return df
end

function load_masturbations()
	df = CSV.read(MASTURBATIONS_FILE, DataFrame)
	df.datetime = parse_datetime_robust.(df.datetime)
	df = df[.!ismissing.(df.datetime), :]

	period_data = assign_period.(df.datetime)
	df.date = [p[1] for p in period_data]
	df.period = [p[2] for p in period_data]

	return df
end

function load_outcome_df(variable)
	variable ∈ MOOD_VARIABLES ? load_mood() : load_mental()
end

# Build training data
function build_training_data(substances_df, outcome_df, supplements, variable, period,
                            med_df=nothing, light_df=nothing, mast_df=nothing, interventions=String[])
	# Filter substances to supplements we care about
	sub_filtered = filter(r -> r.substance ∈ supplements, substances_df)

	# Daily outcome aggregation
	outcome_agg = combine(groupby(outcome_df, :date),
		variable => (x -> mean(skipmissing(x))) => :outcome,
		variable => length => :count)

	# Drop rows with missing outcomes
	outcome_agg = outcome_agg[.!isnan.(outcome_agg.outcome), :]

	# Filter to dates >= MIN_TRAINING_DATE
	outcome_agg = filter(r -> r.date >= MIN_TRAINING_DATE, outcome_agg)

	if isempty(outcome_agg)
		n_features = length(supplements) + length(interventions)
		return zeros(Float64, 0, n_features), Float64[], Float64[], Date[], vcat(supplements, interventions)
	end

	all_dates = outcome_agg.date
	date_idx_map = Dict(d => i for (i, d) in enumerate(all_dates))

	# Build substance matrix for all outcome dates
	X_sub = zeros(Float64, length(all_dates), length(supplements))

	if !isempty(sub_filtered)
		# Group by date and substance
		daily_intake = combine(groupby(sub_filtered, [:date, :substance]), nrow => :count)
		daily_intake.present = min.(daily_intake.count, 1)

		# Fill in X_sub matrix
		supp_idx_map = Dict(s => i for (i, s) in enumerate(supplements))

		for row in eachrow(daily_intake)
			if row.date ∈ keys(date_idx_map) && row.substance ∈ keys(supp_idx_map)
				X_sub[date_idx_map[row.date], supp_idx_map[row.substance]] = row.present
			end
		end
	end

	# Build intervention matrix
	X_int = zeros(Float64, length(all_dates), length(interventions))

	if !isempty(interventions)
		int_idx_map = Dict(i => idx for (idx, i) in enumerate(interventions))

		# Meditation intervention
		if !isnothing(med_df) && "meditation" ∈ interventions
			med_filtered = filter(r -> r.period == period, med_df)
			if !isempty(med_filtered)
				med_agg = combine(groupby(med_filtered, :date),
					:meditation_duration => sum => :total_duration)
				threshold_seconds = MEDITATION_THRESHOLD_MIN * 60

				int_idx = int_idx_map["meditation"]
				for row in eachrow(med_agg)
					if row.date ∈ keys(date_idx_map)
						X_int[date_idx_map[row.date], int_idx] = row.total_duration > threshold_seconds ? 1.0 : 0.0
					end
				end
			end
		end

		# Lumenator intervention (morning only)
		if !isnothing(light_df) && "lumenator" ∈ interventions
			light_filtered = filter(r -> r.period == period, light_df)
			if !isempty(light_filtered)
				light_agg = combine(groupby(light_filtered, :date),
					:duration => sum => :total_duration)
				threshold_seconds = LUMENATOR_THRESHOLD_MIN * 60

				int_idx = int_idx_map["lumenator"]
				for row in eachrow(light_agg)
					if row.date ∈ keys(date_idx_map)
						X_int[date_idx_map[row.date], int_idx] = row.total_duration > threshold_seconds ? 1.0 : 0.0
					end
				end
			end
		end

		# Masturbation intervention
		if !isnothing(mast_df) && "masturbation" ∈ interventions
			mast_filtered = filter(r -> r.period == period, mast_df)
			if !isempty(mast_filtered)
				mast_agg = combine(groupby(mast_filtered, :date), nrow => :count)

				int_idx = int_idx_map["masturbation"]
				for row in eachrow(mast_agg)
					if row.date ∈ keys(date_idx_map)
						X_int[date_idx_map[row.date], int_idx] = row.count > 0 ? 1.0 : 0.0
					end
				end
			end
		end
	end

	# Combine substance and intervention matrices
	X = hcat(X_sub, X_int)
	features = vcat(supplements, interventions)

	y = Vector{Float64}(outcome_agg.outcome)
	counts = Vector{Float64}(outcome_agg.count)
	dates = outcome_agg.date

	return X, y, counts, dates, features
end

# GP model
function make_kernel(n_supplements, kernel_type="matern")
	if kernel_type == "matern"
		# Matérn 5/2 with ARD
		length_scales = ones(n_supplements)
		return Matern52Kernel() ∘ ARDTransform(length_scales)
	elseif kernel_type == "poly2"
		# Polynomial degree 2
		return PolynomialKernel(; degree=2, c=1.0)
	elseif kernel_type == "poly3"
		# Polynomial degree 3
		return PolynomialKernel(; degree=3, c=1.0)
	else
		error("Unknown kernel type: $kernel_type")
	end
end

function fit_gp(X, y, counts, kernel_type="matern")
	n, d = size(X)

	# Kernel
	kernel = make_kernel(d, kernel_type)

	# Observation noise (heteroskedastic)
	noise = 1.0 ./ counts

	# Create GP
	f = GP(kernel)
	fx = f(RowVecs(X), noise)

	# Posterior
	post = AbstractGPs.posterior(fx, y)

	return post, fx
end

# Thompson sampling
function all_stacks(n)
	# All 2^n binary vectors
	stacks = zeros(Int, 2^n, n)
	for i in 0:(2^n - 1)
		for j in 1:n
			stacks[i+1, j] = (i >> (j-1)) & 1
		end
	end
	return Float64.(stacks)
end

function thompson_sample(posterior, candidates)
	# Draw from joint posterior
	pred = posterior(RowVecs(candidates))
	μ, Σ = mean(pred), cov(pred)

	# Add jitter for numerical stability
	Σ += I * 1e-6

	sample = rand(MvNormal(μ, Σ))
	best_idx = argmax(sample)

	return best_idx, sample
end

function filter_candidates(candidates, supplements, excluded)
	if isempty(excluded)
		return candidates
	end

	excluded_idx = [i for (i, s) in enumerate(supplements) if s ∈ excluded]
	if isempty(excluded_idx)
		return candidates
	end

	mask = vec(all(candidates[:, excluded_idx] .== 0, dims=2))
	return candidates[mask, :]
end

# Display
function stack_label(supplements, vector)
	selected = [supplements[i] for (i, v) in enumerate(vector) if v == 1]
	isempty(selected) ? "(nothing)" : join(selected, ", ")
end

# State persistence
state_path(variable, period) = joinpath(STATE_DIR, "gp_data_$(variable)_$(period).json")
model_path(variable, period) = joinpath(STATE_DIR, "gp_model_$(variable)_$(period).jld2")

function save_model(posterior, variable, period)
	jldsave(model_path(variable, period); posterior=posterior)
end

function load_model(variable, period)
	path = model_path(variable, period)
	!isfile(path) && return nothing
	data = load(path)
	return data["posterior"]
end

function save_state(X, y, counts, dates, supplements, variable, period)
	data = Dict(
		"supplements" => supplements,
		"X" => [collect(X[i, :]) for i in 1:size(X, 1)],
		"y" => y,
		"counts" => counts,
		"dates" => string.(dates)
	)
	open(state_path(variable, period), "w") do f
		JSON3.write(f, data)
	end
end

function load_state(variable, period)
	path = state_path(variable, period)
	!isfile(path) && return nothing

	data = JSON3.read(read(path, String))
	X = reduce(vcat, transpose.(data.X))
	y = Vector{Float64}(data.y)
	counts = Vector{Float64}(data.counts)
	dates = Date.(data.dates)
	supplements = Vector{String}(data.supplements)

	return X, y, counts, dates, supplements
end

# Commands
function cmd_init(variable, kernel_type="matern")
	substances_df = load_substances()
	outcome_df = load_outcome_df(variable)
	med_df = load_meditations()
	light_df = load_lumenator()
	mast_df = load_masturbations()

	for period in ["morning", "evening"]
		supplements = period == "morning" ? MORNING_SUBSTANCES : EVENING_SUBSTANCES
		interventions = period == "morning" ? MORNING_INTERVENTIONS : EVENING_INTERVENTIONS

		X, y, counts, dates, features = build_training_data(substances_df, outcome_df, supplements, variable, period,
		                                                     med_df, light_df, mast_df, interventions)

		if isempty(X)
			println("ERROR: No training data for $variable ($period).")
			exit(1)
		end

		save_state(X, y, counts, dates, features, variable, period)

		posterior, fx = fit_gp(X, y, counts, kernel_type)
		save_model(posterior, variable, period)

		candidates = all_stacks(length(features))
		pred = posterior(RowVecs(candidates))
		μ = mean(pred)

		best_idx = argmax(μ)
	end
end

function cmd_recommend(variable; cached=false, excluded=String[], kernel_type="matern")
	substances_df = cached ? nothing : load_substances()
	outcome_df = cached ? nothing : load_outcome_df(variable)
	med_df = cached ? nothing : load_meditations()
	light_df = cached ? nothing : load_lumenator()
	mast_df = cached ? nothing : load_masturbations()

	results = Dict{String, String}()

	for period in ["morning", "evening"]
		supplements = period == "morning" ? MORNING_SUBSTANCES : EVENING_SUBSTANCES
		interventions = period == "morning" ? MORNING_INTERVENTIONS : EVENING_INTERVENTIONS

		if cached
			posterior = load_model(variable, period)
			state = load_state(variable, period)
			if isnothing(posterior) || isnothing(state)
				println("ERROR: No cached $period model. Run without --cached first.")
				exit(1)
			end
			X, y, counts, dates, features = state
		else
			X, y, counts, dates, features = build_training_data(substances_df, outcome_df, supplements, variable, period,
			                                                     med_df, light_df, mast_df, interventions)
			posterior, fx = fit_gp(X, y, counts, kernel_type)
			save_model(posterior, variable, period)
		end

		candidates = all_stacks(length(features))
		candidates = filter_candidates(candidates, features, excluded)

		if isempty(candidates)
			println("ERROR: All $period stacks excluded.")
			exit(1)
		end

		best_idx, _ = thompson_sample(posterior, candidates)
		results[period] = stack_label(features, candidates[best_idx, :])
	end

	println("morning: $(results["morning"])")
	println("evening: $(results["evening"])")
end

function cmd_stats(variable, kernel_type="matern")
	substances_df = load_substances()
	outcome_df = load_outcome_df(variable)
	med_df = load_meditations()
	light_df = load_lumenator()
	mast_df = load_masturbations()

	for period in ["morning", "evening"]
		supplements = period == "morning" ? MORNING_SUBSTANCES : EVENING_SUBSTANCES
		interventions = period == "morning" ? MORNING_INTERVENTIONS : EVENING_INTERVENTIONS
		X, y, counts, dates, features = build_training_data(substances_df, outcome_df, supplements, variable, period,
		                                                     med_df, light_df, mast_df, interventions)

		println("\nFitting $period GP on $(size(X, 1)) observations (kernel: $kernel_type)...")
		posterior, fx = fit_gp(X, y, counts, kernel_type)

		candidates = all_stacks(length(features))
		pred = posterior(RowVecs(candidates))
		μ = mean(pred)
		σ = std(pred)

		# Marginal effects
		println("\n" * "="^72)
		println("  $(titlecase(period)) — Marginal Feature Effects")
		println("="^72)
		println("  $(rpad("Feature", 40)) $(lpad("With", 7)) $(lpad("W/o", 7)) $(lpad("Effect", 7))")
		println("  $(repeat("-", 40)) $(repeat("-", 7)) $(repeat("-", 7)) $(repeat("-", 7))")

		for (i, feat) in enumerate(features)
			with_mask = candidates[:, i] .== 1
			without_mask = candidates[:, i] .== 0

			with_mean = mean(μ[with_mask])
			without_mean = mean(μ[without_mask])
			effect = with_mean - without_mean

			println("  $(rpad(feat, 40)) $(lpad(round(with_mean, digits=4), 7)) $(lpad(round(without_mean, digits=4), 7)) $(lpad(round(effect, digits=4), 7))")
		end

		# Top 10 stacks
		top10_idx = sortperm(μ, rev=true)[1:min(10, length(μ))]

		println("\n  $(titlecase(period)) — Top 10 Stacks")
		println("="^90)
		println("  $(rpad("#", 3)) $(rpad("Stack", 64)) $(lpad("Mean", 6)) $(lpad("Std", 6))")
		println("  $(repeat("-", 3)) $(repeat("-", 64)) $(repeat("-", 6)) $(repeat("-", 6))")

		for (rank, idx) in enumerate(top10_idx)
			label = stack_label(features, candidates[idx, :])
			println("  $(rpad(rank, 3)) $(rpad(label, 64)) $(lpad(round(μ[idx], digits=4), 6)) $(lpad(round(σ[idx], digits=4), 6))")
		end
		println("="^90)

		println("\n  Training: $(size(X, 1)) days ($(minimum(dates)) to $(maximum(dates)))")
	end
end

# CLI
const USAGE = """Supplement Stack Optimizer (GP + Thompson Sampling)

Usage:
    julia optimizer.jl [--cached] [--exclude sub1,sub2] [--kernel TYPE] [variable]
                                                    recommend (default: productivity)
    julia optimizer.jl stats [--kernel TYPE] [variable]
                                                    show effects & top stacks
    julia optimizer.jl init [--kernel TYPE] [variable]
                                                    explicit rebuild

Flags:
    --cached            skip rebuild, use last saved state (faster for repeated samples)
    --exclude sub1,sub2 exclude substances from recommendations (comma-separated, no spaces)
    --kernel TYPE       kernel type: matern (default), poly2, poly3

Variables: $(join(ALL_VARIABLES, ", "))
"""

function main()
	args = collect(ARGS)

	# Parse --cached
	cached = "--cached" ∈ args
	filter!(x -> x != "--cached", args)

	# Parse --kernel
	kernel_type = "matern"
	kernel_idx = findfirst(x -> startswith(x, "--kernel"), args)
	if !isnothing(kernel_idx)
		arg = args[kernel_idx]
		if contains(arg, "=")
			kernel_type = split(arg, "=")[2]
		elseif kernel_idx < length(args)
			kernel_type = args[kernel_idx + 1]
			deleteat!(args, kernel_idx + 1)
		end
		deleteat!(args, kernel_idx)
	end

	if kernel_type ∉ ["matern", "poly2", "poly3"]
		println("ERROR: Unknown kernel type '$kernel_type'. Use matern, poly2, or poly3.")
		exit(1)
	end

	# Parse --exclude
	excluded = String[]
	exclude_idx = findfirst(x -> startswith(x, "--exclude"), args)
	if !isnothing(exclude_idx)
		arg = args[exclude_idx]
		if contains(arg, "=")
			excluded = split(split(arg, "=")[2], ",")
		elseif exclude_idx < length(args)
			excluded = split(args[exclude_idx + 1], ",")
			deleteat!(args, exclude_idx + 1)
		end
		deleteat!(args, exclude_idx)
	end

	if isempty(args)
		cmd_recommend("productivity"; cached=cached, excluded=excluded, kernel_type=kernel_type)
	elseif args[1] ∈ ALL_VARIABLES
		cmd_recommend(args[1]; cached=cached, excluded=excluded, kernel_type=kernel_type)
	elseif args[1] == "stats"
		variable = length(args) > 1 ? args[2] : "productivity"
		cmd_stats(variable, kernel_type)
	elseif args[1] == "init"
		variable = length(args) > 1 ? args[2] : "productivity"
		cmd_init(variable, kernel_type)
	else
		println(USAGE)
		exit(1)
	end
end

if abspath(PROGRAM_FILE) == @__FILE__
	main()
end
