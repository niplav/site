[home](./index.md)
-------------------

*author: niplav, created: 2021-10-14, modified: 2022-01-08, language: english, status: in progress, importance: 2, confidence: likely*

> __This page contains some solutions to exercises from the textbook
“Reactive Systems” by Ingólfsdóttir et al. 2007.__

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

I'm not going to draw all the images, I'm way too lazy for that.

* Using COM1: SmUni transitions to `$(\text{CM}|\text{CS}_1)\backslash\{\text{coin},\text{coffee}\}$` via `$\overline{\text{pub}}$`
* Using COM3: `$(\text{CM}|\text{CS}_1)\backslash\{\text{coin},\text{coffee}\}$` transitions to `$(\text{CM}_1|\text{CS}_2)\backslash\{\text{coin},\text{coffee}\}$` via `$τ$`, internally `$\text{coin}$`
* Using COM3: `$(\text{CM}_1|\text{CS}_2)\backslash\{\text{coin},\text{coffee}\}$` transitions to SmUni via `$τ$`, internally `$\text{coffee}$`

### 2.12

#### Defining a Bag

`$\text{Bag} \overset{\text{def}}{=} (\text{Cell}|\text{Cell}).\text{Bag}$`

This definition works by keeping two Cells running in parallel. If both
cells are emptied, the Bag restarts, otherwise it keeps its state.

#### Defining a FIFO queue

The two-place FIFO queue should have the following traces available
(for different values of `$x$` and `$y$`):

* `$\text{in}(x) \rightarrow \text{in}(y) \rightarrow \overline{\text{out}}(x) \rightarrow \overline{\text{out}}(y).\text{FIFO}$`
* `$\text{in}(x) \rightarrow \overline{\text{out}}(x).\text{FIFO}$`

(The case where `$x$` is input and output, and then `$y$` is input and
output, is equivalent to the second trace).

`$\text{FIFO} \overset{\text{def}}{=} (\text{Cell}+(\text{in}(x).\text{in}(y).\text{Cell}(x).\text{Cell}(y)).\text{FIFO}$`

This is much uglier than I thought it would be. Maybe there's a nicer
version? Just concatenating two cells doesn't work, of course.

Chapter 3
----------

### 3.1

Identity relation is an equivalence relation, as well as the universal
relation is.  The standard `$\le$` relation is not an equivalence relation
(but it is a preorder, since it is an order). However, the parity relation
`$M_2$` is.

### Stray Exercise 1

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

To be shown: `$\{(P|Q, Q|P) |\text{where }P,Q \text{ are CCS processes}\}$`
is a strong bisimulation.

I am slightly confused: doesn't strong bisimilarity apply to *states*,
and aren't `$P|Q$` and `$Q|P$` processes?

If there is no `$α$` so that either `$P$` or `$Q$` can transition to
another state, `$P|Q$` and `$Q|P$` are strongly bisimilar.

If `$P|Q \overset{α}{\rightarrow} P'|Q$`, then `$Q|P \overset{α}{\rightarrow} Q|P'$`
by first applying COM1 and then COM2, and so `$P'|Q$` and `$Q|P'$`
are strongly bisimilar.

Another idea: we can prove this by backward induction, e.g. assuming that
there is a final state `$P_f|Q_f$`, which can't transition further, and
then proving that every `$α$` transition that lands there is a strong
bisimulation, and induced back as well?

The same holds if `$Q$` can transition via `$α$`.

If `$(P|Q)\backslash \{α\} \overset{τ}{\rightarrow} P'|Q'$`, then
similarly `$(Q|P)\backslash \{α\} \overset{τ}{\rightarrow} Q|P$`
per COM3, so they're strongly bisimilar.

To be shown: `$\{(P|\mathbf{0}, P) |\text{where }P \text{ is a CCS process}\}$`
is a strong bisimulation.

Isn't this trivial? If `$P \overset{α}{\rightarrow} P'$`, then surely
also `$P|\mathbf{0} \overset{α}{\rightarrow} P'|\mathbf{0}$`, and if
`$P|\mathbf{0} \overset{α}{\rightarrow} P'|\mathbf{0}$`, then
`$P \overset{α}{\rightarrow} P'$`. `$τ$`-transitions are not possible here.

To be shown: `$\{((P|Q)|R,P|(Q|R)) |\text{where }P,Q,R \text{ are CCS processes}\}$`
is a strong bisimulation.

Assume that `$(P|Q)|R$` makes an `$α$` transition. Then:

