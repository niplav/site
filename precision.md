[home](./index.md)
-------------------

*author: niplav, created: 2022-02-04, modified: 2022-06-28, language: english, status: notes, importance: 4, confidence: likely*

> __I discuss proposals for a function that estimates how much predictive
information additional degrees of precision in forecasts add and at which
point additional precision is just noise, and investigate these proposals
with empirical forecasting data. I furthermore describe desirable boundary
conditions for such functions.__

<!--https://nitter.hu/tenthkrige/status/1412457737380839432-->
<!--https://stanford.edu/~knutson/nfc/mellers15.pdf-->
<!--https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/D9FAZL-->

Precision of Sets of Forecasts
=================================

*epistemic status: likely not just reinventing the wheel, but the whole bicycle*

<!--
TODO: Revamp the naming & notation a bit. Granularity or precision instead?
-->

Say we have a set of resolved forecasts and can display them on a
calibration plot.

We can grade the forecasts according to some proper scoring rule,
e.g. the [Brier score](https://en.wikipedia.org/wiki/Brier_score)
or the [logarithmic scoring
rule](https://en.wikipedia.org/wiki/Scoring_rule#Logarithmic_scoring_rule).

But we can also ask the question: how fine-grained are the predictions of
our forecaster? I.e., at which level of finesse can we assume that
the additional information is just noise?

Take, for example, a hypothetical forecaster Baktiu who always gives
their forecasts with 5 decimal digits of precision, such as forecasting a
"24.566% probability of North Korea testing an ICBM in the year 2022",
even though if we look at their calibration plot, we see that they are
pretty much random in any given interval of length 0.1 (i.e., their
forecast with 15% and a forecast of 5% can be expected to resolve to
the same outcome with equal probability). This means that 4 of the 5
decimal digits of precision are just noise!

Baktiu would be behaving absurdly; misleading their audience into
believing they had spent much more time on their forecasts than they
actually had (or, more likely, into correctly leading the audience into
believing that there was something epistemically sketchy going on).

As an aside, I believe something similar is going on when people
encounter others putting probabilities on claims: It appears like
an attempt at claiming undue quantitativeness (quantitativity?) in
their reasoning, and at making the listener fall prey to [precision
bias](https://en.wikipedia.org/wiki/Precision_bias). However,
not all precision in prediction is [false
precision](https://en.wikipedia.org/wiki/False_precision): At some
point, if remove digits of precision, the forecasts will become worse
in expectation.

But how might we confront our forecaster Baktiu from above? How might we
estimate the level of degrees of precision after which their forecasts
gave no more additional information?

Available Information
----------------------

Definitions
------------

Let us call this number the finesse `$\mathcal{F}$` of a set of forecasts.

We can eyeball this number, sure, but how can we determine it
programatically?

Let `$\mathbf{D}=((f_1, o_1), \dots, (f_n, o_n)) \in ((0,1),\{0,1\})^n$`
be a dataset of `$n$` forecasts `$f_i$` and resolutions `$o_i$`, and
`$\mathcal{F} \in [0;1]$` a finesse. Then the score is a function
`$s: ((0,1),\{0,1\})^n \times [0;1] \mapsto [0;1]$` from a set of
forecasts and a finesse to the degree to which the forecasts are random at
`$\mathcal{F}$`, which is `$0$` if the forecasts are completely random
at `$\mathcal{F}$` and `$1$` if the forecasts are completely linear at
`$\mathcal{F}$`.

Conditions for a Finesse Evaluation Function
---------------------------------------------

Use finesse `$ᚠ$` and noise `$ⴟ$`

1. If `$n=0$`, `$s(\emptyset, \mathcal{F})$` is undefined.
2. If `$n=1$`, `$s(\mathbf{D}, \mathcal{F})=0$`: We are generally suspicious of any single forecast.
	1. More generally, if `$\mathbf{D}$` contains an `$f_i$` so that there is no other prediction with a probability within `$[f_i-\frac{\mathcal{F}}{2}; f_i+\frac{\mathcal{F}}{2}]$`, then `$s(\mathbf{D}, \mathcal{F})=0$`. Yes, even if the set of forecasts is "dense" and non-random in other places.
3. If `$n=2$`, then it should hold for an `$ε>0$` (but close to 0): `$s(((ε, 0), (1-ε, 1)), 1)=1$`, and `$s(((ε, 0), (1-ε, 1)), 0.5)=0$`.
	1. More generally, if we have only zeros in the left half and ones in the right half, with `$n \rightarrow \infty$`, and a sufficiently small `$\frac{1}{n}>ε>0$`, it should hold that `$s(((ε,0),(2ε,0), \dots, (\lfloor \frac{n}{2} \rfloor ε, 0), (\lceil \frac{n}{2} \rceil ε, 1), \dots, (nε, 1)), \mathcal{F})$` is `$1$` for `$\mathcal{F}=1$` and `$0$` for `$\mathcal{F} \le 0.5$`.
4. For a sufficiently large `$n \rightarrow \infty$`, and a sufficiently small `$\frac{1}{n}>ε>0$`, and `$r(p)$` being 1 with probability `$p$` and 0 with probability `$1-p$`, it should hold that `$s(((ε,r(ε)),(2ε,r(2ε)), \dots, (\lfloor \frac{n}{2} \rfloor ε, r(\lfloor \frac{n}{2} \rfloor ε)), (\lceil \frac{n}{2} \rceil ε, r(\lceil \frac{n}{2} \rceil ε)), \dots, (nε, r(nε))), \mathcal{F})=1$` for any `$\mathcal{F}$`: If we have lots of datapoints, all perfectly calibrated, the score is nearly 0 at all finesses.
5. In expectation, if we sample every `$o_i$` uniformly from `$\{0, 1\}$` with replacement, `$s(\mathbf{D}, \mathcal{F})=0$`.
6. With `$\mathcal{F}_1<\mathcal{F}_2$`, `$s(\mathbf{D}, \mathcal{F}_1) \le s(\mathbf{D}, \mathcal{F}_2)$` (smaller finesse shouldn't lead to a greater score, since if you're uncalibrated at a finesse of 10%, you're not going to be suddenly calibrated at a finesse of 5%)
	1. We can't just do this by multiplying the result with the finesse, since that would violate condition 4

But what should be done about a calibration plot that looks like this?

![A lopsided calibration plot: Linear and ascending up to 0.5, and then linearly descending to 0](./img/finesse/cap.png "A lopsided calibration plot: Linear and ascending up to 0.5, and then linearly descending to 0")

There are two ways of arguing what, morally, the finesse of the
forecasts is:

* The argument *for* having a score of `$~1$` for every finesse (assuming a large `$n$`) is that inferring the correct way to make forecasts from this calibration plot is trivial: With forecasts of probability `$f_i>0.5$`, re-assign a probability `$f_i:=1-f_i$`.
* The argument *against* giving a score of `$~1$` is that extending this rule would mean that at every kind of correction on the plot is valid, but there is no clear cutoff point that prevents us from applying this to individual predictions ("If you predict 99% instead of 43%, and 1% instead of 13%, and 1% instead of 23%, and […], then you achieve perfect resolution and calibration.")

* Algorithms for quantifying the finesse of calibration plots
	* Input: A list of `n` forecasts and their resolutions
	* First idea:
		* For i=2, n
			* Segment the forecasts into i different segments, ordered by probability
			* Calculate average outcome
			* For two adjacent segments, calculate the slope for those values
			* Append the mean of all slopes of adjacent segments to the array `output`
		* Return `output`
	* Second idea:
		* For i=2, n
			* Segment the forecasts into i different segments, ordered by probability
			* Re-scale each segment to give probabilities from 0 to 1
			* Use a proper scoring rule? Idk I haven't thought this through
	* Third idea:
		* Something like the first idea, but with a sliding window
	* Fourth idea:
		* Average linear regression of all subsequences with length`$\ge \mathcal{F}$`
* Additional ideas:
	* Multiply score with the average number of datapoints inside the given finesse

----

* Add more & more noise to the forecasts and see how Brier score develops
* Start with perfect predictor, the level of noise at which its Brier score is equal to the dataset

----

	import csv
	import statistics
	import numpy as np

	d1=np.array([[1,0.8],[0,0.4],[0,0.65],[1,0.99]]).T
	oc=d1[0]
	pr=d1[1]

	def mse(o,p):
		return np.mean(np.abs(o-p)**2)

	def logit(p):
		return np.log(p/(1-p))

	def logistic(p):
		return 1/(1+np.exp(-p))

	np.random.default_rng().normal(0,1,len(d1[1]))

	def finesse(d, pert=1, s=100):
		o=d[0]
		p=d[1]
		score=mse(o,p)
		print(score)
		pert_scores=[]
		for i in range(0,s):
			perturbed=logistic(logit(p)+np.random.default_rng().normal(0,pert,len(p)))
			pert_scores.append(mse(o,perturbed))
		return np.mean(pert_scores)-score
