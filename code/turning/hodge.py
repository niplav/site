import numpy as np
import networkx as nx
import itertools as it

def prefgraph(prefs):
	g=nx.DiGraph()
	g.add_nodes_from(list(prefs.keys()))
	edges=positive_edges(prefs)
	g.add_edges_from(edges)

	return g

def weightgraph(graph):
	g=graph.copy()
	for e in g.edges:
		g[e[0]][e[1]]['weight']=1
		g[e[0]][e[1]]['n']=1

	return g

def positive_edges(prefs):
	edges=[]
	for e in it.combinations(prefs.keys(), 2):
		if np.all(np.isnan(prefs[e[0]]-prefs[e[1]])):
			weight=np.nan
		else:
			weight=np.nanmean(prefs[e[0]]-prefs[e[1]])

		n=np.sum(~np.isnan(prefs[e[0]]-prefs[e[1]]))
		if np.isnan(weight):
			continue
		elif weight>=0:
			edges.append((e[0], e[1], {'weight': weight, 'n': n}))
		else:
			edges.append((e[1], e[0], {'weight': -weight, 'n': n}))
	return edges

def decompose(g):
	f=np.array([g[e[0]][e[1]]['weight'] for e in g.edges])
	W=np.diag([g[e[0]][e[1]]['n'] for e in g.edges])

	idx=dict()
	nodes=list(g.nodes)
	for i in range(0, len(nodes)):
		idx[nodes[i]]=i

	origins=np.zeros((len(g.edges), len(g.nodes)))
	c=0
	for e in g.edges:
		sign=np.sign(g[e[0]][e[1]]['weight'])
		if np.isnan(sign):
			sign=0
		origins[c][idx[e[0]]]=sign*-1
		origins[c][idx[e[1]]]=sign
		c=c+1

	try:
		s=-np.linalg.pinv(origins.T@W@origins)@origins.T@W@f
	except LinAlgError:
		s=np.zeros(len(list(g.nodes)))

	values=dict()

	for option in idx.keys():
		values[option]=s[idx[option]]

	return values

def potential_to_graph(potential):
	res=nx.DiGraph()
	res.add_nodes_from(potential.keys())

	for x, y in it.combinations(potential.keys(), 2):
		if np.isclose(potential[x], potential[y]):
			res.add_edges_from([(x,y, {'weight': 0}), (y,x, {'weight': 0})])
		elif potential[x]>potential[y]:
			res.add_edges_from([(x,y, {'weight': potential[x]-potential[y]})])
		else:
			res.add_edges_from([(y,x, {'weight': potential[y]-potential[x]})])

	return res

def hodgerank(prefs):
	g=prefgraph(prefs)
	return decompose(g)

def hodgeresolve(graph):
	potential=decompose(graph)

	return potential_to_graph(potential)
