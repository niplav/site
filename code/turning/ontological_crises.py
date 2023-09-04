import networkx as nx
import itertools as it

def ontological_shift(graph, s, resolver):
	incrisis=nx.DiGraph()
	for e in graph.edges():
		for n1, coeff1 in s(e[0]):
			for n2, coeff2 in s(e[1]):
				incrisis.add_nodes_from([n1, n2])
				curt=0
				if (n1, n2) in incrisis.edges():
					curt=incrisis.edges()[(n1, n2)]['weight']
				newt=curt+coeff1*coeff2*graph.edges[(e[0], e[1])]['w']
				incrisis.add_edges_from([(n1, n2, {'weight': newt, 'n': 1})])
	res=resolver(incrisis)
	return res

animals=nx.DiGraph()
animals.add_edges_from([('L', 'A', {'w': 1}), ('A', 'W', {'w': 1}), ('L', 'W', {'w': 2})])

def linn(n):
	if n=='L':
		return [('M', 0.5), ('I', 0.5)]
	elif n=='A':
		return [('B', 0.45), ('I', 0.45), ('M', 0.1)]
	elif n=='W':
		return [('F', 0.9), ('M', 0.1)]
