import random
import networkx as nx

import turn

def check_largest(turnings, g):
	largest=turn.get_largest(g)
	for t in turnings:
		if not turn.is_largest(largest, t):
			print(str(largest)+","+str(g.edges))
		else:
			print("has largest, got preserved", str(largest)+","+str(g.edges))

#for i in range(0,5):
#	graphs=turn.all_directed_graphs(i)
#	for g in graphs:
#		if turn.get_largest(g)==None:
#			continue
#		turnings=turn.turn_all(g)
#		check_largest(turnings, g)

lim=16
samples=256

for i in range(4,lim):
	for j in range(0,samples):
		g=nx.generators.random_graphs.gnp_random_graph(i, 0.5, directed=True)
		for n in g.nodes:
			g.add_node(n, ind=n)
			if random.random()>=0.5:
				g.add_edge(n,n)
		g.add_node('a', ind=len(g.nodes()))
		for n in g.nodes:
			if n!='a':
				g.add_edge('a', n)
		if turn.get_largest(g)==None:
			continue
		turnings=turn.turn_all(g)
		check_largest(turnings, g)
