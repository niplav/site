using LinearAlgebra
using Plots
using StatsPlots
using Graphs
using Statistics

# Constants
const DEFAULT_THRESHOLD = 0.5
const SPARSE_THRESHOLD = 0.25
const SEM_SIZE_RANGE = 4:4:52
const SAMPLE_POWERS = 6:12
const DEFAULT_SEM_SAMPLES = 500
const DEFAULT_INPUT_SAMPLES = 500
const CORRELATION_EXPERIMENTS = 500
const CORRELATION_SEM_SIZE = 48
const CORRELATION_INNER_SAMPLES = 1000
const SAMPLES_SEM_SIZE = 36

# Constants for causal hierarchy analysis
const HIERARCHY_SEM_SAMPLES = 200
const HIERARCHY_INNER_SAMPLES = 4000
const HIERARCHY_SIZE_RANGE = 4:2:52

# Plotting constants

const DEFAULT_DPI = 140

struct LinearSEM
	g::SimpleDiGraph{Int64}
	coefficients::Dict{Edge{Int64}, Float64}
end

### Small helper functions

triangular_number(n::Int)::Int = return (n^2 + n) ÷ 2

has_causal_path(g::SimpleDiGraph, source::Int, target::Int)::Bool = (sum(adjacency_matrix(g)^k for k in 1:nv(g))[source, target] > 0)

is_intervention_identifiable(sem::LinearSEM, x::Int, y::Int)::Bool = has_edge(sem.g, x, y) || has_causal_path(sem.g, x, y)

function is_counterfactual_identifiable(sem::LinearSEM, x::Int, y::Int)::Bool
	is_intervention_identifiable(sem, x, y) || return false
	relevant_edges = [e for e in edges(sem.g) if e.src == x || e.dst == y]
	isempty(relevant_edges) || all(c >= -0.1 for c in [sem.coefficients[e] for e in relevant_edges])
end

### Causal non-correlations functions

function random_linear_sem(n::Int, threshold::Float64=DEFAULT_THRESHOLD)::LinearSEM
	n > 0 || throw(ArgumentError("Number of variables must be positive"))
	0.0 <= threshold <= 1.0 || throw(ArgumentError("Threshold must be between 0 and 1"))

	edges_to_add = [(i,j) for i in 1:n for j in (i+1):n if rand() < threshold]

	g = DiGraph(n)
	coefficients = Dict(Edge(i,j) => randn() for (i,j) in edges_to_add)

	for (i,j) in edges_to_add
	    add_edge!(g, i, j)
	end

	@assert !is_cyclic(g)
	return LinearSEM(g, coefficients)
end

