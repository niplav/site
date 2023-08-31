import math
import networkx as nx
import itertools as it

import networkx.algorithms.isomorphism.isomorph as isomorph

def turn(graph):
	mindist=math.inf
	worlds=list(graph.nodes)
	for perm in it.permutations(worlds):
		perm=list(perm)
		pathgraph=nx.path_graph(perm, nx.DiGraph)
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
		pathgraph=nx.path_graph(perm, nx.DiGraph)
		pathgraph=nx.algorithms.dag.transitive_closure(pathgraph)
		dist=len(set(graph.edges)^set(pathgraph.edges))
		if dist<mindist:
			results=set([pathgraph])
			mindist=dist
		elif dist==mindist:
			results.add(pathgraph)
	return results

def stepwise(g):
	decycleds=set()
	solutions=set()

	graph=g.copy()

	graph.remove_edges_from([(x,x) for x in graph.nodes])

	if is_consistent(graph):
		return set([graph])

	if is_acyclic(graph):
		decycleds.add(graph)
	else:
		mfass=minimal_feedback_arc_sets(graph)
		for mfas in mfass:
			decycled=nx.DiGraph(graph)
			decycled.remove_edges_from(mfas)
			decycleds.add(decycled)

	for decycled in decycleds:
		if is_consistent(decycled):
			solutions.add(decycled)
			continue

		solutions.update(set(totalizations(decycled)))

	return solutions

def totalizations(graph):
	if len(list(graph.nodes()))==0:
		return [graph]

	solutions=list()
	indegrees=dict(graph.in_degree())

	for k,v in indegrees.items():
		if v==0:
			ablated=nx.DiGraph(graph)
			ablated.remove_node(k)
			totalized=totalizations(ablated)
			for t in totalized:
				t.add_node(k)
				for n in t.nodes():
					t.add_edge(k, n)
				t.remove_edge(k,k)
			solutions=solutions+totalized

	return solutions

def minimal_feedback_arc_sets(graph):
	edges=list(graph.edges)
	nedges=len(edges)
	mfas=[]
	found_minimal=False
	for i in range(0,nedges):
		candidates=it.combinations(edges, i)
		for c in candidates:
			graph.remove_edges_from(c)
			if is_acyclic(graph):
				found_minimal=True
				mfas.append(c)
			graph.add_edges_from(c)
		if found_minimal==True:
			break
	return mfas

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

def preserves_dominance(graph, result):
	try:
		if not nx.is_weakly_connected(graph):
			return True
	except nx.NetworkXPointlessConcept:
		return True

	dominating_sets=gen_dominating_sets(graph)

	result_tmp=result.copy()
	for p in dominating_sets:
		if not is_dominating_set(result_tmp, p):
			return False
		result_tmp.remove_nodes_from(p)

	return True

def gen_dominating_sets(graph):
	g=graph.copy()
	dominating_sets=list()
	while len(g.nodes)>0:
		for p in powerset(g.nodes):
			if len(p)>0 and is_dominating_set(g, p):
				g.remove_nodes_from(p)
				dominating_sets.append(p)
				break
	return dominating_sets

def is_dominating_set(graph, dominating):
	rest=set(graph.nodes).difference(dominating)
	for d in dominating:
		for r in rest:
			if not (d,r) in graph.edges or (r,d) in graph.edges:
				return False
	return True

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

def map_5_graphs(f, reflexive=True, resume_at=None):
	n=5
	saved=dict()
	graphs=all_directed_graphs(n-1)
	i=1

	if resume_at==None:
		resume=True
	else:
		resume=False

	for g in graphs:
		g.add_node(n, ind=n)
		if reflexive==True:
			limit=n+1
		else:
			limit=n
		for tosubset in powerset(range(1, limit)):
			for fromsubset in powerset(range(1, n)):
				gnew=g.copy()
				for element in tosubset:
					gnew.add_edge(n, element)
				for element in fromsubset:
					gnew.add_edge(element, n)
				if resume==False and gequals(gnew, resume_at):
					resume=True
				if resume==True:
					f(gnew)

def gequals(g, h):
	return set(g.edges).issubset(set(h.edges)) and set(h.edges).issubset(set(g.edges))

def issubgraph(s, g):
	return set(s.edges) <= (set(g.edges))

def is_acyclic(graph):
	try:
		cycles=nx.find_cycle(graph, orientation="original")
	except nx.NetworkXNoCycle:
		return True
	return False

def is_consistent(graph):
	try:
		cycles=nx.find_cycle(graph, orientation="original")
	except nx.NetworkXNoCycle:
		if nx.algorithms.tournament.is_tournament(graph):
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

smallworld=['a', 'b', 'c']
smallgraph=nx.DiGraph()

for i in range(0, len(smallworld)):
	smallgraph.add_node(smallworld[i], ind=i)

smallgraph.add_edges_from([('a', 'b')])
smallre=turn(smallgraph)

domgraph=smallgraph.copy()
domgraph.add_edges_from([('a', 'c')])

mediumworld=['a', 'b', 'c', 'd', 'e', 'f', 'g']
mediumgraph=nx.DiGraph()
for i in range(0, len(mediumworld)):
	mediumgraph.add_node(mediumworld[i], ind=i)

mediumgraph.add_edges_from([('a', 'b'), ('b', 'c'), ('c', 'd'), ('c', 'e'), ('e', 'f'), ('f', 'g'), ('g', 'b')])

mediumres=turn(mediumgraph)

bigrev=nx.DiGraph()
bigrev_opts=['a','b','c','d','m1','m2','m3','m4','m5']
bigrev.add_edges_from([('a','m1'), ('m1', 'b'), ('a', 'b'), ('b', 'm2'), ('m2','c'), ('b', 'c'), ('a', 'm3'), ('m3', 'd'), ('a', 'd'), ('d', 'm4'), ('m4', 'c'), ('d', 'c'), ('c', 'm5'), ('m5', 'a'), ('c', 'a')])

animals=nx.DiGraph()
animals.add_nodes_from(['M', 'I', 'B', 'F'])
animals.add_edges_from([('M', 'M', {'weight': 0.11, 'n': 1}), ('M', 'B', {'weight': 0.225, 'n': 1}), ('B', 'M', {'weight': 0.045, 'n': 1}), ('M', 'I', {'weight': 0.225, 'n': 1}), ('I', 'M', {'weight': 0.145, 'n': 1}), ('I', 'B', {'weight': 0.225, 'n': 1}), ('I', 'I', {'weight': 0.225, 'n': 1}), ('I', 'F', {'weight': 0.855, 'n': 1}), ('B', 'F', {'weight': 0.405, 'n': 1}), ('M', 'F', {'weight': 0.54, 'n': 1})])
