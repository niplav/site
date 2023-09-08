import random
import networkx as nx
import itertools as it

import hodge
import ontological_crises as oc

def gen_weight_graph(n):
	potential=dict()
	for i in range(n):
		potential[i]=random.random()
	return hodge.potential_to_graph(potential)

def gen_shift(preimage, m, p):
	shift=dict()
	nextset=range(m)
	for pi in preimage:
		mappedto=[]
		for ne in nextset:
			if random.random()<p:
				mappedto=mappedto+[(ne, random.random())]
		shift[pi]=mappedto
	return shift

g1=gen_weight_graph(2)
s1=gen_shift(g1.nodes, 3, 0.5)
g2=oc.ontological_shift(g1, s1, oc.noresolver)
g2res=oc.ontological_shift(g1, s1, oc.hodgewrap)
s2=gen_shift(g2.nodes, 2, 0.5)
g3=oc.ontological_shift(g2, s2, oc.hodgewrap)
g3res=oc.ontological_shift(g2res, s2, oc.hodgewrap)

#Example that doesn't distribute
eg1=nx.DiGraph()
eg1.add_edges_from([(0,1,{'weight': 1})])
es1={0: [(1, 0.28)], 1: [(0, 0.57), (2, 0.43)]}
es2={0: [(0, 0.014), (1, 0.38)], 1: [], 2: [(0, 0.34), (1, 0.66)]}
eg2=oc.ontological_shift(eg1, es1, oc.noresolver)
eg2res=oc.ontological_shift(eg1, es1, oc.hodgewrap)
eg3=oc.ontological_shift(eg2, es2, oc.noresolver)
egnodist3=oc.hodgewrap(eg3)
eg3res=oc.ontological_shift(eg2res, es2, oc.hodgewrap)
