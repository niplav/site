[home](./index.md)
-------------------

*author: niplav, created: 2021-03-23, modified: 2023-03-24, language: english, status: notes, importance: 1, confidence: draft*

> __People write mathematics in a specific way, and use different
conventions. Here I collect mine, mainly for myself.__

Mathematics Notation Convention
================================

<!--TODO: See also Maths for Intelligent Systems (Toussaint 2022) p. 6-->

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
* `$0 \in \mathbb{N}$`, `$\mathbb{N}^+:=\mathbb{N}\backslash \{0\}$`.
	* First of all, [there's an ISO standard](https://en.wikipedia.org/wiki/Natural_number) (ISO-80000-2) that states that `$0 \in \mathbb{N}$`. I know it's kind of dumb, but standards are nice & there for a reason.
	* `$(\mathbb{N}, +)$` and `$(\mathbb{N}^+, \cdot)$` are both commutative [monoids](https://en.wikipedia.org/wiki/Monoid).
	* `$(\mathbb{N}, +, \cdot)$` is a semiring.
	* `$(\mathbb{N}^+, +, \cdot)$` is…nothing in particular?
		* `$\cdot$` distributes over `$+$`
		* No identity for `$+$`, so it can't be a [rng](https://en.wikipedia.org/wiki/Rng_\(algebra\)) or a [semiring](https://en.wikipedia.org/wiki/semiring)
		* Associativity and commutativity are given for both `$+$` and `$\cdot$`
		* Neither have inverses
		* Only `$\cdot$` has an identity, so it can't be a [near-ring](https://en.wikipedia.org/wiki/Near-ring) (but we also can't make `$(\mathbb{N}^+, \cdot, +)$` a rng or semiring because `$+$` doesn't distribute over `$\cdot$`)
	* Therefore, because `$(\mathbb{N}, +, \cdot)$` is the nicer structure, `$0 \in \mathbb{N}$`.
	* (I'm not super confident about the arguments above, maybe I missed a structure. If so, please tell me!)
* Setting operator precedence and passing arguments to functions is done with parentheses `$()$`, sets are denoted using `$\{\}$`, and `$[]$` is sometimes used in the context of statistics (variance of a variable, mean of a variable, and so on). These are not mixed.
* `$[n] = \{x \in \mathbb{N} | 1 \le x \le n \}$` for `$n \in \mathbb{N}$`.
* For function definitions, use `$\mapsto$` instead of `$\rightarrow$`, e.g. `$f: ℝ^n \mapsto ℝ$` instead of `$f: ℝ^n \rightarrow ℝ$`<!--TODO: bad! bad! think of better option-->
* In multiplication of reals (and maybe complex numbers), I prefer central dots `$a \cdot b \cdot c$`, and *sometimes* concatenation `$abcd$`. Rarely asterisks `$a * b * c * d$`, but I try to avoid them.
* Words
	* Instead of [__"numerator"__/__"denominator"__](https://en.wikipedia.org/wiki/Fraction) I instead use __"upper number"__/__"lower number"__
	* A function `$f(x)=x^p$` is __"quadratic"__ iff `$p=2$`, and __"radical"__ iff `$p \in (0,1)$`

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

* Use the generalized everything
	* Write the first/second/third and so on [moment](https://en.wikipedia.org/wiki/Moment_\(mathematics\)) as `$\mathbb{M_{1}}, \mathbb{M_{2}}, \mathbb{M_{3}}$`.
	* Only use the [generalized mean](https://en.wikipedia.org/wiki/Generalized_mean).
	* Only refer to the Euclidean/Manhattan/max-norm with their respective `$p$`-norm.
* Use a `$\newcommand{\bigplus}{\mathop{\Large+\normalsize}} \bigplus_{i \in I}V_i$` and `$\newcommand{\bigdot}{\mathop{\Large•\normalsize}} \bigdot_{i \in I}V_i$` or `$\newcommand{\bigmult}{\mathop{\Large*\normalsize}} \bigmult_{i \in I}V_i$` instead of `$\sum_{i \in I} V_i$` and `$\prod_{i \in I} V_i$`.<!--TODO: LW link-->
* [This notation](https://www.youtube.com/watch?v=sULa9Lc4pck) for logarithms, exponents and roots.
* Start with the integers `$\mathbb{Z}$`, and then specify when one wants only the positive numbers (`$\mathbb{Z}^+$`), the positive numbers with 0 (`$\mathbb{Z}^+_0$`), the negative numbers (`$\mathbb{Z}^-$`) and the negative numbers with 0 (`$\mathbb{Z}^-_0$`). That would be much nicer than using `$\mathbb{N}$`, since `$\mathbb{Z}$` is a [commutative ring](https://en.wikipedia.org/commutative_ring) under addition and multiplication.
* Treat `$-$` and `$+$` as [idempotent](https://en.wikipedia.org/wiki/Idempotence) operators for making expressions negative and positive, and sign flipping being done by explicitely multiplying with `$-1$`.
	* Alternatively, use the same notation as for the [complex conjugate](https://en.wikipedia.org/wiki/Complex_conjugate).
* Use more different symbols from many different scripts. Sure, よ for the [Yoneda embedding](https://en.wikipedia.org/wiki/Yoneda_lemma) and Ш for the [Tate-Shafarevich group](https://en.wikipedia.org/wiki/Tate-Shafarevich_group) or the [Dirac comb](https://en.wikipedia.org/wiki/Dirac_comb) are cute, but what about இ, ᚠ, ཧ, ದ, 𖤶 ,ᕚ and the entire [Yi script](https://en.wikipedia.org/wiki/Yi_script)? One might want to object that these are hard to remember and therefore pronounce correctly, which is one of the reasons I don't use them. But on the other hand, one could focus on one script at a time, making it easier to learn the different symbols, especially if they are mostly used in text.

Things I'm Unsure About
------------------------

* Basically every usage of `$\ell$` feels weird to me (except for the `$\ell_p$` norm and `$\ell^p$` space maybe). It often seems too important/out of place for a simple variable (or, *god forbid*, an index).
