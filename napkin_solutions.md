[home](./index.md)
-------------------

*author: niplav, created: 2024-01-26, modified: 2024-01-26, language: english, status: in progress, importance: 2, confidence: certain*

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
