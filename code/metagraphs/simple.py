#!/usr/bin/env python3
"""
Simple Metagraph Enumeration (Fixed Version)

Counts unlabeled simple metagraphs with n components using proper isomorphism checking.
A simple metagraph has nodes and edges, where each edge has exactly one
source and one target, both of which can be either nodes or edges.
"""

from itertools import product, permutations
from collections import defaultdict


def enumerate_configs(num_nodes, num_edges):
    """Generate all labeled simple metagraph configurations."""
    nodes = [f"n{i}" for i in range(num_nodes)]
    edges = [f"e{i}" for i in range(num_edges)]
    all_components = nodes + edges

    if num_edges == 0:
        return [{"nodes": nodes, "edges": []}]

    configs = []

    # Each edge needs a source and target from all_components
    for assignment in product(all_components, repeat=2*num_edges):
        edge_specs = []
        for i in range(num_edges):
            src = assignment[2*i]
            tgt = assignment[2*i + 1]
            edge_specs.append((edges[i], src, tgt))

        configs.append({
            "nodes": nodes,
            "edges": edge_specs
        })

    return configs


def are_isomorphic(config1, config2):
    """Check if two configurations are isomorphic under relabeling."""
    if len(config1["nodes"]) != len(config2["nodes"]) or \
       len(config1["edges"]) != len(config2["edges"]):
        return False

    # Try all permutations of nodes and edges
    for node_perm in permutations(config1["nodes"]):
        for edge_perm in permutations([e[0] for e in config1["edges"]]):

            # Create mapping
            mapping = {}
            for i, node in enumerate(config1["nodes"]):
                mapping[node] = node_perm[i]
            for i, edge in enumerate([e[0] for e in config1["edges"]]):
                mapping[edge] = edge_perm[i]

            # Apply mapping to config1
            mapped_edges = []
            for edge, src, tgt in config1["edges"]:
                mapped_src = mapping.get(src, src)
                mapped_tgt = mapping.get(tgt, tgt)
                mapped_edges.append((mapping[edge], mapped_src, mapped_tgt))

            # Sort both edge lists for comparison
            mapped_edges_sorted = sorted(mapped_edges)
            config2_edges_sorted = sorted(config2["edges"])

            if mapped_edges_sorted == config2_edges_sorted:
                return True

    return False


def count_unique_proper(configs):
    """Count unique configurations using proper isomorphism checking."""
    unique = []

    for config in configs:
        is_new = True
        for existing in unique:
            if are_isomorphic(config, existing):
                is_new = False
                break
        if is_new:
            unique.append(config)

    return len(unique), unique


def compute_simple_metagraphs(n):
    """Compute the number of unlabeled simple metagraphs with n components."""
    print(f"=== Computing n={n} Simple Metagraphs ===")

    total = 0
    breakdown = {}
    all_unique = {}

    for num_nodes in range(n + 1):
        num_edges = n - num_nodes
        if num_edges < 0:
            continue

        print(f"Computing ({num_nodes},{num_edges})...")

        if num_edges == 0:
            # Just disconnected nodes
            count = 1
            unique_configs = [{"nodes": [f"n{i}" for i in range(num_nodes)], "edges": []}]
        else:
            configs = enumerate_configs(num_nodes, num_edges)
            count, unique_configs = count_unique_proper(configs)
            print(f"  {len(configs)} labeled → {count} unlabeled")

        breakdown[(num_nodes, num_edges)] = count
        all_unique[(num_nodes, num_edges)] = unique_configs
        total += count

    print(f"\nBreakdown for n={n}:")
    for (nodes, edges), count in breakdown.items():
        print(f"  ({nodes},{edges}): {count}")

    print(f"Total: {total}")
    return total, breakdown, all_unique


def show_examples(unique_configs, case_name, max_examples=10):
    """Show example configurations for a given case."""
    print(f"\n{case_name} examples:")
    for i, config in enumerate(unique_configs[:max_examples]):
        print(f"  {i+1}: nodes={config['nodes']}, edges={config['edges']}")
    if len(unique_configs) > max_examples:
        print(f"  ... and {len(unique_configs) - max_examples} more")


def main():
    """Run the complete analysis."""
    print("Simple Metagraph Sequence Calculator (Fixed)")
    print("===========================================")

    # Compute sequence for small values
    sequence = []
    all_cases = {}

    for n in range(1, 4):  # Start with n=1,2,3 to verify
        total, breakdown, unique_configs = compute_simple_metagraphs(n)
        sequence.append(total)
        all_cases[n] = unique_configs
        print()

    print("=== SEQUENCE ===")
    for i, count in enumerate(sequence, 1):
        print(f"n={i}: {count}")

    print(f"\nSequence: {sequence}")

    # Show examples for verification
    print("\n=== EXAMPLES FOR VERIFICATION ===")
    show_examples(all_cases[2][(0, 2)], "n=2, (0,2)", max_examples=10)
    show_examples(all_cases[2][(1, 1)], "n=2, (1,1)", max_examples=4)
    show_examples(all_cases[3][(0, 3)], "n=3, (0,3)", max_examples=10)

if __name__ == "__main__":
    main()
