[home](./index.md)
-------------------

*author: niplav, created: 2022-04-04, modified: 2022-04-08, language: english, status: notes, importance: 7, confidence: highly likely*

> __Beginnings of a research agenda about judgmental forecasting.__

Forecasters: What Do They Know? Do They Know Things?? Let's Find Out!
======================================================================

Judgmental forecasting is a fairly recent and (imho) fairly
under-researched & under-appreciated human endeavour.

The Four Horsemen of Hard Forecasting
---------------------------------------

In general, judgmental forecasting methods operate best in areas with
fast feedback loops, large existing datasets (or at least good reference
classes for base rates) and continuous historical trends.

How good are we at forecasting?
--------------------------------

* How good are long-term forecasts?
* How good are our forecasts on low-probability events?
* How good are our forecasts on extinction events?
* How good are our forecasts in situations where we have historical discontinuities?
* How quickly/slowly do our forecasts converge to the final answer?
	* When don't they converge?
	* Can we classify convergence/divergence/oscillation behaviors?
* How do prediction markets, professional forecasting teams, internet enthusiasts and large language models compare?
	* `https://forum.effectivealtruism.org/posts/qZqvBLvR5hX9sEkjR/comparing-top-forecasters-and-domain-experts`
* What is a good formalization of the idea of a forecaster being accurate at a level of n%?
	* See [finesse](./finesse.html)
	* Are better short-term forecasters also better long-term forecasters?
	* Do forecasters become better at forecasting over time?
		* How quickly?
		* Over time/over more forecasts
	* How much does forecaster quantity affect forecast quality on continuous questions? (i.e., extend [Dillon 2021](https://rethinkpriorities.org/publications/how-does-forecast-quantity-impact-forecast-quality-on-metaculus) to continuous data)
		* How much does forecasting time affect forecast quality?
			* Generally, scaling laws for forecasting would be interesting/cool to see

How can we become better at forecasting?
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
