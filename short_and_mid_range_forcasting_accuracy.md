[home](./index.md)
-------------------

*author: niplav, created: 2020-03-24, modified: 2020-04-03, language: english, status: notes, importance: 6, confidence: possible*

> __This text looks at the accuracy of forecasts in relation
> to the time between forecast and resolution, and asks three
> questions: First; is the accuracy higher between forecasts;
> Second; is the accuracy higher between questions; Third: is the
> accuracy higher within questions. These questions are analyzed
> using data from [PredictionBook](https://predictionbook.com/) and
> [Metaculus](https://www.metaculus.com/questions/), the answers turn
> out to be no, \_ and \_. Possible reasons are discussed.__

Short and Mid Range Forecasting Accuracy
========================================

<!--https://en.wikipedia.org/wiki/Simpson's_paradox-->
<!--https://www.openphilanthropy.org/blog/how-feasible-long-range-forecasting-->
<!--https://github.com/gimpf/metaculus-question-stats-->
<!--http://foresightr.com/2016/05/06/a-brief-history-of-forecasting-->

[Probabilistic forecasting](https://en.wikiki_Probabilistic_forecasting)
that aggregates both [qualitative and quantitative
methods](https://en.wikipedia.org/wiki/Forecasting#Qualitative_vs._quantitative_methods)
is a comparatively simple idea. Basically, one needs to have only very few tools at ones
disposal to being ready to start forecasting:

* View of belief as probabilistic (perhaps with some bayesian epistemology)
* Track records (grading results of forecasts using for example brier scores or log scores)
* Probability theory (a concept of probabilities, and maybe some simple probability distributions)

The [Brier score](https://en.wikipedia.org/wiki/Brier_score) was invented
in 1950, [Bayes' theorem](https://en.wikipedia.org/wiki/Bayes'_theorem)
was first described in 1763, and [probability
theory](https://en.wikipedia.org/wiki/Probability_theory) was properly
invented at the beginning of the 18th century.

However, attempting to use forecasting to seriously determine the
probability of future events, training & selecting people for their
forecasting ability and creating procedures that incorporate both
intuition-based and model-based predictions have only been around since
the mid 1980's<!--TODO: citation needed-->, mostly popularized by the
work of [Philip Tetlock](https://en.wikipedia.org/wiki/Ehpilp_E._Tetlock).

Since then, forecasting has slowly but surely matured from "X is going
to happen because my intuition/divine revelation told me so" to "my
probability distribution on the outcome of this random variable is
an X distribution", or alternatively "I assign a probability of X%
to this event".

However, since this kind of forecasting is relatively recent, information
about the accuracy of long-range forecasting is basically non-existent:

<!--TODO: quote the findings from the OpenPhil report here-->

In this text, I will try to look at the accuracy of short-term and
mid-term forecasting, which may shine some light on the relation between
the range of forecasts and their accuracy in general. The range of a
forecast is defined as the length of the timespan between the forecast
and the resolution of the forecast. Keeping with the report by the Open
Philanthropy Project<!--TODO: link-->, I will define short-term forecasts
as forecasts with a range of less than a year, mid-range forecasts as
forecasts with a range between 1 and 10 years, and long-term forecasts
as forecasts with a range of more than 10 years (this distinction is
not central to the following analysis, though).

Fortunately, for short- and mid-range forecasts, two easily accessible
sources of forecasts and their resolutions are available online: The
two forecasting websites [PredictionBook](https://predictionbook.com)
and [Metaculus](https://www.metaculus.com).

To find out about the range of forecasts, I download, parse & analyse
forecasting data from these sites.

<!--
Make a point here that making forecasts is one of the best existing
practical method of rationality verification & exercises:
https://www.lesswrong.com/s/pvim9PZJ6qHRTMqD3/p/5K7CMa6dEL7TN7sae
-->

<!--
Distinction between {probabilistic,non-probabilistic}
{model-based,intuition-based} forecasting
-->

<!--
Tetlock-style forecasting is "Worse is Better"
If we can't develop explicit numerical models, why
not train people in becoming good at estimating the future,
but this time with probabilistic estimates?
-->

Metaculus and PredictionBook
----------------------------

[PredictionBook](https://predictionbook.com) and
[Metaculus](https://www.metaculus.com) are both forecasting focussed
sites, though both are not prediction markets, but rather function on
the base of merit and track records: although you don't win money by
being right, you can still boast about it (although it seems questionable
whether other people will be impressed). Besides that, these sites make
it easier to train ones calibration on real-world questions and become
less wrong in the process.

However, both sites differ in their approach to writing, judging
and scoring forecasts. Predictionbook is much older than Metaculus:
the former was first released in 2008, the latter started in 2015. It
is also much less formal than Metaculus: it doesn't require stringent
resolution criteria, making possible for everybody to judge a question
(unrelated to whether the person has even made a prediction on the
question themselves!), while Metaculus requires a short text explaining
the context and resolution criteria for a question, with the questions
being resolved by moderators or admins. This leads to Metaculus having
less questions than Predictionbook, each question having more predictions
on it. Of the two, Metaculus is much more feature-rich: It supports
not only binary questions, but also range questions with probability
distributions, comment threads, having closed questions (questions
that haven't yet been resolved, but that can still be predicted on),
three different kinds of scores (the Brier score<!--TODO: link-->, and
a log score for discrete and continuous forecasts each), as well as the
Metaculus prediction, a weighted aggregation of the forecasts of the
best forecasters on the site.

Another significant difference between these two websites is the amount of
data they publish: Predictionbook shows every single forecast made, while
on Metaculus one can only see the community forecast (a the time-weighted
median of the forecasts made on the question). This is relevant for this
analysis: The two approaches must be analysed separately.

Accuracy Between Forecasts
--------------------------

The first approach I took was to simply take the probability, result and
range for all forecasts made, sort these forecasts into buckets by range
(e.g. one bucket for all forecasts made 1 day before their resolution
(and their results), one bucket for all forecasts made 2 days before
their resolution, and so on). I then calculated the Brier score for each
of these buckets, and then checked what the relation between brier score
and range (the time between forecast & resolution) was (correlation &
linear regression).

### Getting the Data

#### For Metaculus

The Metaculus data is relatively easy to obtain:
The forecasts are available on a JSON API at
`https://www.metaculus.com/api2/questions/?page=`. Fortunately,
gimpf has already published [a collection of
scripts](https://github.com/gimpf/metaculus-question-stats) for fetching &
analysing Metaculus data, I reused their script `fetch` to download the
raw JSON. I then converted the distinct page objects in the generated
file to a list of questions:

	$ cd /usr/local/src
	$ git clone https://github.com/gimpf/metaculus-question-stats
	$ cd metaculus-question-stats
	$ ./fetch
	$ z site
	$ jq -s '[.]|flatten' </usr/local/src/metaculus/data-questions-raw.json >data/metaculus.json

The resulting data is available [here](./data/metaculus.json).

I then wrote a python script to convert the JSON data to CSV in the form
`forecasting_probability,result,range`, while also filtering out yet
unresolved questions and range questions.

The script is not terribly interesting: It just reads in the JSON data,
parses and traverses it, printing the CSV in the process.

Code:

	#!/usr/bin/env python3

	import json
	import time

	from time import mktime

	f=open("../../data/metaculus.json")
	jsondata=json.load(f)

	for page in jsondata:
	        for question in page["results"]:
	                if question["possibilities"]["type"]=="binary" and (question["resolution"]==1 or question["resolution"]==0):
	                        try:
	                                restime=time.strptime(question["resolve_time"],"%Y-%m-%dT%H:%M:%S.%fZ")
	                        except:
	                                restime=time.strptime(question["resolve_time"],"%Y-%m-%dT%H:%M:%SZ")
	                        for pred in question["prediction_timeseries"]:
	                                timediff=mktime(restime)-pred["t"]
	                                print("{},{},{}".format(question["resolution"],pred["community_prediction"],timediff))

The resulting CSV file with over 40K predictions is available
[here](./data/met.csv).

#### For PredictionBook

Accuracy Between Questions
--------------------------

Accuracy Within Questions
-------------------------
