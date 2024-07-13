[home](./index.md)
------------------

*author: niplav, created: 2024-04-22, modified: 2024-07-07, language: english, status: in progress, importance: 5, confidence: highly likely*

> __How to compare how similarly programs compute their outputs.__

Logical Correlation
====================

<!--TODO: wentworth post about eding programs as causal diagrams-->

In the [twin prisoners
dilemma](https://www.lesswrong.com/tag/psychological-twin-prisoner-s-dilemma),
I cooperate with my twin because we're implementing the same algorithm. If
we modify the twin slightly, for example to have a slightly longer right
index-finger-nail, I would still cooperate, even though we're different
algorithms, since little enough has been changed about our algorithms
that the internal states and the output are basically the same.

But it could be that I'm in a prisoner's dilemma with some program
`$p^{\star}$` that, given some inputs, returns the same outputs as I do,
but for completely different "reasons"—that is, the internal states
are very different, and a slight change in input would cause the output
to be radically different. Intuitively, my similarity to `$p^{\star}$`
is pretty small, because even though it gives the same output, it gives
that output for very different reasons, so I don't have much control
over its outputs by controlling my own computations.

Let's call this similarity of two algorithms the __logical correlation__
between the two algorithms, a term also used in [Demski & Garrabrant
2020](./cs/ai/alignment/agent_foundations/embedded_agency_demski_garrabrant_2020.pdf):

> One idea is that exact copies should be treated as 100% under
your “logical control”. For approximate models of you, or merely
similar agents, control should drop off sharply as logical correlation
decreases. But how does this work?

*—Abram Demski & Scott Garrabrant, [“Embedded Agency”](./cs/ai/alignment/agent_foundations/embedded_agency_demski_garrabrant_2020.pdf) p. 12, 2020*

Similarly:

> The reasoning behind cooperation does not involve a common cause of
all collaborators' decisions. Instead, the correlation may be viewed
as logical (Garrabrant et al., 2016): if I cooperate, then this implies
that all other implementations of my decision algorithm also cooperate.

*—Caspar Oesterheld, “Multiverse-wide Cooperation via Correlated Decision Making” p. 18, 2018*

We don't yet have a way of estimating the logical correlation between
different decision algorithms.

Thus: Consider proposing the most naïve formula (which we'll designate
by `$合$`[^2]) for logical correlation[^1]: Something that takes in
two programs and returns a number that quantifies how similarly the two
programs compute what they compute.

### Setup

Let a program `$p$` be a tuple of code for a [Turing
machine](https://en.wikipedia.org/wiki/Turing_Machine), intermediate
tape states after each command execution, and output. All in binary.

That is `$p=(c, t, o)$`, with `$c \in \{0, 1\}^+, t \in (\{0, 1\}^+)^+$` and `$o \in \{0, 1\}^+$`.
Let `$l=|t|$` be the number of steps that `$p$` takes to halt.

### Possible Desiderata

1. If possible, we would want our formula for logical correlation to be a [metric](https://en.wikipedia.org/wiki/Metric_space) on the space of programs:
	1. `$合(p, p)=0$`.
	2. [Symmetry](https://en.wikipedia.org/wiki/Symmetric_function): `$合(p_1, p_2)=合(p_2, p_1)$`.
	3. If `$p_1 \not=p_2$`, then `$合(p_1, p_2)>0$`.
	4. The [triangle inequality](https://en.wikipedia.org/wiki/Triangle_Inequality): `$合(p_1, p_3) \le 合(p_1, p_2)+合(p_2, p_3)$`.
2. If `$p_1$` and `$p_2$` have very similar outputs, and `$p_3$` has a very different output, then `$合(p_1, p_2)<合(p_1, p_3)$` (and `$合(p_1, p_2)<合(p_2, p_3)$`).
	1. I'm not *so sure* about this one: Let's say there's `$p$`, which outputs a binary string `$o \in \{0, 1\}$`, and `$p^{\not \sim}$`, which computes `$o$` in a completely different way, as well as `$p^{\lnot}$`, which first runs `$p$`, and then flips every bit on the tape, finally returning the negation of `$o$`. In this case, it seems that if `$p$` is a decision algorithm, it has far more "control" over the output of `$p^{\lnot}$` than over `$p^{\not \sim}$`.
	2. For the time being, I'm going to accept this, though ideally there'd be some way of handling the tradeoff between "computed the same output in a different way" and "computed a different output in a similar way".

### Formal Definition

Then a formula for the logical correlation `$合$` of two halting
programs `$p_1=(c_1, t_1, o_1), p_2=(c_2, t_2, o_2)$`, a tape-state
discount factor `$γ$`[^3], and a [string-distance metric](https://en.wikipedia.org/wiki/String_similarity_metric)
`$d: \{0, 1\}^+ \times \{0, 1\}^+ \rightarrow ℕ$` could be

<div>
        $$合(p_1, p_2, γ)=d(o_1, o_2)+0.5-\frac{1}{2+\sum_{k=0}^{\min(l_1, l_2)} γ^k \cdot d(t_1(l_1-k), t_2(l_2-k))}$$
</div>

The lower `$合$`, the higher the logical correlation between `$p_1$`
and `$p_2$`.

If `$d(o_1, o_2)<d(o_1, o_3)$`, then it's also the case that `$合(p_1, p_2, γ)<合(p_1, p_3, γ)$`.

One might also want to be able to deal with the fact that programs have
different trace lengths, and penalize that, e.g. amending the formula:

<div>
        $$合'(p_1, p_2, γ)=合(p_1, p_2, γ)+2^{|l_1-l_2|}$$
</div>

I'm a bit unhappy that the code doesn't factor into the logical
correlation, and ideally one would want to be able to compute the logical
correlation without having to run the program.

How does this relate to
[data=code](https://wiki.c2.com/?DataAndCodeAreTheSameThing)?

#### Desiderata Fulfilled?

Does this fulfill our desiderata from earlier? I'll assume that the
string distance `$d$` is a metric, in the mathematical sense.

1. `$合(p, p)=0$`. (The minimal logical correlation is 0.)

<!--TODO: check with brainfuck-->
<!--TODO: prove or disprove that this is a metric-->

[^1]: Actually not explained in detail anywhere, as far as I can tell.
[^2]: Suggested by GPT-4. Stands for [joining, combining, uniting](https://en.wiktionary.org/wiki/%E5%90%88#Definitions). Also "to suit; to fit", "to have sexual intercourse", "to fight, to have a confrontation with", or "to be equivalent to, to add up". Maybe I could've used one of the [ghost characters](https://en.wikipedia.org/wiki/Ghost_characters).
[^3]: Which is needed because tape states close to the output are more important than tape states early on.
