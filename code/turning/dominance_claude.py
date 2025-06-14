import networkx as nx
from typing import Set, Tuple, Optional

def find_required_V2_members(G: nx.DiGraph, v: str, current_V2: Set[str], forbidden: Set[str]) -> Optional[Set[str]]:
    """
    Given a vertex v that we want to put in V₂, find all vertices that must also be in V₂.
    Returns None if this would require including a forbidden vertex.
    Time complexity: O(V + E)

    Each vertex only needs to be processed once when it's added to V₂ because:
    1. Processing a vertex only adds new vertices to V₂
    2. Once added to V₂, a vertex is never removed
    3. If processing a vertex doesn't add any new vertices, we don't need to process it again
    """
    required_V2 = current_V2 | {v}
    all_vertices = set(G.nodes())

    # Queue of vertices that we've added to V₂ but haven't processed yet
    to_process = {v}

    while to_process:
        # Take one vertex from the queue
        vertex = to_process.pop()

        # 1. All out-neighbors must be in V₂
        out_neighbors = set(G.successors(vertex))
        new_required = out_neighbors - required_V2
        if new_required & forbidden:
            return None

        # 2. All vertices that don't point to this vertex must be in V₂
        non_in_neighbors = all_vertices - set(G.predecessors(vertex)) - {vertex}
        new_required.update(non_in_neighbors - required_V2)
        if new_required & forbidden:
            return None

        # Add new vertices to both sets
        required_V2.update(new_required)
        to_process.update(new_required)

    return required_V2

def find_complete_domination(G: nx.DiGraph) -> Tuple[Set[str], Set[str]]:
    """
    Finds sets V₁ and V₂ where V₁ completely dominates V₂.
    Returns (V₁, V₂) if such sets exist, raises ValueError otherwise.
    Time complexity: O(V × (V + E))
    """
    all_vertices = set(G.nodes())

    # Try each vertex as a potential V₂ member
    for v in all_vertices:
        V2 = find_required_V2_members(G, v, set(), set())
        if V2 is not None:
            V1 = all_vertices - V2
            if V1:  # If V1 is non-empty
                # Verify the partition is valid (redundant but good for safety)
                valid = True
                # Check V₁ → V₂ edges exist
                for v1 in V1:
                    if not V2.issubset(set(G.successors(v1))):
                        valid = False
                        break
                # Check no V₂ → V₁ edges exist
                if valid:
                    for v2 in V2:
                        if V1.intersection(set(G.successors(v2))):
                            valid = False
                            break
                if valid:
                    return V1, V2

    raise ValueError("No complete domination partition exists")

