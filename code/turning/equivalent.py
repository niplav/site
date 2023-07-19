import random
import networkx as nx

import turn

def algos_equivalent(g):
	turnings=turn.turn_all(g)
	stepwises=turn.stepwise(g)

	if len(turnings)!=len(stepwises):
		print(g.edges, g.nodes, "unequal number of resolutions")
		exit(1)

	for t in turnings:
		present=False
		for s in stepwises:
			if turn.gequals(t, s):
				present=True
				break
		if not present:
			print(g.edges, g.nodes, "not present in stepwises: ", t.edges)
			exit(1)

for i in range(0,5):
	print("checking for", i)
	graphs=turn.all_directed_graphs(i)
	for g in graphs:
		algos_equivalent(g)

print("checking for 5")

turn.map_5_graphs(algos_equivalent)

lim=16
samples=65536

for i in range(6,lim):
	print("checking for ", i)
	for j in range(0,samples):
		g=nx.generators.random_graphs.gnp_random_graph(i, 0.5, directed=True)
		for n in g.nodes:
			g.add_node(n, ind=n)
			if random.random()>=0.5:
				g.add_edge(n,n)
			algos_equivalent(g)
