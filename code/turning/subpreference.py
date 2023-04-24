import random
import networkx as nx

import turn

for i in range(0,5):
	graphs=turn.all_directed_graphs(i)
	for g in graphs:
		turnings=turn.turn_all(g)
		subprefs=turn.maximal_consistent_subgraphs(g)
		for s in subprefs:
			present_in=0
			for t in turnings:
				if set(s.nodes).issubset(set(t.nodes)) and set(s.edges).issubset(set(t.edges)):
					print(s.edges, t.edges)
		print('{0},{1},"{2}"'.format(i, len(turn.turn_all(g)), g.edges))

lim=16
samples=65536

for i in range(5,lim):
	for j in range(0,samples):
		g=nx.generators.random_graphs.gnp_random_graph(i, 0.5, directed=True)
		for n in g.nodes:
			g.add_node(n, ind=n)
			if random.random()>=0.5:
				g.add_edge(n,n)
		print('{0},{1},"{2}"'.format(i, len(turn.turn_all(g)), g.edges))
