[home](./index.md)
-------------------

*author: niplav, created: 2022-04-05, modified: 2022-04-05, language: english, status: in progress, importance: 2, confidence: likely*

> __Solutions to the textbook “Algorithmic Game Theory”.__

Solutions to “Algorithmic Game Theory”
========================================

Chapter 1
----------

<!--
TODO
### 1.1

Inputs: A set of actions `$A_1$` for player `$1$`, and `$A_2$` for player
`$2$`, as well as utility functions `$u_1: A_1 \mapsto ℝ$` and
`$u_2: A_2 \mapsto ℝ$` for the two players.

	for $s_1, s_2$ in $2^{A_1} \times 2^{A_2}$:

Uhhh…hmm. Let's think about this one.
-->

### 1.3

Let `$g$` be a two-player game. Now construct a 3-player zero-sum game
`$g'$` as following: Add another player `$3$`, with one action, and let
the utility of that player be
`$u_3'(a_3, a_{-3})=0-(u_1(a_{-3})+u_2(a_{-3})$`.

Then the Nash equilibria of `$G$'$` are the same as for `$g$`: player
`$3$` can't deviate, and the utilities of the other players are not
affected by the actions of `$3$`. Therefore, the Nash equilibria in `$g'$`
are the same as for `$g$`, and equally hard to find—which means that
Nash equilibria for three-player zero-sum games are at least as hard to
find as for two-player games.
