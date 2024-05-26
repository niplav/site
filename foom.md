[home](./index.md)
------------------

*author: niplav, created: 2024-01-30, modified: 2024-05-20, language: english, status: in progress, importance: 3, confidence: certain*

> __Some thoughts on discontinuous and/or fast takeoff during TAI
development, in response to a twitter question.__

On Discontinuous and Fast Takeoff
==================================

The most fleshed-out model of AI takeoff is [Davidson
2023](https://niplav.site/doc/cs/ai/alignment/takeoff/a_compute_centric_framework_of_takeoff_speeds_davidson_2023.pdf),
which makes the median prediction of 20% automation to 100% automation
in ~3 years (10th percentile: 0.8 years, 90th percentile: 12.5 years).

Along the axes of {fast, slow}×{continuous, discountinuous}, that feels
quite fast to me, even if it isn't very discountinuous.

The other reasons make me move towards "but it might be a lot faster
than that". One reason is that the Davidson model assumes that the human
brain performs 10¹⁵ FLOP/s, and that the AI systems will be at most
that efficient or slightly less efficient. So a lot of my disagreement is
around: __how much the ceiling of cognitive algorithms is above humans__
(my belief: very high<sub>80%</sub>), and the rest of the disagreement
is __how quickly can AI systems move towards that ceiling__ (my belief:
not sure, but potentially within days<sub>40%</sub>).

Better Algorithms Exist
------------------------

One reason is that human brains don't seem like the optimal substrate
for performing cognition: Warm & wet, very low information transmission
speed (signals on neurons are limited to at most 200 m/s) [Kokotajlo
2021](https://www.lesswrong.com/posts/HhWhaSzQr6xmBki8F/birds-brains-planes-and-ai-against-appeals-to-the-complexity),
needing to self-construct and self-repair — and
still brains are incredibly sample-efficient! And I
suspect that, if anything, humans are at best at a [subspace
optimum](https://www.lesswrong.com/posts/yuP4D4Pz79uyPS9KW) of cognitive
algorithms.

Then there's the *power of error-corrected/discrete/serial computation*:
Digital computers can make very long inferences in discrete domains
without problems, and when I introspect, I have the strong intuition
that my system 2 tries to approximate this, especially when trying
to enumerate options in a decision, recursively decompose a plan
into its components (which gets much easier [once you have a world
model](https://bmk.sh/2020/08/17/Building-AGI-Using-Language-Models/)),
perform abstraction (while caching which parts of the
abstraction are tight and which are leaky)—but my system 2 only has
[7±2](https://en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two)
(or maybe [actually just
4](https://en.wikipedia.org/wiki/Working_Memory#Capacity)?) usable
slots. And unless the limit is due to combinatorial explosion (which
might be handleable by careful pruning, or prioritized search), AI
systems could have larger (perhaps vastly larger?) working memories.

The standard rejoinder here is that evolution has optimized human
brains really really hard, and our current technology is usually 2-6
orders of magnitude worse than what evolution has come up with<!--TODO:
find Christiano investigation into this-->. But if we believe that
error-corrected computation is quite rare in biology, then this opens
up a new niche to make progress in, similar to how there are no plants
in space because they couldn't evolve rocket-like tech and transparent
shells that were resistant enough in vacuum.

This points at an intuition I have: There is a bunch of α left
in combining error-corrected/discrete/serial computation (which
computers are good at) with error-resistant/continuous/parallel
computation (à la neural networks or brains). And especially if
I think about cognition through the lens of algorithms, it feels
like there's a *deep mine of algorithms*: The space of possible
algorithms is vast, and even in *very* simple problem domains we have
found surprising innovations (such as going from the [Karatsuba
algorithm](https://en.wikipedia.org/wiki/Karatsuba_algorithm)
to the [Schönhage-Strassen
algorithm](https://en.wikipedia.org/wiki/Schönhage-Strassen_algorithm),
or from the naive algorithm for the [maximum subarray
problem](https://en.wikipedia.org/wiki/Maximum_Subarray_problem)
to Kadane's algorithm). My "optimism" here has been hindered
somewhat by some evidence on how well [old chess algorithms perform on new
hardware](https://www.lesswrong.com/posts/J6gktpSgYoyq5q3Au/benchmarking-an-old-chess-engine-on-new-hardware),
and the observation that the surprising algorithms we find are
usually galactic (such as in the case of the [decreasing shrinking
rate of the best-case exponent in the computational complexity of matrix
multiplication](https://en.wikipedia.org/wiki/Computational_complexity_of_matrix_multiplication#Matrix_multiplication_exponent)—where
yet we still only use [Strassen's
algorithm](https://en.wikipedia.org/wiki/Strassen's_algorithm)).

Additionally, there's some domains of computation of which we have
made little use, *because* our minds are limited in a way that makes
it difficult to think about them. As the adage goes, programming is
divided into four levels of difficulty: `if` statements, `while`
loops, [recursion](https://en.wikipedia.org/wiki/Recursion) and
[parallelism](https://en.wikipedia.org/wiki/Parallelism_\(computing\));
but what about domains like [self-modifying
code](https://en.wikipedia.org/wiki/Self-modifying_code) (where, except
maybe [Gödel machines](https://en.wikipedia.org/wiki/Gödel_machine),
there is no respectable theory, and except [Alexia
Massalin's](https://en.wikipedia.org/wiki/Alexia_Massalin)
[superoptimization](https://en.wikipedia.org/wiki/Superoptimization) there
isn't really any application)? Although, to be fair, [neural architecture
search](https://en.wikipedia.org/wiki/Neural_architecture_search) might
be getting there, sometime.

<!--TODO: Additionally, people seem to have *forgotten about thinking*:-->

My view on better algorithms existing is *not*
informed very much by [specific observations about
evolution](https://www.lesswrong.com/posts/hvz9qjWyv8cLX9JJR/evolution-provides-no-evidence-for-the-sharp-left-turn).

Better Algorithms are Quickly Reachable
----------------------------------------

As in the section about better algorithms existing, many of my intuitions
here come from algorithm design and/or regular software engineering.

One argument against discountinuous takeoff is a response
to the hypothesis of recursive self-improvement, in
which AI systems start finding improvements to their own
architectures more and more quickly (which I try to model
[here](./toy_ai_takeoff_model.html)). The counterargument says that
before there will be AI systems that are really good at self-improvement,
there [will be systems that are first crappy and then merely okay at
self-improvement](https://sideways-view.com/2018/02/24/takeoff-speeds/).<!--TODO:
link page that collects examples of these in current ML?-->

But usually, with algorithms, having a 99%-finished implementation of the
algorithm doesn't give you 99% of the benefit, nor does it give you 50%
or even 1% of the benefit. It simply doesn't work. And here intuitions
collide: I find it plausible that, in this case, the [The Gods of Straight
Lines](https://www.lesswrong.com/posts/xkRtegmqL2iyhtDB3/the-gods-of-straight-lines)
do not interfere, and instead something far stranger is afoot, but
the machine learning intuition tells people that everything in neural
networks is continuous, so why wouldn't there be a continous path to a
TAI architecture?<!--TODO: link continuity assumption post by Kulveit?-->

See Also
---------

* [Takeoff speeds (Paul Christiano, 2018)](https://sideways-view.com/2018/02/24/takeoff-speeds/)
* [Optimization and the Intelligence Explosion (Eliezer Yudkowsky, 2015)](https://www.lesswrong.com/rationality/optimization-and-the-intelligence-explosion)
