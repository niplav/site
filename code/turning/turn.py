import math
import networkx as nx
import itertools as it

def turn(graph):
	mindist=math.inf
	worlds=list(graph.nodes)
	for perm in it.permutations(worlds):
		perm=list(perm)
		pathgraph=nx.DiGraph()
		for i in range(0, len(worlds)):
			pathgraph.add_node(worlds[i], ind=i)
		# The transitive closure over this particular path graph
		# Simplify to nx.algorithms
		for i in range(0, len(perm)-1):
			pathgraph.add_edge(perm[i], perm[i+1])
		pathgraph=nx.algorithms.dag.transitive_closure(pathgraph)
		# Compute the graph edit distance, disabling node insertion/deletion/substition and edge substitution
		edge_cost=lambda x: 1
		unaffordable=lambda x: 10e10
		same_node=lambda x, y: x['ind']==y['ind']
		edge_matches=lambda x, y: True
		dist=nx.algorithms.similarity.graph_edit_distance(graph, pathgraph, node_match=same_node, edge_match=edge_matches, node_del_cost=unaffordable, node_ins_cost=unaffordable, edge_ins_cost=edge_cost, edge_del_cost=edge_cost)
		if dist<mindist:
			result=pathgraph
			mindist=dist
	return result

def turn_all(graph):
	results=set()
	mindist=math.inf
	worlds=list(graph.nodes)
	for perm in it.permutations(worlds):
		perm=list(perm)
		pathgraph=nx.DiGraph()
		for i in range(0, len(worlds)):
			pathgraph.add_node(worlds[i], ind=i)
		for i in range(0, len(perm)-1):
			pathgraph.add_edge(perm[i], perm[i+1])
		pathgraph=nx.algorithms.dag.transitive_closure(pathgraph)
		# Compute the graph edit distance, disabling node insertion/deletion/substition and edge substitution
		edge_cost=lambda x: 1
		unaffordable=lambda x: 10e10
		same_node=lambda x, y: x['ind']==y['ind']
		edge_matches=lambda x, y: True
		dist=nx.algorithms.similarity.graph_edit_distance(graph, pathgraph, node_match=same_node, edge_match=edge_matches, node_del_cost=unaffordable, node_ins_cost=unaffordable, edge_ins_cost=edge_cost, edge_del_cost=edge_cost)
		if dist<mindist:
			results=set([pathgraph])
			mindist=dist
		elif dist==mindist:
			results.add(pathgraph)
	return results

def powerset(iterable):
	s = list(iterable)
	allcomb=[]
	for r in range(len(s)+1):
		allcomb+=list(it.combinations(s,r))
	return allcomb

def all_directed_graphs(n):
	if n<=0:
		return [nx.DiGraph()]
	graphs=all_directed_graphs(n-1)
	newgraphs=[]
	for g in graphs:
		g.add_node(n, ind=n)
		for tosubset in powerset(range(1, n+1)):
			for fromsubset in powerset(range(1, n)):
				gnew=g.copy()
				for element in tosubset:
					gnew.add_edge(n, element)
				for element in fromsubset:
					gnew.add_edge(element, n)
				newgraphs.append(gnew)
	return newgraphs
