using TSne, UMAP, Plots

datapoints=1000
dims=200

data=rand(datapoints, dims)

reduced=tsne(data)

tsne_plot=scatter(reduced[:,1],reduced[:,2], label="t-SNE")
savefig(tsne_plot, "tsne_plot.png")

reduced_umap=umap(transpose(data))

umap_plot=scatter(reduced_umap[1,:],reduced_umap[2,:], color=:red, label="UMAP")
savefig(umap_plot, "umap_plot.png")

reduced_5=tsne(data, 2, 0, 100, 5.0)
tsne_5_plot=scatter(reduced_5[:,1],reduced_5[:,2], color=:green, label="t-SNE, perplexity=5")
savefig(tsne_5_plot, "tsne_5_plot.png")

tsne_plots=[]
umap_plots=[]

for dims in datapoints*[0.25, 0.5, 1, 2, 4, 8, 16, 32, 64]
	data=rand(datapoints, Int(dims))

	print(datapoints, dims)

	reduced_moredims=tsne(data)
	tsne_moredims_plot=scatter(reduced_moredims[:,1],reduced_moredims[:,2], color=:yellow, label=string(Int(dims))*" dimensions")
	push!(tsne_plots, tsne_moredims_plot)
	#savefig(tsne_moredims_plot, "tsne_moredims_"*string(Int(dims))*".png")

	reduced_moredims_umap=umap(transpose(data))
	umap_moredims_plot=scatter(reduced_moredims[:,1],reduced_moredims[:,2], color=:purple, label=string(Int(dims))*" dimensions")
	push!(umap_plots, umap_moredims_plot)
	#savefig(umap_moredims_plot, "umap_moredims_"*string(Int(dims))*".png")
end

tsne_moredims_plot=plot(tsne_plots[1], tsne_plots[2], tsne_plots[3], tsne_plots[4], tsne_plots[5], tsne_plots[6], tsne_plots[7], tsne_plots[8], tsne_plots[9], layout=(3,3), size=(850, 850))
savefig(tsne_moredims_plot, "tsne_moredims.png")

umap_moredims_plot=plot(umap_plots[1], umap_plots[2], umap_plots[3], umap_plots[4], umap_plots[5], umap_plots[6], umap_plots[7], umap_plots[8], umap_plots[9], layout=(3,3), size=(850, 850))
savefig(umap_moredims_plot, "umap_moredims.png")
