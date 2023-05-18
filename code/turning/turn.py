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

def is_consistent(graph):
	try:
		cycles=nx.find_cycle(graph, orientation="original")
	except nx.NetworkXNoCycle:
		if nx.algorithms.tournament.is_tournament(graph) and len(graph.edges)>0:
			return True
	return False

def is_largest(c, g):
	for n in g.nodes():
		if n==c:
			continue
		if (n,c) in g.edges():
			return False
		if not (c,n) in g.edges():
			return False
	return True

def get_largest(g):
	largest=None
	for n in g.nodes():
		if is_largest(n,g):
			largest=n
	return largest

def maximal_consistent_subgraphs(graph):
	maximal_consistencies=set()
	for p in reversed(powerset(graph.nodes)):
		subgraph=graph.subgraph(p)
		if is_consistent(subgraph):
			smaller_subprefs=set()
			ignore=False
			for m in maximal_consistencies:
				if set(subgraph.nodes()).issubset(set(m.nodes())):
					ignore=True
					continue
				elif set(m.nodes()).issubset(set(subgraph.nodes())):
					smaller_subprefs.add(m)
			if ignore:
				continue
			else:
				maximal_consistencies=maximal_consistencies-smaller_subprefs
				maximal_consistencies.add(subgraph)
	return list(maximal_consistencies)

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

smallworld=['a', 'b', 'c']
smallgraph=nx.DiGraph()

for i in range(0, len(smallworld)):
	smallgraph.add_node(smallworld[i], ind=i)

smallgraph.add_edges_from([('a', 'b')])
smallre=turn(smallgraph)

mediumworld=['a', 'b', 'c', 'd', 'e', 'f', 'g']
mediumgraph=nx.DiGraph()
for i in range(0, len(mediumworld)):
	mediumgraph.add_node(mediumworld[i], ind=i)

mediumgraph.add_edges_from([('a', 'b'), ('b', 'c'), ('c', 'd'), ('c', 'e'), ('e', 'f'), ('f', 'g'), ('g', 'b')])

mediumres=turn(mediumgraph)

bigrev=nx.DiGraph()
bigrev_opts=['a','b','c','d','m1','m2','m3','m4','m5']
#TODO: finish the edges
bigrev.add_edges_from([('a','d'),('d','b')])
