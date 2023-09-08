import hodge

import networkx as nx
import itertools as it

def ontological_shift(graph, s, resolver):
	incrisis=nx.DiGraph()
	for e in graph.edges():
		for n1, coeff1 in s[e[0]]:
			for n2, coeff2 in s[e[1]]:
				incrisis.add_nodes_from([n1, n2])
				curt=0
				if (n1, n2) in incrisis.edges():
					curt=incrisis.edges()[(n1, n2)]['weight']
				newt=curt+coeff1*coeff2*graph.edges[(e[0], e[1])]['weight']
				incrisis.add_edges_from([(n1, n2, {'weight': newt, 'n': 1})])
	res=resolver(incrisis)
	return res


def noresolver(g):
	return g

def hodgewrap(g):
	for e in g.edges:
		g.add_edges_from([(e[0], e[1], {'n': 1})])
	return hodge.hodgeresolve(g)

animals=nx.DiGraph()
animals.add_edges_from([('L', 'A', {'w': 1}), ('A', 'W', {'w': 1}), ('L', 'W', {'w': 2})])

linn=dict()
linn['L']=[('M', 0.5), ('I', 0.5)]
linn['A']=[('B', 0.45), ('I', 0.45), ('M', 0.1)]
linn['W']=[('F', 0.9), ('M', 0.1)]
