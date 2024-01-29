[home](./index.md)
------------------

*author: niplav, created: 2024-01-29, modified: 2024-01-29, language: english, status: in progress, importance: 4, confidence: possible*

> __What perfect sum of cycles and potential!__

Nothing to See Here, Just An Implementation of HodgeRank
=========================================================

<!--TODO: Schizo theories about how Hodge Theory is the solution to
everything?-->

[Jiang et al.
2011](./doc/preference/statistical_ranking_and_combinatorial_hodge_theory_jiang_et_al_2011.pdf "Statistical ranking and combinatorial Hodge theory")
propose a ranking algorithm for incomplete and cyclic data, but neglect
to give code or even pseudo-code for this algorithm. The algorithm turns out
to be easy to implement in Python using networkx and numpy, with some help from [this
guide](https://medium.com/@zj444/hodgerank-generating-movie-ranking-from-imdb-movie-ratings-part-1-2a88ec148f10 "HodgeRank: Generating Movie Ranking From IMDb Movie Ratings (Part 1: Problem Formulation)").
Since other people might find the code valuable as well, I provide it here
(mostly without comment or explanation).

        import numpy as np
        import networkx as nx
        import itertools as it

        def positive_edges(prefs):
                edges=[]
                for e in it.combinations(prefs.keys(), 2):
                        if np.all(np.isnan(prefs[e[0]]-prefs[e[1]])):
                                weight=np.nan
                        else:
                                weight=np.nanmean(prefs[e[0]]-prefs[e[1]])

                        n=np.sum(~np.isnan(prefs[e[0]]-prefs[e[1]]))
                        if np.isnan(weight):
                                continue
                        elif weight>=0:
                                edges.append((e[0], e[1], {'weight': weight, 'n': n}))
                        else:
                                edges.append((e[1], e[0], {'weight': -weight, 'n': n}))
                return edges

        def prefgraph(prefs):
                g=nx.DiGraph()
                g.add_nodes_from(list(prefs.keys()))
                edges=positive_edges(prefs)
                g.add_edges_from(edges)

        def decompose(g):
                f=np.array([g[e[0]][e[1]]['weight'] for e in g.edges])
                W=np.diag([g[e[0]][e[1]]['n'] for e in g.edges])

                origins=np.zeros((len(g.edges), len(g.nodes)))

                idx=dict()
                nodes=list(g.nodes)
                for i in range(0, len(nodes)):
                        idx[nodes[i]]=i

                origins=np.zeros((len(g.edges), len(g.nodes)))
                c=0
                for e in g.edges:
                        sign=np.sign(g[e[0]][e[1]]['weight'])
                        if np.isnan(sign):
                                sign=0
                        origins[c][e[0]]=sign*-1
                        origins[c][e[1]]=sign
                        c=c+1

                try:
                        s=-np.linalg.pinv(origins.T@W@origins)@origins.T@W@f
                except LinAlgError:
                        s=np.zeros(len(list(g.nodes)))

                values=dict()

                for option in idx.keys():
                        values[option]=s[idx[option]]

                return values

        def hodgerank(prefs):
                g=prefgraph(prefs)
                return decompose(g)

If `decompose` can't find a solution to the given preferences, it returns
a vector of 0s as a default result.

The input for `hodgerank` is a dictionary of preferences, where the
keys are the options and the preferences are arrays of the same size,
empty answers being designated as `np.nan`. The output is a dictionary
with the options as keys and the corresponding HodgeRank values.

Examples:

        >>> prefs1={0:np.array([5,3]),1:np.array([4,5]),2:np.array([3, np.nan]),3:np.array([5,2])}
        >>> hodgerank(prefs1)
        {0: 0.4642857142857137, 1: 0.7499999999999991, 2: -1.2499999999999987, 3: 0.0357142857142852}

        >>> prefs2={0:np.array([5,3]),1:np.array([4,5]),2:np.array([3, 1]),3:np.array([5,2])}
        >>> hodgerank(prefs2)
        {0: 0.5000000000000002, 1: 0.9999999999999998, 2: -1.4999999999999993, 3: 4.163336342344337e-16}

`prefs2` is an interesting case: We know from
[Jiang et al.
2011](.doc/preference/statistical_ranking_and_combinatorial_hodge_theory_jiang_et_al_2011.pdf "Statistical ranking and combinatorial Hodge theory")
that if the preferences are all complete, then HodgeRank is equivalent
to the sum of values under some linear transformation. That linear
transformation here is `$(x \cdot 2)+7$`, and yields the values
`{0: 8, 1: 9, 2: 4, 3: 7}`.

        >>> prefs3={0:np.array([4,np.nan,3]),1:np.array([3,4,np.nan]),2:np.array([np.nan, 3,4])}
        >>> hodgerank(prefs3)
        {0: 0.0, 1: 1.3877787807814457e-17, 2: 0.0}

        >>> prefs4={0:np.array([5,np.nan,3]),1:np.array([3,4,np.nan]),2:np.array([np.nan, 3,4])}
        >>> hodgerank(prefs4)
        {0: 0.3333333333333334, 1: -0.3333333333333334, 2: -1.1102230246251565e-16}

Going from `prefs3` to `prefs4` shows that HodgeRank can be manipulated
by the first voter: they simply increase their score of the first option
(which they like most anyway) and thereby make it the highest ranking
option in the global ranking.

        >>> prefs5={0:np.array([5,np.nan,3]),1:np.array([3,4,np.nan]),2:np.array([1, 3,4])}
        >>> hodgerank(prefs5)
        {0: 1.0000000000000002, 1: 5.551115123125783e-17, 2: -1.0000000000000004}

        >>> prefs6={0:np.array([1,1]),1:np.array([1,1]),2:np.array([1,1])}
        >>> hodgerank(prefs6)
        {0: 0.0, 1: 0.0, 2: 0.0}

        >>> prefs7={0:np.array([5,3]),1:np.array([4,5]),2:np.array([3, np.nan]),3:np.array([5,2]),4:np.array([np.nan,2])}
        >>> hodgerank(prefs7)
        {0: 0.6357142857142856, 1: 1.1357142857142855, 2: -0.971428571428572, 3: 0.3142857142857142, 4: -1.114285714285714}

        >>> prefs8={'a':np.array([5,3]),'b':np.array([4,5]),'c':np.array([3, np.nan]),'d':np.array([5,2])}
        >>> hodgerank(prefs8)
        {'a': 0.4642857142857137, 'b': 0.7499999999999991, 'c': -1.2499999999999987, 'd': 0.0357142857142852}