function calculate_sem_values(sem::LinearSEM, input_values::Dict{Int, Float64})::Dict{Int, Float64}
	n = nv(sem.g)
	A = adjacency_matrix(sem.g)
	W = zeros(n, n)
	for edge in edges(sem.g)
		W[src(edge), dst(edge)] = sem.coefficients[edge]
	end

	input_nodes = [i for i in 1:n if indegree(sem.g, i) == 0]
	x = zeros(n)
	for node in input_nodes
		x[node] = get(input_values, node, 0.0)
	end

	result_vec = (I - W') \ x
	return Dict(i => result_vec[i] for i in 1:n)
end

function correlations(sem::LinearSEM, inner_samples::Int)::Matrix{Float64}
	n = nv(sem.g)
	input_nodes = findall(i -> indegree(sem.g, i) == 0, 1:n)

	# Generate all samples at once
	inputs = randn(inner_samples, length(input_nodes))
	results = hcat([calculate_sem_values(sem, Dict(zip(input_nodes, inputs[i,:]))) |>
                       vals -> [vals[i] for i in 1:n]
                       for i in 1:inner_samples]...)'

	cor_matrix = cor(results)
	cor_matrix[diagind(cor_matrix)] .= 0
	return abs.(cor_matrix)
end

function influences(sem::LinearSEM)::Matrix{Bool}
	return Matrix(Bool.(transpose(adjacency_matrix(transitiveclosure(sem.g)))))
end

function different_cors(sem::LinearSEM, inner_samples::Int)::Tuple{Matrix{Float64}, Matrix{Float64}}
	correlation=correlations(sem, inner_samples)
	influence=influences(sem)
	not_influence=tril(.!(influence), -1)
	non_causal_cors=not_influence.*correlation
	causal_cors=influence.*correlation
	return non_causal_cors, causal_cors
end

function misclassifications(sem::LinearSEM, inner_samples::Int)::Int
	non_causal_cors, causal_cors=different_cors(sem, inner_samples)
	return sum((causal_cors .!= 0) .& (causal_cors .< mean(non_causal_cors)))
end

function misclassified_absence_mc(n::Int, outer_samples::Int, inner_samples::Int)::Vector{Int}
	return [misclassifications(random_linear_sem(n, SPARSE_THRESHOLD), inner_samples) for i in 1:outer_samples]
end

function collect_correlation_data(n_experiments::Int=CORRELATION_EXPERIMENTS, sem_size::Int=CORRELATION_SEM_SIZE,
                                  inner_samples::Int=CORRELATION_INNER_SAMPLES)::Tuple{Vector{Float64}, Vector{Float64}}
	results = [different_cors(random_linear_sem(sem_size, SPARSE_THRESHOLD), inner_samples)
                   for _ in 1:n_experiments]

	non_causal = vcat([filter(>(0), nc) for (nc, _) in results]...)
	causal = vcat([filter(>(0), c) for (_, c) in results]...)

	return non_causal, causal
end

### Pearl Hierarchy

function analyze_hierarchy_identifiability(sem::LinearSEM, correlation_threshold::Float64=0.1,
                                           inner_samples::Int=HIERARCHY_INNER_SAMPLES)::Dict{Symbol, Float64}
	n = nv(sem.g)
	corr_matrix = correlations(sem, inner_samples)

	# Create index arrays for all pairs (i,j) where i≠j
	pairs = [(i,j) for i in 1:n for j in 1:n if i != j]

	# Vectorized checks
	assoc_valid = [corr_matrix[i,j] > correlation_threshold for (i,j) in pairs]
	interv_valid = [is_intervention_identifiable(sem, i, j) for (i,j) in pairs]
	counter_valid = [is_counterfactual_identifiable(sem, i, j) for (i,j) in pairs]

	total = length(pairs)
	Dict(:association => sum(assoc_valid)/total,
             :intervention => sum(interv_valid)/total,
             :counterfactual => sum(counter_valid)/total)
end

hierarchy_identifiability_mc(n::Int, outer_samples::Int, inner_samples::Int) =
	reduce((acc, _) -> begin
		props = analyze_hierarchy_identifiability(random_linear_sem(n, SPARSE_THRESHOLD), 0.1, inner_samples)
		Dict(k => push!(get(acc, k, Float64[]), v) for (k,v) in props)
	end, 1:outer_samples, init=Dict{Symbol, Vector{Float64}}())

function run_hierarchy_experiments(size_range::StepRange{Int64, Int64}=HIERARCHY_SIZE_RANGE,
                                   sem_samples::Int=HIERARCHY_SEM_SAMPLES,
                                   inner_samples::Int=HIERARCHY_INNER_SAMPLES)
	results = Dict{Int, Dict{Symbol, Vector{Float64}}}()
	Threads.@threads for n in collect(size_range)
		println("Processing hierarchy analysis for SEM size: $n")
		results[n] = hierarchy_identifiability_mc(n, sem_samples, inner_samples)
	end
	results
end

function run_size_experiments(size_range::StepRange{Int64, Int64}=SEM_SIZE_RANGE, sem_samples::Int=DEFAULT_SEM_SAMPLES,
                              input_samples::Int=DEFAULT_INPUT_SAMPLES)::Dict{Int, Vector{Int}}
	results=Dict{Int, Vector{Int}}()
	Threads.@threads for i in size_range
		println("Processing SEM size: $i")
		results[i]=misclassified_absence_mc(i, sem_samples, input_samples)
	end
	return results
end

function run_sample_experiments(sem_size::Int=SAMPLES_SEM_SIZE, sample_powers::UnitRange{Int64}=SAMPLE_POWERS)::Dict{Int, Vector{Int}}
	more_samples=Dict{Int, Vector{Int}}()
	input_samples_range=2 .^ sample_powers
	sem=random_linear_sem(sem_size, SPARSE_THRESHOLD)

	Threads.@threads for input_sample in input_samples_range
		println("Processing sample size: $input_sample")
		more_samples[input_sample]=[misclassifications(sem, input_sample) for i in 1:DEFAULT_SEM_SAMPLES]
	end
	return more_samples
end

### Plotting

function plot_correlations(non_causal_cors::Vector{Float64}, causal_cors::Vector{Float64}, filename::String="correlations.png")
	cors_plot=plot(dpi=DEFAULT_DPI, xlabel="Correlation", ylabel="Density", legend=:topleft)
	density!(cors_plot, non_causal_cors, c=:red, label="Non-causal correlations")
	density!(cors_plot, causal_cors, c=:blue, label="Causal correlations")
	savefig(cors_plot, filename)
	return cors_plot
end

function plot_summaries(results::Dict{Int, Vector{Int}}, filename::String="summaries.png")
	sorted_results=sort(results)
	keys_vec=[key for (key, _) in sorted_results]
	result_means=[mean(values) for (_, values) in sorted_results]
	result_props=[mean(values)/triangular_number(key) for (key, values) in sorted_results]

	p1=plot(keys_vec, result_means, title="Mean Causal Non-Correlations", legend=false, c=:red)
	p2=plot(keys_vec, result_props, title="Proportion Causal Non-Correlations", legend=false, c=:blue)
	combined_plot=plot(p1, p2, layout=(1, 2), size=(900, 600))
	savefig(combined_plot, filename)
	return combined_plot
end

function plot_hierarchy_scaling(results::Dict{Int, Dict{Symbol, Vector{Float64}}}, filename::String="hierarchy_scaling.png")
	sorted_keys = sort(collect(keys(results)))
	levels = [:association, :intervention, :counterfactual]
	colors = [:blue, :red, :green]

	# Extract means and stds in one go
	data = [
		(level =>
		([mean(results[k][level]) for k in sorted_keys],
		[std(results[k][level]) for k in sorted_keys]))
		for level in levels
		]

	hierarchy_plot = plot(dpi=DEFAULT_DPI, xlabel="Number of Variables",
                              ylabel="Proportion Identifiable", title="Causal Hierarchy Identifiability Scaling",
                              legend=:topright)

	for (i, (level, (means, stds))) in enumerate(data)
             plot!(hierarchy_plot, sorted_keys, means, ribbon=stds,
                   label=string(level), linewidth=2, c=colors[i], alpha=0.7)
	end

	savefig(hierarchy_plot, filename)
	hierarchy_plot
end

function plot_hierarchy_detailed(results::Dict{Int, Dict{Symbol, Vector{Float64}}}, filename::String="hierarchy_detailed.png")
	sorted_keys = sort(collect(keys(results)))
	levels = [:association, :intervention, :counterfactual]
	colors = [:blue, :red, :green]
	titles = ["Association Identifiability", "Intervention Identifiability", "Counterfactual Identifiability"]

	plots = [plot(sorted_keys, [mean(results[k][level]) for k in sorted_keys],
                 title=titles[i], xlabel="Variables", ylabel="Proportion",
                 legend=false, c=colors[i], linewidth=2)
                 for (i, level) in enumerate(levels)]

	combined_plot = plot(plots..., layout=(1, 3), size=(1200, 400))
	savefig(combined_plot, filename)
	combined_plot
end

function plot_misclassifications(results::Dict{Int, Vector{Int}}, filename::String="misclassifications.png")
	sorted_results=sort(results)
	max_key=maximum(keys(results))
	max_value=maximum(results[max_key])

	non_corrs_plot=plot(legend=:topright, dpi=DEFAULT_DPI, xlabel="Number of causal non-correlations",
                            ylabel="Density", palette=palette([:orange, :blue], length(results)))

	for (key, values) in sorted_results
		density!(non_corrs_plot, values, label="$key variables in SEM", linewidth=2,
			yscale=:log10, ylims=(0.00001, 10), xlims=(-1, max_value))
	end

	savefig(non_corrs_plot, filename)
	return non_corrs_plot
end

function plot_sample_misclassifications(more_samples::Dict{Int, Vector{Int}}, filename::String="misclassifications_samples.png")
	samples_plot=plot(legend=:topleft, dpi=DEFAULT_DPI, xlabel="Number of causal non-correlations",
                          ylabel="Density", palette=palette([:orange, :blue], length(more_samples)))
	for (key, values) in sort(more_samples, rev=true)
		density!(samples_plot, values, label="$key samples from each SEM", linewidth=2)
	end
	savefig(samples_plot, filename)
	return samples_plot
end

function run_all_experiments()
	println("Collecting correlation data...")
	non_causal_cors, causal_cors=collect_correlation_data()
	plot_correlations(non_causal_cors, causal_cors)

	println("Running size experiments...")
	size_results=run_size_experiments()
	plot_summaries(size_results)
	plot_misclassifications(size_results)

	println("Running sample experiments...")
	sample_results=run_sample_experiments()
	lot_sample_misclassifications(sample_results)

	println("Running causal hierarchy experiments...")
	hierarchy_results = run_hierarchy_experiments()
	plot_hierarchy_scaling(hierarchy_results)
	plot_hierarchy_detailed(hierarchy_results)
end

run_all_experiments()
