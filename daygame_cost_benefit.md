[home](./index.md)
-------------------

*author: niplav, created: 2019-12-25, modified: 2024-07-05, language: english, status: in progress, importance: 3, confidence: possible*

> __Is daygame worth it, and if yes,
how much? I first present a simple [point
estimate](https://en.wikipedia.org/wiki/Point_estimation) [cost-benefit
value estimation](https://en.wikipedia.org/wiki/Cost-benefit_analysis)
written in Klong and find that daygame is probably worth ~\\$996 maximum,
at ~499 approaches, though the number varies strongly under different
assumptions. After that, I modify the model to capture more of the nuance,
and arrive at ~\\$2098 of value for ~1000 approaches. I then perform a
[Monte-Carlo simulation](https://en.wikipedia.org/wiki/Monte_Carlo_method)
to determine the uncertainty around the [expected
value](https://en.wikipedia.org/wiki/Expected_value) and find that in
the simple case the value of daygame ranges from -\\$3297 to \\$3200
(5th/95th percentile), with a median of \\$899 and a mean of \\$550,
and in the complex case \_.__

<!--
TODO:

distinguish opportunity cost and incidental benefits from sunlight,
light exercise and improvement of social skills
-->

Daygame Cost-Benefit Analysis
=============================

> These things should be left to the frigid and impersonal
> investigator, for they offer two equally tragic alternatives to
> the man of feeling and action: despair if he fail in his quest,
> and terrors unutterable and unimaginable if he succeed.

*— [Howard Phillips Lovecraft](https://en.wikipedia.org/wiki/H._P._Lovecraft), [“From Beyond”](http://www.hplovecraft.com/writings/texts/fiction/fb.aspx), 1934*

> Daygame is the art of meeting and attracting women during the daytime
> in different locations and at different times of the day.

*— [Sebastian Harris](https://www.globalseducer.com/), [“Daygame: A Quick Beginner’s Guide“](https://www.globalseducer.com/daygame/), 2018*

Many daygamers follow the [London Daygame
Model](https://tddaygame.com/london-daygame-model/) which is fairly
linear and based on approaches that last 5-10 minutes each.

Is this method of daygame worth it, and if yes, how much should one
be doing?

In this text, I first review existing texts on the topic and find them
lacking in several ways. I then present a simple and general model for
the value of doing a number of daygame approaches, and find that it
recommends doing 484 approaches with a value of \\$969 in the optimum. I
then extend the model to more subjective and hard to measure factors
such as positive side effects, effects of daygame on mood and similar
other factors, and estimate that the optimal number of approaches is 1024
(power of two not indended, but appreciated), at a value of \\$2110.

The models presented don't consider externalities, be they positive or
negative. That is the subject of a different debate.

Similar Analyses
----------------

One already existing cost analysis of game is [Free Northerner
2012](https://freenortherner.wordpress.com/2012/06/12/economic-analysis-of-casual-sex-prostitution-vs-game/ "Economic Analysis of Casual Sex – Prostitution vs Game"),
he focuses on nightgame in bars and clubs and concludes that

> Cost for Sex [from prostitution]: \\$300  
> Cost for sex [from game]: \\$460 (\\$200 is you enjoy clubbing, gaming,
> and dating for their own sake)  
> […]  
> For casual sex, a mid-range prostitute is cheaper than game.
> On the other hand, most of game’s costs are in the form of time
> opportunity costs, so if you have a lot of free time and little money
> or you enjoy the activities of clubbing, game, or dating even without
> the promise of sex, then game might be a better deal.
> In addition, the higher your average wage, the more expensive game
> becomes relative to prostitution, as the opportunity costs of game
> increase the more potential earning you sacrifice.
> Conclusion: For obtaining casual sex, game is the better option if you
> are paid low wages and have free time or if you enjoy game and related
> activities. Prostitution is the better option if you are middle-class,
> don’t have the free time, or dislike engaging in game.

*— [Free Northerner](https://freenortherner.com/), [“Economic Analysis of Casual Sex – Prostitution vs Game”](http://freenortherner.com/2012/06/12/economic-analysis-of-casual-sex-prostitution-vs-game/), 2012*

(Inconsistent capitalization is in the original text)

However, his analysis doesn't take daygame into account (he mentions
it at the end). Daygame seems to me to be a much better option (not
just for people who don't like nightclubs): it's healthy due to moving
around a lot outside, getting drunk is mostly not an option, it doesn't
mess up the sleep schedule, one doesn't have to pay to get into clubs,
and it can be combined with sightseeing in foreign cities.

He also doesn't consider positive side-effects from game (such as
increased confidence), negative side-effects from prostitution (such as
addiction<!--TODO: link-->), and diminishing
returns in his analysis.

<!--TODO: he has written a text about marriage & relationships, analyze that too?
https://freenortherner.com/2012/11/01/financial-analysis-of-sex-relationship-vs-marriage/
-->
<!--TODO: link & consider Thomas Crown's “Is Daygame Efficient?” https://thomascrownpua.com/2021/05/10/is-daygame-efficient/-->

Ratios
------

<!--
TODO: Read & comment on https://interpersona.psychopen.eu/index.php/interpersona/article/download/3397/3397.html
Comment: https://www.lesswrong.com/posts/gosGW6oBf3fzDHPbd/dating-roundup-5-opening-day?commentId=PCx4KxqSmyXgmFSis
-->

In daygame-lingo, the word "ratio" usually refers to the ratio between
approaches and contact information (such as phone numbers)/dates/women
slept with (colloquially "lays"). In this text, I'm interested in the
approach-to-date ratio (here the ratio of first dates to approaches)
and the approach-to-lay ratio.

> 30 approaches will get me between 10 - 15 phone numbers.  
> Half of these phone numbers will flake leaving me messaging around 5 -
> 8 girls.  
> I will get half of these girls out on dates (between 2 - 4) and sleep
> with 1 or 2.  
> These are realistic stats, this is cold approach, cold approach
> is tough.

*— [James Tusk](https://project-tusk.com), [“Realistic Daygame Statistics (Daygame Tips)”](https://project-tusk.com/blogs/the-tusk-diaries/realistic-daygame-statistics), 2017*

James Tusk is a very good looking daygame coach, so these numbers are
quite high.

[daygamersbible
2018](https://daygamersbible.wordpress.com/2018/05/23/daygame-statistics-and-what-they-tell-your-daygame/ "Daygame Statistics and What They Tell About Your Daygame")
proclaims
16.9% numbers/approaches, 22.4% dates/numbers and 37.1% lays/dates
(that would be `$0.169 \cdot 0.224=0.0378$` dates per approach, and
`$0.169 \cdot 0.224*0.371=0.0140$` lays per approach).

Tom Torero presents his experiences with daygame ratios in
[this video](https://www.youtube.com/watch?v=7WzKWHvDOOQ)
[(a)](./vid/daygame_cost_benefit/realistic_daygame_expectations.webm).
He claims that a beginner will on average get a lay out of a hundred
approaches, an intermediate one out of fifty, and an advanced daygamer
one lay out of thirty. He doesn't specify how much practice makes
a beginner/intermediate/advanced daygamer.

The numbers for the approach-to-lay ratios were 1 in 100 for beginners,
1 in 50 for intermediate daygamers and 1 in 30 for experts.
### Empirical Data for Ratios

Fortunately, some daygamers are often very diligent in keeping track
records of their ratios and even publish them.

Here, I collect cumulative date and lay ratios from several blogs. I
don't count idates as dates, because I'm not sure whether daygamers
usually pay for them or not.

Note that these numbers are just stats some guys wrote on the internet,
usual qualifiers about the accuracy of these values apply.

#### Roy Walker

I am also not sure whether at some points "dates" was all dates combined,
and later was split into "first date", "second date" etc. For simplicity I
assume that in the beginning, "dates" simply referred to "first date". It
still seems to be coherent.

[Roy Walker](https://roywalkerdaygame.wordpress.com/):

* [Before 2016](https://roywalkerdaygame.wordpress.com/2016/08/07/the-journey-two-years-in/)
* [2016](https://roywalkerdaygame.wordpress.com/2017/01/02/2016-the-year-of-1000-sets/)
	* [March](https://roywalkerdaygame.wordpress.com/2016/04/02/march-review/)
	* [April](https://roywalkerdaygame.wordpress.com/2016/05/02/april-review/)
	* [May](https://roywalkerdaygame.wordpress.com/2016/06/02/may-review/)
	* [June](https://roywalkerdaygame.wordpress.com/2016/07/03/june-review/)
	* [September](https://roywalkerdaygame.wordpress.com/2016/10/01/herpescelling/)
	* [November](https://roywalkerdaygame.wordpress.com/2016/12/02/nonotchvember/)
* [2017](https://roywalkerdaygame.wordpress.com/2018/01/06/2017-the-year-of-ups-and-downs/)
	* [January](https://roywalkerdaygame.wordpress.com/2017/02/04/keep-er-lit/)
	* [February](https://roywalkerdaygame.wordpress.com/2017/02/27/enjoy-the-process/)
	* [March](https://roywalkerdaygame.wordpress.com/2017/04/09/is-daygame-getting-harder-in-london/)
	* [April](https://roywalkerdaygame.wordpress.com/2017/05/15/update-a-month-on-the-road/) (?)
	* [July-September](https://roywalkerdaygame.wordpress.com/2017/10/09/game-over/)
* [2018](https://roywalkerdaygame.wordpress.com/2019/01/09/2018-a-year-of-change/)
* [4000 sets](http://nitter.poast.org/RoyWalkerPUA/status/1183757732551282690)
* [2019](https://roywalkerdaygame.wordpress.com/2020/01/07/2019-the-year-of-meh/)
	* [January](https://roywalkerdaygame.wordpress.com/2019/02/19/ketchup-in-glass-bottles/)

Lay ratios:

	rwlay::[[511 5][901 10][977 10][1060 11][1143 13][1216 14][1380 16][1448 18][1557 19][1990 27][2063 27][2130 27][2230 27][2373 31][2540 35][2876 44][3442 62][3567 63][3991 83][4092 84]]
	rwlayrat::{(*x),%/|x}'rwlay

Date ratios:

	rwdate::[[511 19][901 38][977 38][1060 40][1143 46][1216 48][1380 58][1448 63][1557 64][1990 81][2063 81][2130 84][2230 85][2373 91][2540 97][2876 126][3442 165][3567 170][3991 200][4092 202]]
	rwdaterat::{(*x),%/|x}'rwdate

#### Seven

[Seven](https://sevendaygame.wordpress.com/) (he says that "I started
my daygame journey back in 2014", so there is information missing):

* [2016](https://sevendaygame.wordpress.com/2017/01/21/dec-2016-report-2016-review-and-kicking-off-2017/) (July to December)
	* [July](https://sevendaygame.wordpress.com/2016/10/03/a-year-of-daygame-in-tallinn-estonia-aug-2015-to-aug-216/) (?)
	* [August](https://sevendaygame.wordpress.com/2016/09/08/august-2016-daygame-stats/)
	* [September](https://sevendaygame.wordpress.com/2016/10/12/september-2016-daygame-report/)
	* [October](https://sevendaygame.wordpress.com/2016/11/06/october-2016-daygame-report/)
	* [November](https://sevendaygame.wordpress.com/2016/12/12/november-2016-daygame-report/)
* [2017](https://sevendaygame.wordpress.com/2018/01/15/2017-review-a-year-in-st-petersburg/)
	* [January](https://sevendaygame.wordpress.com/2017/02/15/january-2017-review-end-of-eurojaunt-and-new-life-in-st-petersburg/)
	* [February](https://sevendaygame.wordpress.com/2017/03/13/february-2017-review-need-to-go-back-to-basic-stacking/)
	* [March](https://sevendaygame.wordpress.com/2017/04/02/march-2017-review-no-lay-month/)
	* [April](https://sevendaygame.wordpress.com/2017/05/10/april-2017-review-pretty-standard-month/)
	* [May](https://sevendaygame.wordpress.com/2017/06/13/may-2017-review-feeling-like-a-number-collector/)
	* [June](https://sevendaygame.wordpress.com/2017/07/17/june-2017-review-another-no-lay-month/)
	* [July](https://sevendaygame.wordpress.com/2017/08/07/july-2017-review-best-month-this-year-so-far/)
	* [August](https://sevendaygame.wordpress.com/2017/09/04/august-2017-review-quiet-in-term-of-game/)
* [2018](https://sevendaygame.wordpress.com/2019/01/20/2018-review-well/)

Lay ratios:

	slay::[[38 3][176 4][238 5][318 8][344 9][367 11][434 12][478 13][543 13][588 14][663 15][691 15][752 17][774 18][853 20][942 20][1087 24]]
	slayrat::{(*x),%/|x}'slay

Date ratios:

	sdate::[[38 8][174 11][236 14][318 21][344 23][367 26][434 27][478 27][543 32][588 33][663 36][691 41][752 44][774 47][853 53][942 54][1087 76]]
	sdaterat::{(*x),%/|x}'sdate

His numbers are quite high, and I'm not really sure why—perhaps a
combination of only taking numbers from somebody experienced, combined
with the fact that he does daygame in russia, which is supposedly easier
than London, where most of the others publishing data do daygame.

<!--Add:
https://sevendaygame.wordpress.com/2020/06/28/2019-review-it-was-good/ -->

#### Mr. White

[Mr. White](https://mrwhitedaygame.wordpress.com/) didn't publish
statistics from the beginning (this data is from his 8th & 9th year of
doing daygame), this information is therefore unfortunately incomplete:

* [2018](https://mrwhitedaygame.wordpress.com/2019/01/02/2018-daygame-results-stats-and-overview/)
* [2019](https://mrwhitedaygame.wordpress.com/2020/01/02/2019-daygame-results-stats-and-overview/)

Lay ratios:

	mwlay::[[700 13][1212 25]]
	mwlayrat::{(*x),%/|x}'mwlay

Date ratios:

	mwdate::[[700 30][1212 68]]
	mwdaterat::{(*x),%/|x}'mwdate

#### Thomas Crown

[Thomas Crown](https://thomascrownpua.wordpress.com):

* [2016/2017](https://thomascrownpua.wordpress.com/2016-17/)
* [2018](https://thomascrownpua.wordpress.com/2018-statistics/)
* [2019](https://thomascrownpua.wordpress.com/2020/01/03/2019-in-review/)

The 2019 review unfortunately doesn't contain the number of approaches, but he writes:

> I got 11 lays this year and my approach to lay ratio was around 1:53
> with roughly the same age and quality: an improvement on last year’s
> ratio.

*— [Thomas Crown](https://thomascrownpua.wordpress.com), [“2019 In Review”](https://thomascrownpua.wordpress.com/2020/01/03/2019-in-review/), 2020*

From this one can deduce that the number of approaches was `$11*53=583$`,
or at least a number somewhere near that.

Lay ratios:

	tclay::[[208 2][1638 20][2453 34][3036 45]]
	tclayrat::{(*x),%/|x}'tclay

Date ratios (he talks about dates, but it's not clear what the number
of first dates is. I'll still collect the data, but take with a grain
of salt) (also, his 2019 review doesn't say anything about the number
of dates, so that is omitted):

	tcdate::[[208 12][1638 79][2453 116]]
	tcdaterat::{(*x),%/|x}'tcdate

#### Krauser

[Krauser](https://krauserpua.com/) (who started sometime in 2009,
I believe, so these numbers are after several years of training):

* [2013](https://krauserpua.com/2014/01/01/my-2013-daygame-stats/)
* [2014](https://krauserpua.com/2015/01/03/my-2014-daygame-stats/)
* [2015](https://krauserpua.com/2016/01/02/my-2015-daygame-stats/)

> Most of these numbers rely upon estimates because I didn’t keep notes.

*— [Nick Krauser](https://krauserpua.com/), [“My 2013 Daygame Stats”](https://krauserpua.com/2014/01/01/my-2013-daygame-stats/), 2014*

Lay ratios:

	klay::[[1000 27][1480 50][2150 65]]
	klayrat::{(*x),%/|x}'klay

Date ratios:

	kdate::[[1000 60][1480 110][2150 160]]
	kdaterat::{(*x),%/|x}'kdate

#### Wolfe Daygame

* [First 445 approaches](https://wolfedaygame.wordpress.com/2021/09/30/the-first-three-months/index.html)
* [First 593 approaches](https://wolfedaygame.wordpress.com/2021/11/28/600-not-out/index.html)
* [First 1000 approaches](https://wolfedaygame.wordpress.com/2022/06/05/1000-sets-of-hell/index.html)
* [2022](https://wolfedaygame.wordpress.com/2022/12/20/daygame-review-2022/index.html)
	* [January](https://wolfedaygame.wordpress.com/2022/02/01/january-review/index.html)
	* [February](https://wolfedaygame.wordpress.com/2022/02/28/february-review/index.html)
	* [March](https://wolfedaygame.wordpress.com/2022/04/04/march-review/index.html)
	* [April](https://wolfedaygame.wordpress.com/2022/05/03/april-review-frustrating-progress/index.html)
	* [May](https://wolfedaygame.wordpress.com/2022/06/05/may-review/index.html)
	* [June](https://wolfedaygame.wordpress.com/2022/07/05/june-review-shit-approaches-weekends-with-girls-and-lessons-from-self-coaching/index.html)
	* [July](https://wolfedaygame.wordpress.com/2022/08/02/july-review-much-ado-about-nothing/index.html)
	* [August](https://wolfedaygame.wordpress.com/2022/08/31/august-review-sprezzatura-smv-and-greek-delights/index.html)
	* [September](https://wolfedaygame.wordpress.com/2022/10/08/september-review-am-i-even-doing-daygame/index.html)
	* [October](wolfedaygame.wordpress.com/2022/11/01/october-review-seven-weeks-to-go/index.html)
	* [November](https://wolfedaygame.wordpress.com/2022/12/10/november-review-biting-your-hand-off/index.html)
	* [December](https://wolfedaygame.wordpress.com/2022/12/16/december-review-the-streets-are-yours-son/index.html)

Lay ratios:

	wlay::[[39 1][200 2][396 3][584 4][619 5][678 6][746 7][825 8][961 9][1086 9][1122 9][1174 10][1220 11][1267 11][1317 12][1322 12]]
	wlayrat::{(+/(*+wlay)<x)%x}'1+!1000

Since the data for the first 1000 approaches is complete, we can create
a dense array of ratios over time.

Date ratios:

	wdate::[[445 11][593 12][700 14][783 15][858 19][925 23][1000 32][1086 32][1122 32][1174 35][1220 37][1267 37][1317 39][1322 39]]
	wdaterat::{(*x),%/|x}'wdate

<!--TODO: these three

#### Runner

(Seems offline :-/, and I haven't downloaded the site)

[Runner](http://daygamenyc.com):

* [First 2000 approaches](http://daygamenyc.com/2019/05/31/approaching-2000-approaches/)
* [First 2 years](http://daygamenyc.com/2019/08/06/2-years-on-is-daygame-worth-it/)
* [2019](http://daygamenyc.com/2020/01/01/im-now-an-intermediate-level-daygamer/)

#### Tom Torero

[Tom Torero](https://tomtorero.com/):

* [2013](https://krauserpua.com/2014/01/02/guest-post-tom-toreros-2013-daygame-stats/)

#### Clarky

* [2023](https://scalingthemountain6.wordpress.com/2023/12/31/2023-my-first-year-in-game/)

### D.J. Caird

[Blog](https://djcaird.wordpress.com/).

And this one:

https://old.reddit.com/r/seduction/comments/9ock2a/my_daygame_experience_so_far_statistics_and/

https://gringodaygame.wordpress.com/2024/12/16/2000-and-still-counting/

https://thefurnacesofdaygame.wordpress.com/

https://coffeedaygame.wordpress.com/2025/06/16/my-2025-daygame-stats-climbing-mount-improbable/
-->

### Estimating Parameters

I will assume that this is comparatively over-optimistic,
and assume that the date-to-lay ratio converges towards 1 in
30 on the scale of thousands of approaches in the form of an
[S-curve](https://www.lesswrong.com/posts/oaqKjHbgsoqEXBMZ2 "S-Curves for Trend Forecasting").
The other parameters are estimated using
[`scipy.optimize.curve_fit`](./notes.html#None) with data from Roy Walker,
Mr. Wolfe and Thomas Crown, since we have information from the start.

#### Lays

First we collect the relevant information in a processable form (removing
the first datapoint from Mr. Wolfe because it confuses `curve_fit`):

	import numpy as np
	import scipy.optimize as spo
	rwlay=np.array([[511, 5],[901, 10],[977, 10],[1060, 11],[1143, 13],[1216, 14],[1380, 16],[1448, 18],[1557, 19],[1990, 27],[2063, 27],[2130, 27],[2230, 27],[2373, 31],[2540, 35],[2876, 44],[3442, 62],[3567, 63],[3991, 83],[4092, 84]])
	tclay=np.array([[208, 2],[1638, 20],[2453, 34],[3036, 45]])
	wlay=np.array([[39, 1],[200, 2],[396, 3],[584, 4],[619, 5],[678, 6],[746, 7],[825, 8],[961, 9],[1086, 9],[1122, 9],[1174, 10],[1220, 11],[1267, 11],[1317, 12],[1322, 12]])
	def ratio_of(data):
		return data.T[1]/data.T[0]
	ratios=np.concatenate([ratio_of(rwlay), ratio_of(tclay), ratio_of(wlay)])
	approaches=np.concatenate([rwlay.T[0], tclay.T[0], wlay.T[0]])

Now we can estimate the parameters:

	def shrunk_logistic(x, slope, intercept, ceiling):
		return ceiling*1/(1+np.exp(slope*x+intercept))
	ratio_fit=spo.curve_fit(shrunk_logistic, approaches, ratios, bounds=([-np.inf, 0, 0], [1, np.inf, 0.033]))

These numbers are of course heavily dependant on all kinds of factors:
attractiveness, speed of learning, effort exerted in daygame, logistics
and much much more.

#### Dates


I then repeat the same procedure for dates, collecting the date ratio
data for Walker, Wolfe & Crown:

	rwdate=np.array([[511, 19,], [901, 38,], [977, 38,], [1060, 40,], [1143, 46,], [1216, 48,], [1380, 58,], [1448, 63,], [1557, 64,], [1990, 81,], [2063, 81,], [2130, 84,], [2230, 85,], [2373, 91,], [2540, 97,], [2876, 126,], [3442, 165,], [3567, 170,], [3991, 200,], [4092, 202]])
	tcdate=np.array([[208, 12], [1638, 79], [2453, 116]])
	wdate=np.array([[445, 11,], [593, 12,], [700, 14,], [783, 15,], [858, 19,], [925, 23,], [1000, 32,], [1086, 32,], [1122, 32,], [1174, 35,], [1220, 37,], [1267, 37,], [1317, 39,], [1322, 39,]])

	date_ratios=np.concatenate([ratio_of(rwdate), ratio_of(tcdate), ratio_of(wdate)])
	approaches=np.concatenate([rwdate.T[0], tcdate.T[0], wdate.T[0]])

This time I assume that at best one goes on a date with 1 in 14 women
approached:

	date_ratio_fit=spo.curve_fit(shrunk_logistic, approaches, date_ratios, bounds=([-np.inf, 0, 0], [1, np.inf, 0.07]))
	date_slope, date_intercept, date_ceiling=date_ratio_fit[0]

The Klong code describing the date- and lay- ratios is then as follows:

	layceil::0.032999999999999995
	layslope::-0.00032469342601662376
	layintercept::1.0921062524727312

	layratio::{layceil*1%(1+exp(layintercept+layslope*x))}

	dateceil::0.06999999999999999
	dateslope::-0.00032682619283946467
	dateintercept::0.4249112313623176

	dateratio::{dateceil*1%(1+exp(dateintercept+dateslope*x))}

#### Visualizing the Data

* Green: Roy Walker
* Beige: Seven
* Blue: Mr. White
* Purple: Thomas Crown
* Red: Krauser
* Orange: Mr. Wolfe

The plotted data for lay ratios (and the corresponding fitted sigmoid
curve) look like this:

![Empirical data for the cumulative value of lay-ratios over time](./img/daygame_cost_benefit/layratio_data.png "Empirical data for the cumulative value of lay-ratios over time.")

Similarly, the data for reported date ratios:

![Empirical data for the cumulative value of date-ratios over time](./img/daygame_cost_benefit/dateratio_data.png "Empirical data for the cumulative value of date-ratios over time.")

#### Comparing Date & Lay Ratios

We can also compare date & lay ratios with the fitted parameters, and
I notice that date ratios grow faster than lay ratios. Not sure what is
up with that.

![The date & lay ratios over thousands of approaches](./img/daygame_cost_benefit/ratio_data.png "The date & lay ratios over thousands of approaches")

A Simple Model
--------------

One can separately estimate the costs and the benefits from doing daygame,
and then subtract the costs from the benefits to calculate the value.

### Cost

Daygame has several different obvious costs: [opportunity
costs](https://en.wikipedia.org/wiki/Opportunity_cost) from the time
spent approaching and dating women who then flake (one could be doing
better things in the same time, like pursuing other hobbies, learning
a language or musical instrument) and simply the cost of paying for dates.

#### Approaching Opportunity Cost

> First you'll need to desensitise yourself to randomly chatting up
> hot girls sober during the day. This takes a few months of going out
> 3-5 times a week and talking to 10 girls during each session (keep each
> session to no more than 2 hours).

*— [Tom Torero](https://tomtorero.com/), [“Beginner's Guide to Daygame”](./doc/game/beginners_guide_to_daygame_torero_2018.pdf) p. 6, 2018*

> Most regular hustlers go out 3-5 times a week and do 10 approaches
> each session, meaning 30-50 per week.

*— [Tom Torero](https://tomtorero.com/), [“Beginner's Guide to Daygame”](./doc/game/beginners_guide_to_daygame_torero_2018.pdf) p. 13, 2018*

I will assume that most daygamers will do around 4 approaches an hour
(less in the beginning, with approach anxiety, but more later), with 15
minutes for one approach.

The opportunity cost of daygame is unclear—what would one be doing
instead? One could dream of daygamers instead cultivating friendships,
learning languages or making music or meditating, and while that could
certainly sometimes be the case, a lot of that time would also be spent
on mindlessly browsing the internet, watching netflix or doing other
things that aren't terribly fulfilling or valuable. Economists often
assume that the opportunity cost of an activity to be the money one
could have earned during that time, so I'll just go with that.

The [Clearer Thinking
tool](https://programs.clearerthinking.org/what_is_your_time_really_worth_to_you.html)
for the value of my time returns 20€/hour:

	oppcost::20

Daygamers who could earn more with their day job might want to adjust
this number upwards.

##### Skepticism

I am skeptical that the opportunity cost should be ones wage: an
additional hour spent working might be net negative, even with taking wage
into account (working hours have diminishing and at some point negative
[marginal utility](https://en.wikipedia.org/wiki/Marginal_utility)
because of exhaustion).

It may be that daygame only replaces *productive* personal time, that
the energy exerted in daygame misses in other productive activities,
while the amount spent on downtime & unfulfilling stuff stays constant.

But such things are difficult to quantify, so I'll stick with the
opportunity cost.

<!--
TODO: move to "other benefits"
Furthermore, the physical activity while doing daygame is broadly
good: most people probably don't spend enough time outside walking
around (reducing [Vitamin D](https://en.wikipedia.org/wiki/Vitamin-D)
deficiency), and interacting with other people.
-->

#### Costs from Dates

Dates cost money: both as an opportunity cost and for paying for drinks.

##### Opportunity Cost

[Free Northerner
2012](https://freenortherner.wordpress.com/2012/06/12/economic-analysis-of-casual-sex-prostitution-vs-game/
"Economic Analysis of Casual Sex –
Prostitution vs Game") assumes 3 dates, it is [common
wisdom](https://theredarchive.com/blog/Days-of-Game/part-i-mysterys-seven-hour-rule-and-lmr.22180)
originating from
[Mystery](https://en.wikipedia.org/wiki/Erik_von_Markovik) that 7 hours
is a normal time spent on dates until having sex.

Data from [Roy Walker](https://roywalkerdaygame.wordpress.com/) includes
numbers of dates starting from 2018:

* [2018](https://roywalkerdaygame.wordpress.com/2019/01/09/2018-a-year-of-change/)
* [2019](https://roywalkerdaygame.wordpress.com/2020/01/07/2019-the-year-of-meh/)
	* [January](https://roywalkerdaygame.wordpress.com/2019/02/19/ketchup-in-glass-bottles/)

He reports 76 first dates, 27 second dates, 11 third dates and 5 fourth
dates. This means that he went on 5 dates with 4 women, on 3 dates with
`$11-5=6$` women, and so forth. This means that the average number of dates he
went on per first date was
`$\frac{5\cdot 4+(11-5)\cdot 3+(27-11)\cdot 2+(76-27)}{76} \approx 1.566$`
– quite lower than the 3 assumed by [Free Northerner
2012](https://freenortherner.wordpress.com/2012/06/12/economic-analysis-of-casual-sex-prostitution-vs-game/ "Economic Analysis of Casual Sex – Prostitution vs Game")!

For [Seven](https://sevendaygame.wordpress.com/), the numbers can be
found here<!--TODO: did he update with 2020 numbers?-->:

* [2016](https://sevendaygame.wordpress.com/2017/01/21/dec-2016-report-2016-review-and-kicking-off-2017/)
* [2017](https://sevendaygame.wordpress.com/2018/01/15/2017-review-a-year-in-st-petersburg/)
* [2018](https://sevendaygame.wordpress.com/2019/01/20/2018-review-well/)

He reports 76 first dates, 21 second dates, 13 third
dates, 6 fourth dates and 1 fifth date. This results in
`$\frac{(1\cdot 5+(6-1)\cdot 4+(13-6)\cdot 3+(21-13)\cdot 2+(76-21))}{76} \approx 1.54$`
dates per lay, again smaller.

Similarly, Thomas Crown reports [1.4 dates on average for a lay in
his first year](https://thomascrownpua.wordpress.com/2016-17/ "2016/17 Statistics")
and [1.1 for his
second](https://thomascrownpua.wordpress.com/2018-statistics/ "2018 Statistics").

I will assume 1.7 dates on average lasting 3.5h each, because the numbers
above are from people who have already done many approaches:

	datelen::3.5
	avgdates::1.7

##### Paying for Dates

On dates, one usually needs to pay for drinks, food, and perhaps a taxi,
there doesn't seem to be much information about the exact costs out
there. I will assume \\$20 for a date.

	datecost::20

#### Calculating the Cost

The cost of daygame is the sum of the opportunity cost from approaching,
the opportunity cost of dates and the direct cost of paying for dates:

	cost::{(oppcost*x%apprperhour)+(dateratio(x)*datecost*avgdates*x)+dateratio(x)*datelen*avgdates*oppcost}

The resulting function is linear on the number of approaches:

	.l("./load.kg")

	.l("nplot")

	grid([0],maxappr,[1000];[-12000 0 500])
	xtitle("Approaches")
	ytitle("Cumulative dollar cost of dates")
	plot(cost)
	draw()

![Cumulative cost of approaching & dating](./img/daygame_cost_benefit/cost.png "Cumulative cost of approaching and dating, is pretty much linear over approaches.")

### Benefit

The thing providing most of the value from daygame is the sex with
different women. Sex is not a homogenous commodity, but instead has a
wildly differing value, depending on the attractiveness of the partner
and their skill at sex. Nethertheless I will assume that the value of
sex averages out to the price of prostitution.

I will consider two different components of the value: the value of
the sex itself (as compared to prostitution) and the [sense of pride and
accomplishment](https://knowyourmeme.com/memes/events/star-wars-battlefront-ii-unlockable-heroes-controversy)
(knowing that one is developing ones skills in daygame, while prostitution
is often accompanied with shame<!--TODO: source-->).

#### Value of the Sex Itself

> According to this intro to escorting guide on a business blog
> for escorts (I guess escorts need business advice too; the weird
> things you find on the internet) costs about $250-500/hr depending
> on the city.

*— [Free Northerner](https://freenortherner.com/), [“Economic Analysis of Casual Sex – Prostitution vs Game”](http://freenortherner.com/2012/06/12/economic-analysis-of-casual-sex-prostitution-vs-game/), 2012*

<!--TODO: find own sources-->

This leaves us with ~\\$400 per hour of prostitution, but I want to flag
that the cost of prostitution is highly dependent on the attractiveness
of the escort, with prices in the thousands of dollars for particularly
beautiful women—but realistically I don't expect to find data on the
beauty of women that men sleep with through daygame compared to the
beauty of escorts.

I will assume that one sex session lasts one hour and that the average
daygamer sleeps with the same woman 4 times (some women become regulars
or long-term partners, even if the overwhelming majority is only a
one-night stand).

And I will assume that the diminishing returns on sex with the same
partner _is_ logarithmic, because for men, having sex multiple times with
the same woman carries little *evolutionary* advantage except perhaps for
competition with other mens sperm.

<!--TODO: this is not true? Finding a good match, linear as one drives
down the probability of not having fathered children, etc-->

So we can calculate that the value of sleeping with one woman is

		.l("math")
		350*log(2;4)
	700.0

<!--TODO: what if we tried to maximize the utility from sleeping with a
woman some number of times? Especially since sleeping with more beautiful
women is a higher initial return-->

##### Diminishing Returns on Sex Partners

I will also assume that the dimimishing returns on sex with different
partners are [radical](https://en.wikipedia.org/wiki/Square-root),
with an exponent of `$\frac{199}{200}$`.

I have not found any people discussing this and [other
questions](#Appendix_D_Some_Questions_About_the_Value_of_Offspring),
and there is probably a high variance in these numbers depending on
the daygamer.

My intuition is that it should be linear, which stems from the handwavey
evolutionary argument that men should value additional offspring with
randomly selected women with a constant marginal return, since more
diverse offspring from a basically infinite population of mating partners
result (in expectation) in linearly more grandchildren.

*If* I assume it's linear, then the model just straight up gives
astronomical values for doing daygame. Like, it's no question *at all*
whether one should do daygame, and one should basically never stop
doing it.

If you believe that there are linear returns to the number of sex
partners, then you want to do daygame, unless you value sex very little.
<!--TODO: maybe have *another* version of the model?-->

But, in practice, many men doing pick-up lose the motivation after some
number of lays, their notch hyena<!--TODO: link--> satisfied, so there
must be *some* diminishing returns here. But logarithmic returns are
quite punishing, and don't seem to capture the underlying dynamic very
well—hence the compromise with radical diminishing returns with a
"large" (i.e. very slowly diminishing) exponent. That way, it's not
as crazy as non-diminishing returns, but still captures some of the
real-world dynamics and theoretical intuitions.

	partnerexp::199%200

#### A Sense of Pride and Accomplishment

I will assume that the sense of pride and accomplishment is ~\\$400 for
the first lay. I am making this number up, since I'm lacking any data
on this. (If one believes this to be too much, I'll remind the reader
that men sometimes pay thousands of dollars for pick-up coaching and
bootcamps, which very far from guarantee any sex.)

To wrap it up, one can conclude that the value of the first lay is

		prostcost::350
		prideval::400
		laynum::4
		firstlayval::prideval+prostcost*log(2;laynum)
	1000.0

As said, I assume that the marginal returns on additional sex partners are
radical—except for the sense of pride and accomplishment, which very
much disappears over time. I'll assume it's logarithmic.

#### Calculating the Benefit

The benefit from sex can be calculated by summing the expected sense of
pride and accomplishment and the expected value from having sex. Note
that this number is cumulative, as it considers the benefit of all lays
up for `x` approaches:

	firstlayat::118

	pridevals::{prideval*log(2;x+1)*layratio(x)*x}
	pridemult::prideval%log(2;pridevals(firstlayat)) :"For normalization, so that the first lay is actually worth as much"
	discpridevals::{pridemult*log(2;pridevals(x))}

	layvals::{prostcost*log(2;laynum)*layratio(x)*x}
	laymult::prostcost%layvals(firstlayat)^partnerexp :"same here"
	disclayvals::{(laymult*layvals(x))^partnerexp}

This looks like this for up to 5000 approaches:

	.l("./load.kg")

	.l("nplot")

	grid([0],maxappr,[1000];[0 50000 2000])
	xtitle("Approaches")
	ytitle("Cumulative dollar value of lays")
	plot(layvals)
	draw()

![Value of lays for a given number of approaches, cumulatively](./img/daygame_cost_benefit/layvals.png "Value of lays for a given number of approaches, cumulatively. It is a graph growing approximately by the number of approaches to the power of 199/200.")

Then the total benefit is the discounted pride values and the discounted
value of sex:

	benefit::{discpridevals(x)+disclayvals(x)}

### Value

To now calculate the optimal amount of daygame, one simply calculates
the difference between cumulative benefit and cumulative cost for all
possible number of approaches up to the maximum possible number (in this
case 5000, which is a common number for expert daygamers) and chooses the maximum:

		maxappr::5000
		vals::{benefit(x)-cost(x)}'1+!maxappr
		optim::*>vals
	4999
		optimben::vals@*>vals
	10190.4271226371274

So one can conclude that 5000 approaches (i.e., as many as possible)
are optimal under these assumptions, with a value of \\$10k.

This can be visualized as well:

	.l("nplot")

	.l("./res.kg")

	grid([0],maxappr,[1000];[-15000 15000 1000])
	xtitle("Approaches")
	ytitle("Cumulative total value")

	plot({benefit(x)-cost(x)})
	text(200;250;"Value")

	setrgb(0;0;1)
	plot(benefit)
	text(200;400;"Benefit")

	setrgb(1;0;0)
	plot({-cost(x)})
	text(250;60;"cost")

	bar(optim;15000+optimben;10000)

	draw()

![Visualizing the cost & benefit of daygame, against each other, as well as the optimum](img/daygame_cost_benefit/complete.png "Visualizing the cost & benefit of daygame, against each other, as well as the optimum")

A Slightly More Complex Model
------------------------------

Of course one might answer that the simple model fails to capture much
of the subtlety of the situation: Proponents of daygame might mention
positive psychological side-effects such as increased self-confidence
and resilience to rejection. Opponents of daygame could point at direct
financial expenditures (such as possibly having to buy new clothes,
renting an apartment that is closer to good places for daygame),
and also possible social and psychological costs (scars from constant
rejection and mockery from being found out to be a pick-up "artist"),
if they ever stopped moaning about how they disapprove of daygame.

These influences are of course much harder to quantify, and the numbers
presented here are mostly guesswork. As I get to know more daygamers
and do more daygame myself, I intend to update and refine this model
to better reflect reality.

Note that this slightly more complex model adds to the previous, simpler
model. Previously assumed costs and benefits are not altered.

### Additional Benefits

Besides sex, the additional benefits of daygame can be separated into two
broad categories: Increases in subjective well-being (from cultivating
a skill that requires effort and practice), and positive side effects
such as increased salary resulting from a higher willingness to negotiate
ones salary and search for other jobs.

<!--TODO: Find a better partner benefit-->

#### Positive Side Effects

Let's assume one does 1000 daygame approaches per year.
Let's then assume that doing 1000 daygame approaches increases ones
expected salary by 0.5% in the first year, with then logarithmic increases
for each additional year, for 10 years.
The [parity purchasing power average annual
wage](https://en.wikipedia.org/wiki/List_of_countries_by_average_wage)
in the US was \\$60k in 2017, but many industrialized countries are lower.
I'll assume that the average annual wage for a daygamer is \\$40k, just
to be safe.

The code for calculating the monetary value of the positive side-effects of
doing x daygame approaches then is

	annsal::40000
	yearsben::10
	increase::0.005
	apppy::1000
	sideeff::{yearsben*increase*annsal*ln(1+x%apppy)}

![Positive side effects from doing daygame](img/daygame_cost_benefit/sideeff.png "Positive side effects from doing daygame")

#### Mental Benefit

This one is tricky, especially for somebody who has never done any
daygame approaches. Many daygamers seem to highly enjoy what they
do, but that is probably mostly due to selection bias.
I'll mostly rely on my personal experience and on this very biased sample
set here, so take this with a grain of salt. That said, I haven't read
any reports describing that the author stopped doing daygame due to
stress or uncontrollable anxiety, although people who would do that
would probably never start doing daygame in the first place.

To get to the point, I model the mental effects of daygame to be negative
in the beginning (increased anxiety, self-doubt, and insecurity),
and positive effects such as playful enjoyment, flow-states and
extraverted enthusiasm setting after in after an initial hump. These
positive states become less strong over time because of getting used
to pickup. Specifically, the negative effects peak at ~80 approaches
(with -\\$500), and break even after ~300. The cumulative value approaches
\\$1900 over thousands of approaches.

To model this, I abuse a [log-normal
distribution](https://en.wikipedia.org/wiki/Log-normal_distribution)
to represent the value over time:

	mental::{(10000*(ln.pdf((x*0.005)+0.5;1;1)))-1900}

![Value of mental states due to doing daygame](img/daygame_cost_benefit/mental.png "Value of mental states due to doing daygame")

### Additional Costs

#### Expenditures

Besides the cost for dates & opportunity costs, doing daygame might carry
a great amount of various expenditures: some daygamers move to appartments
that are closer to the centers of cities & are more expensive, there may
be some costs from upgrading ones wardrobe, buying condoms and possibly
sex toys<!--TODO: Red Quest/KYIL post about sex toys-->.

In economics, costs are often divided into fixed costs (costs that are
not dependent on the amount of goods produced, in this case approaches
made) and variable costs (costs that are related to the amount of goods
produced).

Making the distinction between fixed costs and variable costs is sometimes
a bit tricky; similar in this case. Is buying new clothes a fixed or a
variable cost? Clothes wear down over time, and need to be bought again,
but the difference doing daygame makes in wearing down clothes is minor
at best. Also, some costs will depend on the time in ones life doing
daygame, but not on the amount of daygame: Doing daygame for 10 years,
but only with 100 approaches a year, will have different fixed costs
from doing it for a year, but 1000 approaches in that year. In making
the distinction between what counts as a fixed cost in this case and
what counts as a variable cost, I will mostly go with my gut feeling.

Note that it is also important to consider the counterfactual case:
Would these expenditures be made if the person wasn't doing daygame?

##### Fixed Costs

I assume that the fixed costs for doing any daygame at all are \\$500:

	fixcost::500

<!--
To possible fixed costs I'd count the following:

* Logistics (higher rent from living closer to the city center)
* Sex toys
* Clothes (shoes, leather jacket etc.)
* Accessories (bracelets, beads, tattoos)
* Hygiene (better haircuts, marginal other improvements)
* Contacts (instead of glasses)
* Fitness (gym membership, buying weights)

Of course, not every daygamer pays for all of these.

Some of the above are dependent on the duration of the time in ones
life one spends with daygame. Having better logistics is a good example:
one can procrastinate daygaming and still be paying the higher rent for
better logistics.

Also time-dependent is better hygiene (I assume mostly marginal
improvements such as getting better haircuts, buying a bit more mouthwash
& floss and shaving a bit more often) and fitness (at least the fee for
gym memberships, weights don't need to be replaced that often).

For time-dependent costs, I assume that the daygamer is very committed,
and does 1000 approaches per year.

###### Logistics
-->
<!--TODO: find some examples for sources-->
<!--
I (without any research) assume that a daygamer will pay \\$200 more per
year for logistics.

It seems to be relatively common for daygamers to move because of daygame,
I'll assume that 30% of them will do it.

###### Sex Toys
-->
<!--Find sources for average vibrator cost-->
<!--
I assume the daygamer counterfactually buys one vibrator (those who
buy more probably would also have bought sex toys in the counterfactual
case where they weren't doing daygame). A vibrator seems to cost ~\\$30
on average.

Although buying sex toys has
been recommended by for example [The Red Quest
2019](https://theredquest.wordpress.com/2019/03/13/tell-your-girl-to-use-a-vibrator-during-sex-and-other-bedroom-tips/ "Tell your girl to use a vibrator during sex, and other bedroom tips and sex skills for guys"),
I haven't heard much discussion of this, and therefore assume that only
10% of daygamers will buy any kind of sex toys.

###### Clothes
-->
<!--TODO: find some sources/discussion?-->
<!--
Many daygamers seem to buy less flashy clothes, sometimes of higher
quality. I'm unsure how much these clothes introduce additional costs
and how much they just displace buying normal clothes. I'll pretty much
baselessly assume that the cost overhead is \\$80.

This seems like something many daygamers do, I'll assume 80%.

###### Accessories

###### Hygiene

###### Contacts

###### Fitness

-->

##### Variable Costs

I assume that the variable costs are \\$0.5 per approach:

	varcost::0.5

<!--
* Condoms
* Transportation (money for gas, public transport)

###### Condoms

###### Transportation

-->

##### Code

With this, one can easily calculate the additional exppenditures:

	expenditures::{fixcost+varcost*x}

#### Social Costs from Being Found Out

For some people doing daygame, being found out as a daygamer can have
negative consequences: Loosing friends, being publicly shamed, or even
having negative effects in the workplace. For this reason (and probably
also as a precautionary measure), many daygamers publish their writing
online anonymously.

But doing daygame can also have negative side-effects even if one doesn't
write about it online: Acquantainces could see one doing daygame and
tell it around in parts of ones social circle, leading to ostracisation
or financial consequences.

On the other hand, being discovered probably doesn't propagate through
ones whole social circle, and often probably has very small effects.

I model this as having a certain probability of being discovered as
a daygamer for every approach. Being found out more than once has
logarithmically increasing costs with the number of being found out.

I'll (somewhat arbitrarily) set the cost of first being found at \\$500,
and the probability of being found out at any approach to 0.1%.

The probability of being discovered `n` times with
`x` approaches can be calculated using the [binomial
distribution](https://en.wikipedia.org/wiki/Binomial_distribution).

To make the code run faster, only the scenarios with a cost of more than
\\$0.01 are being considered.

	fcbfo::300
	pbfo::0.001
	cbfo::{[t];t::x;+/{b.pmf(x;t;pbfo)*fcbfo*ln(e*x)}'1+!{(x<t)&00.1<b.pmf(x;t;pbfo)*fcbfo*ln(e*x)}{x+1}:~1}

### Value in the Complex Model

The global optimum is now calculated the same way as [here](#Value):

		optim::*>vals
	1024
		vals@*>vals
	2110.1350422531768

The more complex model with additional considerations therefore recommends
1024 approaches, with a value of ~\\$2110.13.

Graphically:

	.l("nplot")

	.l("./res_complex.kg")

	grid([0],maxappr,[1000];[-20000 20000 1000])
	xtitle("Approaches")
	ytitle("Cumulative total value")

	plot({benefit(x)-cost(x)})
	text(200;250;"Value")

	setrgb(0;0;1)
	plot(benefit)
	text(200;400;"Benefit")

	setrgb(1;0;0)
	plot({-cost(x)})
	text(250;60;"cost")

	bar(optim;20000+optimben;10000)

	draw()

![Visualizing the cost & benefit of daygame, against each other, as well as the optimum. Using the more complex model.](img/daygame_cost_benefit/complete_complex.png "Visualizing the cost & benefit of daygame, against each other, as well as the optimum. Using the more complex model.")

Conclusion
----------

I have presented both a simple and a more complicated cost-benefit
analysis for daygame. Both conclude that daygame is worth it, at around
500-1000 approaches, but the value is not enormous, with only a \\$1-2k,
and decreases rapidly with less lenient assumptions.

I tentatively conclude that daygame may be worth it, but
it's definitely not a surefire positive deal. Sign up for
[cryonics](./considerations_on_cryonics.html "Considerations on Cryonics")
first.

Appendix A: A Guesstimate Version of the Simple Model
-----------------------------------------------------

Since there is a lot of uncertainty in the presented model, I thought
it'd be good to make a Monte-Carlo version of the model using the website
[Guesstimate](https://www.getguesstimate.com).

The model can be found [here](https://www.getguesstimate.com/models/15526).

### Inputs

Appendix B: A Slightly More Complex Guesstimate Model of the Value
------------------------------------------------------------------

### Inputs

Appendix C: Empirically Checking the Assumptions
-------------------------------------------------

Appendix D: Some Questions About the Value of Sex
---------------------------------------------------

A cost-benefit analysis of daygame contains some questions that
are not obvious to answer, but some of which feel tractable from a
[population-genetics](https://en.wikipedia.org/wiki/Population_Genetics)
perspective:

1. If one has sex as the result of daygame, how long does one have sex?
2. How often do daygamers sleep with the women they have seduced?
3. How strong are the diminishing returns to sex with different partners?
	1. Or, in more general terms:
	2. For a male animal, what is the function that describes the marginal value of mating once with a female randomly selected from the fertile population? I have the feeling that I would be able to answer this if I new more population genetics.
	3. For example, a male animal should be willing to die for the expectation of >2 offspring with a randomly selected female. But the chance of fathering a child with a random woman depends on the time of the woman's period, her age &c.
	4. One could then take ones life-time discounted estimated earning potential, calculate the expected value over the [pregnancy rate for sexual intercourse](https://en.wikipedia.org/wiki/Pregnancy_rate#Pregnancy_rate_for_sexual_intercourse) given the age of the woman and the man, and multiply these together.
	5. It's unclear to me whether there should be any effect of diminishing returns at all in the number of partners slept with, except perhaps through the fact that the population is not infinitely big and therefore the number of offspring with different partners' genes declines. But given that the world population is in the billions, we might just as well treat it as infinite.
4. And how strong are the diminishing returns to sex with the same partner?
	1. This could be investigated in the same way as the question above.

<!--TODO: Is this something?-->
