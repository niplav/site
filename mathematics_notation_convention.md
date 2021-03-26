[home](./index.md)
-------------------

*author: niplav, created: 2021-03-23, modified: 2021-03-2., language: english, status: notes, importance: 1, confidence: log*

> __People write mathematics in a specific way, and use different
conventions. Here I collect mine, mainly for myself.__

Mathematics Notation Convention
================================

* Clearly differentiate between stating something being a proper subset or not: only use `$A \subset B$` if definitely `$A \not =B$`, otherwise say `$A \subseteq B$`
* `$0 \in \mathbb{N}$`, `$\mathbb{N}^+:=\mathbb{N}\backslash \{0\}$`. It makes much more sense when treating `$\mathbb{N}$` as a commutative monoid under addition (one could answer that it's equally possible to treat `$\mathbb{N}^+$` as a commutative monoid under multiplication, to which my answer is that addition is a more fundamental operation than multiplication)
	* However, one could ditch the whole thing and do notation as such: One starts with the integers `$\mathbb{Z}$`, and then specifies when one wants only the positive numbers (`$\mathbb{Z}^+$`), the positive numbers with 0 (`$\mathbb{Z}^+_0$`), the negative numbers (`$\mathbb{Z}^-$`) and the negative numbers with 0 (`$\mathbb{Z}^-_0$`). That would be much nicer, since `$\mathbb{Z}$` is a ring under addition and multiplication.
* Set difference is written with a backslash `$\backslash$`, not with a minus `$-$`.
* If e is not an element of S, then `$e \not \in S$` (and not something like `$e \in' S$`)
* `$[n] = \{x \in \mathbb{N} | 1 \le x \le n \}$`
* Use `$:=$` for assignment, not `$\rightarrow$` or `$\leftarrow$`
