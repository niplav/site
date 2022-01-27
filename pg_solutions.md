[home](./index.md)
-------------------

*author: niplav, created: 2022-01-25, modified: 2022-01-26, language: english, status: in progress, importance: 2, confidence: likely*

> __.__

Solutions to “Population Genetics”
===================================

Chapter 1
---------

### Problem 1.1

For three it would be `$A_1A_1A_1, A_1A_1A_2, A_1A_2A_2, A_1A_2A_3, A_2A_2A_2, A_2A_2A_3, A_3A_3A_3$`,
with 7 different genotypes.

For four it would be 32 different genotypes:

`$A_1 A_1 A_1 A_1, A_1 A_1 A_1 A_2, A_1 A_1 A_1 A_3, A_1 A_1 A_1 A_4, A_1 A_1 A_2 A_2, A_1 A_1 A_2 A_3, A_1 A_1 A_2 A_4, A_1 A_1 A_3 A_3, A_1 A_1 A_3 A_4, A_1 A_1 A_4 A_4, A_1 A_2 A_2 A_2, A_1 A_2 A_2 A_3, A_1 A_2 A_2 A_4, A_1 A_2 A_3 A_4, A_1 A_2 A_4 A_4, A_1 A_3 A_4 A_4, A_1 A_4 A_4 A_4, A_2 A_2 A_2 A_2, A_2 A_2 A_2 A_3, A_2 A_2 A_2 A_4, A_2 A_2 A_3 A_3, A_2 A_2 A_3 A_4, A_2 A_2 A_4 A_4, A_2 A_3 A_3 A_3, A_2 A_3 A_3 A_4, A_2 A_3 A_4 A_4, A_2 A_4 A_4 A_4, A_3 A_3 A_3 A_3, A_3 A_3 A_3 A_4, A_3 A_3 A_4 A_4, A_3 A_4 A_4 A_4, A_4 A_4 A_4 A_4$`

<!--TODO: what closed form formula describes the above counting
partition?-->

So apparently, per solution, this is wrong, because I assumed that `$n$`
different alleles resulted in a `$n$`ploid organism, which isn't the case.

For three alleles it would be `$A_1 A_1, A_1 A_2, A_1 A_3, A_2 A_2, A_2 A_3, A_3 A_3$`,
which is 6 different genotypes.

For four different alleles it would be 10 different genotypes:

`$A_1 A_1,A_1 A_2,A_1 A_3,A_1 A_4,A_2 A_2,A_2 A_3,A_2 A_4,A_3 A_3,A_3 A_4,A_4 A_4$`

The general formula is `$\frac{n (n+1)}{2}$` different genotypes,
because it's just the upper half of the square again.
