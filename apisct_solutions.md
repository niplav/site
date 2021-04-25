[home](./index.md)
-------------------

*author: niplav, created: 2021-04-18, modified: 2021-04-21, language: english, status: in progress, importance: 2, confidence: likely*

> __.__

Solutions to “A Primer in Social Choice Theory”
================================================

Note: Instead of using `$xIy, xRy$` and `$xPy$`,
I will write `$x \sim y, x \succeq y$` and `$x \succ y$`
like any normal person.

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
