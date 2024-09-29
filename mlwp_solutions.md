[home](./index.md)
-------------------

*author: niplav, created: 2024-09-26, modified: 2024-09-29, language: english, status: in progress, importance: 2, confidence: likely*

> __.__

Solutions to “ML For The Working Programmer”
=============================================

Chapter 2
----------

### 2.1

Done.

### 2.2

Reasons for treating reals and integers as different:

1. *Speed*. Knowing that a variable is an integer can allow compiler-writers to write compilers that produce faster programs.
2. *No access to the reals*. The reals are, ah, unreal. [Almost all](https://en.wikipedia.org/wiki/Almost_all) are uncomputable, many computable ones are better conceived of as *functions*, not numbers—pi, or Euler's constant, or whatever, are never stored anywhere fully, we just have access to some digits by executing the function.
3. *Approximation through floating points is meh*. 32-bit floating point numbers actually can't represent some integers above ~10⁷.

Reasons for treating reals and reals
(in this case probably floating point numbers or
[arbitrary-precision](https://en.wikipedia.org/wiki/Arbitrary-precision_arithmetic)
[rational numbers](https://en.wikipedia.org/wiki/Rational_numbers))
as the same:

1. *Convience*.
2. *Ease of learning*.
3. *Elegance*.

I think that scripting languages can treat them as the same by default
by now (given our [Moorean](https://en.wikipedia.org/wiki/Moore's_Law)
utopia), but anything that wants to be used in product needs to give
users the option to specify the type, and optimize accordingly.

### 2.3

* `double`: No, since 2 is clearly not a `real`.
* `f`: No, since `Math.sin` is only defined for `real`s.
* `g`: Yes.

### 2.4

Prediction: Error messages for both `~1` and `10`.

Result: Uncaught exception. Close enough.
