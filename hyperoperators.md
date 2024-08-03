[home](./index.md)
------------------

*author: niplav, created: 2024-01-30, modified: 2024-01-30, language: english, status: finished, importance: 2, confidence: certain*

> __I implement an obscure mathematical construct in an obscure
programming language. Edge cases are encountered.__

Implementing Commutative Hyperoperations
=========================================

[Ghalimi 2019](https://observablehq.com/@ishi/arithmetic "Hyperlogarithmic Arithmetic")
presents and discusses a novel construction of a class of
[hyperoperations](https://en.wikipedia.org/wiki/Hyperoperation), here I
implement these in [Klong](http://t3x.org/klong/index.html).

I choose to implement these operators on base `$e$`, just as the author
recommends.

The problem with this is that with with operations of order 4 or
higher, the results are in `$\mathbb{C}$` (because `$ln(ln(2))<0$`),
so we would need a logarithm function that deals with complex numbers
to implement this, this is not available natively under Klong yet, so I
have to write the principal function of the complex logarithm using [this
section](https://en.wikipedia.org/wiki/Complex_logarithm#Calculating_the_principal_value)
from the Wikipedia article:

        .l("math")
        cln::{ln(sqr(+/x^2)),atan2@x}

Since the complex logarithm is only defined for
`$\mathbb{C}^{\times}:=\mathbb{C} \backslash \{0\}$`, `cln` returns
a nonsense value for `$0+0i$`:

                cln(0,0)
        [:undefined -1.57079632679489661]

We know that `$e^{\log z}=z$` for all `$z \in \mathbb{C}^{\times}$`,
which we can test here:

                cexp(cln(1,1))
        [0.999999999999999911 0.999999999999999915]
                cexp(cln(1,2))
        [1.00132433601450641 1.9993372837280625]
                cexp(cln(2,1))
        [2.00148381847841902 0.997026842351321174]
                cexp(cln(1,-1))
        [0.999999999999999928 -1.00000000000000105]
                cexp(cln(-1,1))
        [-0.999999999999999908 -1.00000000000000151]
                cexp(cln(-1,-1))
        [-0.999999999999999812 0.999999999999999918]
                cexp(cln(-1,0))
        [-0.999999999999998211 0.0]
                cexp(cln(0,-1))
        [0.00000000000000001 -1.00000000000000078]
                cexp(cln(1,0))
        [0.999999999999999984 0.0]
                cexp(cln(0,1))
        [0.0 0.999999999999999984]

This all looks relatively fine (the rounding errors are probably
unavoidable), however, we see that `cexp(cln(-1,1))=[-1 -1]≠[-1 1]`
(and `cexp(cln(-1,-1))=[-1 1]≠[-1 -1]`).  This is very unfortunate. I
suspect that the implementation of `atan2` is at fault: `atan2(1;0)=0`
here, but the python math library gives `math.atan2(1,0)=π/2` (python
gives `0` for `math.atan2(0,1)` and Klong's `atan2` gives `π/2` for
`atan2(0;1)`).

<!--TODO: fix local atan2-->

With this, one can implement the commutative hyperoperation:

        comhyp::{:[z=0;cln(cadd(cexp(x);cexp(y))):|
                z=1;cadd(x;y):|
                z=2;cmul(x;y):|
                z=3;cexp(cmul(cln(x);cln(y)));
                cexp(comhyp(cln(x);cln(y);z-1))]}

This implementation deals only in `$\mathbb{C}$`.

Nearly identically, one can treat reversion:

        revhyp::{:[z=0;cln(csub(cexp(x);cexp(y))):|
                z=1;csub(x;y):|
                z=2;cdiv(x;y):|
                z=3;cexp(cdiv(cln(x);cln(y)));
                cexp(revhyp(cln(x);cln(y);z-1))]}

For implementing transaction, one needs to implement exponentiation in
`$\mathbb{C}$` (for `$x, y \in \mathbb{C}$`, `$x^y=e^{y*\ln(x)}$`):

        cpow::{cexp(cmul(y;cln(x)))}

Next, one can turn ones attention to the transaction operation itself:

        tranhyp::{:[z=0;cadd(x;cexp(y)):|
                z=1;cmul(x;cexp(y)):|
                z=2;cpow(x;y):|
                z=3;cexp(cpow(cln(x);cln(y)));
                cexp(tranhyp(cln(x);cln(y);z-1))]}

And thereby we have implemented the entire class of hyperoperations.

<!--When you're less tired, check over this again:
2^x^y=b^{1^log_b(x)^{log_b(y)}}=b^{log_b(x)*b^log_b(y)}=x^{b^_log_b(y)}=x^y
I think this checks out-->
