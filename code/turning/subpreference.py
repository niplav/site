import random
import networkx as nx

import turn

def check_subprefs(subprefs, turnings):
	for s in subprefs:
		present_in=0
		for t in turnings:
			if set(s.nodes).issubset(set(t.nodes)) and set(s.edges).issubset(set(t.edges)):
				present_in=present_in+1
		if present_in==0:
			print(present_in, s.edges, g.edges)
		else:
			print(present_in/len(turnings), s.edges)


for i in range(0,5):
	graphs=turn.all_directed_graphs(i)
	for g in graphs:
		turnings=turn.turn_all(g)
		subprefs=turn.maximal_consistent_subgraphs(g)
		check_subprefs(subprefs, turnings)

lim=16
samples=1024

for i in range(5,lim):
	for j in range(0,samples):
		g=nx.generators.random_graphs.gnp_random_graph(i, 0.5, directed=True)
		for n in g.nodes:
			g.add_node(n, ind=n)
			if random.random()>=0.5:
				g.add_edge(n,n)
		subprefs=turn.maximal_consistent_subgraphs(g)
		turnings=turn.turn_all(g)
		check_subprefs(subprefs, turnings)