def test_cases():
    # Test Case 1: a->b->c->a, a->d, b->d, c->d, a->e, b->e, c->e
    G1 = nx.DiGraph()
    G1.add_edges_from([
        ('a','b'), ('b','c'), ('c','a'),
        ('a','d'), ('b','d'), ('c','d'),
        ('a','e'), ('b','e'), ('c','e')
    ])

    # Test Case 2: a->b
    G2 = nx.DiGraph()
    G2.add_edge('a', 'b')

    # Test Case 3: a->c, b->c, a->d, b->d
    G3 = nx.DiGraph()
    G3.add_edges_from([('a','c'), ('b','c'), ('a','d'), ('b','d')])

    # Test Case 4: a->b->c->a
    G4 = nx.DiGraph()
    G4.add_edges_from([('a','b'), ('b','c'), ('c','a')])

    # Test Case 4: a->b->c->a
    G5 = nx.DiGraph()
    G5.add_edges_from([('a','c'), ('b','c'), ('a','d'), ('b', 'd')])

    # Test Case 4: a->b->c->a
    G6 = nx.DiGraph()
    G6.add_edges_from([('a', 'b'), ('a','c'), ('b','c'), ('a','d'), ('b', 'd')])

    # Test Case 4: a->b->c->a
    G7 = nx.DiGraph()
    G7.add_edges_from([('a','c'), ('b','c'), ('a','d'), ('b', 'd'), ('c', 'd')])

    # Test Case 4: a->b->c->a
    G8 = nx.DiGraph()
    G8.add_edges_from([('a','b'), ('b','c'), ('a', 'c')])

    # Test Case 4: a->b->c->a
    G9 = nx.DiGraph()
    G9.add_edges_from([('a','b'), ('b','c'), ('c', 'd')])

    # Test Case 4: a->b->c->a
    G10 = nx.DiGraph()
    G10.add_nodes_from(['a', 'b'])

    # Test Case 11: Complete graph (no valid partition should exist)
    G11 = nx.complete_graph(4, create_using=nx.DiGraph())

    # Test Case 12: Empty graph with nodes (should support valid partitions)
    G12 = nx.DiGraph()
    G12.add_nodes_from(['a', 'b', 'c'])

    # Test Case 13: Multiple possible valid partitions
    # a->b->c, a->c, d->b->e, d->e (can have either {a,d} dominating {b,c,e} or {a} dominating {b,c})
    G13 = nx.DiGraph()
    G13.add_edges_from([('a','b'), ('b','c'), ('a','c'), ('d','b'), ('b','e'), ('d','e')])

    # Test Case 14: Large V₁ to small V₂ ratio
    G14 = nx.DiGraph()
    G14.add_edges_from([
        ('a','z'), ('b','z'), ('c','z'), ('d','z'), ('e','z'),
        ('a','y'), ('b','y'), ('c','y'), ('d','y'), ('e','y')
    ])

    # Test Case 15: Small V₁ to large V₂ ratio
    G15 = nx.DiGraph()
    G15.add_edges_from([('x', v) for v in 'abcdefgh'])

    # Test Case 16: Chain that should fail
    G16 = nx.DiGraph()
    G16.add_edges_from([('a','b'), ('b','c'), ('c','d'), ('d','e'), ('e','a')])

    # Test Case 17: Disconnected components with valid partition
    G17 = nx.DiGraph()
    G17.add_edges_from([('a','b'), ('c','d')])

    # Test Case 18: Self-loops
    G18 = nx.DiGraph()
    G18.add_edges_from([('a','a'), ('a','b'), ('b','b')])

    # Test Case 19: Bidirectional edges in V₁ but complete domination still possible
    G19 = nx.DiGraph()
    G19.add_edges_from([
        ('a','b'), ('b','a'),  # bidirectional in V₁
        ('a','c'), ('b','c')   # both dominate c
    ])

    # Test Case 20: Almost complete domination but one edge missing
    G20 = nx.DiGraph()
    G20.add_edges_from([
        ('a','c'), ('a','d'),
        ('b','c')  # missing b->d edge prevents complete domination
    ])

    # Run all test cases
    test_cases = [
        (G1, "Graph 1 (triangle with two dominated vertices)"),
        (G2, "Graph 2 (single edge)"),
        (G3, "Graph 3 (two vertices dominating two others)"),
        (G4, "Graph 4 (triangle - should fail)"),
        (G5, "Graph 5 (duplicate of G3)"),
        (G6, "Graph 6 (extra edge a->b)"),
        (G7, "Graph 7 (extra edge c->d)"),
        (G8, "Graph 8 (transitive closure)"),
        (G9, "Graph 9 (chain)"),
        (G10, "Graph 10 (isolated vertices)"),
        (G11, "Graph 11 (complete graph)"),
        (G12, "Graph 12 (empty graph with nodes)"),
        (G13, "Graph 13 (multiple valid partitions)"),
        (G14, "Graph 14 (large V₁ to small V₂)"),
        (G15, "Graph 15 (small V₁ to large V₂)"),
        (G16, "Graph 16 (cyclic chain)"),
        (G17, "Graph 17 (disconnected components)"),
        (G18, "Graph 18 (self-loops)"),
        (G19, "Graph 19 (bidirectional V₁ edges)"),
        (G20, "Graph 20 (almost complete domination)")
    ]

    for G, desc in test_cases:
        print(f"\nTesting {desc}")
        try:
            V1, V2 = find_complete_domination(G)
            print(f"Found partition: V₁={V1}, V₂={V2}")
            # Verify the solution
            print("Verification:")
            print(f"V₁ to V₂ edges complete:", all(all((u,v) in G.edges() for v in V2) for u in V1))
            print(f"No V₂ to V₁ edges:", all(all((u,v) not in G.edges() for v in V1) for u in V2))
        except ValueError as e:
            print(f"Result: {e}")

if __name__ == "__main__":
    test_cases()
