using LinearAlgebra
using Plots
using StatsPlots
using Graphs
using Statistics

function generate_random_linear_sem(n::Int)
	# Create a random DAG
	g=DiGraph(n)
	for i in 1:n
		for j in (i+1):n
			if rand() < 0.5 # Adjust this threshold to control density
				add_edge!(g, i, j)
			end
		end
	end
	@assert !is_cyclic(g)
	coefficients=Dict()
	for edge in edges(g)
		coefficients[edge]=randn()
	end

	return g, coefficients
end

function calculate_sem_values(sem::DiGraph, coefficients::Dict, input_values::Dict)
	sorted_nodes=topological_sort_by_dfs(sem)

	# Initialize values dictionary with input variables
	values=copy(input_values)

	for node in sorted_nodes
		if !haskey(values, node) # If the node's value hasn't been calculated yet
			incoming_edges=inneighbors(sem, node)
			values[node]=sum([values[source_node] * coefficients[Edge(source_node, node)] for source_node in incoming_edges])
		end
	end
	return values
end

function correlation_in_sem(sem::DiGraph, coefficients::Dict, inner_samples::Int)
	n=size(vertices(sem), 1)
	input_nodes=[node for node in vertices(sem) if indegree(sem, node) == 0]
	results=Matrix{Float64}(undef, inner_samples, n) # Preallocate results matrix
	for i in 1:inner_samples
		input_values=Dict([node => randn() for node in input_nodes])
		sem_values=calculate_sem_values(sem, coefficients, input_values)
		sem_value_row=reshape(collect(values(sort(sem_values))), 1, :)
		results[i, :]=sem_value_row
	end

	correlations=cor(results)

	for i in 1:size(correlations, 1)
		correlations[i, i]=0
	end
	return abs.(correlations)
end

function misclassifications(sem::DiGraph, coefficients::Dict, inner_samples::Int)
	correlations=correlation_in_sem(sem, coefficients, inner_samples)

	influence=Matrix(Bool.(transpose(adjacency_matrix(transitiveclosure(sem)))))
	not_influence=tril(.!(influence), -1)

	non_causal_correlations=not_influence.*correlations
	causal_correlations=influence.*correlations

	return sum((causal_correlations .!= 0) .& (causal_correlations .< maximum(non_causal_correlations)))
end

function misclassified_absence_mc(n::Int, outer_samples::Int, inner_samples::Int)
	return [misclassifications(generate_random_linear_sem(n)..., inner_samples) for i in 1:outer_samples]
end

results=Dict{Int, Array{Int, 1}}()

sem_samples=200
inputs_samples=20000

Threads.@threads for i in 4:16
	println(i)
	results[i]=misclassified_absence_mc(i, sem_samples, inputs_samples)
end

result_means=[mean(values) for (key, values) in sort(results)]
result_props=[mean(values)/((key^2+key)/2) for (key, values) in sort(results)]

keys = [key for (key, values) in sort(results)]

# Create subplots
p1 = plot(keys, result_means, title="Mean misclassified", legend=false)
p2 = plot(keys, result_props, title="Proportion misclassified", legend=false)

# Combine subplots into a single plot with 3 rows and 1 column
combined_plot = plot(p1, p2, layout=(1, 2), size=(1200, 600))

# Display the combined plot
savefig(combined_plot, "summaries.png")

non_corrs_plot=plot(legend=:topright, dpi=140, xlabel="Number of causal non-correlations", ylabel="Density",
	palette=palette([:orange, :blue], length(results)))
for (key, values) in sort(results, rev=true)
	density!(non_corrs_plot, values, label="$key variables in SEM", linewidth=2)
end

savefig(non_corrs_plot, "misclassifications.png")

more_samples=Dict{Int, Array{Int, 1}}()

samples_test_size=12
sem_samples=100
inputs_samples=2 .^(6:17)

for inputs_sample in inputs_samples
	println(inputs_sample)
	more_samples[inputs_sample]=misclassified_absence_mc(samples_test_size, sem_samples, inputs_sample)
end

samples_plot=plot(legend=:topleft, dpi=140, xlabel="Number of causal non-correlations", ylabel="Density",
	palette=palette([:orange, :blue], length(more_samples)))
for (key, values) in sort(more_samples, rev=true)
	density!(samples_plot, values, label="$key samples from each SEM", linewidth=2)
end

savefig(samples_plot, "misclassifications_samples.png")
