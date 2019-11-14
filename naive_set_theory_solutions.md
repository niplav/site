[home](./index.md)
-------------------

*author: niplav, created: 2019-03-20, modified: 2019-11-14, language: english, status: in progress, importance: 2, confidence: likely*

> __[“Naive Set
> Theory”](https://en.wikipedia.org/wiki/Naive_Set_Theory_\(book\))
> by Paul Halmos is a short introduction to set theory. Here, I present
> solutions to the explicitely stated exercises and problems in that book.__

Solutions to “Naive Set Theory“
================================

Section 3, Exercise 1
----------------------

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

Section 4, Exercise 1
---------------------

I am not exactly sure what I'm supposed to do here. I guess
"observe" means "prove" here, so "prove that the condition
has nothing to do with the set B".

Proof:

<div>
	$$(A \cap B) \cup C = A \cap (B \cup C) \Leftrightarrow C \subset A\\
	(A \cup C) \cap (B \cup C) = A \cap (B \cup C) \Leftrightarrow C \subset A\\
	A \cup C = A \Leftrightarrow C \subset A$$
</div>

This is trivially true.

□

Section 5, Some easy exercises
------------------------------

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

Section 5, Exercise 1
---------------------

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

Section 5, Exercise 2
---------------------

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

Section 6, A non-trivial exercise
---------------------------------

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

Section 6, Exercise 1
----------------------

(i) To be shown: `$(A \cup B) \times X=(A \times X) \cup (B \times X)$`

Proof:

<div>
	$$(A \cup B) \times X=\\
	\{(e, x): \forall e \in A \lor e \in B, x \in X\}=\\
	\{(e, x): \forall e \in A, x \in X\} \cup \{(e, x): \forall e \in B, x \in X\}=\\
	(A \times X) \cup (B \times X)$$
</div>

□
