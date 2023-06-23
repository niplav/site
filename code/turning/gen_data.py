import random
import networkx as nx

import turn

confusions=open('./confusions.txt', mode='w', buffering=1)
preservations=open('./subgraphs.txt', mode='w', buffering=1)

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
	turnings=turn.turn_all(g)
	turn_summary(g, turnings)
	subgraphs=turn.maximal_consistent_subgraphs(g)
	subgraph_summary(g, subgraphs, turnings)

for i in range(0,5):
	graphs=turn.all_directed_graphs(i)
	for g in graphs:
		write_summary(g)

confusions.close()
preservations.close()

confusions=open('./confusions.txt', mode='a', buffering=1)
preservations=open('./subgraphs.txt', mode='a', buffering=1)

exit(1)

turn.map_5_graphs(write_summary)

confusions.close()
preservations.close()

confusions=open('./confusions.txt', mode='a', buffering=1)
preservations=open('./subgraphs.txt', mode='a', buffering=1)

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
