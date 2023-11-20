[home](./index.md)
------------------

*author: niplav, created: 2022-07-15, modified: 2023-04-14, language: english, status: notes, importance: 6, confidence: certain*

> __Iqisa is [a library](https://github.com/niplav/iqisa) for handling and comparing forecasting datasets from different platforms.__

Iqisa: A Library For Handling Forecasting Datasets
===================================================

> The eventual success of my archives reinforced my view that
public permission-less datasets are often a bottleneck to
research: you cannot guarantee that people will use your dataset,
but you can guarantee that they won’t use it.

*—[Gwern Branwen](https://gwern.net/), [“2019 News”](https://gwern.net/newsletter/2019/13), 2019*

Iqisa is a collection of forecasting datasets and a simple
library for handling those datasets. Code and data available
[here](https://github.com/niplav/iqisa). Documentation is
[here](./iqisadoc.html).

So far it contains data from:

* The [Good Judgment Project](https://en.wikipedia.org/wiki/The_Good_Judgment_Project): ~790k market trades+~3.14m survey predictions≈3.9m forecasts
* The [Metaculus public API](https://www.metaculus.com/api2/schema/redoc/): ~210k forecasts
* [PredictionBook](https://predictionbook.com/): ~64k forecasts

for a total of ~4.2m forecasts, as well as code for handling private
[Metaculus](https://metaculus.com) data (available to researchers on
request to Metaculus), but I plan to also add data from various other
sources.

The documentation can be found [here](./iqisadoc.html), but a simple
example for using the library is seeing whether traders with more than
100 trades have a better Brier score than traders in general:

	import gjp
	import iqisa as iqs
	market_fcasts=gjp.load_markets()

	def brier_score(probabilities, outcomes):
		return np.mean((probabilities-outcomes)**2)

	def brier_score_user(user_forecasts):
		user_right=(user_forecasts['outcome']==user_forecasts['answer_option'])
		probabilities=user_forecasts['probability']
		return np.mean((probabilities-user_right)**2)

	trader_scores=iqs.score(market_fcasts, brier_score, on=['user_id'])
	filtered_trader_scores=iqs.score(market_fcasts.groupby(['user_id']).filter(lambda x: len(x)>100), brier_score, on=['user_id'])

And we can see:

	>>> np.mean(trader_scores)
	score    0.159194
	dtype: float64
	>>> np.mean(filtered_trader_scores)
	score    0.159018
	dtype: float64

Concluding that more experienced traders are only very slightly better
at trading.

Advantages
-----------

Iqisa offers some advantages over existing datasets:

* Ease of use: data can be loaded using two lines of code
* Unified data format: the data from different platforms and projects has been brought into the same format that enables easier comparisons and cross-platform analyses
* Pre-defined functionalities for analysis: Some functionalities (such as for scoring or aggregation) have been implemented for easier use

Requirements
-------------

* [NumPy](https://numpy.org/)
* [Pandas](https://pandas.pydata.org)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

Uses
------

* [Range and Forecasting Accuracy (niplav, 2023)](./range_and_forecasting_accuracy.html#Analysis__Results)
* [Precision of Sets of Forecasts (niplav, 2023)](./precision.html)

Possible Projects
------------------

* Take questions from different platforms that are close to each other on [sentence2vec](https://github.com/stanleyfok/sentence2vec), and check which platform made the better predictions on that question.

Known Bugs
-----------

Since this is a project I'm now doing in my free time, it might not be
as polished as it should be. Sorry :-/

If you decide to work with this library, feel free to [contact me](./about.md#Contact).

* Issues with the time fields
	* The native pandas datetime format is too restricted for some time ranges in these datasets, those values might be set to `NaT`.
	* Not all time-related fields have timezone information attached to them.
* Some predictions in the dataset have occurred after question resolution. There should be a way to filter those out programmatically.
* The columns of the datasets are not sorted the same way for question DataFrames and forecast DataFrames.
* I fear that despite my best efforts, not all data frome the GJP data has been transferred.
* The default fields in the Metaculus & PredictionBook data should be `NA` more often than they are right now.
* The documentation is still *slightly* spotty, and tests are mostly nonexistent.
* Some variables shouldn't be exposed, but are.
* The code hasn't been updated for the new [Metaculus API](https://www.metaculus.com/api2/schema/redoc/)

Feature Wishlist
-----------------

* Create a pip package
* Add data from more platforms

### Potential Additional Sources for Forecasting Data

* [Metaforecast API](https://metaforecast.org/api/graphql?query=%23%0A%23+Welcome+to+Yoga+GraphiQL%0A%23%0A%23+Yoga+GraphiQL+is+an+in-browser+tool+for+writing%2C+validating%2C+and%0A%23+testing+GraphQL+queries.%0A%23%0A%23+Type+queries+into+this+side+of+the+screen%2C+and+you+will+see+intelligent%0A%23+typeaheads+aware+of+the+current+GraphQL+type+schema+and+live+syntax+and%0A%23+validation+errors+highlighted+within+the+text.%0A%23%0A%23+GraphQL+queries+typically+start+with+a+%22%7B%22+character.+Lines+that+start%0A%23+with+a+%23+are+ignored.%0A%23%0A%23+An+example+GraphQL+query+might+look+like%3A%0A%23%0A%23+++++%7B%0A%23+++++++field%28arg%3A+%22value%22%29+%7B%0A%23+++++++++subField%0A%23+++++++%7D%0A%23+++++%7D%0A%23%0A%23+Keyboard+shortcuts%3A%0A%23%0A%23++Prettify+Query%3A++Shift-Ctrl-P+%28or+press+the+prettify+button+above%29%0A%23%0A%23+++++Merge+Query%3A++Shift-Ctrl-M+%28or+press+the+merge+button+above%29%0A%23%0A%23+++++++Run+Query%3A++Ctrl-Enter+%28or+press+the+play+button+above%29%0A%23%0A%23+++Auto+Complete%3A++Ctrl-Space+%28or+just+start+typing%29%0A%23%0A)
* [Autocast Dataset](https://github.com/andyzoujm/autocast)
* [Foretell (CSET)](https://www.cset-foretell.com/)
* [Good Judgment Open](https://www.gjopen.com/)
* [Hypermind](https://www.hypermind.com)
* [Augur](https://augur.net/)
* [Foretold](https://www.foretold.io/)
* [Omen](https://www.fsu.gr/en/fss/omen)
* [GiveWell](https://www.givewell.org/)
* [Open Philanthropy Project](https://www.openphilanthropy.org/)
* [PredictIt](https://www.predictit.org/)
* [Elicit](https://elicit.org/)
* [PolyMarket](https://polymarket.com/)
* [Iowa Electronic Markets](https://en.wikipedia.org/wiki/Iowa_Electronic_Markets)
* [INFER](https://www.infer-pub.com/)
* [Manifold](https://manifold.markets/home)
* [Smarkets](https://smarkets.com/)
* [The Odds API](https://the-odds-api.com/)
* Kalshi

Acknowledgements
-----------------

Credits go to [Arb Research](https://arbresearch.com/) for funding the
first 85% of this work, and Misha Yagudin in particular for guidance
and mentorship.

Thanks also to [hrosspet](https://github.com/hrosspet) for making the
library more usable.
