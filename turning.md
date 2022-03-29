[home](./index.md)
-------------------

*author: niplav, created: 2022-03-04, modified: 2022-03-26, language: english, status: notes, importance: 8, confidence: unlikely*

> __Representing inconsistent preferences with specific mathematical
structures can clarify thoughts about how to make those preferences
consistent while only minimally changing them. This is discussed in
the case of preferences over world states, represented by [directed
graphs](https://en.wikipedia.org/wiki/Directed_graph); and preferences
over [lotteries](https://en.wikipedia.org/wiki/Lottery_\(probability\))
of world states, represented by [vector
fields](https://en.wikipedia.org/wiki/Vector_field) over probability
[simplices](https://en.wikipedia.org/wiki/Simplex). Implications for
scenarios such as ontological crises are discussed.__

<!--TODO: Read Transitive Reduction, Graph Edit Distance on WP-->

Turning Some Inconsistent Preferences into Consistent Ones
===========================================================

> A kind of God-made (or evolution-created) fairness between species is
also unexpectedly found.

*– [Yew-Kwang Ng](https://en.wikipedia.org/wiki/Yew-Kwang_Ng), [“Towards Welfare Biology: Evolutionary Economics of Animal Consciousness and Suffering”](./doc/better_words/towards_welfare_biology_evolutionary_economics_of_animal_consciousness_and_suffering_ng_1995.pdf) p. 1, 1995*

> Random testing is simple in concept, often easy to implement, has been
demonstrated to effectively detect failures, is good at exercising systems
in unexpected ways (which may not occur to a human tester), and may be
the only practical choice when the source code and the specifications
are unavailable or incomplete.

*– Tsong Yueh Chen/Fei-Ching Kuo/Robert G. Merkel/T.H. Tse, [“Adaptive Random Testing: the ART of Test Case Diversity”](./doc/turning/adaptive_random_testing_chen_et_al_2010.pdf), 2010*

Consider an agent which displays (von Neumman-Morgenstern) inconsistent
preferences, for example choosing two incompatible options in the two
scenarios in the Allais paradox. We might want to interact with that
agent, e.g. trade with it, help it, or generally know how it will act. But
how to go about that if the agent displays inconsistent preferences?

One way we could approach the problem is by trying to turn those
inconsistent preferences consistent, i.e. constructing a function `$f: \succsim \mapsto \succeq$`
that takes in an inconsistent preference and transforms it into a
consistent preference, while retaining as much of the original structure
of the preference as possible (it would make little sense if we replaced
the original preference relation with indifference over all options).

Representing inconsistent preferences turns out to be key to constructing
`$f$`. I discuss two options for representing subsets of all possible
inconsistent preferences:

1. Inconsistent preferences over discrete options are represented via directed graphs
2. Inconsistent preferences over lotteries of options are represented via vector fields on probability simplices

Discrete Case
--------------

When we have discrete sets of options `$O$`, we can represent some
inconsistent preferences by using a directed graph `$G_{\succsim}=(V,E_{\succsim}), V=O, E_{\succsim} \subseteq O \times O$`.
The presence of an edge `$(o_1, o_2)$` would mean that `$o_1 \succsim
o_2$`, that is `$o_1$` is preferred to `$o_2$`.

The consistent equivalent to an inconsistent preference represented by a
directed graph would be a path graph `$G_{\succeq}=(V, E_{\succeq})$`
over the same set of vertices `$O$`.  The method for transforming
`$G_{\succsim}$` into `$G_{\succeq}$` would be by adding/deleting/merging
the minimal amount vertices from `$E_{\succsim}$`.

This leads to an interesting ethical consideration: is it a larger
change to a preference relation to add new information, combine
existing information, or remove information? It is discussed how to
incorporate those weights into an algorithm for minimally transforming
`$G_{\succsim}$` into `$G_{\succeq}$`.

### Encoding Inconsistencies

The two relevant von Neumman-Morgenstern axioms are completeness and
transitivity, with a directed graph one can also represent incompleteness
and intransitivity.

#### Incompleteness

Incompleteness (or incomparability) between two options `$o_1, o_2$`
can be represented by not specifying an edge between the two options,
that is `$(o_1, o_2) \not \in E, (o_2, o_1) \not \in E$`.

![](./img/turning/incomplete.png)

#### Intransitivity

Intransitivity can be represented by cycles in the graph:

![](./img/turning/intransitive.png)

#### Non-Encodable Inconsistencies

With option set `$\{a,b\}$` have preference `$a \succsim b$`, with
option set `$\{a,b,c\}$` have preferences
`$b \succsim a, a \succsim c, b \succsim c$`.

### Resolving Inconsistencies

![](./img/turning/unbalanced_cycle.png)

#### Intransitivity

#### Incompleteness

"Zipping" DAGs.

Continuous Case
----------------

### Vector Fields over Probability Simplices

Vector field over the probability simplex over the options (representing
local preferences over lotteries).

#### Encoding Inconsistencies

##### Incompleteness

* Minima/maxima in the vector field
* Discontinuities
* Undifferentiable points

##### Intransitivity

Curl in the vector field?

##### Discontinuities

Can only exist with incompleteness?

##### Dependence of Irrelevant Alternatives

#### Resolving Inconsistencies

Find mapping from vector field to another that makes the vector field
consistent by minimizing the amount of turning/shrinking the vectors
have to perform.

### Graphons

?

Look into extremal graph theory.

Implications for AI Alignment
------------------------------

### Ambitious Value Learning

Learn human values, check if known inconsistencies are encoded (to ensure
learning at the correct level of abstraction), then make consistent.

### Ontological Crises

If you know a mapping between objects from human to AI ontology, you
could find the mapping from the (consistent) human probability simplex
to the AI simplex?

Further Questions
------------------

* Is there a canonical way to turn graphs into path graphs with a minimal number of "operations"?
* Does every graph `$G$` have a unique graph `$G'$` so that `$G$` is the transitive closure of `$G'$`?

<!--
*epistemic status: butterfly idea, I really should learn more topology
and vector calculus, potentially very fruitful line of research in
theoretical ethics*

Consider an agent with inconsistent preferences. How can we represent
their inconsistent preferences so that they can be turned into consistent
variants of themselves, while minimally changing their structure?

One way to approach this is to represent the preferences as a directed
graph. In this case, we have for example an intransitive preference

![](https://niplav.github.io/img/turning/intransitive.png)

We can make this preference consistent by deleting an edge, but
unfortunately we don't have a unique solution to making this preference
consistent. I am interested in the combinatorics of turning a directed
graph into a [path graph](https://en.wikipedia.org/wiki/Path_graph) (or
its transitive closure) while making the minimal number of modificiations
(deleting edges, adding edges, merging edges) to the initial graph.

If we look at preferences over lotteries, we could represent a subset
of all possible inconsistent preferences as a vector field over the
probability simplex of all underlying options. Circular preferences
would then be represented by the curl of the vector field, violations
of continuity would be points in the vector field where the vectors
are "0": for example on the line simplex, it would be the vector field
"flipping around" at some point on the line (I don't know vector calculus
that well).

It might then be possible to define a function that minimally modifies
that vector field to convert it to a consistent preference relation
(i.e. a vector field that "flows toward a single option"). Defining
"minimally" is the trick here: I'm imagining something akin to taking
the integral over the rotation & size of the vectors of the difference
of the vector field before and after (I told you I don't really know
the math of that yet).

I suspect that there are interesting further extensions to be discovered
in extremal graph theory, for example graphons which look like they
might be able to represent more & different preferential inconsistencies,
but this is more of a hunch.

If solved, this could be relevant to ambitious value learning and
potential resolving ontological crises.

Here are some questions I have:

* I bet there is research on how to turn inconsistent preferences into consistent ones, but a cursory search hasn't shown me anything satisfactory yet. Where is it?
* I would be fairly sure that there is also research on how to turn arbitrary directed graphs into directed path graphs, but I don't know about it yet.
* What kinds of preferential inconsistencies can be represented via directed graphs/vector fields on probability simplices?
* What would the vector field over a probability simplex look like to be equivalent to a consistent preference?
* What is the topology of minimally transforming such a "inconsistent" vector field into a "consistent" vector field?
* Does any of this actually make sense?
-->
