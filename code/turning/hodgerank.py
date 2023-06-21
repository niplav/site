import numpy as np
import networkx as nx
import itertools as it

prefs1={0:np.array([5,3]),1:np.array([4,5]),2:np.array([3, np.nan]),3:np.array([5,2])}
prefs2={0:np.array([5,3]),1:np.array([4,5]),2:np.array([3, 1]),3:np.array([5,2])}
prefs3={0:np.array([4,np.nan,3]),1:np.array([3,4,np.nan]),2:np.array([np.nan, 3,4])}
prefs4={0:np.array([5,np.nan,3]),1:np.array([3,4,np.nan]),2:np.array([np.nan, 3,4])}
prefs5={0:np.array([5,np.nan,3]),1:np.array([3,4,np.nan]),2:np.array([1, 3,4])}
prefs6={0:np.array([1,1]),1:np.array([1,1]),2:np.array([1,1])}

# Maybe edges should be so that each edge has positive weight?

def positive_edges(prefs):
	edges=[(e[0], e[1], {"weight":np.nanmean(prefs[e[0]]-prefs[e[1]])}) for e in it.combinations(prefs.keys(), 2)]
	edges=[e if e[2]['weight']>=0 else (e[1], e[0], {"weight": -e[2]['weight']}) for e in edges]
	return edges

def prefgraph(prefs):
	g=nx.DiGraph()
	g.add_nodes_from(list(prefs.keys()))
	edges=positive_edges(prefs)
	g.add_edges_from(edges)

	return g

def decompose(g, prefs):
	edges=positive_edges(prefs)
	f=np.array([e[2]['weight'] for e in edges])
	W=np.diag([np.sum(~np.isnan(prefs[e[0]]-prefs[e[1]])) for e in it.combinations(prefs.keys(), 2)])

	origins=np.zeros((len(g.edges), len(g.nodes)))

	c=0
	for e in g.edges:
		sign=np.sign(g[e[0]][e[1]]['weight'])
		origins[c][e[0]]=sign*-1
		origins[c][e[1]]=sign*1
		c=c+1

	s=-np.linalg.pinv(origins.T@W@origins)@origins.T@W@f
	return s,f,W,origins

def hodgerank(prefs):
	g=prefgraph(prefs)
	return decompose(g, prefs)
