[home](./index.md)
-------------------

*author: niplav, created: 2021-03-23, modified: 2022-03-03, language: english, status: notes, importance: 1, confidence: draft*

> __People write mathematics in a specific way, and use different
conventions. Here I collect mine, mainly for myself.__

Mathematics Notation Convention
================================

> Zum Schein nämlich steht das Ausdruckslose, wiewohl im Gegensatz,
doch in derart notwendigem Verhältnis, daß eben das Schöne, ob auch
selber nicht Schein, aufhört ein wesentlich Schönes zu sein, wenn der
Schein von ihm schwindet.

*— Walter Benjamin, “Goethes Wahlverwandschaften”, 1925*

### Basics

* Use `$:=$` for assignment, not `$\rightarrow$` or `$\leftarrow$`
* When denoting choosing elements from a set based on some criterion, use the bar |: `$\{x|x \in P(x) \land \forall y \in S: x \succ y\}$` (some people use a colon)
* Usually, with `$\bigcup/\bigvee/\sum/\prod$` etc, use `$i$` and `$j$` as the variables. If there are more, use `$i_1, i_2, \dots$`.
* A variable with the name "abcd" is written as `$\text{abcd}$`, `$abcd$` is the product of four variables `$a, b, c$` and `$d$`.
* `$0 \in \mathbb{N}$`, `$\mathbb{N}^+:=\mathbb{N}\backslash \{0\}$`. It makes much more sense when treating `$\mathbb{N}$` as a commutative monoid under addition (one could answer that it's equally possible to treat `$\mathbb{N}^+$` as a commutative monoid under multiplication, to which my answer is that addition is a more fundamental operation than multiplication).
* Setting operator precedence and passing arguments to functions is done with parentheses `$()$`, sets are denoted using `$\{\}$`, and `$[]$` is sometimes used in the context of statistics (variance of a variable, mean of a variable, and so on). These are not mixed.
	* `$[n] = \{x \in \mathbb{N} | 1 \le x \le n \}$` for `$n \in \mathbb{N}$`.
* For function definitions, use `$f: ℝ^n \mapsto ℝ$` instead of `$f: ℝ^n \rightarrow ℝ$`

### Set Theory

* Clearly differentiate between stating something being a proper subset or not: only use `$A \subset B$` if definitely `$A \not =B$`, otherwise write `$A \subseteq B$`.
* Set difference is written with a backslash `$\backslash$`, not with a minus `$-$`.
* If e is not an element of S, then `$e \not \in S$` (and not something like `$e \in' S$`).
* The size of a set `$A$` is `$|A|$`, not `$\#(A)$`

### Logic

* Use `$\Rightarrow$` or `$\Leftarrow$` for implication and `$\Leftrightarrow$` for the biconditional instead of `$\leftarrow$` or `$\rightarrow$` and `$\leftrightarrow$`.

### Probability Theory and Statistics

* I write the expectation of the probability distribution `$X$` as `$\mathbb{E}[X]$` and the variance of `$X$` as `$\mathbb{V}[X]$`. Unfortunately, `$\mathbb{C}$` is already taken for the complex numbers, so I am forced to write `$\text{cov}[X,Y]$` for the covariance, and `$\text{cor}[X,Y]$` for the correlation.

### Game Theory

(Or social choice theory/decision theory/utility theory…)

* Some people use `$P, R, I$` instead of `$\prec, \preceq, \sim$`. I often don't.
* As per [Wikipedia](https://en.wikipedia.org/wiki/Minimax#Maximin), the term "maximin" refers to the strategy of maximizing one's own minimum payoff in non-zero-sum games, while "minimax" is the strategy of minimizing the opponent's maximum payoff in zero-sum games
	* In zero-sum games, minimizing the opponent's maximum payoff is equivalent to maximizing one's own minimum payoff
	* This is unfortunately asymmetric: What term would we use if we wanted to minimize our own maximum?
		* Looking at this symmetrically, it would create a set of strategies (some nonsensical):

<table>
<tbody>
	<tr>
		<td>(Optimizing one's own value)</td>
		<td>Maximum</td>
		<td>Minimum</td>
	</tr>
	<tr>
		<td>maximize</td>
		<td>maximax</td>
		<td>maximin</td>
	</tr>
	<tr>
		<td>minimize</td>
		<td>minimax</td>
		<td>minimin</td>
	</tr>
</tbody>
</table>

----

<table>
<tbody>
	<tr>
		<td>(Optimizing the other player's value)</td>
		<td>Maximum</td>
		<td>Minimum</td>
	</tr>
	<tr>
		<td>maximize</td>
		<td>maxmaxi</td>
		<td>maxmini</td>
	</tr>
	<tr>
		<td>minimize</td>
		<td>minmaxi</td>
		<td>minmini</td>
	</tr>
</tbody>
</table>

(This is *not* the terminology I will use, but I would if I were brave enough)

Things I Would Like To Do But I'm Not Brave Enough
---------------------------------------------------

* Write the first/second/third and so on moment as `$\mathbb{M_{1}}, \mathbb{M_{2}}, \mathbb{M_{3}}$`.
* Use a big `$+$` and `$*$` instead of `$\sum$` and `$\prod$`.
* [This notation](https://www.youtube.com/watch?v=sULa9Lc4pck) for logarithms, exponents and roots.
* Start with the integers `$\mathbb{Z}$`, and then specifies when one wants only the positive numbers (`$\mathbb{Z}^+$`), the positive numbers with 0 (`$\mathbb{Z}^+_0$`), the negative numbers (`$\mathbb{Z}^-$`) and the negative numbers with 0 (`$\mathbb{Z}^-_0$`). That would be much nicer than using `$\mathbb{N}$`, since `$\mathbb{Z}$` is a ring under addition and multiplication.
* Treat `$-$` and `$+$` as [idempotent](https://en.wikipedia.org/wiki/Idempotence) operators for making expressions negative and positive, which sign flipping being done by explicitely multiplying with `$-1$`.
	* Alternatively, use the same notation as for the [complex conjugate](https://en.wikipedia.org/wiki/Complex_conjugate).
* Use more different symbols from many different scripts. Sure, よ for the [Yoneda embedding](https://en.wikipedia.org/wiki/Yoneda_lemma) and Ш for the [Tate-Shafarevich group](https://en.wikipedia.org/wiki/Tate-Shafarevich_group) or the [Dirac comb](https://en.wikipedia.org/wiki/Dirac_comb) are cute, but what about இ, ᚠ, ཧ, ದ, 𖤶 and ᕚ? One might want to object that these are hard to remember and therefore pronounce correctly, which is one of the reasons I don't use them. But on the other hand, one could focus on one script at a time, making it easier to learn the different symbols, especially if they are mostly used in text.

Things I'm Unsure About
------------------------

* In multiplication of reals (and maybe complex numbers), is it best to just use concatenation `$abc$`, asterisks `$a*b*c$` or central dots `$a \cdot b \cdot c$`?
	* Or just be flexible?
* Basically every usage of `$\ell$` feels weird to me (except for the `$\ell_p$` norm and `$\ell^p$` space maybe). It often seems too important/out of place for a simple variable (or, *god forbid*, an index).