* If `$(P|Q)$` made the transition, then:
	* If `$P$` made the transition, then on the right side `$P$` can also make the transition
	* If `$Q$` made the transition, then on the right side `$(Q|R)$` can make the transition (e.g. to `$(Q'|R)$`)
* If `$R$` made the transition, then on the right side `$(Q|R)$` can make the transition (e.g. to `$(Q|R')$`)

Otherwise asume that `$(P|Q)|R \overset{τ}{\rightarrow} (P|Q')|R'$`. Then
there must be a `$β$` so that `$Q \overset{β}{\rightarrow} Q'$`
and `$R \overset{\overline{β}}{\rightarrow} R'$` (or `$R$` outputs
`$β$` and `$Q$` inputs `$β$`, but that's symmetric). Then similarly
`$P|(Q|R) \overset{τ}{\rightarrow} P|(Q'|R')$` by the same internal
`$β$` transitions.

All other cases are symmetric, and I won't enumerate them here.

Since these relations are all bisimulations, it is clear that for any
`$P,Q,R$`, the mentioned combined processes are bisimilar.

> Find three CCS processes `$P,Q,R$` such that `$(P+Q)|R \not \sim (P|R)+(Q|R)$`.

I haven't been able to solve this completely yet. Let's take something
like `$P \overset{\text{def}}{=}a.a.a.a.a$`, `$Q \overset{\text{def}}{=}a.a.a.a.b$`
and `$R \overset{\text{def}}{=}a.a.a.a.(a+b)$`. Then it *could* be the
case that in a bisimulation game, the attacker has chosen the `$P$`
path on the left hand side, while the defender has chosen the `$Q$`
path on the right hand side. But this is not guaranteed.

### 3.30

> Show that observational equivalence is the largest symmetric relation
`$\mathcal{R}$` satisfying that whenever `$s_1 \mathcal{R} s_2$` then, for
each action `$α$` (including `$τ$`), if `$s_1 \overset{α}{\Rightarrow}
s_1'$` then there is a transition `$s_2 \overset{α}{\Rightarrow} s_2'$`
such that `$s_1' \mathcal{R} s_2'$`.

Assume there is a relation `$\mathcal{R}_{\star}$` which satisfies the
conditions given for `$\mathcal{R}$` above. Then there must be two states
`$s_{\star}, t_{\star}$` so that if
`$s_{\star} \overset{α}{\Rightarrow} s_{\star}'$`, then there must be
a transition `$t_{\star} \overset{α}{\Rightarrow} t_{\star}'$` so that
`$s_{\star}' \mathcal{R}_{\star} t_{\star}'$`. Since
`$\mathcal{R}_{\star}$` is supposed to be symmetric, the same must hold
for `$t_{\star}$`: `$t_{\star} \overset{α}{\Rightarrow} t_{\star}'$`
implies that there is a transition `$s_{\star} \overset{α}{\Rightarrow} s_{\star}'$`
so that `$t_{\star}' \mathcal{R}_{\star} s_{\star}'$`.

We now have to determine whether, if we know that `$s_{\star} \mathcal{R}_{\star} t_{\star}$`,
we also know that `$s_{\star} \approx t_{\star}$`. Then there are four different
cases:

* If `$s_{\star} \overset{α}{\Rightarrow} s_{\star}'$` is realized by `$s_{\star} \overset{α}{\rightarrow} s_{\star}'$` in the LTS, then this is equivalent to the definition of observational equivalence.
* If `$s_{\star} \overset{α}{\Rightarrow} s_{\star}'$` is realized by `$s_{\star} \overset{α}{\rightarrow} s_{\star}'' \overset{τ}{\rightarrow} s_{\star}'$` in the LTS, then there must be a `$t_{\star}''$` so that `$s_{\star}'' \mathcal{R}_{\star} t_{\star}''$` (per definition in the exercise), so we can take that relation as belonging to `$\approx$`.
* If `$s_{\star} \overset{α}{\Rightarrow} s_{\star}'$` is realized by `$s_{\star} \overset{τ}{\rightarrow} s_{\star}'' \overset{α}{\rightarrow} s_{\star}'$` in the LTS, then there must be a `$t_{\star}''$` so that `$s_{\star}'' \mathcal{R}_{\star} t_{\star}''$`, only this time via a `$τ$` transition (i.e. `$t_{\star} \overset{τ}{\rightarrow} t_{\star}''$`). So we can take that relation as belonging to `$\approx$`. (This doesn't work! What if `$t_{\star} \overset{α}{\Rightarrow} t_{\star}'$` is realized by `$t_{\star} \overset{α}{\rightarrow} t_{\star}'' \overset{τ}{\rightarrow} t_{\star}'$`? Then we can't just take the first part of the transition and declare it to be a `$τ$` transition. Hmmm.)
* If `$s_{\star} \overset{α}{\Rightarrow} s_{\star}'$` is realized by `$s_{\star} \overset{α}{\rightarrow} s_{\star}'' \overset{τ}{\rightarrow} s_{\star}'$`, then we can again just chop off the last transition and declare the rest to be the `$α$` transition, so that now `$s_{\star} \approx t_{\star}$` and `$s_{\star}'' \approx t_{\star}'$`.

Since every `$\rightarrow$` transition is also a weak transition,
there can be no observational equivalence that isn't also in
`$\mathcal{R}_{\star}$`. So `$\mathcal{R}_{\star}$` is the biggest
observational equivalence `$\approx$`.

### 3.37

`$s \not \sim t$`. Winning strategy for the attacker:

* `$t \overset{a}{\rightarrow} t_1$`, defender answers with `$s \overset{a}{\rightarrow} s_1$`
* `$t_1 \overset{b}{\rightarrow} t_2$`, defender answers with `$s_1 \overset{b}{\rightarrow} s_2$`
* `$s_2 \overset{b}{\rightarrow} s_2$`, defender can't transition anywhere using `$b$`

`$s \sim u$`. Winning strategy for the defender:

* In `$(s, u)$`
	* If the attacker plays `$\overset{a}{\rightarrow} s_1$`, play `$\overset{a}{\rightarrow} u_1$`
	* If the attacker plays `$\overset{a}{\rightarrow} u_1$`, play `$\overset{a}{\rightarrow} s_1$`
* In `$(s_1, u_1)$`
	* If the attacker plays `$\overset{b}{\rightarrow} s_2$`, play `$\overset{b}{\rightarrow} u_3$`
	* If the attacker plays `$\overset{b}{\rightarrow} u_3$`, play `$\overset{b}{\rightarrow} s_2$`
* In `$(s_2, u_3)$`
	* If the attacker plays `$\overset{b}{\rightarrow} s_2$`, play `$\overset{b}{\rightarrow} u_2$`
	* If the attacker plays `$\overset{b}{\rightarrow} u_2$`, play `$\overset{b}{\rightarrow} s_2$`
	* If the attacker plays `$\overset{a}{\rightarrow} s$`, play `$\overset{a}{\rightarrow} u$`
	* If the attacker plays `$\overset{a}{\rightarrow} u$`, play `$\overset{a}{\rightarrow} s$`
* In `$(s_2, u_2)$`
	* If the attacker plays `$\overset{b}{\rightarrow} s_2$`, play `$\overset{b}{\rightarrow} u_2$`
	* If the attacker plays `$\overset{b}{\rightarrow} u_2$`, play `$\overset{b}{\rightarrow} s_2$`
	* If the attacker plays `$\overset{a}{\rightarrow} s$`, play `$\overset{a}{\rightarrow} u$`
	* If the attacker plays `$\overset{a}{\rightarrow} u$`, play `$\overset{a}{\rightarrow} s$`

Strong bisimulation relating the pair of processes:
`$\mathcal{R}=\{(u,s), (u_1, s_1), (u_3, s_2), (u_2, s_2)\}$`.

`$s\not \sim v$`. Winning strategy for the attacker:

* `$s \overset{a}{\rightarrow} s_1$`, defender answers with `$v \overset{a}{\rightarrow} v_1$`
* `$s_1 \overset{b}{\rightarrow} s_2$`
	* defender answers with `$v_1 \overset{b}{\rightarrow} v_2$`
		* `$s_2 \overset{b}{\rightarrow} s_2$`
		* defender can't transition using `$b$` from `$v_2$`
	* defender answers with `$v_1 \overset{b}{\rightarrow} v_3$`
		* `$s_2 \overset{a}{\rightarrow} s$`
		* defender can't transition using `$a$` from `$v_3$`

### 3.41

Assume that there is some `$α$` that the attacker would be able to play
`$s \overset{α}{\Rightarrow} s_3$`, but not `$s \overset{α}{\rightarrow}
s'$`. Then the `$\overset{α}{\Rightarrow}$` would decompose into
`$s \overset{τ}{\rightarrow}^+ s_1 \overset{α}{\rightarrow} s_2 \overset{τ}{\rightarrow}^* s_3$`.
So the only additional possible action the attacker could additionally
play would be `$τ$`. But in this case, the defender can answer by doing
nothing, i.e. idling on the same state (see p. 89). So the additional
`$τ$` transition doesn't give the attacker any useful moves, and both
versions of the game are equivalent.

### Stray Exercise 2

> For example, you should be able to convince yourself
that the LTS associated with the CCS expression
`$a_1.\mathbf{0}|a_2.\mathbf{0}|\dots|a_n.\mathbf{0}$` has `$2^n$` states.

Actually, I don't have a good idea of how to put this into LTS form?
I would have to invent a starting state `$s_0$`, or maybe a set of
`$n$` starting states, or perhaps `$2^n$` starting states? Then those
would transition to `$\mathbf{0}$` via any subset of
`$\{a_1, a_2, \dots, a_n\}$`.

I should clarify how this is done.

Chapter 4
----------

### 4.1

Show that the set of strings `$A^*$` over an alphabet `$A$` with prefix
ordering `$\le$` is a poset (prefix ordering is for all `$s, t \in A^*: s \le t$`
iff there exists a `$w \in A^*$` so that `$sw=t$`).

* Reflexive: Yes, `$s$` is a prefix for `$s$` with `$w=ε$`.
* Antisymmetric: Yes, if `$sw=t$` and `$tw=s$`, then `$sw=tw$`, so `$s=t$` and `$w=ε$`.
* Transitive: Yes, if `$r$` is a prefix for `$s$` with `$v$` and `$s$` is a prefix for `$t$` with `$w$`, then `$r$` is a prefix for `$t$` with `$vw$`.

<!--TODO: finish with other examples-->

### 4.2

> Is the poset `$(2^S, \subseteq)$` totally ordered?

No: Let `$S=\{a,b,c\}$`, then it is the case that
`$\{a,b\} \not \subseteq \{b,c\}$` and `$\{b,c\} \not \subseteq \{a,b\}$`.

### 4.3

> Prove that the lub and the glb of `$X$` are unique, if they exist.

`$d$` must be an upper bound for `$X$`, and `$d \sqsubseteq d'$` for every
upper bound `$d' \in D$` of `$X$`. Per antisymmetry of `$\sqsubseteq$`,
there can be no `$d'$` so that `$d' \sqsubseteq d$` and `$d \sqsubseteq
d'$` with `$d' \not = d$`. And for `$d$` to be an upper bound, then it
must be comparable to every other upper bound of `$X$`, so there is no
uncomparable least other upper bound `$d'$`.

The same argument applies symmetrically to the greatest lower bound,
and is not worth elaborating.

<!--
### Stray Exercise 3

p. 99, prove snd part of Tarski's fixed point theorem.

TODO
-->

### 4.9

Least fixed point:

Start with `$d=\emptyset$`. Then `$f^0(d)=\{2\}$`, and `$f^1(d)=\{2\}$`
as well. So `$\{2\}$` is the least fixed point.

Largest fixed point:

Start with `$d=\{0,1,2\}$`. Then `$f^0(d)=\{1,2\}$`, and
`$f^1(d)=\{1,2\}$`. So `$\{1,2\}$` is the largest fixed point.

### Stray Exercise 4

> We note that if `$\mathcal{R}, \mathcal{S} \in 2^{(\text{Proc} \times \text{Proc})}$`
and `$\mathcal{R} \subseteq \mathcal{S}$` then
`$\mathcal{F}(\mathcal{R}) \subseteq \mathcal{F}(\mathcal{S})$`,
that is, the function `$\mathcal{F}$` is monotonic over
`$(2^{(\text{Proc} \times \text{Proc})}, \subseteq)$`.

Assume that `$\mathcal{R} \subseteq \mathcal{S}$`, but
`$\mathcal{F}(\mathcal{R}) \not \subseteq \mathcal{F}(\mathcal{S})$`
(that is, `$\mathcal{F}(\mathcal{S}) \subset \mathcal{F}(\mathcal{R})$`).

Then there must be a `$(p,q) \in \mathcal{F}(\mathcal{R})$`
(`$p, q \in \text{Proc}$`) that is not in `$\mathcal{F}(\mathcal{S})$`.

Then there are `$(p', q') \in \mathcal{R}$` so that `$p, q$` can transition
to `$p', q'$` via some `$α$`, and `$(p', q') \not \in \mathcal{S}$`. But
that can't be the case, since we assumed that `$\mathcal{R} \subseteq \mathcal{S}$`.
This is a contradiction.

Chapter 5
----------

### 5.1

`$\langle \cdot b \cdot \rangle \{s_1, t_1\}=\{t_1\}$`

`$[ \cdot b \cdot ] \{s_1, t_1\}=\{s,t,t_1\}$`
