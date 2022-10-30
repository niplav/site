[home](./index.md)
-------------------

*author: niplav, created: 2022-10-19, modified: 2022-10-24, language: english, status: in progress, importance: 2, confidence: likely*

> __Solutions to the textbook “Maths for Intelligent Systems”.__

Solutions to “Maths for Intelligent Systems”
=============================================

Chapter 2
----------

### Stray Non-Exercise 1

> Let me start with an example: We have three real-valued quantities `$x,
g$` and `$f$` which depend on each other. Specifically, $f(x,g)=3x+2g$
and `$g(x)=2x$`.  
> Question: What is the “derivative of `$f$` w.r.t. `$x$`”?

Intuitively, I'd say that `$\frac{\partial}{\partial x}f(x,g)=3$`. But then I notice that `$g$`
is allegedly a "real-valued quantity", what is that supposed to mean? Is
it not a function?

Alas, plugging in `$g$` into `$f$` gives `$f(x)=3x+2(2x)$` and
`$\frac{\partial}{\partial x}f(x)=3+4=7$`.

### i) to iv)

See [here](./ito_solutions.html#401).
