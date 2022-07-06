import math
import networkx as nx
import itertools as it

def turn(W, G):
	mindist=math.inf
	for L in it.permutations(W):
		L=list(L)
		LG=nx.DiGraph()
		for i in range(0, len(W)):
			LG.add_node(W[i], ind=i)
		# The transitive closure over this particular path graph
		# Simplify to nx.algorithms
		for i in range(0, len(L)-1):
			LG.add_edge(L[i], L[i+1])
		LG=nx.algorithms.dag.transitive_closure(LG)
		print(LG.nodes, LG.edges)
		# Compute the graph edit distance, disabling node insertion/deletion/substition and edge substitution
		oas=lambda x: 1
		oah=lambda x: 10e10
		nm=lambda x, y: x['ind']==y['ind']
		em=lambda x, y: True
		dist=nx.algorithms.similarity.graph_edit_distance(G, LG, node_match=nm, edge_match=em, node_del_cost=oah, node_ins_cost=oah, edge_ins_cost=oas, edge_del_cost=oas)
		print(dist)
		if dist<mindist:
			R=LG
			mindist=dist
	return R

def turn_all(W, G):
	R=set()
	mindist=math.inf
	for L in it.permutations(W):
		L=list(L)
		LG=nx.DiGraph()
		for i in range(0, len(W)):
			LG.add_node(W[i], ind=i)
		for i in range(0, len(L)-1):
			LG.add_edge(L[i], L[i+1])
		LG=nx.algorithms.dag.transitive_closure(LG)
		# Compute the graph edit distance, disabling node insertion/deletion/substition and edge substitution
		oas=lambda x: 1
		oah=lambda x: 10e10
		nm=lambda x, y: x['ind']==y['ind']
		em=lambda x, y: True
		dist=nx.algorithms.similarity.graph_edit_distance(G, LG, node_match=nm, edge_match=em, node_del_cost=oah, node_ins_cost=oah, edge_ins_cost=oas, edge_del_cost=oas)
		if dist<mindist:
			R=set([LG])
			mindist=dist
		elif dist==mindist:
			R.add(LG)
	return R
