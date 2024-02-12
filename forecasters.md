[home](./index.md)
-------------------

*author: niplav, created: 2022-04-04, modified: 2024-01-26, language: english, status: notes, importance: 6, confidence: highly likely*

> __Beginnings of a research agenda about [judgmental
forecasting](https://en.wikipedia.org/wiki/Forecasting#Judgmental_methods).__

Forecasters: What Do They Know? Do They Know Things?? Let's Find Out!
======================================================================

Judgmental forecasting is a fairly recent and (in my humble opinion)
fairly under-researched & under-appreciated human endeavour & field of
research, with some low-hanging fruit (which are getting picked almost
as fast as I can write them up).

The Five Horsemen of Hard Forecasting
---------------------------------------

In general, judgmental forecasting methods operate best in areas with
fast feedback loops, large existing datasets (or at least good reference
classes for base rates) and continuous historical trends.

We can therefore identify the five horsemen of hard forecasting:

* __Long time horizons__: Because most forecasters and traders
[discount](https://en.wikipedia.org/wiki/Discounting) the
future (either due to rewards further in the future being less
certain, or because whatever investment is bound up in a bet
could be used in the mean term, or because they actually weigh
the future lower), and because long term thinking activates [far
mode](https://www.overcomingbias.com/2010/06/near-far-summary.html)
from [construal level
theory](https://en.wikipedia.org/wiki/Construal_level_theory),
the incentives to perform well on long-term questions are weaker
than on short-term questions. Additionally, forecasters receive
much more & better feedback on short-term questions. One would
expect long-term questions to receive less accurate forecasts
because of this, and the evidence points to this being the case ([Dillon
2021](https://rethinkpriorities.org/publications/data-on-forecasting-accuracy-across-different-time-horizons),
[Niplav
2022](https://rethinkpriorities.org/publications/data-on-forecasting-accuracy-across-different-time-horizons)).
But we're often especially interested in long-term questions: How can
we incentivize or create good forecasts on those questions?
* __Reward-correlated predictions__: The clearest examples of this problem
are questions on extinction events: If you forecast doom, you're never
going to get rewarded for it, because the resolution happens *only* in
worlds where the bad outcome didn't occur. Forecasters are [embedded
agents](https://www.lesswrong.com/s/Rm6oQRJJmhGCcLvxh) in the world
they are predicting on, and there is no Cartesian boundary. This can
happen with prediction markets as well: when making predictions on the
outcome of a decision, with the payout of the prediction market being
in a currency that is affected by the decision (for example devaluing
it respective to other currencies), the market might choose the "worse"
decision (according to the metric used for scoring it) because it prevents
the currency from being devalued as much.
* __Low probability events__: Some events are very important, but
have a low probability (extreme stock market crashes, extinction
events, rare diseases, encounters with aliens etc.). But low
probability events are maybe even harder to forecast than long
time horizon events: they often don't have good reference classes,
while long time horizon questions do (that's why we have history and
time series data!), and forecasters very rarely encounter them. We
might just round all probabilities <1% to 0%, lest we get [Pascal's
mugged](https://en.wikipedia.org/wiki/Pascal's_mugging), but in doing
so we close our eyes to possible dangers (and prizes) out there, the
[Talebian](https://en.wikipedia.org/wiki/Nassim_Nicholas_Taleb) approach
of erring on the side of caution by "rounding them *up*" condemns us to
eternal overcaution and conservatism, so as a first step we definitely
want our probabilities to be as accurate as possible.
* __Out-of-distribution situations__: Whenever things with no
clear existing reference class occur, such as novel technologies
(social media, the internet in general, nuclear weapons,
international shipping logistics, and in the future potentially
genetic engineering or self-driving cars), forecasters struggle to
anticipate the consequences (or foresee those shifts). This isn't
limited to forecasters and prediction markets: if regular people,
pundits and domain experts on average do worse than top forecasters
(though as a counterpoint to forecasters>experts see [Leech & Yagudin
2022](https://forum.effectivealtruism.org/posts/qZqvBLvR5hX9sEkjR/comparing-top-forecasters-and-domain-experts)),
then we wouldn't expect them to do much better specifically in very
novel & unforeseen situations (reasons why this could still happen:
experts might have detailed causal models that are outperformed by
simple heuristics in the modal case, but as we go outside of the normal
course of events, those causal & theoretical models break down much more
gracefully than simple surface heuristics).
* __Hard-to-specify events__: Maybe we are slicing up forecasting
the wrong way: as the old adage goes, the hard part is not coming
up with the answer, it is coming up with the right question to
ask. Similarly, for forecasting, we often run into the problem of
specifying exactly *what* we want to know about: Too broad and
you drive away forecasters and traders [who don't want to waste
their time on predicting the whims of whoever resolves the market in the
end](https://www.lesswrong.com/posts/a4jRN9nbD79PAhWTB/prediction-markets-when-do-they-work#I__Well_Defined),
too narrow and you miss what you actually care about or invite
[Goodharting](https://www.lesswrong.com/tag/goodhart-s-law). An
additional layer of complexity is added when hobbyists do your
forecasting, in which case narrow questions just *aren't very interesting
to do predictions on*. This could be seen with the [Metaculus clean meat
tournament](https://www.metaculus.com/questions/3061/animal-welfare-series-clean-meat/):
many questions were just different combinatorial variations on
each other, with maybe five being interesting to predict on,
but not all fourteen, leading to many questions receiving less
than 100 predictions during the tournament. But "interestingness"
and "specifiability" appear to be tugging in opposite directions:
hobbyists are probably most interested in making broad claims that flow
from their worldview, instead of finding minutiae for very specific
questions. Finding ways to create more specific questions on events
(or avoid doing so with clever tricks while still receiving accurate
forecasts) is important and difficult. [Latent variable prediction
markets](https://www.lesswrong.com/posts/ufW5LvcwDuL6qjdBT/latent-variables-for-prediction-markets-motivation-technical)
offer one approach—how easy are they to implement with acceptable UX?

We can use these categories as guideposts: How bad are these as
problems? What approaches have been proposed/tried/implemented so far? If
we can improve one of them without harming our ability to perform well
on the others, we have made progress, if we improve several in tandem,
that's even better.

How Good Are We At Forecasting?
--------------------------------

* How good are long-term forecasts?
	* How quickly does our forecasting ability decrease with increasing range of the question/forecast?
		* Does it decrease at all, or just oscillate wildly?
		* How quickly does performance degrade in different categories of questions (finance, meteorology, global economics, technological development) and by different forecasters (prediction markets, superforecasters & teams)?
	* Are there people who are better long-term forecasters and people who are better short-term forecasters?
		* See [here](https://twitter.com/Simeon_CPS/status/1655277260524453892)
* How good are our forecasts on low-probability events?
* How good are our forecasts on extinction events?
* How good are our forecasts in situations where we have historical discontinuities?
* How quickly/slowly do our forecasts converge to the final answer?
	* When don't they converge?
	* Can we classify convergence/divergence/oscillation behaviors?
* How do prediction markets, professional forecasting teams, internet enthusiasts and large language models compare?
	* <https://forum.effectivealtruism.org/posts/qZqvBLvR5hX9sEkjR/comparing-top-forecasters-and-domain-experts>
	* <https://github.com/MperorM/gpt3-metaculus>
* What is a good formalization of the idea of a forecaster being accurate at a level of n%?
	* See [Precision of Sets of Forecasts](./precision.html)
	* Are better short-term forecasters also better long-term forecasters?
	* Do forecasters become better at forecasting over time?
		* How quickly?
		* Over time/over more forecasts
	* How much does forecaster quantity affect forecast quality on continuous questions? (i.e., extend [Dillon 2021](https://rethinkpriorities.org/publications/how-does-forecast-quantity-impact-forecast-quality-on-metaculus) to continuous data)
		* How much does forecasting time affect forecast quality? That is, what is the relation of accuracy of prediction to the time spent on refining that prediction?
			* Generally, scaling laws for forecasting would be interesting/cool to see.
		* How much do number of resolutions/forecasts matter for forecast quality/learning?
* Do laypeople/pundits/domain experts perform better than forecasters/superforecasters/forecasting teams/prediction markets *specifically* under novel & unforeseen situations?
* Are more extreme views or more conservative views more accurate?
	* Question originally asked in [Hanson 2007](https://www.overcomingbias.com/2007/02/is_truth_in_the.html)
	* Are there people who are better long-term forecasters and people who are better short-term forecasters?
		* See [here](https://twitter.com/Simeon_CPS/status/1655277260524453892)

How Can We Become Better At Forecasting?
-----------------------------------------

### Scoring Rules

* What possible forecasting scoring rules could we develop?
	* Taking into account:
		* Accuracy compared to others
		* Importance of question
	* That incentivize collaboration and positive-sum interactions instead of information-hiding
		* The literature on information elicitation could be useful here
* How can we compare the skill and reliability of forecasters to one another?
	* Metaculus at the moment does this by "who writes good comments". That seems inadequate.
	* Taking into account:
		* Number of questions each forecaster predicted on
		* Calibration
		* Resolution
		* Importance of questions
	* Two boundary methods:
		* Compare using a scoring rule on any question the forecasters predicted on
		* Compare using a scoring rule on the intersection of the questions the forecasters predicted on
	* Two functions of scoring rules: Rewarding or comparing forecasters
	* Related field: honest reporting and information elicitation
		* See also: Section 27.4.2 from Algorithmic Game Theory (Nisan et al. 2007)

### Difficult Types of Questions

* How can we deal with questions with unclear resolution criteria?
	* Collect Metaculus experiments on this
* How do we incentivise good predictions on long-term questions?
	* Ideas:
		* chained temporal forecasts
* How do we incentivise good predictions on low-probability events?
	* Ideas:
		* chained conditional forecasts
* Is there any conceivable way of incentivizing good predictions on extinction events?

### Forecasting Techniques

#### Question Decomposition

If we say "`$X$` will happen if and only if `$Y_1$` and `$Y_2$` and
`$Y_3$`... *all* happen, so we estimate `$P(Y_1)$` and `$P(Y_2|Y_1)$`
and `$P(Y_3|Y_1, Y_2)$` &c, and then multiply them together to estimate
`$P(X)=P(Y_1)·P(Y_2|Y_1)·P(Y_3|Y_2,Y_1·)·$`…", do we usually get a
probability that is close to `$P(X)$`?  Does this *improve* forecasts where
one tries to estimate `$P(X)$` directly?

This type of question decomposition (which one could
call __multiplicative decomposition__) appears to be a
relatively common method for forecasting, see [Allyn-Feuer & Sanders
2023](https://forum.effectivealtruism.org/posts/ARkbWch5RMsj6xP5p/transformative-agi-by-2043-is-less-than-1-likely),
[Silver
2016](http://fivethirtyeight.com/features/donald-trumps-six-stages-of-doom/),
[Kaufman
2011](https://www.jefftk.com/p/breaking-down-cryonics-probabilities),
[Carlsmith 2022](https://arxiv.org/abs/2206.13353) and [Hanson
2011](https://www.overcomingbias.com/p/break-cryonics-downhtml),
but there have been conceptual arguments against this technique, see
[Yudkowsky 2017](https://arbital.com/p/multiple_stage_fallacy/), [AronT
2023](https://www.lesswrong.com/posts/kmZkCmz6AiJntjWDG/multiple-stages-of-fallacy-justifications-and-non)
and [Gwern 2019](https://gwern.net/forking-path), which all argue that
it reliably underestimates the probability of events.

What is the empirical evidence for decomposition being a technique that
*improves* forecasts?

[Lawrence et al.
2006](https://www.sciencedirect.com/science/article/abs/pii/S0169207006000501)
summarize the state of research on the question:

> Decomposition methods are designed to improve accuracy by splitting
the judgmental task into a series of smaller and cognitively less
demanding tasks, and then combining the resulting judgements. [Armstrong
(2001)](https://www.researchgate.net/publication/267198099_The_Forecasting_Dictionary)
distinguishes between decomposition, where the breakdown of
the task is multiplicative (e.g. sales forecast=market size
forecast×market share forecast), and segmentation, where it is
additive (e.g. sales forecast=Northern region forecast+Western
region forecast+Central region forecast), but we will use the
term for both approaches here. **Surprisingly, there has been
relatively little research over the last 25 years into the value
of decomposition and the conditions under which it is likely to
improve accuracy. In only a few cases has the accuracy of forecasts
resulting from decomposition been tested against those of control
groups making forecasts holistically.** One exception is [Edmundson
(1990)](https://onlinelibrary.wiley.com/doi/abs/10.1002/for.3980090403)
who found that for a time series extrapolation task, obtaining separate
estimates of the trend, seasonal and random components and then combining
these to obtain forecasts led to greater accuracy than could be obtained
from holistic forecasts.  Similarly, [Webby, O’Connor and Edmundson
(2005)](https://www.sciencedirect.com/science/article/abs/pii/S0169207004001049)
showed that, when a time series was disturbed in some periods by several
simultaneous special events, accuracy was greater when forecasters were
required to make separate estimates for the effect of each event, rather
than estimating the combined effects holistically. [Armstrong and Collopy
(1993)](https://core.ac.uk/download/pdf/76362507.pdf) also constructed
more accurate forecasts by structuring the selection and weighting
of statistical forecasts around the judge’s knowledge of separate
factors that influence the trends in time series (causal forces).
Many other proposals for decomposition methods have been based on an
act of faith that breaking down judgmental tasks is bound to improve
accuracy or upon the fact that decomposition yields an audit trail
and hence a defensible rationale for the forecasts ([Abramson & Finizza,
1991](https://d1wqtxts1xzle7.cloudfront.net/49278189/0169-2070_2891_2990004-f20161001-25533-1nihj7p-libre.pdf?1475369537=&response-content-disposition=inline%3B+filename%3DUsing_belief_networks_to_forecast_oil_pr.pdf&Expires=1693237828&Signature=JtQssSZv0KaUbWLf3fPA70ho1ECj9zYkBC~EnNVIrFfIgcQ5dDVeK5stSWj1tR7OQrcur7PG~y8wHNuAorqrPAjqHwEq3T88klt23BzmzXwMWUNR~ZPKimTrcDTGgrj0WcC~~gM51fzvvCJrK2hO7oPsmc-mQsgvBL5VIywRLw6-GpQjBbpILXJk90c3-JTXwWeUwhwt1zv3h6U-WAyQn-Y88tZg~R7AUFJBRAdbwV8A67o7mHcCZNbKLdluGYDgG9uC516BWr4lckSd7VcoqzfywkjpxZWTjBEFLvmJoWuSRwNvqak3SzHBO5Hv86zZ4oJtWXbxwTdsVw61JGmt6Q__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA);
[Bunn & Wright,
1991](https://www.researchgate.net/profile/George-Wright-11/publication/227446292_Interaction_of_Judgemental_and_Statistical_Forecasting_Methods_Issues_Analysis/links/0c9605375ff870d3c9000000/Interaction-of-Judgemental-and-Statistical-Forecasting-Methods-Issues-Analysis.pdf);
[Flores, Olson, & Wolfe,
1992](https://www.sciencedirect.com/science/article/abs/pii/0169207092900277);
[Saaty &
Vargas, 1991](https://link.springer.com/book/9789401579544); [Salo & Bunn,
1995](https://d1wqtxts1xzle7.cloudfront.net/56667412/0040-1625_2894_2900050-720180527-12155-ptp70l-libre.pdf?1527455229=&response-content-disposition=inline%3B+filename%3DDecomposition_in_the_assessment_of_judgm.pdf&Expires=1693237988&Signature=Np4MDK~nFPb3xPknH2QaBnyOnnYT8FPgpsx7PTKkZEhmPVRQ5RTKSKzOQ7j9KDstvWfF~X7pIQdd~OJxn4OntioCsEPCPxRzLtOUscn3~UuGBnWYNsZ4JO8iBaREvH2N~DL0um~6moufhk69-lNkSjV~x2MLC5KMDBGJUwbxSwZmTp0sx3vANfZGpq~~f5ojnSkSfVJ1NYvWr82KK5UUxtU08HtGsSqOKlBB8NA7~IxsTcJnUKONHm5lczVeWq8KBEMGaNLI0GBr1y4e2bPA~Y8aKcCqnDbsOriQ0f7rNclqsY-cEEarUmd8UXRFJZc6vtPjgdF5Xv0CgrPEGIh0xA__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA);
[Wolfe & Flores,
1990](https://onlinelibrary.wiley.com/doi/abs/10.1002/for.3980090407)).
Yet, as [Goodwin and Wright
(1993)](https://d1wqtxts1xzle7.cloudfront.net/46103856/0169-2070_2893_2990001-420160531-2191-1mlbayr-libre.pdf?1464718211=&response-content-disposition=inline%3B+filename%3DImproving_judgmental_time_series_forecas.pdf&Expires=1693238053&Signature=PDCGfnyMHtluH1q9RsZffGSGZU02oBJZvEFChvofGx0nzBDrpCnlErCwx5OFUv0rXIRsULnJL~LA57rWsRXBEXcAbUtaObpC6rJTmAqe1RJLkDE59eD7787zBpqxYCkBHx5-uOou2gPpBCrxpMzc9JS3zDt4HXSs3eiXMzhzw0jPHkPyYGPwIFK5Xae1JVOkmZccnBe-9QwZhwyIcLEqoEWIoAr34d2EW19zendk~9NA182Kaf4MgKXaUCzMxSwcyMIWfoJ5K~VdfWr5Cf1LOToCb638Nn354gpcOtTX~gwCfaK0lwWcqc9Ew-3AJ7w7EBtStETgW3rSbOvuSV9WrA__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA)
point out, decomposition is not guaranteed to improve accuracy and may
actually reduce it when the decomposed judgements are psychologically more
complex or less familiar than holistic judgements, or where the increased
number of judgements required by the decomposition induces fatigue.

(Emphasis mine).

The types of decomposition described here seem quite different from
the ones used in the sources above: Decomposed time series are quite
dissimilar to multiplied probabilities for binary predictions, and in
combination with the conceptual counter-arguments the evidence appears
quite weak.

It appears as if a team of a few (let's say 4) dedicated forecasters could
run a small experiment to determine whether multiplicative decomposition
for binary forecasts a good method, by randomly spending 20 minutes either
making explicitely decomposed forecasts or control forecasts (although
the exact method for control needs to be elaborated on). Working in
parallel, making 70 forecasts should take $70 \text{ forecasts} \cdot \frac{1 \text{hr}}{3 \text{ forecasts}} \cdot \frac{1}{4}
\approx 5.8\text{hr}$ less than 6 hours, although it'd be useful to search for
more recent literature on the question.

* Would decomposition work better if one were operating with log-odds instead of probabilities?

##### Classification and Improvements

The description of such decomposition in [this
section](#Forecasting_Techniques) is, of course, lacking: A
*better* way of decomposition would be, for a specific outcome,
to find a set of preconditions for `$X$` that are [mutually
exclusive](https://en.wikipedia.org/wiki/Mutually-exclusive)
and [collectively
exhaustive](https://en.wikipedia.org/wiki/Collectively_exhaustive), find
a chain that precedes them (or another MECE decomposition), and iterate
until a whole (possibly interweaving) tree of options has been found.

Thus one can define three types of question decomposition:

1. __Multiplicative Decomposition__: Given an event `$X$`, find conditions `$Y_1, \dots Y_n$` so that `$X$` if any only if all of `$Y_1, \dots, Y_n$` happen. Estimate `$P(Y_1)$` and `$P(Y_2|Y_1)$` and `$P(Y_3|Y_1, Y_2)$` &c, and then multiply them together to estimate `$P(X)=P(Y_1)·P(Y_2|Y_1)·P(Y_3|Y_2,Y_1·) \dots P(Y_n | Y_{n-1}, \dots, Y_2, Y_1)$`.
2. __Additive Decomposition__ or __[ME](https://en.wikipedia.org/wiki/Mutually-exclusive)[CE](https://en.wikipedia.org/wiki/Collectively_Exhaustive_Events) Decomposition__: Given an event `$X$`, find a set of scenarios `$Y_1, \dots Y_n$` such that `$X$` happens if any `$Y$` happens, and only then, and no two `$Y_k, Y_l$` have `$P(Y_k \cap Y_l)>0$`. Estimate `$P(Y_1), P(Y_2), \dots P(Y_n)$` and then estimate `$P(X)=\sum_{i=1}^n P(Y_i)$`.
3. __Recursive Decomposition__: For each scenario `$X'$`, decide to pursue one of the following strategies:
	1. Estimate `$P(X')$` directly
	2. Multiplicative decomposition of `$P(X')$`
		1. Find a multiplicative decomposition `$Y_1', \dots Y_n'$` for `$X'$`
		2. Estimate `$P(Y_1'), \dots P(Y_n' | Y_1', \dots Y_{n-1}')$` each via recursive decomposition
		3. Determine `$P(X')=P(Y_1')·P(Y_2'|Y_1')·P(Y_3'|Y_2', Y_1') \dots P(Y_n' | Y_{n-1}', \dots, Y_2', Y_1')$`.
	3. Additive decomposition of `$P(X')$`
		1. Find a multiplicative decomposition `$Y_1', \dots Y_n'$` for `$X'$`
		2. Estimate `$P(Y_1'), \dots P(Y_n')$` each via recursive decomposition
		3. Determine `$P(X')=P(Y_1')+P(Y_2')+ \dots P(Y_n')$`.

A keen reader will notice that recursive decomposition is similar to
[Bayes nets](https://en.wikipedia.org/wiki/Bayesian_Network). True, though
it doesn't deal as well with conditional probabilities.

##### Using LLMs

This is a scenario where large language models are quite useful, and
we have a testable hypothesis: Does question decomposition (or MECE
decomposition) improve language model forecasts by any amount?

Frontier LLMs are [at](https://dynomight.net/predictions/)
[best](https://www.lesswrong.com/posts/c3cQgBN3v2Cxpe2kc/getting-gpt-3-to-predict-metaculus-questions)
[mediocre](https://arxiv.org/pdf/2206.15474v1) at
forecasting real-world events, but similar to how [asking
for calibration](https://arxiv.org/pdf/2305.14975v2)
improves performance, so perhaps
[chain-of-thought](https://blog.research.google/2022/05/language-models-perform-reasoning-via.html)-like
question decomposition improves (or reduces) their performance (and
therefore gives us reason to believe that similar practices will (or
won't) work with human forecasters).

Direct:

	Provide your best probabilistic estimate for the following question.
	Give ONLY the probability, no other words or explanation. For example:
	10%. Give the most likely guess, as short as possible; not a complete
	sentence, just the guess!
	The question is: ${QUESTION}. ${RESOLUTION_CRITERIA}.

Multiplicative decomposition:

	Provide your best probabilistic estimate a question.

	Your output should be structured in three parts.

	First, determine a list of factors X₁, …, X_n that are necessary
	and sufficient for the question to be answered "Yes". You can choose
	any number of factors.

	Second, for each factor X_i, estimate and output the conditional
	probability P(X_i|X₁, X₂, …, X_{i-1}), the probability that X_i
	will happen, given all the previous factors *have* happened. Then, arrive
	at the probability for Q by multiplying the conditional probabilities
	P(X_i):

	P(Q)=P(X₁)*P(X₂|X₁)…P(X_n|X₁, X₂, …, X_{n-1}).

	Third and finally, In the last line, report P(Q), WITHOUT ANY ADDITIONAL
	TEXT. Just write the probability, and nothing else.

	Example (Question: "Will my wife get bread from the bakery today?"):

	Necessary factors:
	1. My wife remembers to get bread from the bakery.
	2. The car isn't broken.
	3. The bakery is open.
	4. The bakery still has bread.

	1. P(My wife remembers to get bread from the bakery)=0.75
	2. P(The car isn't broken|My wife remembers to get bread from the bakery)=0.99
	3. P(The bakery is open|The car isn't broken, My wife remembers to get bread from the bakery)=0.7
	4. P(The bakery still has bread|The bakery is open, The car isn't broken, My wife remembers to get bread from the bakery)=0.9
	Multiplying out the probabilities: 0.75*0.99*0.7*0.9=0.467775
	46.7775%
	(End of output)
	The question is: ${QUESTION}. ${RESOLUTION_CRITERIA}

#### Discussions

* [LessWrong](https://www.lesswrong.com/posts/YjZ8sJmkGJQhNcjHj/the-evidence-for-question-decomposition-is-weak)
* [Effective Altruism Forum](https://forum.effectivealtruism.org/posts/beRtXkMpCT39y8bPj/there-is-little-evidence-on-question-decomposition)

How Can We Ask Better Forecasting Questions?
---------------------------------------------

* What are methods of scoring/defining how good a question was?
* How many questions resolve due to technicalities in the resolution criteria?
	* Are the ratios here different across different question categories?
	* How does this ratio develop as one puts more effort into specifying resolution criteria?
	* This might be studied qualitatively/semi-quantitatively.

Other Questions
----------------

* Where are the big datasets of past judgmental forecasts?
* What is the rate of positive resolution by range?
* How good a predictor is forecasting performance of intra-individual cognitive performance?
* How difficult is it to manipulate real existing prediction platforms?
	* Markets
		* PredictIt
		* BetFair
	* Hobbyist sites
		* Metaculus
		* PredictionBook
* How can we develop better forecast aggregation methods?
	* Use momentum of past forecasts
	* Use the [generalized mean](https://en.wikipedia.org/wiki/Generalized_mean) with changing `$p$` as the time to question resolution shrinks
		* Should `$p$` be increasing/decreasing/following a more complicated pattern?
		* Can we do something cool with the [quasi-arithmetic mean](https://en.wikipedia.org/wiki/Quasi-arithmetic_mean)?
