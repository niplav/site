
### A Toy Scaling Law

Correcting my own 3.5: consider a choice, before birth and behind a
veil of ignorance (only known: one will be male), between (a) siring
exactly two offspring then dying, and (b) a randomly drawn male life.
At population equilibrium (~50/50 sex ratio, zero growth), every
offspring has one father, so `$E[\text{offspring} \mid \text{random male life}] = 2$`
by pure bookkeeping — the two options are EV-equal, no kin-selection
discount needed.

EV-equal isn't fitness-equal, though: selection tracks something closer
to the *geometric* mean of reproductive success across generations
(Gillespie 1977), so a same-mean, *higher-variance* strategy is
disfavored. Promiscuous/tournament mating is close to zero-sum over a
shared partner pool — it inflates variance in male reproductive success
without raising the mean — so pair-bonding can be more evolutionarily
rational purely on variance-aversion grounds, before paternal
investment even enters.

This only bites at finite `$N_e$`, though. Two distinct
"variance matters" mechanisms exist: cross-generation environmental
stochasticity (classical bet-hedging, holds even at infinite population
size), and within-generation variance in individual offspring number
(Gillespie's mechanism — a drift effect `$\sim N_e^{-1}$`, vanishing as
`$N_e \to \infty$`). For the latter, the relevant N is the *ancestral
breeding population's* effective size, not census size: human `$N_e$`
is estimated around `$10^4$`, suppressed partly *because* high-variance
male reproductive success itself shrinks `$N_e$` (Wright's correction).
So 3.5's "just treat it as infinite" doesn't work — the relevant
population was never close to infinite.

### An Age-Fertility Law

Putting structure on 3.2–3.4: model the value of `$m$` "chances"
(fertile-cycle exposures, not literal acts — evolution doesn't track
contraception, so what matters is opportunities across cycles) with a
partner of age `$n$`:

<div>$$V(n, m) = W \cdot \left[1 - (1 - p(n))^m\right]$$</div>

`$p(n)$` is per-cycle conception probability by age; `$W$` is a
paternal-investment discount (fixed at 1 under the zero-investment
idealization; in reality this is where most of casual sex's real
discount lives, given human altriciality).

A stylized logistic law for `$p(n)$` (not fit to real data — see
Dunson, Colombo & Baird 2002):

<div>$$p(n) = \frac{p_{max}}{1 + \exp\left(\frac{n - n_0}{s}\right)}$$</div>

`$1-(1-p(n))^m$` answers question 4 directly: concave and saturating
fast in `$m$`. It also answers 3.4's "&c.": more chances are worth more
with a younger (more fertile) partner, since the curves in `$m$` fan
out by age. And it gives the shape behind the
[Coolidge effect](https://en.wikipedia.org/wiki/Coolidge_effect):
`$V(n,m)$` diminishes fast in `$m$` for one partner but resets high for
a new one.

Code + plots:
[`code/daygame/scaling.jl`](https://github.com/niplav/site/blob/master/code/daygame/scaling.jl).

![A stylized age-fertility curve](./img/daygame/scaling_fertility.png "A stylized logistic age-fertility curve for per-cycle conception probability.")

![Diminishing returns to repeated chances with the same partner, by partner age](./img/daygame/scaling_value_m.png "V(n,m) against m for several fixed ages n — steep diminishing returns, fanning out with younger/more fertile partners.")

![The V(n,m) surface](./img/daygame/scaling_heatmap.png "The full V(n,m) surface across partner age and number of chances.")

### Perceived Effective Population Size as a Value Input (Speculative)

Pushing `$N_e$` further than the evidence supports: what if the value
function itself took a *perceived* `$N_e$` as input, on the (unlikely,
indulge-it) theory that organisms sense local density and tune a
risk-aversion knob accordingly? Not a rigorous derivation — the real
Gillespie effect is population-level, not a per-decision utility — but
a coherent toy.

For `$k$` independent partners at fixed `$(n,m)$`, each yields at least
one offspring with probability `$c = 1-(1-p(n))^m$`, so aggregate
offspring `$\sim \mathrm{Binomial}(k,c)$` with mean `$\mu = kc$` and
variance `$\sigma^2 = kc(1-c)$`. A mean-variance utility with
risk-aversion `$\gamma(N_e)$` decreasing in `$N_e$`:

<div>$$U(n,m,k;N_e) = kc - \gamma(N_e)\,kc(1-c)$$</div>

This only *looks* like it drops `$n$` and `$m$` — `$c$` is shorthand for
`$c(n,m)$`, and since `$1-c=(1-p(n))^m$` exactly, it has a genuine
closed form in all four parameters:

<div>$$U(n,m,k;N_e) = k\left[1-(1-p(n))^m\right]\left[1-\gamma(N_e)(1-p(n))^m\right]$$</div>

with `$p(n)$` as above and `$\gamma(N_e) = C \cdot N_e^{-1}$` for some
constant `$C$`. The marginal value of one more partner,

<div>$$\frac{\partial U}{\partial k} = c\left(1 - \gamma(N_e)(1-c)\right)$$</div>

goes negative for low-`$c$` (low `$m$`, old `$n$`) partners once
`$\gamma(N_e)$` is large enough — `$c(1-c)$` peaks at `$c=0.5$` and
vanishes as `$c \to 1$`, so the model specifically penalizes *uncertain*
partners. Small perceived `$N_e$` should push toward concentrating on
fewer, surer partners (raise `$m$`) over spreading across many uncertain
ones (raise `$k$`); as `$N_e \to \infty$`, it collapses to plain
EV-maximization.

`code/daygame/scaling.jl` implements this (`gamma_risk`,
`marginal_value(n, m, Ne)`) with `$N_e$` as an explicit parameter, using
an illustrative constant to make the crossover visible:

![Marginal value of one more partner, by perceived N_e](./img/daygame/scaling_Ne.png "The marginal value of pursuing one more partner at (n,m), for several values of perceived N_e — small N_e drives low-chance partners to negative marginal value; large N_e recovers plain expected-value maximization.")
