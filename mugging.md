[home](./index.md)
-------------------

*author: niplav, created: 2025-08-27, modified: 2025-10-27, language: english, status: in progress, importance: 4, confidence: possible*

> __I [~formalize](#Formalizing_Pascals_Mugging) [Pascal's
mugging](https://nickbostrom.com/papers/pascal.pdf)
for utility-maximizing [Solomonoff
inductors](https://en.wikipedia.org/wiki/Solomonoff_induction) with a
[simplicity prior](https://en.wikipedia.org/wiki/Kolmogorov_complexity),
and then characterize a set of utility functions that are [immune to
mugging](#Mugging_Immunity). The utility functions in this set have
strongly diminishing marginal returns, utilities must grow slower than
`$2^{CB^{-1}(k)}$`, that is, slower than the exponential of the inverse
of a busy-beaver-like function. This "breaks the boundedness barrier"
for mugging-immune utility functions.__
>
> __[Switching to a Levin-style speed prior](#The_Need_for_Speed)
half-solves this kind of Pascal's mugging, using the Leverage penalty
fully solves it, but at the cost of strongly penalizing high-utility
hypotheses.__

Mugging-Immune Utility Functions
=================================

I first attempt to formalize Pascal's mugging, then characterize a set
of mugging-immune utility functions, and finally speculate on how one
might escape the very harsh bound I have discovered.

In previous discussions, a commonly-agreed upon
solution to Pascal's mugging was to have a [bounded utility
function](https://www.lesswrong.com/posts/gJxHRxnuFudzBFPuu/better-impossibility-result-for-unbounded-utilities),
which is unsatisfying from a utilitarian perspective—a
utilitarian ideally wants to be able to say that twice as much
of a good thing is twice as good, or at least say that [strictly
more](https://en.wikipedia.org/wiki/Strictly_increasing_function) of a
good thing is strictly better.

### ~Formalizing Pascal's Mugging

__Summary__: The prior probability of worlds decreases exponentially with
increasing program length, but the utility of some program output can
grow *very quickly*: Almost as fast as the busy beaver numbers.

Consider a muggee `$\Finv$` that implements [Solomonoff
induction](https://en.wikipedia.org/wiki/Solomonoff_induction)
as its epistemic process. Specifically, for the set of computable
programs `$\mathbf{C}$` with binary tape state, the prior probability
assigned by `$\Finv$` for `$C \in \mathbf{C}$` is proportional to
`$2^{-l(C)}$`—we're using the simplicity prior[^semi].

[^semi]: I think this is technically called a universal semimeasure. I don't think this distinction kills the below arguments/proof-sketches<sub>85%</sub>, but obviously can't guarantee it.

That is, intuitively, the prior probability decreases exponentially in
the length of the program.

Let `$U_\Finv$` be the muggee's [quasilinear utility
function](https://en.wikipedia.org/wiki/Quasilinear_utility_function),
that is, the muggee has a
[numéraire](https://en.wikipedia.org/wiki/Numéraire) `$n_\Finv \in \{0,
1\}^+$` which their utility function is linear in. This numéraire can be
anything from money, happy observer-moments, paperclips, you name it. We
can call the shortest program that outputs one instance of our numéraire
`$C_n$`.

We can now handwavingly construct a mugging program `$M_k$` from
`$\mathbf{C}$`.

Given a budget of `$k$` bits (`$k>l(C_n)$`): First it runs
`$C_n$` and thus writes an instance of our numéraire `$n_\Finv$`
to the tape, and then copies that instance as many times as
it can before it halts. The number of copies written to the
tape in the second step is upper-bounded by the [busy-beaver
number](https://en.wikipedia.org/wiki/Busy_Beaver_Number) `$S(2,
k-l(C_n))$`, that is the maximum number of steps possibly taken
by the second part program. (It is unfortunately *not* bounded by
`$\Sigma(2,k-l(C_n))$`, the number of `1`s written to the tape, since
writing the numéraire may require writing zeroes.)

#### Sketch

More detail on `$M_k$`: You can take the busy beaver program, and then add
some business logic where the numéraire output is interleaved between
the busy beaver logic, plus some subroutines that copy and move more
than one step.

	busy beaver step
	walk to offset
	copy
	walk back
	busy beaver step

This program is a constant number of bits larger than the busy beaver
program, namely the code for the "business logic".

---------------------

`$M_k$` will, I believe, behave busy-beaver-*like* in that it writes
an enormous number of `$n_\Finv$` to the tape before halting. It won't
quite write `$S(2, k-l(C_n)$` copies of the numéraire on the tape,
but it will grow much faster than any standard sequence one may care to
name, definitely faster than any polynomial, faster than factorials,
surely faster than the Ackermann function… and, most notably, much
*much* faster than an exponential.

__Definition__: I'll give the growth rate of `$M_k$` the name `$CB(k)$`,
the "__copy-beaver number__", which is the maximal number of copies a
program of length `$n$` can make of a pre-written tape-state.

The copy-beaver
number is definitely smaller than the busy-beaver number, but my best
guess is that it still grows much faster than almost all functions we
can characterize<sub>85%</sub>, that it has "busy-beaver-like" growth
behavior.

This leads to a simple consequence: in `$k$`, the expected
value of the mugging program `$M_k$` for the muggee `$\Finv$` is
[unbounded](https://www.lesswrong.com/posts/hbmsW2k9DxED5Z4eJ/impossibility-results-for-unbounded-utiliti
es)
in program length.

<div>
        $$\lim_{k \rightarrow \infty} 2^{-k} \cdot CB(k) = \infty$$
</div>

I don't know if this is the only way of formalizing Pascal's mugging.

### Mugging Immunity

__Summary__: We can circumvent Pascal's mugging by having utilities grow
*extremely slowly* in whatever goods we are presented with, almost as
slowly as the inverse of the busy beaver function.

Note that this is *not* solved by having logarithmically [diminishing
returns](https://en.wikipedia.org/wiki/Diminishing_Returns) in some
resource, if we believe that the copy beaver function has a slower growth
rate than a double exponential, which, nah.

<div>
        $$2^{-k} \cdot \log(CB(k)) \le c \Leftrightarrow \\
        CB(k) \le \exp(c \cdot 2^{k})$$
</div>

Note that in this case `$n_\Finv$` isn't a numéraire anymore, since
utility functions are linear in those.

__Definition__: I'll call the goods a utility function is
[monotonic](https://en.wikipedia.org/wiki/Monotonic_function) but not
linear in "__pseudo-numéraires__". `$c$` is just some constant.

But we now have an interesting foothold! Logarithmic utility grows
too quickly, *but* we can *identify* the growth rate of utility for
our pseudo-numéraire so that we don't get this kind of divergence
of utilities.

Specifically, we need a utility function `$U_i$` immune to mugging so that `$U_i(CB(k)) \cdot 2^{-k} \le c$`, which (under the
assumption that `$CB$` is invertible) leads to:

<div>
        $$U_i(CB(k)) \cdot 2^{-k} \le c \Leftrightarrow \\
        U_i(CB(k)) \le c \cdot 2^k \Leftrightarrow \\
        U_i(k) \le c \cdot 2^{CB^{-1}(k)}$$
</div>

(Abusing notation, `$U_i(k)$` is the utility of `$k$` copies of the
pseudo-numéraire.)

__Definition__: We can now identify a set of "__mugging-immune utility
functions__" with a single pseudo-numéraire `$k$`:

<div>
        $$\mathcal{I}=\{U_i : \mathbb{R}^+ \rightarrow \mathbb{R} \mid U_i(k) \le c \cdot 2^{CB^{-1}(k)}\}$$
</div>

This result isn't *exact*—there may be programs that are mugger-like
but grow somewhat faster (e.g. by not first writing the pseudo-numéraire
and then copying, but doing something more complex and interleaved.) But
the result is "spiritually correct".

### Multiple Numéraires

One issue that may come up is that a muggee has multiple
pseudo-numéraires. I'm pretty sure that a small number of
pseudo-numéraires isn't a problem and difficult to mug, assuming that
all of them grow slower than the bound outlined above.

But if a muggee has a truly astronomical number of pseudo-numéraires
that are easy to generate programmatically, e.g. all [prefix
codes](https://en.wikipedia.org/wiki/Prefix_code), we do get
issues. Similar to a "death by a thousand cuts" the mugger basically
tells us "Ah, but what about a world in which you have this one thing
you like the first instance of, and this other thing, and yet this other
thing…", for a lot of different numéraires.

Specifically, if the number of pseudo-numéraires is greater than
`$CB(\log_2(k))$`, then a mugger of Kolmogorov complexity `$k$` can still
succeed by writing one instance of each pseudo-numéraire on the tape,
receiving the high utility from the first marginal instance of each
pseudo-numéraire. The number of numéraires here needs to increase
very rapidly because there's such harsh diminishing returns for each
numéraire.

I think that this will not happen in practice for most utility functions,
but it seemed worth noting.

### Escaping?

These bounds are pretty harsh. The inverse copying beaver grows *very
slowly*<sub>99%</sub>; you're not quite upper-bounded in utility, but
you might as well be.

Is there hope?

Well, maybe. I elided a lot of constant factors, asymptotic growth
rates &c from the sketch above. My hope is that one can "choose"
the level at which one becomes mugging-immune by selecting the
right constants and tweaking the growth rate. The resulting utility
function should then be ~linear for the resources attainable in
our current guesses for the attainable value in the [reachable
universe](https://en.wikipedia.org/wiki/Observable_Universe), and grows
more slowly after that. After all, the inverse copying beaver grows
so slowly that it can look *like* a bounded utility function if the
constants are selected right.

But I don't have a great intuition for when that kind of constant-picking
is possible and when it isn't; we may be stuck.

#### The Need for Speed

<!--TODO: Instead switch to explaining the leverage penalty here-->

One way of defeating Pascal's mugging is to switch to a different prior,
specifically one in which the construction of the copy-beaver receives
a very low prior probability—as low as the fake utility it "provides".

One possible solution is to use the [speed
prior](https://en.wikipedia.org/wiki/Speed_Prior)
instead of the [simplicity
prior](https://en.wikipedia.org/wiki/Minimum_description_length):
For the set of computable programs `$\mathbf{C}$` with binary
tape state, the prior probability assigned by by the speed prior
for `$C \in \mathbf{C}$` is proportional to `$2^{-l(C)} \cdot
\frac{1}{s(C)}$` where `$s(C)$` is the number of steps `$C$` takes
before halting[^priors].

[^priors]: Indeed, since we normalize our prior so that it sums to `$1$`, theoretically we can take any function `$f : \mathbf{C} \rightarrow ℕ^+$` of our programs and create a new prior by normalizing `$2^{-(l(C)+f(C))}$` or `$2^{-l(C)} \cdot \frac{1}{f(C)}$`. `$f$` can be [sophistication](https://en.wikipedia.org/wiki/Sophistication_\(complexity_theory\)), [logical depth](https://en.wikipedia.org/wiki/Logical_depth), number of bitflips performed during program execution… any crazy thing you can come up with as long as `$f$` returns positive natural numbers.<!--TODO: is this really true? I haven't *proved* it, maybe there's strange measure theory things going on here-->

I think that the speed prior simply solves mugging in this formalization.

My sketchy reason for believing this looks like this:

<div>
	$$
	\begin{align}
	\lim_{k \rightarrow \infty} \mathbb{E}[U(k)] & \approx \\
	\lim_{k \rightarrow \infty} 2^{-k} \cdot \frac{1}{CB(k)} \cdot CB(k) & = \\
	0
	\end{align}
	$$
</div>

However: It may be that normalization upweights the prior probability
under the speed prior by a "superexponential amount", that is, the
`$2^{-CB(k)}$` vanishes because normalization moves the program up by a
significant amount in terms of prior probability. My guess is that that
doesn't happen (and GPT-5 assures me it doesn't), but I think to prove
it would require thinking about the structure of computable programs,
which I'm not very good at.

Intuitively, the prior cares to equal amounts about how long the program
is and how long it takes to execute. This makes total sense to me,
a human mind composed of neurons trained with an algorithm selected
for by natural and sexual selection: I care about my theories maximally
compressing the world, sure, but I also care about being able to finish
thinking them.

A cool fact about this is that it's almost a pure a-priori
argument: You need to know nothing about the real world, and have
to make remarkably few mathematical assumptions[^assumptions], to arrive at
this conclusion: Mixing in a speed prior into your complexity prior
saves you from this type of copying Pascal's mugging.

[^assumptions]: Diverging utilities are bad, you're a Solomonoff inductor whose prior has been defined in a particular way.

> All logic is a prior.

*—M Ls, [Comment on “Updatelessness doesn't solve most problems”](https://www.lesswrong.com/posts/g8HHKaWENEbqh2mgK/updatelessness-doesn-t-solve-most-problems-1?commentId=Gxp7tzot2MTWo38md), 2024*

I imagine an extremely advanced agent coming into existence, doing some
mathematics, and then *modifying its prior* based on pure mathematical
reasoning.

Acknowledgements
-----------------

Thanks to Claude 4 & 4.5 Sonnet, Claude 4 & 4.1 Opus and GPT-5 for
discussions on this topic.

See Also
---------

<!--TODO: anthropic capture-->

* [Saint Petersburg Paradox](https://en.wikipedia.org/wiki/St_Petersburg_Paradox)
* [Most* small probabilities aren't pascalian (Gregory Lewis, 2022)](https://forum.effectivealtruism.org/posts/5y3vzEAXhGskBhtAD/most-small-probabilities-aren-t-pascalian)
* [Optimization daemons (Eliezer Yudkowsky, 2016)](https://arbital.com/p/daemons/), [Open question: are minimal circuits daemon-free? (Paul Christiano, 2018)](https://www.lesswrong.com/posts/nyCHnY7T5PHPLjxmN/open-question-are-minimal-circuits-daemon-free)
* [Anthropics and the Universal Distribution (Joe Carlsmith, 2022)](https://joecarlsmith.com/2021/11/28/anthropics-and-the-universal-distribution)
* [GPT-5 on this post](./outputs/mugging_feedback.html), some complaints already fixed.

Appendix A: The Pure Speed Prior
---------------------------------

I have a very impractical idea: Can we have a *pure* speed prior? One
that only cares about how fast programs finish running?

The intuitive answer may seem "no" at first, since unlike with program
length we have, for every number of steps a program needs to halt,
countably infinitely many programs that take that many steps to halt,
forcing us to say that any particular program has a prior [Lebesgue
measure of zero](https://en.wikipedia.org/wiki/Almost_Never).

<!--TODO: nevertheless press on with the need for speed, describing the
pure speed prior, note that it's a bad prior-->
