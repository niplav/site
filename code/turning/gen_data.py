import random
import networkx as nx

import turn

def subgraph_summary(g, subgraphs, turnings):
	overall_preservation=0
	nsubgraphs=len(subgraphs)
	for s in subgraphs:
		present_in=0
		for t in turnings:
			if set(s.nodes).issubset(set(t.nodes)) and set(s.edges).issubset(set(t.edges)):
				present_in=present_in+1
		overall_preservation=overall_preservation+present_in/len(turnings)
		preservations.write('\t{0},{1},"{2}","{3}","{4}"\n'.format(len(g.nodes), present_in/len(turnings), nsubgraphs, s.edges, g.edges))
	preservations.write('{0},{1},{2},"{3}"\n'.format(len(g.nodes), overall_preservation/len(subgraphs), nsubgraphs, g.edges))

def turn_summary(g, turnings):
	confusion=len(turnings)
	confusions.write('{0},{1},"{2}"\n'.format(len(g.nodes), confusion, g.edges))

def write_summary(g):
	turnings=turn.stepwise(g)
	turn_summary(g, turnings)
	subgraphs=turn.maximal_consistent_subgraphs(g)
	subgraph_summary(g, subgraphs, turnings)

confusions=open('./confusions_fast.csv', mode='w', buffering=1)
preservations=open('./subgraphs_fast.csv', mode='w', buffering=1)

#for i in range(0,5):
#	graphs=turn.all_directed_graphs(i)
#	for g in graphs:
#		write_summary(g)

last=nx.DiGraph()
for i in range(1,5):
	last.add_node(i, ind=i+1)
last.add_edges_from([(1,2), (1,5), (2,4), (4,3), (5,4)])

turn.map_5_graphs(write_summary, resume_at=last)

lim=16
samples=65536

for i in range(6,lim):
	for j in range(0,samples):
		g=nx.generators.random_graphs.gnp_random_graph(i, 0.5, directed=True)
		for n in g.nodes:
			g.add_node(n, ind=n)
			if random.random()>=0.5:
				g.add_edge(n,n)
		write_summary(g)
