[home](./index.md)
-------------------

*author: niplav, created: 2020-03-24, modified: 2020-04-09, language: english, status: notes, importance: 6, confidence: possible*

> __This text looks at the accuracy of forecasts in relation
> to the time between forecast and resolution, and asks three
> questions: First; is the accuracy higher between forecasts;
> Second; is the accuracy higher between questions; Third: is the
> accuracy higher within questions. These questions are analyzed
> using data from [PredictionBook](https://predictionbook.com/) and
> [Metaculus](https://www.metaculus.com/questions/), the answers turn
> out to be no, \_ and \_. Possible reasons are discussed.__

Range and Forecasting Accuracy
===============================

> Above all, don’t ask what to believe—ask what to anticipate. Every
question of belief should flow from a question of anticipation, and that
question of anticipation should be the center of the inquiry. Every guess
of belief should begin by flowing to a specific guess of anticipation,
and should continue to pay rent in future anticipations. If a belief
turns deadbeat, evict it.

*– [Eliezer Yudkowsky](https://en.wikipedia.org/wiki/Eliezer_Yudkowsky), [“Making Beliefs Pay Rent (in Anticipated Experiences)“](https://www.lesswrong.com/posts/a7n8GdKiAZRX86T5A/making-beliefs-pay-rent-in-anticipated-experiences), 2007*
<!--Also look at this guy:
https://en.wikipedia.org/wiki/J._Scott_Armstrong#Forecasting
-->
<!--https://en.wikipedia.org/wiki/Simpson's_paradox-->
<!--https://www.openphilanthropy.org/blog/how-feasible-long-range-forecasting-->
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
[gimpf](https://github.com/gimpf/) has already published [a collection of
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

I then wrote a python script to convert the JSON data to CSV in the
form `id,result,probability,range` (`id` is a unique ID per question,
which will come in handy later), while also filtering out yet unresolved
questions and range questions.

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
					print("{},{},{},{}".format(question["id"], question["resolution"], pred["community_prediction"], timediff))

The resulting CSV file with over 40K predictions is available
[here](./data/met.csv).

#### For PredictionBook

As far as I know, PredictionBook doesn't publish the forecasting
data over an API. However, all individual predictions are visible
on the web, which means I had to parse the HTML itself using
[BeautifulSoup](https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)).

This time the code is more complex, but just slightly so: It starts at
the [first page](https://predictionbook.com/predictions/page/1)
of predictions, and loops down to the [last
one](https://predictionbook.com/predictions/page/326), every time iterating
through the questions on that page.

It then loops through the predictions on each question and parses out
the date for the prediction and the credence.

Every question on PredictionBook has two dates related to its
resolution: the 'known on' date, for which the resolution was originally
planned, and by which the result should be known, and the 'judged on'
date, on which the resolution was actually made. I take the second date
to avoid predictions with negative differences between prediction and
resolution time.

Also, the 'known on' date has the CSS class `date created_at`, which
doesn't seem right.

The output of this script is in the same format as the one for Metaculus
data: `id,result,probability,range`.

Code:

	#!/usr/bin/env python2

	import urllib2
	import sys
	import time

	from bs4 import BeautifulSoup
	from time import mktime

	def showforecasts(linkp, res):
		urlp="https://predictionbook.com{}".format(linkp)
		reqp=urllib2.Request(urlp, headers={"User-Agent" : "Firefox"})
		try:
			conp=urllib2.urlopen(reqp)
		except (urllib2.HTTPError, urllib2.URLError) as e:
			return
		datap=conp.read()
		soupp=BeautifulSoup(datap, "html.parser")

		timedata=soupp.find(lambda tag:tag.name=="p" and "Created by" in tag.text)

		resolved=timedata.find("span", class_="judgement").find("span", class_="date created_at").get("title")
		restime=time.strptime(resolved,"%Y-%m-%d %H:%M:%S UTC")

		responses=soupp.find_all("li", class_="response")
		for r in responses:
			forecasts=r.find_all("span", class_="confidence")
			if forecasts!=[]:
				est=float(r.find_all("span", class_="confidence")[0].text.strip("%"))/100
			else:
				continue
			estimated=r.find("span", class_="date").get("title")
			esttime=time.strptime(estimated,"%Y-%m-%d %H:%M:%S UTC")
			print("{},{},{},{}".format(linkp.replace("/predictions/", ""), res, est, mktime(restime)-mktime(esttime)))

	for page in range(1,400):
		url="https://predictionbook.com/predictions/page/{}".format(page)
		req=urllib2.Request(url, headers={"User-Agent" : "Firefox"})
		try:
			con=urllib2.urlopen(req)
		except (urllib2.HTTPError, urllib2.URLError) as e:
			continue
		data=con.read()
		soup=BeautifulSoup(data, "html.parser")
		predright=soup.find_all("li", {"class": "prediction right"})
		predwrong=soup.find_all("li", {"class": "prediction wrong"})
		for pred in predright:
			linkp=pred.span.a.get("href")
			showforecasts(linkp, "1.0")
		for pred in predwrong:
			linkp=pred.span.a.get("href")
			showforecasts(linkp, "0.0")

Surprisingly, both platforms had almost the same amount of individual
predictions on binary resolved questions: ~43K for Metaculus, and ~42K
for PredictionBook.

The resulting data from PredictionBook is available [here](./data/pb.csv).

### Analysis

Now that the two datasets are available, they can be properly analyzed.

First, the raw data is loaded from the two CSV files and then the ID is
converted to integer, and the rest of the fields are converted to floats
(the range is a float for some Metaculus questions, and while the result
can only take on 0 or 1, using float there makes it easier to calculate
the brier score using `mse.set`):

	.fc(.ic("../../data/pb.csv"));pbraw::csv.load()
	.fc(.ic("../../data/met.csv"));metraw::csv.load()

	pbdata::+flr({0<*|x};{(1:$*x),1.0:$'1_x}'pbraw)
	metdata::+flr({0<*|x};{(1:$*x),1.0:$'1_x}'metraw)

To compare the accuracy between forecasts, one can't deal with individual
forecasts, only with sets of forecasts and outcomes. Here, I organise
the predictions into buckets according to range. The size of the buckets
seems important: bigger buckets contain bigger datasets, but are also
less granular. Also, should the size of buckets increase with increasing
range (e.g. exponentially: the first bucket is for all predictions made
one day or less before resolution, the second bucket for all predictions
made 2-4 days before resolution, the third bucket for all predictions
4-8 days before resolution, and so on) or stay the same?

I decided to use evenly sized buckets, and test with varying sizes of
one day, one week, one month (30 days) and one year (365 days).

	spd::24*60*60
	spw::7*spd
	spm::30*spd
	spy::365*spd
	dpbdiffs::{_x%spd}pbdata@3
	wpbdiffs::{_x%spw}'pbdata@3
	mpbdiffs::{_x%spm}'pbdata@3
	ypbdiffs::{_x%spy}'pbdata@3
	dmetdiffs::{_x%spd}'metdata@3
	wmetdiffs::{_x%spw}'metdata@3
	mmetdiffs::{_x%spm}'metdata@3
	ymetdiffs::{_x%spy}'metdata@3

The [Brier Score](https://en.wikipedia.org/wiki/Brier_score) is
a scoring rule for binary forecasts. It takes into account both
calibration and resolution by basically being the [mean squared
error](https://en.wikipedia.org/wiki/Mean_squared_error) of forecast
(`$f_{t}$`) and outcome (`$o_{t}$`):

<div>
	$$BS=\frac{1}{N}\sum_{t=1}^{N}(f_{t}-o_{t})^{2}$$
</div>

In Klong, it's easy to implement (and also available through
the function `mse.set`):

	brier::{mu((x-y)^2)}

Now, one can calculate the brier score for the forecasts and outcomes
in each bucket (here I only show it for the days buckets, but it's
similar for weeks, months and years):

	pbress::pbdata@1
	pbfcs::pbdata@2

	dpbdg::=dpbdiffs
	dpbdiffbrier::{(dpbdiffs@*x),brier(pbfcs@x;pbress@x)}'dpbdg
	dpbdiffbrier::dpbdiffbrier@<*'dpbdiffbrier

	metress::metdata@1
	metfcs::metdata@2

	dmetdg::=dmetdiffs
	dmetdiffbrier::{(dmetdiffs@*x),brier(metfcs@x;metress@x)}'dmetdg
	dmetdiffbrier::dmetdiffbrier@<*'dmetdiffbrier

Every `diffbrier` list contains lists with two elements, the first
one being the time between forecast and resolution, and the second one
being the brier score for all forecasts made in that time. For example,
`ypbdiffbrier` is

	[[0 0.162]
	[1 0.168]
	[2 0.164]
	[3 0.159]
	[4 0.13]
	[5 0.12]
	[6 0.128]
	[7 0.147]
	[8 0.121]
	[9 0.215]
	[10 0.297]]

(Brier scores truncated using `{(*x),(_1000**|x)%1000}'ypbdiffbrier`).

First, one can check how high the range of these two datasets really is.
The PredictionBook forecasts with the highest range span 3730 days
(more than 10 years), for Metaculus it's 1387 days (nearly 4 years).

One can now look at the correlation between range and Brier score first
for Metaculus, and then for PredictionBook:

		cor@+dmetdiffbrier
	-0.209003553312708299
		cor@+wmetdiffbrier
	-0.255272030357598017
		cor@+mmetdiffbrier
	-0.304951730306590024
		cor@+ymetdiffbrier
	-0.545313822494739663
		cor@+dpbdiffbrier
	-0.0278634569332282397
		cor@+wpbdiffbrier
	0.0121150252846883416
		cor@+mpbdiffbrier
	0.0752110636215072744
		cor@+ypbdiffbrier
	0.411830122003081247

For Metaculus, the results are pretty astonishing: the correlation is
negative for all four options, meaning that the higher the range of
the question, the lower the Brier score (and therefore, the higher the
accuracy)! And the correlation is extremly low either: -0.2 is quite
formidable.

PredictionBook, on the other hand, is not as surprising: the correlations
are mostly weak and indicate that accuracy doesn't change with range
– a [null result](https://en.wikipedia.org/wiki/Null_result).

Visualizing the forecasts with
[scatterplots](https://en.wikipedia.org/wiki/Scatter_plot) and [linear
regressions](https://en.wikipedia.org/wiki/Linear_regression) shows a
very similar picture (red dots are for Metaculus forecasts, blue dots
are for PredictionBook forecasts):

![Scatterplot with linear regression for Metaculus & PredictionBook forecasts by range (in days)](img/range_and_forecasting_accuracy/alldays.png "Scatterplot with linear regression for Metaculus & PredictionBook forecasts by range (in days)")

*Scatterplot with linear regression for Metaculus & PredictionBook forecasts by range (in days)*

![Scatterplot with linear regression for Metaculus & PredictionBook forecasts by range (in weeks)](img/range_and_forecasting_accuracy/allweeks.png "Scatterplot with linear regression for Metaculus & PredictionBook forecasts by range (in weeks)")

*Scatterplot with linear regression for Metaculus & PredictionBook forecasts by range (in weeks)*

![Scatterplot with linear regression for Metaculus & PredictionBook forecasts by range (in months)](img/range_and_forecasting_accuracy/allmonths.png "Scatterplot with linear regression for Metaculus & PredictionBook forecasts by range (in months)")

*Scatterplot with linear regression for Metaculus & PredictionBook forecasts by range (in months)*

![Scatterplot with linear regression for Metaculus & PredictionBook forecasts by range (in years)](img/range_and_forecasting_accuracy/allyears.png "Scatterplot with linear regression for Metaculus & PredictionBook forecasts by range (in years)")

*Scatterplot with linear regression for Metaculus & PredictionBook forecasts by range (in years)*

The high amounts of noise are probably due to the low number of
predictions for single days (or, in the case of weeks and months, for
years/months with a high range, as not enough questions with this range
have resolved yet).

### Why Assume Accuracy will Increase?

### Simpson's Paradox

Accuracy Between Questions
--------------------------

Another way to determine at the relation between forecasting accuracy
and range is to look at the range of questions and not of individual
forecasts.

Accuracy Within Questions
-------------------------
