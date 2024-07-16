using LinearAlgebra
using Plots
using StatsPlots
using Graphs
using Statistics

struct LinearSEM
	g::SimpleDiGraph{Int64}
	coefficients::Dict
end

function random_linear_sem(n::Int, threshold=0.5)
	g=DiGraph(n)
	for i in 1:n
		for j in (i+1):n
			if rand() < threshold
				add_edge!(g, i, j)
			end
		end
	end
	@assert !is_cyclic(g)
	coefficients=Dict()

	for edge in edges(g)
		coefficients[edge]=randn()
	end

	return LinearSEM(g, coefficients)
end

function calculate_sem_values(sem::LinearSEM, input_values::Dict)
	sorted_nodes=topological_sort_by_dfs(sem.g)

	# Initialize values dictionary with input variables
	values=copy(input_values)

	for node in sorted_nodes
		if !haskey(values, node) # If the node's value hasn't been calculated yet
			incoming_edges=inneighbors(sem.g, node)
			values[node]=sum([values[source_node] * sem.coefficients[Edge(source_node, node)] for source_node in incoming_edges])
		end
	end
	return values
end

function correlations(sem::LinearSEM, inner_samples::Int)
	n=size(vertices(sem.g), 1)
	input_nodes=[node for node in vertices(sem.g) if indegree(sem.g, node) == 0]
	results=Matrix{Float64}(undef, inner_samples, n) # Preallocate results matrix

	for i in 1:inner_samples
		input_values=Dict([node => randn() for node in input_nodes])
		sem_values=calculate_sem_values(sem, input_values)
		sem_value_row=reshape(collect(values(sort(sem_values))), 1, :)
		results[i, :]=sem_value_row
	end

	cor_matrix=cor(results)
	cor_matrix[diagind(cor_matrix)].=0
	return abs.(cor_matrix)
end

function influences(sem::LinearSEM)
	return Matrix(Bool.(transpose(adjacency_matrix(transitiveclosure(sem.g)))))
end

function different_cors(sem::LinearSEM, inner_samples::Int)
	correlation=correlations(sem, inner_samples)
	influence=influences(sem)

	not_influence=tril(.!(influence), -1)

	non_causal_cors=not_influence.*correlation
	causal_cors=influence.*correlation

	return non_causal_cors, causal_cors
end

function misclassifications(sem::LinearSEM, inner_samples::Int)
	non_causal_cors, causal_cors=different_cors(sem, inner_samples)

	return sum((causal_cors .!= 0) .& (causal_cors .< mean(non_causal_cors)))
end

function misclassified_absence_mc(n::Int, outer_samples::Int, inner_samples::Int)
	return [misclassifications(random_linear_sem(n, 0.25), inner_samples) for i in 1:outer_samples]
end

vnon_causal_cors=[]
vcausal_cors=[]

for i in 1:100
	sem=random_linear_sem(48, 0.25)
	non_causal_cors, causal_cors=different_cors(sem, 10000)
	vnon_causal_cors=vcat(vnon_causal_cors, filter(e->e>0, non_causal_cors))
	vcausal_cors=vcat(vcausal_cors, filter(e->e>0, causal_cors))
end

cors_plot=plot(dpi=140, xlabel="Correlation", ylabel="Density", legend=:topleft)
density!(cors_plot, vnon_causal_cors, c=:red, label="Non-causal correlations")
density!(cors_plot, vcausal_cors, c=:blue, label="Causal correlations")

savefig(cors_plot, "correlations.png")

# TODO: move plots to their own functions

results=Dict{Int, Array{Int, 1}}()

sem_samples=400
inputs_samples=10000
upperlim=52
stepsize=4
#sem_samples=100
#inputs_samples=1000

Threads.@threads for i in 4:stepsize:upperlim
	println(i)
	results[i]=misclassified_absence_mc(i, sem_samples, inputs_samples)
end

result_means=[mean(values) for (key, values) in sort(results)]
result_props=[mean(values)/((key^2+key)/2) for (key, values) in sort(results)]

keys = [key for (key, values) in sort(results)]

more_samples=Dict{Int, Array{Int, 1}}()

samples_test_size=20
sem_samples=400
#samples_test_size=10
#sem_samples=10
inputs_samples=2 .^ (6:16)

Threads.@threads for inputs_sample in inputs_samples
	println(inputs_sample)
	more_samples[inputs_sample]=misclassified_absence_mc(samples_test_size, sem_samples, inputs_sample)
end

# Create subplots
p1 = plot(keys, result_means, title="Mean Causal Non-Correlations", legend=false, c=:red)
p2 = plot(keys, result_props, title="Proportion Causal Non-Correlations", legend=false, c=:blue)

combined_plot = plot(p1, p2, layout=(1, 2), size=(900, 600))

savefig(combined_plot, "summaries.png")

non_corrs_plot=plot(legend=:topright, dpi=140, xlabel="Number of causal non-correlations", ylabel="Density",
	palette=palette([:orange, :blue], length(results)))

for (key, values) in sort(results)
	density!(non_corrs_plot, values, label="$key variables in SEM", linewidth=2,
		yscale=:log10, ylims=(0.00001, 10), xlims=(-1, maximum(results[upperlim])))
end

savefig(non_corrs_plot, "misclassifications.png")

samples_plot=plot(legend=:topleft, dpi=140, xlabel="Number of causal non-correlations", ylabel="Density",
	palette=palette([:orange, :blue], length(more_samples)))
for (key, values) in sort(more_samples, rev=true)
	density!(samples_plot, values, label="$key samples from each SEM", linewidth=2)
end

savefig(samples_plot, "misclassifications_samples.png")
