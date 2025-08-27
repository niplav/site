[home](./index.md)
-------------------

*author: niplav, created: 2025-08-27, modified: 2025-08-27, language: english, status: draft, importance: 4, confidence: possible*

> __I formalize [Pascal's
mugging](https://nickbostrom.com/papers/pascal.pdf)
for utility-maximizing [Solomonoff
inductors](https://en.wikipedia.org/wiki/Solomonoff_induction), and then
characterize a set of utility functions that are immune to mugging. The
utility functions in this set have strongly diminishing marginal returns,
utilities must grow slower than `$2^{CB^{-1}(k)}$`, that is, slower than
the exponential of the inverse of a busy-beaver-like function.__

Mugging-Immune Utility Functions
=================================

I first attempt to formalize Pascal's mugging, then characterize a set
of mugging-immune utility functions, and finally speculate on how one
might escape the very harsh bound I have discovered.

### Formalizing Pascal's Mugging

__Summary__: The prior probability of worlds decreases exponentially with
increasing program length, but the utility of some program output can
grow *very quickly*: Almost as fast as the busy beaver numbers.

Consider a muggee `$\Finv$` that implements [Solomonoff
induction](https://en.wikipedia.org/wiki/Solomonoff_induction)
as its epistemic process. Specifically, for the set of computable
programs `$\mathbf{C}$` with binary tape state, the prior probability
assigned by `$\Finv$` for `$C \in \mathbf{C}$` is proportional to
`$2^{-l(C)}$`—we're using the simplicity prior, after all.

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
`$\Sigma(2,k-l(C_n))$` since writing the numéraire may require writing
zeroes.)

`$M_k$` will, I believe, behave busy-beaver-*like* in that it writes
an enormous number of `$n_\Finv$` to the tape before halting. It won't
quite write `$S(2, k-l(C_n)$` copies of the numéraire on the tape,
but it will grow much faster than any standard sequence one may care to
name, definitely faster than any polynomial, faster than factorials,
surely faster than the Ackermann function… and, most notably, much
much faster than an exponential.

I'll call this growth rate `$CB(k)$`, the "__copy-beaver number__", which
is the maximal number of copies a program of length `$n$` can make of
a pre-written tape-state. The copy-beaver number is definitely smaller
than the busy-beaver number, but my best guess is that it still grows
much faster than almost all functions we can characterize, that it has
"busy-beaver-like" growth behavior.

#### Sketch

You can take the busy beaver program, and then add some business logic
where the numéraire output is interleaved between the busy beaver logic,
plus some subroutines that copy and move more than one step. So the
program is a constant number of bits larger than the busy beaver number:

	busy beaver step
	walk to offset
	copy
	walk back
	busy beaver step

---------------------

This leads to a simple consequence: in `$k$`, the expected
value of the mugging program `$M_k$` for the muggee `$\Finv$` is
[unbounded](https://www.lesswrong.com/posts/hbmsW2k9DxED5Z4eJ/impossibility-results-for-unbounded-utiliti
es)
in program length.

<div>
        $$\lim_{k \rightarrow \infty} 2^{-k} \cdot CB(k) = \infty$$
</div>

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
utility functions are linear in those. I'll call the goods the utility
function is monotonic but not linear in "pseudo-numéraires". `$c$`
is just some constant.

But we now have an interesting foothold! Logarithmic utility grows too
quickly, *but* we can *identify* the growth rate of utility for our
pseudo-numéraire so that we don't get this kind of unboundedness.

Specifically, we need `$U(CB(k)) \cdot 2^{-k} \le c$`, which (under the
assumption that `$CB$` is invertible) leads to:

<div>
        $$U(CB(k)) \cdot 2^{-k} \le c \Leftrightarrow \\
        U(CB(k)) \le c \cdot 2^k \Leftrightarrow \\
        U(k) \le c \cdot 2^{CB^{-1}(k)}$$
</div>

(Abusing notation, `$U(k)$` is the utility of `$k$` copies of the
pseudo-numéraire.)

We can now identify a set of mugging-immune utility functions with a
single pseudo-numéraire `$k$`:

<div>
        $$\mathcal{I}=\{U : \mathbb{R}^+ \rightarrow \mathbb{R} \mid U(k) \le c \cdot 2^{CB^{-1}(k)}\}$$
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

Well, maybe. I elided a lot of constant factors, asymptotic growth rates
&c from the sketch above; my hope is that one can "choose" the level at
which one becomes mugging-immune by selecting the right constants and
tweaking the growth rate. After all, the inverse copying beaver grows
so slowly that it can look *like* a bounded utility function if the
constants are selected right.

But I don't have a great intuition for when that kind of constant-picking
is possible and when it isn't; we may be stuck.

### Questions

1. Can we formulate a prior in which this doesn't happen?
	1. What about a prior that also penalizes the size of the finally output, exponentially in length?
	2. Does the speed prior basically fulfill this condition?

See Also
---------

<!--TODO: anthropic capture-->

* [Most* small probabilities aren't pascalian (Gregory Lewis, 2022)](https://forum.effectivealtruism.org/posts/5y3vzEAXhGskBhtAD/most-small-probabilities-aren-t-pascalian)
* [Optimization daemons (Eliezer Yudkowsky, 2016)](https://arbital.com/p/daemons/), [Open question: are minimal circuits daemon-free? (Paul Christiano, 2018)](https://www.lesswrong.com/posts/nyCHnY7T5PHPLjxmN/open-question-are-minimal-circuits-daemon-free)
* [Anthropics and the Universal Distribution (Joe Carlsmith, 2022)](https://joecarlsmith.com/2021/11/28/anthropics-and-the-universal-distribution)
