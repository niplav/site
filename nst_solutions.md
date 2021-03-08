[home](./index.md)
-------------------

*author: niplav, created: 2019-03-20, modified: 2021-03-02, language: english, status: in progress, importance: 2, confidence: likely*

> __[“Naive Set
> Theory”](https://en.wikipedia.org/wiki/Naive_Set_Theory_\(book\))
> by [Paul Halmos](https://en.wikipedia.org/wiki/Paul_Halmos) is a short
> introduction to set theory. Here, I present solutions to the explicitely
> stated exercises and problems in that book.__

Solutions to “Naïve Set Theory“
================================

Section 3
---------

### Exercise 1

It seems like there is no way one could use either insetting (putting
a given set into another set) and pairing or pairing on two different
inputs to obtain the same set. However, if one sees pairing the same set,
then pairing `$\emptyset$` with `$\emptyset$` would result in `$\{\emptyset\}$`,
which is also the result of insetting `$\emptyset$`.

Proof:

Insetting and pairing must have different results because insetting
will always result in a set with 1 element, and pairing will always
result in a set with 2 elements. Therefore, they can't be the same set.

Pairing the sets a, b and c, d can't result in the same set unless
`$a=c$` and `$b=d$` or `$a=d$` and `$b=c$`. Otherwise, `$\{a,b\}$` would contain
at least one element not in `$\{c,d\}$`.

□

Section 4
---------

### Exercise 1

I am not exactly sure what I'm supposed to do here. I guess
"observe" means "prove" here, so "prove that the condition
has nothing to do with the set B".

Proof:

<div>
	$$(A \cap B) \cup C = A \cap (B \cup C) \Leftrightarrow C \subset A\\
	(A \cup C) \cap (B \cup C) = A \cap (B \cup C) \Leftrightarrow C \subset A\\
	A \cup C = A \Leftrightarrow C \subset A$$
</div>

The last statement is trivially true.

□

Section 5
----------

### Some Easy Exercises

`$A-B=A \cap B'$`

Proof:

`$A-B=\{a | a \in A \land a \not \in B\}=\{a | a \in A \land a \in B'\}=A \cap B'$`

□

`$A \subset B \hbox{ if and only if } A-B=\emptyset$`

Proof:

<div>
	$$A \subset B \Leftrightarrow \forall a \in A:\\
	a \in B \Leftrightarrow \exists C:\\
	B=A \cup C \Leftrightarrow A-(A \cup C)=\emptyset \Leftrightarrow A-B=\emptyset$$
</div>

□

`$A-(A-B)=A \cap B$`

Proof:

<div>
	$$ A-(A-B)=\\
	A-(A \cap B')=\\
	A \cap (A \cap B')'=\\
	A \cap (A' \cup B)=\\
	A \cap A' \cup A \cap B=\\
	\emptyset \cup A \cap B=\\
	A\cap B$$
</div>

□

`$A \cap (B-C)=(A \cap B)-(A \cap C)$`

Proof:

<div>
	$$(A \cap B)-(A \cap C)=\\
	(A \cap B) \cap (A \cap C)'=\\
	(A \cap B) \cap (A' \cup C')=\\
	(A \cap B \cap A') \cup (A \cap B \cap C')=\\
	A \cap B \cap C'=\\
	A \cap (B-C)$$
</div>

□

`$A \cap B \subset (A \cap C) \cup (B \cap C')$`

Proof:

<div>
	$$A \cap B \subset (A \cap C) \cup (B \cap C')\\
	=((A \cap C) \cup B) \cap ((A \cap C) \cup C')\\
	=((A \cap C) \cup B) \cap ((A \cup C') \cap (C \cup C'))\\
	=((A \cap C) \cup B) \cap (A \cup C')\\
	=(A \cup B) \cap (C \cup B) \cap (A \cup C')$$
</div>

`$A \cap B \subset (A \cup B) \cap (C \cup B) \cap (A \cup C')$` is true
because `$A \subset (A \cup B)$` and `$B \subset (C \cup B)$` and
`$A \subset (A \cup C')$`.

□

`$ (A \cup C) \cap (B \cup C') \subset A \cup B $`

Proof:

<div>
	$$ (A \cup C) \cap (B \cup C')\\
	= ((A \cup C) \cap B) \cup ((A \cup C) \cap C')\\
	= ((A \cup C) \cap B) \cup A\\
	= (A \cap B) \cup (C \cap B) \cup A \subset A \cup B $$
</div>

This is the case because `$(A \cap B) \cup (C \cap B) \subset B$` (since
intersections with `$B$` are subsets of `$B$`), and the union with `$A$`
doesn't change the equation.

□

### Exercise 1

To be shown: The power set of a set with n elements has `$2^n$` elements.
Proof by induction.

Proof:

Induction base: The power set of the empty set contains 1 element:

`$|P(\emptyset)|=|{\emptyset}|=1=2^0=2^{|\emptyset|}$`

Induction assumption:

`$|P(A)|=2^{|A|}$`

Induction step:

To be shown: `$|P(A \cup \{a\}|=2*2^{|A|}=2^{|A|+1}$`.

`$P(A \cup \{a\})$` contains two disjunct subsets: `$P(A)$` and `$N=\{\{a\}\cup S | S \in P(A)\}$`.
Those are disjunct because every element in `$N$`
contains `$a$` (`$\forall n \in N: a \in n$`), but there is no element of
`$P(A)$` that contains `$a$`. Also, it holds that `$P(A) \cup N=P(A \cup\{a\})$`,
because elements in the power set can either contain `$a$`
or not, there is no middle ground. It is clear that `$|N|=|P(A)|$`,
therefore `$|P(A \cup \{a\})|=|P(A)|+|N|=2*|P(A)|=2*2^{|A|}=2^{|A|+1}$`.

□

### Exercise 2

To be shown:

`${\cal{P}}(E) \cap {\cal{P}}(F)={\cal{P}}(E \cap F)$`

Proof:

If `$S \in {\cal{P}}(E \cap F)$`, then `$\forall s \in S: s \in E \cap F$`. Therefore,
`$S \subset E$` and `$S \subset F$` and thereby `$S \in {\cal{P}}(E)$` and `$S \in {\cal{P}}(F)$`.
This means that `$S \in {\cal{P}}(E) \cap {\cal{P}}(F)$`.

If `$S \in {\cal{P}}(E) \cap {\cal{P}}(F)$`, then a very similar proof
can be written: `$S \subset E$` and `$S \subset F$`, so
`$\forall s \in S:s \in E$` and `$\forall s \in S: s \in F$`.
Then `$S \subset E \cap F$` and therefore `$S \in {\cal{P}}(E \cap F)$`.

□

To be shown:

`${\cal{P}}(E) \cup {\cal{P}}(F)\subset{\cal{P}}(E \cup F)$`

Proof:

If `$S \in {\cal{P}}(E) \cup {\cal{P}}(F)$`, then
`$S \in {\cal{P}}(E) \Leftrightarrow S \subset E$` or
`$S \in {\cal{P}}(F) \Leftrightarrow S \subset F$`. Since it
is true for any set `$X$` that `$S \subset E \Rightarrow S \in {\cal{P}}(E \cup X)$`,
it is true that `$S \in {\cal{P}}(E \cup F)$`
(similar argumentation if `$S \subset F$`).

□

A reasonable interpretation for the introduced notation:
If `${\cal{C}}={X_1, X_2, \dots, X_n}$`, then

`$\bigcap_{X \in \cal{C}} X=X_1 \cap X_2 \cap \dots X_n$`

Similarly, if `${\cal{C}}={X_1, X_2, \dots, X_n}$`, then

`$\bigcup_{X \in \cal{C}} X=X_1 \cup X_2 \cup \dots X_n$`

The symbol `${\cal{P}}$` still stands for the power set.

To be shown:

`$\bigcap_{X \in \cal{C}} {\cal{P}}(X)={\cal{P}}(\bigcap_{X \in \cal{C}} X)$`

Proof by induction.

Induction base:

`${\cal{P}}(E) \cap {\cal{P}}(F)={\cal{P}}(E \cap F)$`

Induction assumption:

`$\bigcap_{X \in \cal{C}} {\cal{P}}(X)={\cal{P}}(\bigcap_{X \in \cal{C}} X)$`

Induction step:

<div>
	$${\cal{P}}(Y) \cap \bigcap_{X \in \cal{C}} {\cal{P}}(X)\\
	={\cal{P}}(Y) \cap {\cal{P}}(\bigcap_{X \in \cal{C}} X)\\
	={\cal{P}}(Y \cap \bigcap_{X \in \cal{C}} X)$$
</div>

The last step uses `${\cal{P}}(E) \cap {\cal{P}}(F)={\cal{P}}(E \cap F)$`,
since `$\bigcap_{X \in \cal{C}} X$` is also just a set.

□

To be shown:

`$\bigcup_{X \in \cal{C}} {\cal{P}}(X) \subset{\cal{P}}(\bigcup_{X \in \cal{C}} X)$`

Proof by induction.

Induction base:

`${\cal{P}}(E) \cup {\cal{P}}(F) \subset {\cal{P}}(E \cup F)$`

Induction assumption:

`$\bigcup_{X \in \cal{C}} {\cal{P}}(X) \subset {\cal{P}}(\bigcup_{X \in \cal{C}} X)$`

Induction step:

<div>
	$${\cal{P}}(Y) \cup \bigcup_{X \in \cal{C}} {\cal{P}}(X)\\
	\subset {\cal{P}}(Y) \cup {\cal{P}}(\bigcup_{X \in \cal{C}} X)\\
	\subset {\cal{P}}(Y \cup \bigcup_{X \in \cal{C}} X)$$
</div>

The last step uses `${\cal{P}}(E) \cup {\cal{P}}(F) \subset {\cal{P}}(E\cup F)$`,
since `$\bigcup_{X \in \cal{C}} X$` is also just a set.

□

To be shown:

`$\bigcup {\cal{P}}(E)=E$`

Proof:

`$\forall X \in {\cal{P}}(E): X \subset E$`. Furthermore, `$E \in {\cal{P}}(E)$`.
Since `$A \subset E \Rightarrow A \cup E=E$`, it holds
that `$E=\bigcup_{X \in {\cal{P}}(E)}=\bigcup {\cal{P}}(E)$`.

□

And "E is always equal to `$\bigcup_{X \in {\cal{P}}(E)}$` (that is
`$\bigcup {\cal{P}}(E)=E$`), but that the result of applying `${\cal{P}}$`
and `$\bigcup$` to `$E$` in the other order is a set that includes E as a
subset, typically a proper subset" (p. 21).

I am not entirely sure what this is supposed to mean. If it means
that we treat `${\cal{E}}$` as a collection, then
`$\forall X \in {\cal{E}}:\bigcup_{E \in {\cal{E}}} E \subset X$`.
But that doesn't mean that
`${\cal{E}} \subset {\cal{P}}(\bigcup_{E \in {\cal{E}}}E)$`:
If `${\cal{E}}=\{\{a,b\},\{b,c\}\}$`, then `$\bigcup_{E \in {\cal{E}}} E=\{b\}$`,
and
`${\cal{E}}=\{\{a,b\},\{b,c\}\} \not\subset {\cal{P}}(\{b\})=\{\{b\},\emptyset\}$`.

If we treat `$E$` simply as a set, then `$\bigcup E=E$`, and it is of course
clear that `$E \subset {\cal{P}}(E)$`, as for all other subsets of `$E$`.

□

Section 6
----------

### A Non-Trivial Exercise

"find an intrinsic characterization of those sets of subsets of A that
correspond to some order in A"

Let `${\cal{M}} \subset {\cal{P}}({\cal{P}}(A))$` be the set of all possible
orderings of `$A$`. In the case of `$A=\{a, b\}$`, `$\cal{M}$` would be
`$\{\{\{a\}, \{a, b\}\}, \{\{b\}, \{a, b\}\}\}$`.

Some facts about every element `$M \in \cal{M}$`:

`$\bigcap M=\{min\}$`, where `$\{min\}$` is the smallest element in the ordering
`$M$`, the element in `$M$` for which there is no other element `$a \in M$`
so that `$a \subset \{min\}$` (which means that `$\emptyset \not \in M$`).

`$\bigcup M=A$`. `$A$` must therefore be in `$M$` and be the biggest element
(no element `$a \in M$` so that `$a \supset A$`).

For all elements `$m \in M$` except `$\{min\}$` there exists at least one
element `$n \in M$` so that `$n \subset m$`.

Similarly, for all elements `$m \in M$` except `$A$` there exists at least
one element `$n \in M$` so that `$n \supset m$`.

For every `$m \in M$` except `$A$` and `$\{min\}$`, there exist two unique
elements `$x,y \in M$` so that `$m$` is the only set in `$M$` for which it
is true that `$x \subset m \subset y$`.

For every `$a \in A$`, there must exist two sets `$m,n \in M$` so that
`$n=m \cup \{a\}$` (except for `$min$`). This means that the `$|A|=|M|$`,
the size of `$A$` is the size of `$M$`.

These conditions characterise `$\cal{M}$` intrinsically and are the solution
to the question.

### Exercise 1

(i) To be shown: `$(A \cup B) \times X=(A \times X) \cup (B \times X)$`

Proof:

<div>
	$$(A \cup B) \times X=\\
	\{(e, x): e \in A \lor e \in B, x \in X\}=\\
	\{(e, x): e \in A, x \in X\} \cup \{(e, x): e \in B, x \in X\}=\\
	(A \times X) \cup (B \times X)$$
</div>

□

(ii) Te be shown: `$(A \cap B) \times (X \cap Y)=(A \times X) \cap (B \times Y)$`

<div>
	$$(A \times X) \cap (B \times Y)=\\
	\{(x,y), x \in A, y \in X\} \cap \{(v,w), v \in B, w \in Y\}=\\
	\{(x,y), x \in A \land x \in B, y \in X \land y \in Y\}=\\
	\{(x,y), x \in A \cap B, y \in X \cap Y\}=\\
	(A \cap B) \times (X \cap Y)$$
</div>

□

(iii) To be shown: `$(A-B) \times X = (A \times X)-(B \times X)$`

Two-sided proof by contradiction:

1\. `$(A-B)\times X \subset (A \times X)-(B \times X)$`

Let `$(u,v) \in (A-B) \times X$`. Then `$u \in (A-B)$`, and `$v \in X$`.
Suppose `$(u, v) \not \in (A \times X)-(B\times X)$`. Then
`$(u,v) \in (A \times X) \cap (B \times X)$`. Then `$(u,v) \in (A \cap B) \times (X \cap X)$`.
Then `$u \in A \cap B$` and `$v \in X$`. But if `$u \in A \cap B$`,
then `$u \not \in A-B$`! Contradiction.

2\. `$ (A \times X)-(B \times X) \subset (A-B)\times X$`

Let `$(u,v) \in (A \times X)-(B\times X)$`. Then `$(u,v)\in(A \times X)$`
and `$(u,v)\not \in (B \times X)$`. Because `$v$` must be in `$X$`, and there
is no flexibility there, `$u \not \in B$`. Suppose `$(u,v)\not \in (A-B) \times X$`.
Since necessariliy `$v \in X$, $u \not \in A-B$`. But if `$u \not \in A-B$, $u$`
must be an element of `$A\cap B$`. Then `$u \in B$`,
and there is a contradiction.

□

Section 7
----------

### Exercise 1

Reflexive, but neither symmetric nor transitive (symmetry violation:
`$(b,a)\not\in$`, transitivity violation: `$(a,c)\not\in$`):
`$\{(a,a),(a,b),(b,b),(b,c),(c,c)\}$`

Symmetric, but neither reflexive nor transitive (reflexivity violation:
`$(a,a)\not\in$`, transitivity violation: `$(a,c)\not\in$`):
`$\{(a,b),(b,a),(b,c),(c,b)\}$`

Transitive, but neither reflexive nor symmetric (reflexivity
violation: `$(a,a)\not\in$`, symmetry violation: `$(b,a)\not\in$`):
`$\{(a,b),(b,c),(a,c)\}$`

### Exercise 2

> We shall write `$X/R$` for the set of all equivalence classe. (Pronounce
> `$X/R$` as “X modulo R,“ or, in abbreviated form, “X mod R.“ Exercise:
> show that `$X/R$` is indeed a set by exhibiting a condition that specifies
> exactly the subset `$X/R$` of the power set `${\cal{P}}(X)$`).

*– [Paul Halmos](https://en.wikipedia.org/wiki/Paul_Halmos), [“Naïve Set Theory“](https://en.wikipedia.org/wiki/Naive_Set_Theory_\(book\)) p. 38, 1960*

To be honest, I'm not quite sure what exactly I am supposed to do here.
`$X/R$` has been defined as being a set, how can I prove a definition?

But I can try and construct `$X/R$` from `${\cal{P}}(X)$`:

`$X/R=\{E: (\forall x, y \in E: x R y) \land E \in {\cal{P}}(X) \} \subset {\cal{P}}(X)$`

□, I guess?

Section 8
----------

### Exercise 1

Basically, the question is "Which projections are one-to-one", or,
"Which projections are injective"?

The answer is: A projection `$p: X\times Y \mapsto X$` is injective iff
`$\forall (x,y)\in X \times Y: \nexists (x,z) \in X \times Y: z \neq y$`.
Or, simpler: Every element of `$X$` occurs at most once in the relation.
This can be extended easily to relations composed of more than 2 sets.

### Exercise 2

(i) To be shown: `$Y^{\emptyset}=\{\emptyset\}$`

1\. `$\emptyset:\emptyset \rightarrow Y$` (the empty set is a function
from `$\emptyset$` to `$Y$`).

This is true because `$\emptyset$` is a relation so that
`$\emptyset \subset \emptyset \times Y$`, and `$\forall x \in \emptyset: \exists (x,y) \in \emptyset$`.
Or: `$\emptyset$` is a set of pairs that maps all elements in
`$\emptyset$` to `$X$`, and therefore a function from `$\emptyset$` to
`$X$`.

2\. Assume `$\exists x \in Y^{\emptyset}: x \neq \emptyset$`

Then `$x: \emptyset \rightarrow Y$`, and `$x \subset \emptyset \times Y$`.
But `$\emptyset \times X$` can only be `$\emptyset$`, but it was assumed
that `$x \neq \emptyset$`. Therefore, no such `$x$` can exist.

(ii) To be shown: `$X \neq \emptyset \Rightarrow \emptyset^{X}=\emptyset$`

Assume `$\exists f \in \emptyset^{X}$`. Then
`$f \subset X \times \emptyset \land \forall x \in X: \exists (x,y) \in f: y \in \emptyset$`
(or: `$f$` maps all elements of `$X$` to an element in
`$\emptyset$`). However there are no elements in the empty set (that I
know of), so `$f$` can't exist.

However, if `$X=\emptyset$`, then (i) applies. So `$\emptyset^{\emptyset}=\{\emptyset\}$`.

Section 9
---------

### Exercise 1

Here, the reader is asked to formulate and prove the commutative law
for unions of families of sets.

For context, the associative law for unions of families of sets is
formulated as follows:

> Suppose, for instance, that `$\{I_{j}\}$` is a family of sets with
> domain `$J$`, say; write `$K=\bigcup_{j} I_{j}$`, and let `$\{A_{k}\}$` be
> a family of sets with domain `$K$`. It is then not difficult to prove that
> <div>
>	$$\bigcup_{k \in K} A_{k}=\bigcup_{j \in J}(\bigcup_{i \in I_{j}} A_{i})$$
> </div>

Okay, this is all fine and dandy, but where am I going with this? Well,
I have probably misunderstood this, because the way I understand it,
the correct way to formulate the commutative law for unions of families
does *not* hold.

Let's say `$X$` is a set indexed by `$I$`, or, in other words, `$x_{i}$`
is a family. Let's then define a new operator index-union to make these
expressions easier to read: `$I໔X$` as `$\bigcup_{i \in I} X_{i}$`.

The associative law then expanded reads as

<div>
	$$\bigcup_{k \in \bigcup_{j \in J} I_{j}} A_{k}=\bigcup_{j \in J}(\bigcup_{i \in I_{j}} A_{i})$$
</div>

or, simpler, as `$(J໔I)໔A=J໔(I໔A)$`.

Then, simply, the commutative version of the law would be `$A໔B=B໔A$`.

Then there is a very simple counterexample:

`$A=\{1,2\}$`, `$B=\{a,b\}$`. Then a family from A to B could
be `$\{(1,\{a\}),(2,\{b\})\}$` and a family from B to a could
be `$\{(a,\{1\}),(b,\{2\})\}$`. Then
`$A໔B=\bigcup_{a \in A} B_{a}=\{1,2\}$`
and `$B໔A=\bigcup_{b \in B} A_{b}=\{a,b\}$`, and those
two are different sets.

Despite my obvious love for unnecessarily inventing new notation,
I'm not a very good mathematician, and believe (credence `$\ge 99\%$`)
that I have misunderstood something here (the rest is taken up by this
being an editing/printing mistake). I am not sure what, but would be
glad about some pointers where I'm wrong.

#### Other Failing Ways of Interpreting the Exercise

Other ways of interpreting the exercise also have obvious
counter-examples.

If `$f, g$` are two families in `$X$` (as functions:
`$f: X \rightarrow X, g: X \rightarrow X$`), then the
counterexample is

<div>
	$$X=\{a,b\}\\
	f_{a}=b, f_{b}=b\\
	g_{a}=a, g_{b}=a\\
	f໔g=\{b\}\\
	g໔f=\{a\}$$
</div>

If `$f, g$` are two families of sets in `$X$` (as functions:
`$f: X \rightarrow {\cal{P}}(X), g: X \rightarrow {\cal{P}}(X)$`), then the
counterexample is

<div>
	$$X=\{a,b,c\}\\
	f_{a}=\{b\}, f_{b}=\{b\}, f_{c}=\{b\}\\
	g_{a}=\{a\}, g_{b}=\{c\}, g_{c}=\{c\}\\
	f໔g=\{b\}\\
	g໔f=\{c\}$$
</div>

### Exercise 2

To be shown:

(i): `$(\bigcup_{i \in I} A_{i}) \cap (\bigcup_{j \in J} B_{j})=\bigcup_{(i,j) \in I \times J} (A_{i} \cap B_{j})$`

1\. `$(\bigcup_{i \in I} A_{i}) \cap (\bigcup_{j \in J} B_{j}) \subset \bigcup_{(i,j) \in I \times J} (A_{i} \cap B_{j})$`

Let `$e \in (\bigcup_{i \in I} A_{i}) \cap (\bigcup_{j \in J} B_{j})$`.
Then there exists an `$i_{e} \in I$` so that `$e \in A_{i_{e}}$` and a
`$j_{e} \in J$` so that `$e \in B_{j_{e}}$`.
Then `$(i_{e}, j_{e}) \in I \times J$`, and furthermore `$e \in A_{i_{e}} \cap B_{j_{e}}$`.
Since `$A_{i_{e}} \cap B_{j_{e}} \subset \bigcup_{(i,j) \in I \times J} (A_{i} \cap B_{j})$`,
`$e$` is contained in there as well.

Only in this case I will attempt to write out the the proof more formally:

<div>
	$$e \in (\bigcup_{i \in I} A_{i}) \cap (\bigcup_{j \in J} B_{j}) \Rightarrow \\
	e \in (\bigcup_{i \in I} A_{i}) \land e \in (\bigcup_{j \in J} B_{j}) \Rightarrow \\
	(\exists i_{e} \in I: e \in A_{i_{e}}) \land (\exists j_{e} \in J: e \in B_{j_{e}}) \Rightarrow \\
	\exists i_{e} \in I: \exists j_{e} \in J: e \in A_{i_{e}} \land e \in B_{j_{e}} \Rightarrow \\
	\exists (i_{e}, j_{e}) \in I \times J: e \in (A_{i_{e}} \cap B_{j_{e}}) \Rightarrow \\
	e \in \bigcup_{(i,j) \in I \times J} (A_{i} \cap B_{j})$$
</div>

2\. `$(\bigcup_{i \in I} A_{i}) \cap (\bigcup_{j \in J} B_{j}) \supset \bigcup_{(i,j) \in I \times J} (A_{i} \cap B_{j})$`

Let `$e \in \bigcup_{(i,j) \in I \times J} (A_{i} \cap B_{j})$`.
Then there exists `$(i_{e}, j_{e}) \in I \times J$` so that
`$e \in (A_{i_{e}} \cap B_{j_{e}})$`.
But then `$e \in \bigcup_{i \in I} A_{i}$` and `$e \in \bigcup_{j \in J} B_{j}$`,
which means that `$e$` is also in their intersection.

□

(ii): `$(\bigcap_{i \in I} A_{i}) \cup (\bigcap_{j \in J} B_{j})=\bigcap_{(i,j) \in I \times J} (A_{i} \cup B_{j})$`

1\. `$(\bigcap_{i \in I} A_{i}) \cup (\bigcap_{j \in J} B_{j}) \subset \bigcap_{(i,j) \in I \times J} (A_{i} \cup B_{j})$`

Let `$e \in (\bigcap_{i \in I} A_{i}) \cup (\bigcap_{j \in J}B_{j})$`.
Then `$e$` is an element of all of `$A_{i}$` or an element of all of
`$B_{j}$` (or both). Since that is the case, `$e$` is always an element of
`$A_{i} \cup B_{j}$`. Then `$e$` is also an element of the intersection
of all of these unions `$\bigcap_{(i,j) \in I \times J} (A_{i} \cup B_{j})$`.

This can be written down more formally as well:

<div>
	$$e \in (\bigcap_{i \in I} A_{i}) \cup (\bigcap_{j \in J} B_{j}) \Rightarrow \\
	e \in (\bigcap_{i \in I} A_{i}) \lor e \in (\bigcap_{j \in J} B_{j}) \Rightarrow \\
	\forall i \in I: e \in A_{i} \lor \forall j \in J: e \in B_{j} \Rightarrow \\
	\forall i \in I: \forall j \in J: e \in A_{i} \lor e \in B_{j} \Rightarrow \\
	\forall i \in I: \forall j \in J: e \in A_{i} \cup B_{j} \Rightarrow \\
	e \in \bigcap_{(i,j) \in I \times J} (A_{i} \cup B_{j})$$
</div>

2\. `$(\bigcap_{i \in I} A_{i}) \cup (\bigcap_{j \in J} B_{j}) \supset \bigcap_{(i,j) \in I \times J} (A_{i} \cup B_{j})$`

Let `$e \in \bigcap_{(i,j) \in I \times J} (A_{i} \cup B_{j})$`. Then
for every `$i$` and `$j$`, `$e \in A_{i} \cup B_{j}$`. That means that
for every `$i$`, `$e \in A_{i}$`: if there is just one `$j$` so that `$e \not \in B_{j}$`,
for the last sentence to be true, `$A_{i}$` must compensate for that. Or,
if not an `$e$` in every `$A_{i}$`, then this must be true for every
`$B_{j}$` (with a similar reasoning as for `$A_{i}$`). But if `$e$` in
every `$A_{i}$` or every `$B_{j}$`, it surely must be in their union.

□

### Exercise 3

To be proven:

`$(\bigcup_{i} A_{i}) \times (\bigcup_{j} B_{j})=\bigcup_{i,j}(A_{i} \times B_{j})$`

<div>
$$ e \in \bigcup_{i,j}(A_{i} \times B_{j}) \\
(e_{1},e_{2}) \in \bigcup_{i,j}(A_{i} \times B_{j}) \Leftrightarrow \\
\exists i \in I, j \in J: (e_{1},e_{2}) \in A_{i} \times B_{j} \Leftrightarrow \\
\exists i \in I, j \in J: (e_{1} A_{i}) \land (e_{2} \in B_{j}) \Leftrightarrow \\
\exists i \in I: (e_{1} A_{i}) \land \exists j \in J: (e_{2} \in B_{j}) \Leftrightarrow \\
(e_{1} \in \bigcup_{i} A_{i}) \land (e_{2} \in \bigcup_{j} B_{j}) \Leftrightarrow \\
(e_{1}, e_{2}) \in (\bigcup_{i} A_{i}) \times (\bigcup_{j} B_{j}) \Leftrightarrow \\
e \in (\bigcup_{i} A_{i}) \times (\bigcup_{j} B_{j}) $$
</div>

One can say that
`$(e_{1}, e_{2}) \in (\bigcup_{i} A_{i}) \times (\bigcup_{j} B_{j}) = \exists i \in I, j \in J: e_{1} \in A_{i} \land e_{2} \in B_{j}$`
because there must be at least one `$i$` so that `$e \in A_{i}$`, and
because all combinations of elements are chosen from `$A$` and `$B$`.

□

To be proven:

`$(\bigcap_{i} A_{i}) \times (\bigcap_{j} B_{j})=\bigcap_{i,j}(A_{i} \times B_{j})$`

<div>
$$ e \in \bigcap_{i,j}(A_{i} \times B_{j}) \\
(e_{1},e_{2}) \in \bigcap_{i,j}(A_{i} \times B_{j}) \Leftrightarrow \\
\forall i \in I, j \in J: (e_{1},e_{2}) \in A_{i} \times B_{j} \Leftrightarrow \\
\forall i \in I, j \in J: (e_{1} A_{i}) \land (e_{2} \in B_{j}) \Leftrightarrow \\
\forall i \in I: (e_{1} A_{i}) \land \forall j \in J: (e_{2} \in B_{j}) \Leftrightarrow \\
(e_{1} \in \bigcap_{i} A_{i}) \land (e_{2} \in \bigcap_{j} B_{j}) \Leftrightarrow \\
(e_{1}, e_{2}) \in (\bigcap_{i} A_{i}) \times (\bigcap_{j} B_{j}) \Leftrightarrow \\
e \in (\bigcap_{i} A_{i}) \times (\bigcap_{j} B_{j}) $$
</div>

□

To b proven:

`$\bigcap_{i} X_{i} \subset X_{j} \subset \bigcup_{i} X_{i}$`

Proof:

<div>
	$$ e \in \bigcap_{i} X_{i} \Rightarrow \\
	\forall i: e \in X_{i} \Rightarrow \\
	\forall i: \exists j: {i,j} \subset I \land i=j \land e \in X_{i} \Rightarrow \\
	\forall i: \exists j: i \in I \land j \in J \land i=j \land e \in X_{j} \Rightarrow \\
	e \in X_{j} \Rightarrow \\
	\exists j \in I: e \in X_{j} \Rightarrow \\
	\exists i \in I: e \in X_{i} \Rightarrow \\
	e \in \bigcup_{i} X_{i} $$
</div>

□

Section 10
-----------

### Exercise 1

(i) To be shown: `$f(\bigcup_{i} A_{i}) = \bigcup_{i} f(A_{i}$`

If `$e \in f(\bigcup_{i} A_{i})$`, then there exists an `$i$` for which
`$e \in f(A_{i})$`. Then also `$e \in \bigcup_{i}f(A_{i})$` (since the
same set of indices is iterated over).

If otherwise `$e \in \bigcup_{i} f(A_{i})$`, then there is also an `$i$`
for which `$e \in f(A_{i}$`. Then `$e$` is at least once an element of
`$f(\bigcup_{i} A_{i})$`.

(ii) To be shown: `$f(\bigcap_{i} A_{i}) \neq \bigcap_{i} f(A_{i}$`

Example:
`$I=\{1, 2\}, A_1=\{1\}, A_2=\{2\}, f(\{1\})=\{a\}, f(\{2\})=\{a\}, f(\emptyset)=\emptyset, f(\{1,2\})=\{a\}$`

Then `$f(\bigcap_{i} A_{i})=f(\{1\} \cap \{2\})=f(\emptyset)=\emptyset$`,
but `$\bigcap_{i} f(A_{i})=\{a\} \cap \{a\}=\{a\}$`.

### Exercise 2

> A necessary and sufficient condition that `$f$` map `$X$` onto `$Y$`
is that the inverse image under `$f$` of each non-empty subset of `$Y$`
be a non-empty subset of `$X$`. (Proof?)

<!--TODO: with "maps onto", he probably means "surjective", i.e. all
values are mapped to-->

But that's – false? Unless I understand something different by "map"
(which I just take as relates from one set to another, possibly in a
many-to-one relation).

Example:

`$X=\{1,2\}, Y=\{a,b\}$`. `$f(\{1\})=\{a\}, f(\{2\})=\{a\}$`, etc for
all subsets of $X$. Then `$f^{-1}(\{b\})=\emptyset$`.

### Exercise 3

To be proven: $h(gf)=(hg)f$

Proof:

$((hg)f)(x)=((hg)(f(x)))=h(g(f(x)))=h(gf(x))$

### Query 1

> what do $R^{-1}$, $S^{-1}$, $RS$, and $R^{-1}S^{-1}$ mean?"

$yR^{-1}x$: y father of x, $z S^{-1}y$: z is brother of y. $xRSy$:
x nephew of y. $xR^{-1}S^{-1}$.

### Exercise 4

To be proven: $(SR)^{-1}=R^{-1}S^{-1}$

Proof:

Let $(z,x) \in (SR)^{-1}$. Then $xSRz$. Then $\exists y: xSy \land yRs$. Then
$yS^{-1}x$ and $zR^{-1}y$, and then $zR^{-1}S^{-1}x$.

### Query 2

> is there a connection among I, $RR^{-1}$, and $R^{-1}R$?

Shouldn't $I=RR^{-1}$? No. Because if $xRy$ and $zRy$, then
$xRR^{-1}z$. But $I \subset RR^{-1}$, and $I \subset R^{-1}R$. I think
alsso that $RR^{-1}=(R^{-1}R)^{-1}$, and $R^{-1}R=(RR^{-1})^{-1}$
(which is true by the previously proven theorem). I don't think there's
any further connections here.

### Exercise 5

(i) Given $g: Y \rightarrow X$ and $gf(x)=x$, then $f$ is "one-to-one"
and "$g$ maps $Y$ onto $X$".

Judging from what I understand, "$f$ is one-to-one" would mean that $f$
is [injective](https://en.wikipedia.org/wiki/Injective_function),
and "$g$ maps $X$ onto $X$" just means that $g$ is
[surjective](https://en.wikipedia.org/wiki/Surjective_function)?

Wikipedia agrees with these hunches.

`$\forall x_1, x_2 \in X: x_1 \neq x_2 \Leftrightarrow f(x_1) \neq f(x_2)$`,
because if `$f(x_1)=f(x_2)=y$` for `$x_1 \neq x_2$`, then
`$f(y)=x_1$` and $f(y)=x_2$, which is not possible.

$g$ is surjective, since every element in `$\hbox{dom } f \subset Y$` has
exactly one corresponding element in $X$ through $g$, but elements in `$Y - \hbox{dom } f$`
must also be mapped to $X$ (it could be that
`$Y - \hbox{dom } f=\emptyset$`, but that is not guaranteed).

□

(ii) To be proven: `$f(A \cap B)=f(A) \cap f(B)$` iff for all subsets of
`$A$` and `$B$`, `$f$` injective.

First case: `$f$` injective `$\Rightarrow f(A \cap B) = f(A) \cap f(B)$`.

Let `$y \in f(A \cap B)$`, then there exists exactly one `$x \in X$`
so that `$f(x)=y$`.
That means `$x \in A \land x \in B$`. Then `$e \in f(A) \land e \in f(B)$`.

Second case: `$f(A \cap B)=f(A) \cap f(B) \Rightarrow f$` injective.

More formal:

`$f(A \cap B)=f(A) \cap f(B) \Rightarrow \forall x_1 \neq x_2 \in X, f(x_1) \neq f(x_2)$`.

Let then `$x_1 \neq x_2 \in X$`, so that `$f(x_1)=f(x_2)=y$`. Let then
`$A, B$` so that `$x_1 \in A \backslash B$` and `$x_2 \in B \backslash A$`.

Then `$y \in f(A) \cap f(B)$`, but `$y \not \in f(A \cap B)$`. So those
`$x_1, x_2$` can't exist, therefore f is injective.

□

(iii) To be proven: f injective `$\Leftrightarrow f(X-A) \subset Y-f(A)$`
for all subsets of A.

First case: f inj. `$\Rightarrow f(X-A) \subset Y-f(A)$`

Let `$e \in f(X-A)$` and `$e \not \in Y-f(A)$`. Then `$\exists x \in X-A$`
so that `$f(x)=e$`, and there is no `$x_2 \in A: f(x_2)=e$`
(since f is injective). But since `$e \in Y$` (by definition) and `$e \not \in f(A)$`,
e must be in `$Y-f(A)$`.

Second case: `$f(X-A) \subset Y-f(A) \Rightarrow f$` inj.

Assume `$x_1, x_2 (x_1 \not = x_2)$` so that `$f(x_1)=f(x_2)=y$`. Let
then `$x_1 \not \in A$` and `$x_2 \in A$`. Then `$y \in f(X-A)$`
(since `$x_1 \in X-A$`). But since `$y \in f(A)$`, `$y \not \in Y-f(A)$`.
Contradiction, f must be injective.

□

(iv) To be shown: `$\forall y : \exists x: f(x)=y \Leftrightarrow Y-f(A) \subset f(X-A)$`

First case: f surj. `$\Rightarrow \forall A \subset X: Y-f(A) \subset f(X-A)$`

Assume `$y \in Y$` and `$y \not \in fNA)$`. If `$y \not \in f(X-A)$`, then
`$\lnot \exists x \in X-A$` so that `$f(x)=y$`. But since f is surjective,
there must be an x so that `$f(x)=y$` and `$x \not \in A$`! Contradiction.

Second case:
`$\forall A \subset X: Y-f(A) \subset f(X-A) \Rightarrow \forall y: \exists x: f(x)=y$`.

Assume `$ \exists y \in Y: \lnot \exists x: f(x)=y$`. Then `$y \in Y-f(A)$`
for all A, but `$y \not \in f(X-A)$` (since y is not in the
range). Contradiction of the assumption, such a y can't exist.

Section 11
-----------

### Exercise 1

> Since the intersection of every (non-empty) family of successor sets
is a successor set itself (proof?)

Reminder: a family of sets is a function that maps from an index set
into the powerset of a set, so this function is
`$f: I \rightarrow \mathcal{P}(ω)$`.
