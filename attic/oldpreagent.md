[home](./index.md)
-------------------

*author: niplav & Alexander Gietelink Oldenziel, created: 2023-05-24, modified: 2023-07-06, language: english, status: draft, importance: 9, confidence: likely*

> __Not sure yet.__

Pre-Agent Theory
==================

In 1947, John von Neumann and Oskar Morgenstern published their book
Theory of Games and Economic Behavior. This has made a lot of people
very angry and has been widely regarded as a bad move.

The theorem is deceptively simple. Given a set of options `$\Omega$`
(not further elaborated on), and a preference relation on lotteries
of those options satisfying four axioms (completeness, transitivity,
continuity, indepedence), one can construct a utility function `$u: \Omega \rightarrow [0;1]$`
that assigns real values to all the options. The value of a lottery
`$\mathcal{L}$`, then, is simply the *expected* value of the elements
in the lottery.

However.

There are some points of, ah, contention around the von
Neumman-Morgenstern setup. One of those is around the set `$\Omega$`:
the common examples include sets of fruits, or other cute edible &
easily handleable objects. (Is `$\Omega$` assumed to be finite?)

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

All of this points into a similar direction. Agents don't spring into
the world [fully formed](https://en.wikipedia.org/wiki/Athena#Birth),
instead they grow and develop. They might start out as collections of
dumber "agents", undergo pressure from exploitation, refactor their
models of the world and sometimes their preference, perform internal
bargaining and more.
