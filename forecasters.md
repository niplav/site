[home](./index.md)
-------------------

*author: niplav, created: 2022-04-04, modified: 2022-08-07, language: english, status: notes, importance: 7, confidence: highly likely*

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

We can therefore identify the four horsemen of hard forecasting:

* __Long time horizons__: Because most forecasters and traders [discount](https://en.wikipedia.org/wiki/Discounting) the future (either due to rewards further in the future being less certain, or because whatever investment is bound up in a bet could be used in the mean term, or because they actually weigh the future lower), and because long term thinking activates [far mode](https://www.overcomingbias.com/2010/06/near-far-summary.html) from [construal level theory](https://en.wikipedia.org/wiki/Construal_level_theory), the incentives to perform well on long-term questions are weaker than on short-term questions. Additionally, forecasters receive much more & better feedback on short-term questions. One would expect long-term questions to receive less accurate forecasts because of this, and the evidence points to this being the case ([Dillon 2021](https://rethinkpriorities.org/publications/data-on-forecasting-accuracy-across-different-time-horizons), [Niplav 2022](https://rethinkpriorities.org/publications/data-on-forecasting-accuracy-across-different-time-horizons)). But we're often especially interested in long-term questions: How can we incentivize or create good forecasts on those questions?
* __Reward-correlated predictions__: The clearest examples of this problem are questions on extinction events: If you forecast doom, you're never going to get rewarded for it, because the resolution happens *only* in worlds where the bad outcome didn't occur. Forecasters are [embedded agents](https://www.lesswrong.com/s/Rm6oQRJJmhGCcLvxh) in the world they are predicting on, and there is no Cartesian boundary. This can happen with prediction markets as well: when making predictions on the outcome of a decision, with the payout of the prediction market being in a currency that is affected by the decision (for example devaluing it respective to other currencies), the market might choose the "worse" decision (according to the metric used for scoring it) because it prevents the currency from being devalued as much.
* __Low probability events__: Some events are very important, but have a low probability (extreme stock market crashes, extinction events, rare diseases, encounters with aliens etc.). But low probability events are maybe even harder to forecast than long time horizon events: they often don't have good reference classes, while long time horizon questions do (that's why we have history and time series data!), and forecasters very rarely encounter them. We might just round all probabilities <1% to 0%, lest we get [Pascal's mugged](https://en.wikipedia.org/wiki/Pascal's_mugging), but in doing so we close our eyes to possible dangers (and prizes) out there, the [Talebian](https://en.wikipedia.org/wiki/Nassim_Nicholas_Taleb) approach of erring on the side of caution by "rounding them *up*" condemns us to eternal overcaution and conservatism, but as a first step we definitely want our probabilities to be as accurate as possible.
* __Out-of-distribution situations__: Whenever things with no clear existing reference class occur, such as novel technologies (social media, the internet in general, nuclear weapons, international shipping logistics, and in the future potentially genetic engineering or self-driving cars), forecasters struggle to anticipate the consequences (or foresee those shifts). This isn't limited to forecasters and prediction markets: if regular people, pundits and domain experts on average do worse than top forecasters (though as a counterpoint to forecasters>experts see [Leech & Yagudin 2022](https://forum.effectivealtruism.org/posts/qZqvBLvR5hX9sEkjR/comparing-top-forecasters-and-domain-experts)), then we wouldn't expect them to do much better specifically in very novel & unforeseen situations (reasons why this could still happen: experts might have detailed causal models that are outperformed by simple heuristics in the modal case, but as we go outside of the normal course of events, those causal & theoretical models break down much more gracefully than simple surface heuristics).
* __Hard-to-specify events__: Maybe we are slicing up forecasting the wrong way: as the old adage goes, the hard part is not coming up with the answer, it is coming up with the right question to ask. Similarly, for forecasting, we often run into the problem of specifying exactly *what* we want to know about: Too broad and you drive away forecasters and traders [who don't want to waste their time on predicting the whims of whoever resolves the market in the end](https://www.lesswrong.com/posts/a4jRN9nbD79PAhWTB/prediction-markets-when-do-they-work#I__Well_Defined), too narrow and you miss what you actually care about or invite [Goodharting](https://www.lesswrong.com/tag/goodhart-s-law). An additional layer of complexity is added when hobbyists do your forecasting, in which case narrow questions just *aren't very interesting to do predictions on*. This could be seen with the [Metaculus clean meat tournament](https://www.metaculus.com/questions/3061/animal-welfare-series-clean-meat/): many questions were just different combinatorial variations on each other, with maybe five being interesting to predict on, but not all fourteen, leading to many questions receiving less than 100 predictions during the tournament. But "interestingness" and "specifiability" appear to be tugging in opposite directions: hobbyists are probably most interested in making broad claims that flow from their worldview, instead of finding minutiae for very specific questions. Finding ways to create more specific questions on events (or avoid doing so with clever tricks while still receiving accurate forecasts) is important and difficult.

We can use these categories as guideposts: How bad are these as
problems? What approaches have been proposed/tried/implemented so far? If
we can improve one of them without harming our ability to perform well
on the others, we have made progress, if we improve several in tandem,
that's even better.

How Good Are We At forecasting?
--------------------------------

* How good are long-term forecasts?
	* How quickly does our forecasting ability decrease with increasing range of the question/forecast?
		* Does it decrease at all, or just oscillate wildly?
		* How quickly does performance degrade in different categories of questions (finance, meteorology, global economics, technological development) and by different forecasters (prediction markets, superforecasters & teams)?
* How good are our forecasts on low-probability events?
* How good are our forecasts on extinction events?
* How good are our forecasts in situations where we have historical discontinuities?
* How quickly/slowly do our forecasts converge to the final answer?
	* When don't they converge?
	* Can we classify convergence/divergence/oscillation behaviors?
* How do prediction markets, professional forecasting teams, internet enthusiasts and large language models compare?
	* `https://forum.effectivealtruism.org/posts/qZqvBLvR5hX9sEkjR/comparing-top-forecasters-and-domain-experts`
	* `https://github.com/MperorM/gpt3-metaculus`
* What is a good formalization of the idea of a forecaster being accurate at a level of n%?
	* See [Precision of Sets of Forecasts](./precision.html)
	* Are better short-term forecasters also better long-term forecasters?
	* Do forecasters become better at forecasting over time?
		* How quickly?
		* Over time/over more forecasts
	* How much does forecaster quantity affect forecast quality on continuous questions? (i.e., extend [Dillon 2021](https://rethinkpriorities.org/publications/how-does-forecast-quantity-impact-forecast-quality-on-metaculus) to continuous data)
		* How much does forecasting time affect forecast quality?
			* Generally, scaling laws for forecasting would be interesting/cool to see
* Do laypeople/pundits/domain experts perform better than forecasters/superforecasters/forecasting teams/prediction markets *specifically* under novel & unforeseen situations?

How Can We Become Better At Forecasting?
-----------------------------------------

### Scoring Rules

* What possible forecasting scoring rules could we develop?
	* Taking into account:
		* Accuracy compared to others
		* Importance of question
	* That incentivize collaboration and positive-sum interactions instead of information-hiding
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
	* Related field: information elicitation
		* See also: Chapter 27 from Algorithmic Game Theory (Nisan et al. 2007)

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

How Can We Ask Better Forecasting Questions?
---------------------------------------------

* What are methods of scoring/defining how good a question was?

Other Questions
----------------

* Where are the big datasets of past judgmental forecasts?
* How difficult is it to manipulate real existing prediction platforms?
	* Markets
		* PredictIt
		* BetFair
	* Hobbyist sites
		* Metaculus
		* PredictionBook
