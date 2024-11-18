import networkx as nx

def find_partition_efficient(G):
	# Find strongly connected components
	sccs = list(nx.strongly_connected_components(G))

	# Create a new graph with SCCs as nodes
	scc_graph = nx.DiGraph()
	scc_mapping = {}
	for i, scc in enumerate(sccs):
		scc_node = f"SCC_{i}"
		scc_mapping[scc_node] = set(scc)
		scc_graph.add_node(scc_node)

	# Add edges between SCCs
	for u, v in G.edges():
		u_scc = next(scc_node for scc_node, nodes in scc_mapping.items() if u in nodes)
		v_scc = next(scc_node for scc_node, nodes in scc_mapping.items() if v in nodes)
		if u_scc != v_scc:
			scc_graph.add_edge(u_scc, v_scc)

	# Find nodes with no incoming edges in the SCC graph
	V1_sccs = set(n for n in scc_graph.nodes() if scc_graph.in_degree(n) == 0)
	V2_sccs = set(scc_graph.nodes()) - V1_sccs

	# Map SCC nodes back to original nodes
	V1 = set().union(*(scc_mapping[scc] for scc in V1_sccs))
	V2 = set().union(*(scc_mapping[scc] for scc in V2_sccs))

	# If V2 is empty, no valid partition exists
	if not V2:
		return None

	# Verify that all edges from V1 to V2 exist and no edges from V2 to V1 exist
	if all(G.has_edge(v1, v2) for v1 in V1 for v2 in V2) and \
	   not any(G.has_edge(v2, v1) for v2 in V2 for v1 in V1):
		return V1, V2
	else:
		return None

# Test cases
G1 = nx.DiGraph([('a','b'),('b','c'),('c','a'),('a','d'),('b','d'),('c','d'),('a','e'),('b','e'),('c','e')])
G2 = nx.DiGraph([('a','b')])
G3 = nx.DiGraph([('a','c'),('b','c'),('a','d'),('b','d')])
G4 = nx.DiGraph([('a','b'),('b','c'),('c','a')])
G5 = nx.DiGraph([('a','b'),('a','c'),('b','c')])
G6 = nx.DiGraph([('a','b'),('b','c'),('c','d'),('a','d')])
G7 = nx.DiGraph([('a','b'),('b','c'),('c','d'),('d','e'),('e','f'),('a','f')])
G8 = nx.DiGraph([('a','b'),('b','c'),('c','a'),('c','d'),('d','e'),('e','f'),('f','d')])
G9 = nx.DiGraph([('a','b'),('b','c'),('c','d'),('d','a'),('a','e'),('b','e'),('c','e'),('d','e')])
G10 = nx.DiGraph([('a','b'),('b','c'),('c','d'),('d','a'),('e','a'),('e','b'),('e','c'),('e','d')])
G11 = nx.DiGraph([('a','b'),('b','c'),('c','a'),('d','e'),('e','f'),('f','d'),('a','d'),('b','e'),('c','f')])
G12 = nx.DiGraph([('a','b'),('b','c'),('c','d'),('d','a'),('a','e'),('e','f'),('f','g'),('g','e')])
G13 = nx.DiGraph([('a','b'),('b','c'),('c','a'),('a','d'),('b','d'),('c','d'),('d','e'),('e','f'),('f','d')])
G14 = nx.DiGraph([('a','b'),('b','c'),('c','d'),('d','e'),('e','a'),('a','f'),('b','f'),('c','f'),('d','f'),('e','f')])
G15 = nx.DiGraph([('a','b'),('b','c'),('c','a'),('d','e'),('e','f'),('f','d'),('a','d'),('a','e'),('a','f')])
G16 = nx.DiGraph([('a','b'),('b','c'),('c','d'),('d','a'),('a','e'),('b','e'),('c','e'),('d','e'),('e','f')])
G17 = nx.DiGraph([('a','b'),('b','c'),('c','a'),('b','d'),('d','c'),('c','b'),('a','e'),('b','e'),('c','e'),('d','e')])

test_graphs = [G1, G2, G3, G4, G5, G6, G7, G8, G9, G10, G11, G12, G13, G14, G15, G16, G17]

for i, G in enumerate(test_graphs, 1):
	result = find_partition_efficient(G)
	print(f"G{i}: {result}")
