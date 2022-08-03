import math
import networkx as nx
import itertools as it

import networkx.algorithms.isomorphism.isomorph as isomorph

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
		dist=len(set(graph.edges)^set(pathgraph.edges))
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
		dist=len(set(graph.edges)^set(pathgraph.edges))
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

def all_nonref_directed_graphs(n):
	if n<=0:
		return [nx.DiGraph()]
	graphs=all_nonref_directed_graphs(n-1)
	newgraphs=[]
	for g in graphs:
		g.add_node(n, ind=n)
		for tosubset in powerset(range(1, n)):
			for fromsubset in powerset(range(1, n)):
				gnew=g.copy()
				for element in tosubset:
					gnew.add_edge(n, element)
				for element in fromsubset:
					gnew.add_edge(element, n)
				newgraphs.append(gnew)
	return newgraphs

def collect_all_5():
	n=5
	saved=dict()
	graphs=all_directed_graphs(n-1)
	i=1
	for g in graphs:
		g.add_node(n, ind=n)
		for tosubset in powerset(range(1, n+1)):
			for fromsubset in powerset(range(1, n)):
				gnew=g.copy()
				for element in tosubset:
					gnew.add_edge(n, element)
				for element in fromsubset:
					gnew.add_edge(element, n)
				confusion=len(turn_all(gnew))
				print('{0},{1},"{2}"'.format(5, confusion, gnew.edges))

def collect_all_nonref_5():
	n=5
	saved=dict()
	graphs=all_nonref_directed_graphs(n-1)
	i=1
	for g in graphs:
		g.add_node(n, ind=n)
		for tosubset in powerset(range(1, n)):
			for fromsubset in powerset(range(1, n)):
				gnew=g.copy()
				for element in tosubset:
					gnew.add_edge(n, element)
				for element in fromsubset:
					gnew.add_edge(element, n)
				confusion=len(turn_all(gnew))
				print('{0},{1},"{2}"'.format(5, confusion, gnew.edges))

def collect_all_nonref_5_cache():
	n=5
	saved=dict()
	graphs=all_nonref_directed_graphs(n-1)
	i=1
	for g in graphs:
		g.add_node(n, ind=n)
		for tosubset in powerset(range(1, n)):
			for fromsubset in powerset(range(1, n)):
				gnew=g.copy()
				for element in tosubset:
					gnew.add_edge(n, element)
				for element in fromsubset:
					gnew.add_edge(element, n)
				save_graph(saved, gnew)

def save_graph(saved, g):
	gdeg=",".join(sorted(str(d) for (n,d) in g.degree()))
	if not gdeg in saved.keys():
		saved[gdeg]=dict()
		confusion=len(turn_all(g))
		saved[gdeg][g]=confusion
		print('{0},{1},"{2}"'.format(5, confusion, g.edges))
	else:
		inthere=False
		for h in saved[gdeg].keys():
			if isomorph.is_isomorphic(g, h):
				inthere=True
				print('{0},{1},"{2}"'.format(5, saved[gdeg][h], g.edges))
		if not inthere:
			confusion=len(turn_all(g))
			saved[gdeg][g]=confusion
			print('{0},{1},"{2}"'.format(5, confusion, g.edges))
