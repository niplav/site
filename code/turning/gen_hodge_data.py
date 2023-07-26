import random
import networkx as nx

import hodge
import turn

def subgraph_summary(g, subgraphs, res):
	overall_preservation=0
	nsubgraphs=len(subgraphs)
	for s in subgraphs:
		present_in=0
		if turn.issubgraph(s, res):
			present_in=1
			overall_preservation=overall_preservation+1
		preservations.write('\t{0},{1},{2},"{3}","{4}"\n'.format(len(g.nodes), present_in, nsubgraphs, s.edges, g.edges))
		#print('\t{0},{1},{2},"{3}","{4}"'.format(len(g.nodes), present_in, nsubgraphs, s.edges, g.edges))

	preservations.write('{0},{1},{2},"{3}"\n'.format(len(g.nodes), overall_preservation/nsubgraphs, nsubgraphs, g.edges))
	#print('{0},{1},{2},"{3}"'.format(len(g.nodes), overall_preservation/nsubgraphs, nsubgraphs, g.edges))

def hodge_summary(g, result):
	residual=hodge.residual(g, result)
	dominance_preservation=turn.preserves_dominance(g, result)
	residuals.write('{0},{1},{2},"{3}"\n'.format(len(g.nodes), residual, dominance_preservation, g.edges))
	#print('{0},{1},{2},"{3}"'.format(len(g.nodes), residual, dominance_preservation, g.edges))

def write_summary(g):
	wg=hodge.weightgraph(g)
	res=hodge.hodgeresolve(wg)
	hodge_summary(wg, res)
	subgraphs=turn.maximal_consistent_subgraphs(g)
	subgraph_summary(g, subgraphs, res)

residuals=open('./hodge_residuals.csv', mode='w', buffering=1)
preservations=open('./hodge_subgraphs.csv', mode='w', buffering=1)

for i in range(0,5):
	graphs=turn.all_directed_graphs(i)
	for g in graphs:
		write_summary(g)

turn.map_5_graphs(write_summary)

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
