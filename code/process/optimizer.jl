#!/usr/bin/env julia
"""
Supplement Stack Optimizer — GP + Thompson Sampling (Julia version)

Fits a Gaussian Process over the binary space {0,1}^n of supplement stacks
and recommends stacks via Thompson Sampling.

Usage:
    julia optimizer.jl init happy
    julia optimizer.jl recommend happy
    julia optimizer.jl stats happy
    julia optimizer.jl update 2026-02-04 67.5 happy
"""

using CSV, DataFrames, Dates, JSON3, Statistics
using AbstractGPs, KernelFunctions, LinearAlgebra
using Distributions: MvNormal
using JLD2

# Configuration
const SCRIPT_DIR = @__DIR__
const DATA_DIR = joinpath(SCRIPT_DIR, "..", "..", "data")
const STATE_DIR = joinpath(SCRIPT_DIR, "state")

const SUBSTANCES_FILE = joinpath(DATA_DIR, "substances.csv")
const MOOD_FILE = joinpath(DATA_DIR, "mood.csv")
const MENTAL_FILE = joinpath(DATA_DIR, "mental.csv")

const MOOD_VARIABLES = ["happy", "content", "relaxed", "horny"]
const MENTAL_VARIABLES = ["productivity", "creativity", "sublen", "meaning"]
const ALL_VARIABLES = vcat(MOOD_VARIABLES, MENTAL_VARIABLES)
const MIN_SUPPLEMENT_COUNT = 10

const MORNING_SUBSTANCES = ["caffeine", "creatine", "l-theanine", "nicotine", "omega3", "sugar", "vitaminb12", "vitamind3", "l-glycine", "magnesium"]
const EVENING_SUBSTANCES = ["creatine", "magnesium", "melatonin", "l-glycine"]

const EVENING_CUTOFF_HOUR = 16
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

function load_outcome_df(variable)
	variable ∈ MOOD_VARIABLES ? load_mood() : load_mental()
end

