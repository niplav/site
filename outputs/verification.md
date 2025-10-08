# Verification Complexity of NP Problems

An exploration of how long it takes to *verify* solutions to NP problems,
given an appropriate certificate.

## The Table

| Problem | Input Size | Certificate | Verification | Notes |
|---------|-----------|-------------|--------------|-------|
| **k-SAT** | n clauses, m vars | Assignment to vars | O(n) | Check each clause once |
| **3-Coloring** | n vertices, m edges | Color assignment | O(m) | Check each edge once |
| **Hamiltonian Path** | n vertices, m edges | Sequence of vertices | O(n) | Check consecutive pairs are edges |
| **Subset Sum** | k numbers | Subset membership | O(k) | Sum the chosen numbers |
| **Vertex Cover** | n vertices, m edges | Set of ≤k vertices | O(m) | Check each edge is covered |
| **Independent Set** | n vertices, m edges | Set of k vertices | O(m) | Check no edges between them |
| **Clique** | n vertices, (m edges) | Set of k vertices | O(k²) or O(k² log m) | Check all pairs are edges; depends on graph representation |
| **Graph Isomorphism** | n vertices each | Permutation | O(n²) or O(m) | Check edge preservation; depends on representation |
| **Integer Factorization** | ℓ-bit number | Factor p | O(ℓ²) + primality | Multiplication O(ℓ²), primality test O(ℓ⁶) via AKS |
| **Discrete Log** | ℓ-bit modulus | Exponent x | O(ℓ²·log x) or O(ℓ³) | Modular exponentiation via repeated squaring |
| **Partition** | k ℓ-bit numbers | Subset indicator | O(k·ℓ) | Add k numbers of ℓ bits each |
| **Knapsack (decision)** | k items | Subset indicator | O(k) | Check weight ≤ W, value ≥ V |
| **TSP (decision)** | n cities, distances | Tour permutation | O(n) | Sum edge weights in tour |
| **Hamiltonian Cycle** | n vertices, m edges | Cycle | O(n) | Check edges exist, forms cycle |
| **Exact Cover** | n sets, universe size m | Subcollection | O(nm) | Check each element covered exactly once |

## Observations

**Most problems are linear:** The vast majority of NP problems have
verification complexity O(input size), meaning checking a certificate
takes time proportional to just reading the input and certificate once.

**Few quadratic problems:** Only a handful require O(n²) verification, mostly:

- Graph problems where you must check all pairs (Clique)
- Problems involving graph structure comparison (Graph Isomorphism)
- Number-theoretic problems with multi-digit arithmetic (Factorization, Discrete Log)

**No naturally superquadratic verification:** Surprisingly, there appear
to be no natural NP problems requiring O(n^k) verification for large
k. This is unexpected - NP allows *any* polynomial verification time,
so why don't we see O(n^{100}) verifiers in practice?

**Log factors appear when:**
1. Performing arithmetic on multi-bit integers
2. Binary search during verification
3. Primality testing (though this is already polylog)

**Graph representation matters:** Whether graphs are given as adjacency
matrices or edge lists changes verification complexity. Standard
convention uses edge lists, keeping most graph problems at O(m).

## The Mystery: Where Are the Superquadratic Verifiers?

It's straightforward to *construct* artificial NP problems with
arbitrarily high polynomial verification complexity (e.g., by padding
certificates with redundant validation bits). But finding *natural*
problems that *require* cubic or higher verification seems difficult
or impossible.

**Hypotheses:**
1. **Selection bias:** We don't study problems with impractically expensive verification
2. **Structural reason:** Natural problems ask about locally checkable properties
3. **Deep theorem:** Something fundamental about certificate complexity limits natural problems to near-linear verification

This deserves further investigation.

## Open Questions

- Is there a natural NP problem requiring O(n³) verification as a *minimum*?
- Can we prove all "natural" NP problems have verification ≤ O(n⁴)?
- What structural properties of problems lead to higher verification complexity?
- Is there work systematically classifying NP problems by verification degree?
