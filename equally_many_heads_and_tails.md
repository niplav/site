[home](./index.md)
-------------------

*author: niplav, created: 2019-02-08, modified: 2019-11-19, language: english, status: finished, importance: 4, confidence: highly likely*

> __Imagine getting up every morning and throwing a coin so often that
> heads and tails have come up an equal amount of times. How often
> would you throw the coin on average? Infinitely often, it turns out.
> Code in [Klong](http://t3x.org/klong/index.html).__

Equally Many Heads and Tails
============================

This thought experiment can be modeled as a simple
[expected value](https://en.wikipedia.org/wiki/Expected_value)
calculation in a countably infinite case:

<div>
	$$\mathbb{E}=\sum_{i=1}^{\infty} p_{i}*x_{i}$$
</div>

Finding `$x_{i}$`
-----------------

We know that flipping the coin definitely ends when for 2\*n coin flips,
we have gotten heads n times and tails n times as well. This gives us
`$x_{i}=2*i$`.

Finding `$p_{i}$`
-----------------

Finding out `$p_{i}$` is a bit harder. In order to find it, it is best to look
at the first iterations of the process.

### Observing Coin Flips

After starting, we have flipped the coin 2 times, so the possible solutions are:

	H;H
	H;T
	T;H
	T;T

We are done in two cases, H;T and T;H. p₁ therefore is
`$\frac{2}{4}=0.5$`. We then continue flipping the coin 2 more times,
starting with either H;H or T;T, with the following possible results:

	H;H;H;H
	H;H;H;T
	H;H;T;H
	H;H;T;T
	T;T;H;H
	T;T;T;H
	T;T;H;T
	T;T;T;T

Of these, only two finish: H;H;T;T and T;T;H;H. So the chance of finishing
given 4 coin flips is `$\frac{2}{8}=0.25$`.

We continue flipping the coin with the non-finishing sequences, and our possible
results look like this:

	H;H;H;H;H;H
	H;H;H;H;H;T
	H;H;H;H;T;H
	H;H;H;H;T;T

	H;H;H;T;H;H
	H;H;H;T;H;T
	H;H;H;T;T;H
	H;H;H;T;T;T

	H;H;T;H;H;H
	H;H;T;H;H;T
	H;H;T;H;T;H
	H;H;T;H;T;T

	T;T;T;H;H;H
	T;T;T;H;T;H
	T;T;T;H;H;T
	T;T;T;H;T;T

	T;T;H;T;H;H
	T;T;H;T;T;H
	T;T;H;T;H;T
	T;T;H;T;T;T

	T;T;T;T;H;H
	T;T;T;T;H;T
	T;T;T;T;T;H
	T;T;T;T;T;T

Here, the sequences `H;H;H;T;T;T, H;H;T;H;T;T, T;T;T;H;H;H,T;T;H;T;H;H`
finish, so given six coin flips, the chance of finishing is
`$\frac{4}{24}=0.1666666\dots$`.

Writing down the next step gets messy, but we have already observed
enough iterations to find a pattern in the sequences.

### Considerations on Coin Flips

First of all, the number of finishing sequences given 2\*n coin flips
is the [Catalan number](https://en.wikipedia.org/wiki/Catalan_number)
Cₙ. In this case, it describes the number of [Dyck
words](https://en.wikipedia.org/wiki/Dyck_word) of the length 2\*n. To
quote Wikipedia:

> A Dyck word is a string consisting of n X's and n Y's such that no
> initial segment of the string has more Y's than X's.

*– [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia), [“Dyck word”](https://en.wikipedia.org/wiki/Dyck_word), 2019*

This applies exactly to the given problem. A finishing sequence has
equally many heads and tails, but doesn't begin with a sequence of
equally many heads and tails. Cₙ is defined as `$\frac{1}{n+1}*{2*n \choose n}$`.

Catalan numbers can be easily implemented using the [binomial
coefficient](https://en.wikipedia.org/wiki/Binomial_coefficient):

	fact::{:[0=x;1;*/1+!x]}
	bincoeff::{[n k];n::x;k::y;fact(n)%(fact(k)*fact(n-k))}
	catalan::{bincoeff(2*x;x)%x+1}
	f::{2*catalan(x)}

We call the number of finishing steps given 2\*n coin flips fₙ.

One can also see that the total number of possible sequences of coin flips
oₙ after 2\*n coin flips is `$4*(o_{n-1}-f_{n-1})$`, because
one appends `H;H` or `H;T` or `T;H` or `T;T` to the remaining number of
sequences. So let oₙ be

<div>
	$$o_{1}=4\\
	o_{n}=4*(o_{n-1}-f_{n-1})$$
</div>

One can implement `$o_{n}$` simply:

	o::{:[x=1;4;4*o(x-1)-f(x-1)]}

When one executes `o` and `f`, one notices something peculiar: it seems
that `$o_{n}=2*n*f_{n}$`.

#### Proof that `$o_{n}=2*n*f_{n}$`

Induction basis:

<div>
	$$o_{1}=2*1*f_{1}\\
	4=2*1*2$$
</div>

Induction assumption:

<div>
	$$o_{n}=2*n*f_{n}$$
</div>

Induction step:

<div>
	$$o_{n+1}=2*(n+1)*f_{n+1}\\
	2*(o_{n}-f_{n})=(n+1)*f_{n+1}\\
	2*(2*n*f_{n}-f_{n})=(n+1)*f_{n+1}\\
	8*n*C_{n}-4*C_{n}=(n+1)*2*C_{n+1}\\
	C_{n}*\frac{4*n-2}{n+1}=C_{n+1}$$
</div>

This is equivalent to [a recursive definition](https://oeis.org/A000108)
of the Catalan numbers in the OEIS (sixth formula).

<!--TODO: This seems a tiny bit fishy: There is probably an offset here
(first value of the catalan numbers is not used, so the whole sequence
is shifted). Look at this.-->

### Probability of Finishing at `$2*n$` Steps

So, what's the probability of finishing given `2*n` steps now? Simple:
it's `$\frac{f_{n}}{o_{n}}=\frac{f_n}{2*n*f_{n}}=\frac{1}{2*n}$`.

	pgn::{1%2*x}

Note that this probability is different from finishing at `2*n` steps:
`pgn` simply tells us how likely it is for us to finish in the next 2
flips if we have flipped the coin `2*(n-1)` times steps already. But we
are looking for the probability of finishing at `2*n` steps.

For this, we can now define `$r_{n}$` that tells us the probability
of arriving at a sequence with `2*n` coin flips. This can only have
happened if we arrived at the last step and did not finish there. We
define `$r_{n}$` recursively:

<div>
	$$r_{0}=1\\
	r_{n}=r_{n-1}-\frac{1}{2*(n-1)}*r_{n-1}$$
</div>

Now, defining `$p_{n}$` is simple: `$p_{n}=\frac{1}{2*n}*r_{n}$`.

Final Formula and Final Code
----------------------------

Our final formula for the expected value is thus

<div>
	$$\mathbb{E}=\sum_{i=1}^{\infty} \frac{1}{2*i}*r_{i}*2*i$$
</div>

We could implement `$r_{n}$` very easily:

	r::{r(x-1)-pgn(x-1)*r(x-1)}

But since we don't want to compute `$r_{n}$` every time we execute
a new iteration, we simply embed it into the final evaluation function:

	ev::{[px];px::pgn(x);.p(($x),",",($px*y),",",$z);.f(x+1;y-(y*px);z+2*x*y*px)}

`x` is the number of flips, `y` is the probability of not finishing after
`x` steps, and `z` is the expected value. The function calculates the
probability of finishing at the current step, prints the current expected
value, and passes its updated arguments forward, subtracting `y*px` from
`y`.

We now call ev:

	ev(1;1;0)

Here is a sample output, piped through `tr , '\t'` to make it easier to read:

	1	0.5	0
	2	0.125	1.0
	3	0.0625000000000000001	1.5
	4	0.0390624999999999998	1.875
	...
	99998	0.00000000892092166024425108	356.819024780555414
	99999	0.00000000892078784508119576	356.820808929203776
	100000	0.0000000089206540332635195 	356.822593068931216
	100001	0.00000000892052022479110523	356.824377199737868

The first field is the number of iterations, the second field is the
probability of finishing at the given iteration, and the third field
is the expected value at the given step.

Proof of Divergence
-------------------

After watching the output of the code above for a while, one gets the
suspicion that the expected value diverges to infinity.

To prove this, let the `$\mathbb{E}_n$` for `$n \in \mathbb{N}$` be the
expected value if we finish throwing the coin after `2*n` steps:

<div>
	$$\mathbb{E}_n=\sum_{i=1}^{n} \frac{1}{2*i}*r_{i}*2*i$$
</div>

We now want to show that

<div>
	$$\lim_{n \to \infty} \mathbb{E_{n}}=\lim_{n \to \infty} \sum_{i=1}^{n} r_{i}=\infty$$
</div>

We will show that `$r_{n} \ge \frac{1}{n}$`, and since we know the
[harmonic series](https://en.wikipedia.org/wiki/Harmonic_series_\(mathematics\))
diverges, we can make a
[direct comparison test](https://en.wikipedia.org/wiki/Direct_comparison_test)
and show that `$\sum_{i=1}^{n} r_{i}$` diverges as well.

Let `$r_{n}$` be

`$r_{0}=1$`  
`$r_{n}=r_{n-1}-\frac{1}{2*(n-1)}*r_{n-1}$`

#### Proof that `$r_n \ge \frac{1}{n}$`

Proof by induction.

Induction Basis:

<div>
	$$r_{0}=1 \ge 1=\frac{1}{1}$$
</div>

Induction Assumption:

<div>
	$$r_n \ge \frac{1}{n}$$
</div>

Induction Step:

<div>
	$$r_{n+1} \ge \frac{1}{n+1}\\
	r_{n}-\frac{1}{2*n}*r_{n} \ge \frac{1}{n+1}\\
	r_{n}*(1-\frac{1}{2*n}) \ge \frac{1}{n+1}\\
	r_{n} \ge \frac{1}{(n+1)*(1-\frac{1}{2*n})}\\
	r_{n} \ge \frac{1}{n+\frac{1}{2}-\frac{1}{2*n}}$$
</div>

Inserting the assumption:

<div>
	$$r_{n} \ge \frac{1}{n} \ge \frac{1}{n+\frac{1}{2}-\frac{1}{2*n}}\\
	n+\frac{1}{2}-\frac{1}{2*n} \ge n\\
	\frac{1}{2} \ge \frac{1}{2*n}\\
	n \ge 1$$
</div>

Since `$n \in \mathbb{N}$`, we have therefore proven that

<div>
	$$\lim_{n \to \infty} \sum_{i=1}^{n} \frac{1}{i}=\infty \le \lim_{n \to \infty} \sum_{i=1}^{n} r_{i}=\infty$$
</div>

Further Considerations
----------------------

This model can be generalized to the average length of a random walk
with steps with length 1 in `$\mathbb{Z}$` starting at 0 and ending at 0.

The question poses itself whether the found length would still hold in
`$\mathbb{Z}^n$` (`$n \ge 2$`) for steps of size 1. It _seems_ obvious
that this should be the case, but one shouldn't be too sure of it.

External Links
---------------

* [“Q: If you flip a coin forever, are you guaranteed to eventually flip an equal number of heads and tails?”](https://www.askamathematician.com/2014/01/q-if-you-flip-a-coin-forever-are-you-guaranteed-to-eventually-flip-an-equal-number-of-heads-and-tails/)
* By Neil Webber:
	* [“Flipping a coin until reaching equal heads and tails”](http://neilwebber.com/notes/2018/10/29/flipping-a-coin-until-reaching-equal-heads-and-tails/)
	* [“Coin flips and Catalan Numbers”](http://neilwebber.com/notes/2018/11/18/coin-flips-and-catalan-numbers/)
	* [“Coin flip simulation still running – 62 days!”](http://neilwebber.com/notes/2018/12/26/coin-flip-simulation-still-running-62-days/)
