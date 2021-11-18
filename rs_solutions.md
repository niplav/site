[home](./index.md)
-------------------

*author: niplav, created: 2021-10-14, modified: 2021-11-18, language: english, status: in progress, importance: 2, confidence: likely*

> __This page contains some solutions to exercises from the textbook
“Reactive Systems” by Ingólfsdóttir et al.__

Solutions to “Reactive Systems”
================================

Chapter 2
----------

### 2.1

> Give a CCS process which describes a clock that ticks at least once
and may stop ticking after each clock tick.

`$\text{Clock} \overset{\text{def}}{=} (\text{tick}.\mathbf{0}+\text{tick}.\text{Clock})$`

### 2.2

> Give a CCS process which describes a coffee machine that may behave
like that given by (2.1) but may also steal the money it receives and
fail at any time.

This exercise is not quite well-defined. Should it sometimes take the
money and offer nothing in return, but continue functioning, or should
it actually fail sometimes and break down? The former case would be
described by

`$\text{CTM} \overset{\text{def}}{=} \text{coin}.(\text{CTM}+\overline{\text{coffee}}.\text{CTM}+\overline{\text{tea}}.\text{CTM})$`,

the latter by

`$\text{CTM} \overset{\text{def}}{=} \text{coin}.(\text{CTM}+\mathbf{0}+\overline{\text{coffee}}.\text{CTM}+\overline{\text{tea}}.\text{CTM})$`

Hey look! `$+$` is commutative here!

### 2.3

> A finite process graph `$T$` is a quadruple `$(\mathcal{Q}, A, \delta, q_0)$`, where  
• `$\mathcal{Q}$` is a finite set of states,  
• `$A$` is a finite set of labels,  
• `$q_0 \in \mathcal{Q}$` is the start state, and  
• `$\delta: \mathcal{Q} \times A \rightarrow 2^{\mathcal{Q}}$` is the transition function.  

> Using the operators introduced so far, give a CCS process that describes `$T$`.

<div>
	$$ T=q_0.\underset{a_1 \in A}{\mathbf{+}} (a_1. \underset{q_1 \in δ(q_0, a_1)}{\mathbf{+}} (q_1.\underset{a_2 \in A}{\mathbf{+}} (a_2. \underset{q_2 \in δ(q_1, a_2)}{\mathbf{+}} (q_2. \cdots))))$$
</div>

