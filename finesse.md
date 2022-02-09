[home](./index.md)
-------------------

*author: niplav, created: 2022-02-04, modified: 2022-02-05, language: english, status: notes, importance: 4, confidence: likely*

> __I describe boundary conditions for a function that estimates how
random a set of resolved forecasts in a specific interval of probabilities
is, and describe algorithms that fulfill those conditions.__

Finesse of Sets of Forecasts
=============================

*epistemic status: likely not just reinventing the wheel, but the whole bicycle*

Say we have a set of resolved forecasts and can display them on a
calibration plot.

We can grade the forecasts according to some proper scoring rule,
e.g. the Brier score.

But we can also ask the question: how fine-grained are the predictions of
our forecaster? I.e., at which level of finesse can we assume that
the additional information is just noise?

Take, for example, somebody who always gives their forecasts with 5
decimal digits, even though if we look at the calibration plot, we see
that they are pretty much random in any given interval of length 0.1
(i.e., their forecast with 15% and a forecast of 5% can be expected to
resolve to the same outcome with equal probability).

Let us call this number the finesse `$\mathcal{F}$` of a set of forecasts.

We can eyeball this number, sure, but how can we determine it
programatically?

Available Information
----------------------

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

* If `$n=0$`, `$s(\emptyset, \mathcal{F})$` is undefined.
* If `$n=1$`, `$s(\mathbf{D}, \mathcal{F})=0$`: We are generally suspicious of any single forecast.
	* More generally, if `$\mathbf{D}$` contains an `$f_i$` so that there is no other prediction with a probability within `$[f_i-\frac{\mathcal{F}}{2}; f_i+\frac{\mathcal{F}}{2}]$`, then `$s(\mathbf{D}, \mathcal{F})=0$`. Yes, even if the set of forecasts is "dense" and non-random in other places.
* If `$n=2$`, then it should hold for an `$ε>0$` (but close to 0): `$s(((ε, 0), (1-ε, 1)), 1)=1$`, and `$s(((ε, 0), (1-ε, 1)), 0.5)=0$`.
	* More generally, if we have only zeros in the left half and ones in the right half, with `$n \rightarrow \infty$`, and a sufficiently small `$\frac{1}{n}>ε>0$`, it should hold that `$s(((ε,0),(2ε,0), \dots, (\lfloor \frac{n}{2} \rfloor ε, 0), (\lceil \frac{n}{2} \rceil ε, 1), \dots, (nε, 1)), \mathcal{F})$` is `$1$` for `$\mathcal{F}=1$` and `$0$` for `$\mathcal{F} \le 0.5$`.
* For a sufficiently large `$n \rightarrow \infty$`, and a sufficiently small `$\frac{1}{n}>ε>0$`, and `$r(p)$` being 1 with probability `$p$` and 0 with probability `$1-p$`, it should hold that `$s(((ε,r(ε)),(2ε,r(2ε)), \dots, (\lfloor \frac{n}{2} \rfloor ε, r(\lfloor \frac{n}{2} \rfloor ε)), (\lceil \frac{n}{2} \rceil ε, r(\lceil \frac{n}{2} \rceil ε)), \dots, (nε, r(nε))), \mathcal{F})=1$` for any `$\mathcal{F}$`: If we have lots of datapoints, all perfectly calibrated, the score is nearly 0 at all finesses.
* In expectation, if we sample every `$o_i$` uniformly from `$\{0, 1\}$` with replacement, `$s(\mathbf{D}, \mathcal{F})=0$`.
* With `$\mathcal{F}_1<\mathcal{F}_2$`, `$s(\mathbf{D}, \mathcal{F}_1) \le s(\mathbf{D}, \mathcal{F}_2)$` (smaller finesse shouldn't lead to a greater score, since if you're uncalibrated at a finesse of 10%, you're not going to be suddenly calibrated at a finesse of 5%)

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