# Build training data
function build_training_data(substances_df, outcome_df, supplements, variable)
	# Filter substances to supplements we care about
	sub_filtered = filter(r -> r.substance ∈ supplements, substances_df)

	# Daily outcome aggregation
	outcome_agg = combine(groupby(outcome_df, :date),
		variable => (x -> mean(skipmissing(x))) => :outcome,
		variable => length => :count)

	# Drop rows with missing outcomes
	outcome_agg = outcome_agg[.!isnan.(outcome_agg.outcome), :]

	if isempty(outcome_agg)
		return zeros(Float64, 0, length(supplements)), Float64[], Float64[], Date[]
	end

	all_dates = outcome_agg.date

	# Build intake matrix for all outcome dates
	X = zeros(Float64, length(all_dates), length(supplements))

	if !isempty(sub_filtered)
		# Group by date and substance
		daily_intake = combine(groupby(sub_filtered, [:date, :substance]), nrow => :count)
		daily_intake.present = min.(daily_intake.count, 1)

		# Fill in X matrix
		date_idx_map = Dict(d => i for (i, d) in enumerate(all_dates))
		supp_idx_map = Dict(s => i for (i, s) in enumerate(supplements))

		for row in eachrow(daily_intake)
			if row.date ∈ keys(date_idx_map) && row.substance ∈ keys(supp_idx_map)
				X[date_idx_map[row.date], supp_idx_map[row.substance]] = row.present
			end
		end
	end

	y = Vector{Float64}(outcome_agg.outcome)
	counts = Vector{Float64}(outcome_agg.count)
	dates = outcome_agg.date

	return X, y, counts, dates
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
		"X" => X,
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
	X = Matrix{Float64}(reduce(hcat, data.X)')
	y = Vector{Float64}(data.y)
	counts = Vector{Float64}(data.counts)
	dates = Date.(data.dates)
	supplements = Vector{String}(data.supplements)

	return X, y, counts, dates, supplements
end

# Commands
function cmd_init(variable, kernel_type="matern")
	println("Loading data...")
	substances_df = load_substances()
	outcome_df = load_outcome_df(variable)

	for period in ["morning", "evening"]
		println("\n--- $(titlecase(period)) ---")
		supplements = period == "morning" ? MORNING_SUBSTANCES : EVENING_SUBSTANCES

		X, y, counts, dates = build_training_data(substances_df, outcome_df, supplements, variable)

		if isempty(X)
			println("ERROR: No training data for $variable ($period).")
			exit(1)
		end

		println("Tracking $(length(supplements)) supplements: $(join(supplements, ", "))")
		println("Built $(size(X, 1)) training observations ($(minimum(dates)) to $(maximum(dates)))")

		save_state(X, y, counts, dates, supplements, variable, period)

		println("Fitting GP (kernel: $kernel_type)...")
		posterior, fx = fit_gp(X, y, counts, kernel_type)
		save_model(posterior, variable, period)

		candidates = all_stacks(length(supplements))
		pred = posterior(RowVecs(candidates))
		μ = mean(pred)

		best_idx = argmax(μ)
		println("\nBest predicted stack: $(stack_label(supplements, candidates[best_idx, :]))")
		println("  Predicted: $(round(μ[best_idx], digits=1))")
		println("  State saved to $(state_path(variable, period))")
	end
end

function cmd_recommend(variable; cached=false, excluded=String[], kernel_type="matern")
	substances_df = cached ? nothing : load_substances()
	outcome_df = cached ? nothing : load_outcome_df(variable)

	results = Dict{String, String}()

	for period in ["morning", "evening"]
		supplements = period == "morning" ? MORNING_SUBSTANCES : EVENING_SUBSTANCES

		if cached
			posterior = load_model(variable, period)
			state = load_state(variable, period)
			if isnothing(posterior) || isnothing(state)
				println("ERROR: No cached $period model. Run without --cached first.")
				exit(1)
			end
			X, y, counts, dates, _ = state
		else
			X, y, counts, dates = build_training_data(substances_df, outcome_df, supplements, variable)
			posterior, fx = fit_gp(X, y, counts, kernel_type)
			save_model(posterior, variable, period)
		end

		candidates = all_stacks(length(supplements))
		candidates = filter_candidates(candidates, supplements, excluded)

		if isempty(candidates)
			println("ERROR: All $period stacks excluded.")
			exit(1)
		end

		best_idx, _ = thompson_sample(posterior, candidates)
		results[period] = stack_label(supplements, candidates[best_idx, :])
	end

	println("morning: $(results["morning"])")
	println("evening: $(results["evening"])")
end

function cmd_stats(variable, kernel_type="matern")
	substances_df = load_substances()
	outcome_df = load_outcome_df(variable)

	for period in ["morning", "evening"]
		supplements = period == "morning" ? MORNING_SUBSTANCES : EVENING_SUBSTANCES
		X, y, counts, dates = build_training_data(substances_df, outcome_df, supplements, variable)

		println("\nFitting $period GP on $(size(X, 1)) observations (kernel: $kernel_type)...")
		posterior, fx = fit_gp(X, y, counts, kernel_type)

		candidates = all_stacks(length(supplements))
		pred = posterior(RowVecs(candidates))
		μ = mean(pred)
		σ = std(pred)

		# Marginal effects
		println("\n" * "="^72)
		println("  $(titlecase(period)) — Marginal Supplement Effects")
		println("="^72)
		println("  $(rpad("Supplement", 40)) $(lpad("With", 7)) $(lpad("W/o", 7)) $(lpad("Effect", 7))")
		println("  $(repeat("-", 40)) $(repeat("-", 7)) $(repeat("-", 7)) $(repeat("-", 7))")

		for (i, supp) in enumerate(supplements)
			with_mask = candidates[:, i] .== 1
			without_mask = candidates[:, i] .== 0

			with_mean = mean(μ[with_mask])
			without_mean = mean(μ[without_mask])
			effect = with_mean - without_mean

			println("  $(rpad(supp, 40)) $(lpad(round(with_mean, digits=4), 7)) $(lpad(round(without_mean, digits=4), 7)) $(lpad(round(effect, digits=4, sigdigits=4), 7))")
		end

		# Top 10 stacks
		top10_idx = sortperm(μ, rev=true)[1:min(10, length(μ))]

		println("\n  $(titlecase(period)) — Top 10 Stacks")
		println("="^90)
		println("  $(rpad("#", 3)) $(rpad("Stack", 64)) $(lpad("Mean", 6)) $(lpad("Std", 6))")
		println("  $(repeat("-", 3)) $(repeat("-", 64)) $(repeat("-", 6)) $(repeat("-", 6))")

		for (rank, idx) in enumerate(top10_idx)
			label = stack_label(supplements, candidates[idx, :])
			println("  $(rpad(rank, 3)) $(rpad(label, 64)) $(lpad(round(μ[idx], digits=4), 6)) $(lpad(round(σ[idx], digits=4), 6))")
		end
		println("="^90)

		println("\n  Training: $(size(X, 1)) days ($(minimum(dates)) to $(maximum(dates)))")
	end
end

function cmd_update(variable, date_str, value)
	substances_df = load_substances()
	obs_date = Date(date_str, dateformat"yyyy-mm-dd")

	taken = Set(filter(r -> r.date == obs_date, substances_df).substance)

	for (period, supplements) in [("morning", MORNING_SUBSTANCES), ("evening", EVENING_SUBSTANCES)]
		state = load_state(variable, period)
		if isnothing(state)
			println("ERROR: No $period state file. Run init first.")
			exit(1)
		end

		X, y, counts, dates, _ = state

		vector = [s ∈ taken ? 1.0 : 0.0 for s in supplements]

		println("\n--- $(titlecase(period)) ---")
		println("Date:  $obs_date")
		println("Mood:  $value")
		println("Stack: $(stack_label(supplements, vector))")

		if obs_date ∈ dates
			idx = findfirst(==(obs_date), dates)
			X[idx, :] = vector
			y[idx] = value
			counts[idx] = 1
			println("Updating existing entry for $obs_date")
		else
			X = vcat(X, vector')
			y = vcat(y, value)
			counts = vcat(counts, 1)
			push!(dates, obs_date)
		end

		save_state(X, y, counts, dates, supplements, variable, period)
		println("Saved.")
	end
end

# CLI
const USAGE = """Supplement Stack Optimizer (GP + Thompson Sampling)

Usage:
    julia optimizer.jl [--cached] [--exclude sub1,sub2] [--kernel TYPE] [variable]
                                                    recommend (default: productivity)
    julia optimizer.jl stats [--kernel TYPE] [variable]
                                                    show effects & top stacks
    julia optimizer.jl update <date> <value> [variable]
                                                    log outcome for date (YYYY-MM-DD)
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
	elseif args[1] == "update"
		if length(args) < 3
			println("Usage: julia optimizer.jl update <date> <value> [variable]")
			exit(1)
		end
		variable = length(args) > 3 ? args[4] : "productivity"
		cmd_update(variable, args[2], parse(Float64, args[3]))
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
