[home](./index.md)
-------------------

*author: niplav, created: 2021-04-19, modified: 2021-04-26, language: english, status: in progress, importance: 2, confidence: likely*

> __.__

Solutions to “Pattern Recognition and Machine Learning”
=======================================================

Chapter 1
----------

### 1.1

<!--TODO, unfinished-->

> (*) Consider the sum-of-squares error function given by (1.2) in which
the function `$y(x, \textbf{w})$` is given by the polynomial (1.1). Show that
the coefficients `$\textbf{w}=\{w_i\}$` that minimizes this error function
are given by the solution to the following set of linear equations

<div>
	$$ \sum_{j=0}^{M} A_{ij}w_{j}=T_i$$
</div>

> where

<div>
	$$A_{ij}=\sum_{n=1}^{N} (x_n)^{i+j}, T_i=\sum_{n=1}^{N} (x_n)^i t_n.$$
</div>

> Here a suffix `$i$` or `$j$` denotes the index of a component, whereas
`$(x)^i$` denotes `$x$` raised to the power of `$i$`.

Recap: formula 1.1 is

<div>
	$$ y(x, \textbf{w}) = w_0 + w_1 x + w_2 x^2+ \dots +w_M x^M = \sum_{j=0}^{M} w_j x^j$$
</div>

and formula 1.2 (the error function) is

<div>
	$$E(\textbf{w})=\frac{1}{2} \sum_{n=1}^{N} (y(x_n, \textbf{w})-t_n)^2$$
</div>

Substituting 1.1 into 1.2 gives

<div>
	$$ E(\textbf{w})=\frac{1}{2} \sum_{n=1}^{N} (\sum_{j=0}^{M} w_j x^j-t_n)^2 $$
</div>

Differentiating after `$\textbf{w}$` then returns

<div>
	$$ E(\textbf{w})'=\sum_{n=1}^{N} (\sum_{j=0}^{M} (w_j x^j)'-t_n) $$
</div>

I really should learn multivariable calculus.

### 1.5

> (*) Using the definition (1.38) show that `$\text{var}[f(x)]$` satisfies
(1.39).

<div>
	$$ \mathbb{E}[(f(x)-\mathbb{E}[f(x)])^2]=\\
	\mathbb{E}[f(x)^2-2\mathbb{E}[f(x)]f(x)+\mathbb{E}[f(x)]^2]=\\
	\mathbb{E}[f(x)^2]-\mathbb{E}[2\mathbb{E}[f(x)]f(x)]+\mathbb{E}[\mathbb{E}[f(x)]^2]=\\
	\mathbb{E}[f(x)^2]-2\mathbb{E}[f(x)]^2+\mathbb{E}[f(x)]^2=\\
	\mathbb{E}[f(x)^2]-\mathbb{E}[f(x)]^2$$
</div>
