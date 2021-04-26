[home](./index.md)
-------------------

*author: niplav, created: 2021-04-18, modified: 2021-04-21, language: english, status: in progress, importance: 2, confidence: likely*

> __.__

Solutions to “A Primer in Social Choice Theory”
================================================

Note: Instead of using `$xIy, xRy$` and `$xPy$`, I will *sometimes*
write `$x \sim y, x \succeq y$` and `$x \succ y$`.

Chapter 1
----------

### 1.1

> Show that if R is reflexive, complete, and transitive, then for all `$x, y, z \in X$`:  
> (a) `$(xIy \land yIz) \rightarrow xIz$`;  

We know that `$x \sim y \Leftrightarrow x \succeq y \land x \preceq y$`.

Then:

<div>
	$$(x \sim y \land y \sim z) \Leftrightarrow \\
	x \succeq y \land x \preceq y \land y \succeq z \land z \succeq y \Rightarrow \\
	x \succeq z \land x \preceq z \Rightarrow \\
	x \sim y $$
</div>

> (b) `$(xPy \land yRz) \rightarrow xPz$`

<div>
	$$ x \succ y \land y \succeq z \Leftrightarrow \\
	x \succ y \land (y \succ z \lor y \sim z) \Leftrightarrow \\
	(x \succ y \land y \succ z) \lor (x \succ y \land y \sim z) \Rightarrow \\
	(x \succ z) \lor (x \succ z) \Rightarrow \\
	x \succ z $$
</div>

### 1.2

> Suppose that R is an ordering over the set `$X=\{x,y,z,w\}$` with
`$xIy$`, `$yPz$`, and `$zPw$`. Determine the choice set.

`$R$` is complete, reflexive and transitive. We therefore know:

`$x \sim y \succ z \succ w$`. The choice set is the set of all best
elements, that is the set of all elements who at least as good as any
other element. So, here the choice set is `$\{x,y\}$`.

### 1.3

> Show that if `$S \subset X$` is finite and R is reflexive, complete,
and quasi-transitive over S, then `$C(S, R)$` is non-empty.

If S contains exactly one element (`$S=\{x\}$`), then that element is
automatically the best element (due to reflexivity: `$xRx$`).

If S contains exactly two elements (`$S=\{x, y\}$`), then we have either
`$xPy, yPx \text{ or } xIy$` (due to completeness), with `$\{x\}, \{y\} \text{ and } \{x,y\}$`
being the choice sets.

If S contains three or more elements, due to completeness we know
that for an element `$x$`, there is a finite set `$g(x):=\{y: yRx\} \backslash \{x\}$`.
If `$g(x)=\emptyset$`, `$x$` is the best element. If `$g(x)$` is not
empty, we can pick an element `$y \in g(x)$` and generate `$g(y)$`. We
know that `$|g(y)|<g(x)|$` (because we're removing at least one element
from `$g(x)$`, namely `$y$`). If we repeat the procedure (finitely many
times, since `$g(x) \subset S$` is finite), we finally arrive at a set
`$g(z)$` with size `$|g(z)|=1$`. The element of `$g(z)$` is a chosen
element.

### 1.7

> Let F stand for Fahrenheit and C stand for Celsius. 32° in F are
the same as 0° in C; and 68° in F are the same as 20° in C. Please
specify the mapping F(C) and C(F). Do these mappings have the property
that F values are based on a positive affine transformation of C values,
and vice versa?

I'm unsure what is asked here. The raw mapping given in set form is just
`$F(C)=\{(32, 0), (68, 20)\}$` and `$C(F)=\{(0, 32), (20, 68)\}$`.

The conversion formula for degrees Fahrenheit to Celsius, based on the
given values, can be determined easily from the set of linear equations

<div>
	$$ a+32b=0 \\
	a+36b=20 $$
</div>

Upon solving, one determines that
`$a=-32*\frac{5}{9} \approx -17.7778, b=\frac{5}{9} \approx 0.5556$`,
so `$F(C) \approx -17.7778+0.5556*C$`
and `$C(F)=-0.05625*C-1.8$`. Since [Wikipedia
says](https://en.wikipedia.org/wiki/Affine_transformation#Over_the_real_numbers)
that a linear transformation in `$ℝ$` is an affine transformation,
this is an affine transformation.
