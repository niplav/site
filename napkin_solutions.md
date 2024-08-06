[home](./index.md)
-------------------

*author: niplav, created: 2024-01-26, modified: 2024-01-31, language: english, status: in progress, importance: 2, confidence: certain*

> __I've decided to learn some real math, not just computer scientist
math.__

Solutions to “An Infinitely Large Napkin”
========================================

> Natural explations supersede proofs.

*—Evan Chen, “An Infinitely Large Napkin” p. 6, 2023*

Chapter 1
----------

### Question 1.1.10

> Why do we need the fact that `$p$` is a prime?

If `$p$` weren't a prime, then the operation is not closed (because there
are elements of the group that divide the group size), and therefore there
are elements that are not invertible. Take `$(ℤ/4ℤ)^{\times}$`. Then
the element `$2$` is not invertible:
`$2 \cdot 1=2, 2 \cdot 2=4 \text{ mod } 4=0, 2 \cdot 3=6 \text{ mod } 4=2$`.

So the group operation is not closed, and also `$2$` doesn't have
an inverse.

### Question 1.1.16


> What are the identity and the inverses of the product group?

* Identity: The tuple that contains the identities of each group, `$(1_G, 1_H)$`
* Inverses: The tuple that contains the element-wise inverses for `$(g_1, h_1)^{-1}=(g_1^{-1}, h_1^{-1})$`

### Exercise 1.1.18

> * (a) Rational numbers with odd denominators (in simplest form), where
the operation is addition. (This includes integers, written as `$n/1$`,
and `$0 = 0/1)$`.

This is indeed a group.

1. The identity element is 0.
2. The operation `$+$` is associative.
3. Every element has an inverse, it's simply the negation of the element.

Now, is the `$+$` operation closed?

<div>
	$$\frac{a}{2n+1} + \frac{b}{2m+1}=\frac{(2m+1)a+(2n+1)b}{4mn+2n+2m+1}$$
</div>

It looks like the denominator must stay odd, but I'm not *sure* that's
necessary.

Assume `$(2m+1)a+(2n+1)b=u \cdot k$` and `$4mn+2n+2m+1=l \cdot k$`. Then
`$k$` must be greater than or equal to three.

> * (b) The set of rational numbers with denominator at most 2, where the operation is addition.

I assume we're excluding denominator zero.

Then we have identity (0), associativity and the inverse (again the
negative). The operation looks pretty closed to me as well.

> * (c) The set of rational numbers with denominator at most 2, where the operation is multiplication.

This set is not a group, because with the identity element `$1$` the
number `$3$` doesn't have an inverse.

> * (d) The set of nonnegative integers, where the operation is addition.

This set is also not a group because it doesn't have the inverse for,
e.g., the number `$1$`.

### Exercise 1.2.6

1. `$x \mapsto gx$` is an injection: Assume there is a `$y$` so that no `$x$` so that `$gx=y$`. Then let `$g^{-1}y=x'$` (and ignore the suggestive naming). But then `$gg^{-1}y=gx'$` and therefore `$y=gx'$`. So such a `$y$` can't exist.
2. `$x \mapsto gx$` is an surjection: Assume `$x \not =x'$`. Assume also `$gx=y=gx'$`. Then `$gx=gx'$`. But then `$g^{-1}g=g^{-1}gx'$`, so `$x=x'$`.

A thing that tripped me up was that I then tried to prove that right
multiplication *isn't* a bijection—only to give up in confusion and
later find out that it is *also* a bijection. So much for suggestive
questions.

### Exercise 1.3.5

Let `$g$` be the primite root modulo `$p$`. Then the isomorphism between
`$ℤ/(p-1)ℤ \cong (ℤ/pℤ)^{\times}$` is `$\phi(x)=g^x \mod p$`.

### Question 1.4.5

* 0: Order 1 (it's already the identity element)
* 1: Order 6, `$1+1+1+1+1+1 \mod 6=0$`
* 2: Order 3 `$2+2+2 \mod 6=0$`
* 3: Order 2 `$3+3 \mod 6=0$`
* 4: Order 3 `$4+4+4 \mod 6=0$`
* 5: Order 6 `$5+5+5+5+5+5 \mod 6=0$`

### Exercise 1.5.6

I don't quite get this question. I think I need *more* information about
`$G$` in order to answer it? Otherwise all I can say about `$\langle x \rangle$`
is that it contains 2015 elements (or alternatively infinitely many).

### Problem 1A

The joke here is that a group can only have a proper subgroup isomorphic
to itself if the group is infinitely big. Hence, the person's love for
their partner is infinite.

Sweet.

### Problem 1B

If we allow __Fact 1.4.7__ to be given, then this is easy
to prove: If `$\text{ord } g$` must divide `$|G|$` then
`$g^{|G|}=g^{\frac{|G|}{\text{ord }g} \cdot \text{ord }g}=1_G^{\frac{|G|}{\text{ord }g}}=1_G$`.

However, if we can't assume __Fact 1.4.7__ then we haven't made our
job easier.

Assume `$\text{ord } g$` does not divide `$|G|$`. Then it is either the
case that (1) `$\text{ord } g<|G|$` or (2) `$\text{ord } g>|G|$`.

1. Dunno?
2. In this case, by the pigeonhole principle, there must be some `$i, j \in ℕ$` so that `$g^i=g^j$`, with `$i<j<\text{ord } g$`. But then `$g^j \cdot g^{\text{ ord} g-j}=1$`, but then also `$g^i \cdot g^{\text{ ord} g-j} \not =1$`, even though they are the same operation. This can't be the case, so we exclude `$\text{ord } g>|G|$`.

### Problem 1C

Let the isomorphism `$\phi$` be as follows: `$\phi(1)=\{1, 2, 3\},
\phi(s)=\{1, 3, 2\}, \phi(r)=\{3, 1, 2\}, \phi(r^2)=\{2, 3, 1\}, \phi(rs)=\{2,
1, 3\}, \phi(r^2s)=\{3, 2, 1\}$`.

I could go through the pairs of elements of `$D_6$` individually, but
that seems not smart.
