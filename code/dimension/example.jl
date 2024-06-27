using TSne, UMAP, Plots

data=rand(10000, 2000)

reduced=tsne(data)
reduced_5=tsne(data, 2, 0, 1000, 5.0)

reduced_umap=umap(transpose(data))

scatter(reduced[:,1],reduced[:,2])
scatter(reduced_umap[1,:],reduced_umap[2,:])
