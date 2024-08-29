[home](./index.md)
------------------

*author: niplav, created: 2023-11-04, modified: 2024-02-08, language: english, status: notes, importance: 8, confidence: likely*

> __Summary of a longer investigation into [inconsistent
preferences](./turning.html) and how to resolve them. I investigate
two different ways of representing inconsistent preferences, two
different methods for resolving them into consistent preferences,
how these perform on seven criteria, and how two of those criteria
are incompatible. I conclude by connecting the question to [ontological
crises](./cs/ai/alignment/ontological_crises/ontological_crises_in_artificial_agents_value_systems_de_blanc_2011.pdf),
and offer some ideas for further research in the area.__

تهافت الذكاء الاصطناعي
=======================

In 1947, John von Neumann and Oskar Morgenstern
published their book [Theory of Games and Economic
Behavior](https://en.wikipedia.org/wiki/Theory_of_Games_and_Economic_Behavior).
This has made a lot of people very angry and has been widely regarded
as a bad move.

Their famous theorem is deceptively simple. Given a set of options
`$\Omega$` (not further elaborated on), and a preference relation
on lotteries of those options satisfying four axioms (completeness,
transitivity, continuity, indepedence), one can construct a utility
function `$u: \Omega \rightarrow [0;1]$` that assigns real values to
all the options. The value of a lottery `$\mathcal{L}$`, then, is simply
the *expected* value of the elements in the lottery.

However.

There are some points of, ah, contention around the von
Neumman-Morgenstern setup. One of those is around the set `$\Omega$`:
the common examples include sets of fruits, or other cute edible & easily
handleable objects. Is `$\Omega$` assumed to be finite? Where do we get
it from‽

However, when pressed, proponents of vNM utility theory start talking
about how `$\Omega$` *really* is a set of universe-histories
or multiverse-histories. This introduces some problems: For
example, one can't guarantee that the resulting utility function is
[computable](https://www.lesswrong.com/s/PKKsrXtuptWzaKCjr/p/A8iGaZ3uHNNGgJeaD),
and every behavior can be interpreted as being [compatible with expected
utility maximization](https://www.lesswrong.com/posts/NxF5G6CJiof6cemTw).

But even leaving those aside, there is ample evidence that humans
don't fulfill the axioms stated above, at least in the case where
we partition the world into objects such as distinct amounts of
money. For example, humans violate the independence axiom in the
[Allais Paradox](https://en.wikipedia.org/wiki/Allais_Paradox),
and instead might have preferences with a more [involved
structure](./doc/psychology/on_the_structural_consistency_of_preferences_el_gamal_2013.pdf "On the Structural Consistency of Preferences").
Additionally, there has been some noises that [markets
may](https://www.lesswrong.com/posts/3xF66BNSC5caZuKyC/why-subagents)
(or [may
not](https://www.lesswrong.com/posts/bzmLC3J8PsknwRZbr/why-not-subagents)?)
violate the completeness axiom.

### Motivation

All of this points into a similar direction. Agents don't spring into
the world [fully formed](https://en.wikipedia.org/wiki/Athena#Birth),
instead they grow and develop. They might start out as collections of
dumber "agents", undergo pressure from exploitation, refactor their
models of the world and sometimes their preference, perform internal
bargaining and more.

If we assume that [there is a "natural" or "rational" structure for
preferences](https://www.lesswrong.com/posts/suxvE2ddnYMPJN9HD), then I
find it likely to assume that cognitive systems, before and during their
development, might not have preferences that conform to that structure.

Therefore it is useful to examine procedures to transform preferences
that don't have this "natural" structure into ones that do.

Since the standard model of rationality in economics is expected
utility maximization with preferences that conform to the vNM axioms,
I have mainly focused my efforts in that framework. This is not an
endorsement of the vNM axioms as a normative ideal for rationality,
I selected it purely out of convenience, and in the hope that whatever
the "true" theory of rational preference turns out to be, insights from
inconsistent preferences and their resolution will transfer to this
"true" theory (should it exist).

Representing Inconsistent Preferences
--------------------------------------

### With Deterministic Options

### With Lotteries

Algorithms for Resolution
--------------------------

### Minimizing Edit-Distance

### Hodge Decomposition

Desirable Criteria
-------------------

### Preserving Global Structure

### Preserving Local Structure

### Efficient Computation

Two Impossibility Theorems, with Two Interpretations
-----------------------------------------------------

### Impossibility Theorem: Statement

### Yay!

### Oh No

Relation to Ontological Crises
-------------------------------

Summary
--------

Further Ideas
--------------

Acknowledgements
------------------

This text is a distillation of work other people and I have done on the
theory of value formation. The distillation is completely my own work
and *highly* opinionated, thus all blame and some praise goes to me.

These people pushed this project forward, disagreed, were frustrated,
calmed down, were confused, went silent for a while and then came back:
Kaarel Hänni, Alexander Gietelink-Oldenziehl, Filip Sondej, Felix Harder.
I am grateful for their help.

See Also
----------

* [Using vector fields to visualise preferences and make them consistent (Michael Aird, Justin Shovelain, 2020)](https://www.lesswrong.com/posts/ky988ePJvCRhmCwGo/using-vector-fields-to-visualise-preferences-and-make-them)
* [Inferring utility functions from locally non-transitive preferences (Jan Kirchner, 2022)](https://www.lesswrong.com/posts/QZiGEDiobFz8ropA5/inferring-utility-functions-from-locally-non-transitive)
* [Value Formation: An Overarching Model (Thane Ruthenis, 2022)](https://www.lesswrong.com/posts/kmpNkeqEGvFue7AvA/value-formation-an-overarching-model)
* [0. The Value Change Problem: introduction, overview and motivations (Nora Ammann, 2023)](https://www.lesswrong.com/s/3QXNgNKXoLrdXJwWE/p/mHQHBEuFcEWRnitp4)
* [Value systematization: how values become coherent (and misaligned) (Richard Ngo, 2023)](https://www.lesswrong.com/posts/J2kpxLjEyqh6x3oA4/value-systematization-how-values-become-coherent-and)
* [Crystal Healing — or the Origins of Expected Utility Maximizers (Alexander Gietelink Oldenziel/Kaarel/RP, 2023)](https://www.lesswrong.com/posts/tiftX2exZbrc3pNJt/)
* [A logic to deal with inconsistent preferences (Bob Jacobs, 2023)](https://bobjacobs.substack.com/p/a-logic-to-deal-with-inconsistent)