where `$\mathbf{+}$` is _supposed_ to be a big iterative operator like
`$\sum$`, if only I could get MathJax to accept `\scalerel`. The equation
is nested infinitely deep at most places that result in a loop that
doesn't include `$q_0$`, and in some places end with `$.T$`, if `$q_0
\in δ(q_n,a)$`.

### 2.4

> Consider the following LTS:

![A cyclic diagram for exercise 2.4, described further below.](./img/rs_solutions/diagram_2_4.png "A cyclic diagram for exercise 2.4, described further below.")

> Define the LTS as a triple
`$(\text{Proc}, \text{Act}, \{\overset{α}{\rightarrow}|α \in \text{Act}\})$`.
Use sketches to illustrate the reflexive closure, symmetric closure and
transitive closure of the binary relation `$\overset{α}{\rightarrow}$`?

The process, in triple form, is
`$(\{s, s_1, s_2, s_3\}, \{a\}, \overset{a}{\rightarrow}=\{(s, s_1), (s_1, s_2), (s_2, s_3), (s_3, s)\})$`.

I'm not sure about the sketch part, but I can try to describe the
different closures.

The reflexive closure of `$\overset{a}{\rightarrow}$` would additionally
contain the elements
`$\{(s,s), (s_1, s_1), (s_2, s_2), (s_3, s_3)\}$`.

The symmetric closure is similarly easy to generate: it additionally
contains the elements `$\{(s_1, s), (s_2, s_1), (s_3, s_2), (s, s_3)\}$`.

The transitive closure additionally contains the elements from the set
`$\{(s, s_2), (s, s_3), (s_1, s_3), (s_1, s), (s_2, s), (s_2, s_1), (s_3, s_1), (s_3, s_2)\}$`.

### 2.5

The set of reachable states includes all states: `$p, p_1$` and `$p_2$`.

### 2.6

* `$a.b.A+B$` ✓
* `$(a.\mathbf{0}.\overline{a}.A)\backslash \{a,b\}$` ✓
* `$(a.\mathbf{0}|\overline{a}.A)\backslash \{a,τ\}$` ✗: `$τ$` can't be excluded
* `$a.B+[a/b]$` ✗: a renaming is not a process
* `$τ.τ.B+\mathbf{0}$` ✓
* `$(a.B+b.B)[a/b, b/a]$` ✓
* `$(a.B+τ.B)[a/τ, b/a]$` ✓
* `$(a.b.A+\overline{a}.\mathbf{0})|B$` ✓
* `$(a.b.A+\overline{a}.\mathbf{0}).B$` ✗: the object in the parentheses is not a label, but a process
* `$(a.b.A+\overline{a}.\mathbf{0})+B$` ✓
* `$(\mathbf{0}|\mathbf{0})+\mathbf{0}$` ✓

### 2.7

> Use the rules of SOS semantics for CCS to derive the LTS for the
process `$\text{SmUni}$` defined by (2.4). (Use the definition of CS in
Table 2.1.)

As a refresher:

* `$\text{SmUni}\overset{\text{def}}{=}(\text{CM}|\text{CS})\backslash \text{coin} \backslash \text{coffee}$`
* `$\text{CM}\overset{\text{def}}{=}\text{coin}.\overline{\text{coffee}}.\text{CM}$`
* `$\text{CS}\overset{\text{def}}{=}\overline{\text{pub}}.\overline{\text{coin}}.\text{coffee}.\text{CS}$`

<!--TODO-->

Chapter 3
----------

### 3.1

Identity relation is an equivalence relation, as well as the universal
relation is.  The standard `$\le$` relation is not an equivalence relation
(but it is a preorder, since it is an order). However, the parity relation
`$M_2$` is.

### Unnumbered Exercise

> To answer these questions, consider the coffee and tea machine CTM
defined in (2.2) and compare it with the following machine:

<div>
	$$\text{CTM}'\overset{\text{def}}{=} \text{coin}.\overline{\text{coffee}}.\text{CTM}' + \text{coin}.\overline{\text{tea}}$$
</div>

> You should be able to convince yourself that CTM and CTM' afford the
same traces. (Do so!)

It suffices to show that traces of one recursive iteration of CTM and CTM'
are equivalent. The trace of CTM' is
`$\{(\text{coin}, \overline{\text{coffee}}),(\text{coin}, \overline{\text{tea}})\}$`
(choose at the beginning, then insert coin & get beverage), the trace
of CTM is
`$\{(\text{coin}, \overline{\text{coffee}}), (\text{coin}, \overline{\text{tea}})\}$`
(insert coin, then choose).

### 3.2

> 1\. Do the processes (CA|CTM)\\{coin, coffee, tea} and (CA|CTM')\\{coin,
coffee, tea} defined above have the same completed traces?

Yes. Both processes start able to making the coin transition. Then
(CA|CTM') either finds itself in the coffee arm, makes the coffee
transition and returns to the starting state, or gets stuck only emitting
tea, but only accepting coffee. (CA|CTM) decides after the first coin
transition; if CTM transitions into the tea arm, we have a deadlock,
but if it transitions into the coffee arm, it can transition and returns
to the starting state.

For them to have different traces, CTM in (CA|CTM) would need to decide
which arm to transition into by knowing which transitions are available
in CA, which isn't included in the formalism.

Both processes have traces that can be described by the regular expression
`coin(,coffee,coin)*`

> 2\. Is it true that if P and Q are two CCS processes affording the
same completed traces and L is a set of labels then P\L and Q\L also
have the same completed traces?

Yes. The restriction operator \ only restricts transitions outside of
the process it applies to, inside that process the same transitions can
still occur.

### 3.3

The strong bisimulation of `$P$` and `$Q$` is
`${\mathcal{R}}=\{(P,Q),(P,Q_2),(P_1,Q_1),(P_1,Q_3)\}$`.

To show that this relation is a bisimulation, we examine all steps in
the model:

For `$(P,Q)$`: `$P$` transitions to `$P_1$` via `$a$`, and `$Q$`
transitions to `$Q_1$` via `$a$`, with `$(P_1, Q_1)$` in `$\mathcal{R}$`.  
`$Q$` transitions to `$Q_1$` via `$a$`, and `$P$` transitions to `$P_1$`
via `$a$`, with the same relation as above.

For `$(P,Q_2)$`: `$P$` transitions to `$P_1$` via `$a$`, and `$Q_2$`
transitions to `$Q_3$` via `$a$`, with `$(P_1, Q_3)$` in `$\mathcal{R}$`.
`$Q_2$` transitions to `$Q_3$` via `$a$`, and `$P$` transitions to `$P_1$`
via `$a$`, with the same relation as above.

For `$(P_1,Q_1)$`: `$P_1$` transitions to `$P$` via `$b$`, and `$Q_1$`
transitions to `$Q$` via `$c$`, with `$(P, Q)$` in `$\mathcal{R}$`
(the same holds for the transition action `$b$` instead of `$c$` and
`$Q_2$` instead of `$Q$`).
`$Q_1$` transitions to `$Q$` via `$b$`, and `$P_1$` transitions to `$P$`
via `$b$`, with the same relation as above (and, similarly, also with
`$c$` and `$Q_2$`).

For `$(P_1,Q_3)$`: `$P_1$` transitions to `$P$` via `$b$`, and `$Q_3$`
transitions to `$Q$` via `$b$`, with `$(P, Q)$` in `$\mathcal{R}$`
(the same holds for the transition action `$c$` instead of `$b$` and
`$Q_2$` instead of `$Q_3$`).
`$Q_3$` transitions to `$Q$` via `$b$`, and `$P_1$` transitions to `$P$`
via `$b$`, with the same relation as above (and, similarly, also with
`$c$` and `$Q_2$` instead of `$Q$`).

### 3.9

This screams after a proof by induction.

Induction basis: If `$σ$` is a label, that is, if there exists an action
`$α=σ$`, then the definitions for strong bisimulation and string
bisimulation coincide (I'm not gonna write it all out, sorry).

Induction assumption: Assume that if `$σ$` is a sequence of actions, then
two states `$s$` and `$s'$` are string bisimilar off they are strongly
bisimilar.

Induction step:

String bisimilarity `$\Rightarrow$` strong bisimilarity:

If we know that `$s_1 \mathcal{R} s_2$` are string bisimilar
by a transition `$σα$`, where `$α$` is a single action. Then there must be
some `$s_1'', s_2''$` so that `$s_1 \overset{σα}{\rightarrow} s_1''$`
and `$s_2 \overset{σα}{\rightarrow} s_2''$` and `$s_1'' \mathcal{R} s_2''$`,
and there must be some
`$s_1'$`, `$s_2'$` so that `$s_1 \overset{σ}{\rightarrow} s_1'$` and
`$s_2 \overset{σ}{\rightarrow} s_2'$` with `$s_1' \mathcal{R} s_2'$`
(and the other way around, with `$s_1$` and `$s_2$` exchanged), where
`$s_1'$` transitions to `$s_1''$` via `$α$`. Then the induction
assumption holds, and we know that the states are also strongly bisimilar.

Strong bisimilarity `$\Rightarrow$` string bisimilarity:

This is equivalent to the induction basis: if `$s_1 \mathcal{R} s_2$`
strongly bisimilar via `$β$`, then they are also string bisimilar via
`$σ=β$`.

### 3.12
