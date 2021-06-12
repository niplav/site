[home](./index.md)
------------------

*author: niplav, created: 2021-05-23, modified: 2021-05-30, language: english, status: notes, importance: 3, confidence: unlikely*

> __.__

Notes on Predictions
====================

Total Tesla Sales in 2021
--------------------------

[Link](https://www.metaculus.com/questions/5582/total-tesla-sales-in-2021/).

Question body states 90.65k sales in Q2 2020, and 139k sales in Q3 2020.
That's a `139000/90650=1.53` fold increase, and an increase in 50k.

Interpolating exponentially, that would be `213138` for Q4 2020, and

		+/{213138*1.533^x}'1+!4
	2772646.96740497209

for all of 2021.

Interpolating linearly, that would be `139000+50000=189000`, and

		+/189000+'50000*1+!4
	1256000

for all of 2021.

Overall, I trust the linear extrapolation more – a growth of 50% seems
quite a lot, even for Tesla. But even the linear extrapolation is high.

India GDP growth in Q1-Q3 2021
-------------------------------

[Link](https://www.metaculus.com/questions/6316/india-gdp-growth-in-q1-q3-2021/).

Assuming GDP growth per quarter iid (which it isn't, but I can't be
bothered otherwise).

Assuming 70% chance of positive growth in any quarter. Then chance of
only growth in all quarter `0.7^3=0.343`.

Number of commercial flights on 30 June 2021
---------------------------------------------

[Link](https://www.metaculus.com/questions/5931/number-of-commercial-flights-on-30-june-2021/).

Assuming 2021 numbers are a constant fraction of 2019 numbers, I sample
the first date of every month (maybe this introduces bias? I could also
use the CSV, but can't be bothered to):

		(+/[68909 60576 68976 78173 78207]%[102167 104960 108395 109471 114037])%5
	0.657569826823178416

June 30th 2019 had 123304 commercial flights 7-day averaged.

Naively, we then expect `0.657569826823178416*123304=81080.9899266051914`
flights. This might be increased by higher vaccination numbers, but
not by much – relatively few in the world mostly vaccinated, and many
destinations not sufficiently vaccinated.

Will Scott Morrison be Prime Minister of Australia on 1 July 2021?
-------------------------------------------------------------------

[Link](https://www.metaculus.com/questions/4774/will-scott-morrison-be-prime-minister-of-australia-on-1-july-2021/).

[Wikipedia](https://en.wikipedia.org/wiki/Leadership_spill) states that

> There were 72 leadership spills between 1970 and 2015; the phenomenon
became increasingly more commen in the early 21st century. None occurred
in the 1960s, 10 in the 1970s, 18 in the 1980s, 13 in the 1990s, and 31
between 2000 and 2015. […] five changes of Prime Ministers between
2010 and 2018

Specifically, leadership spills occurred in 2010, 2012, twice in 2013,
twice in 2015, twice in 2018, and once in 2020. That gives 9 leadership
spills in 120 months (~7.5% chance of a spill per month).

Initial Jobless Claims in May 2021
-----------------------------------

[Link](https://www.metaculus.com/questions/7212/initial-jobless-claims-in-may-2021/).

Current average
([source](https://www.investing.com/economic-calendar/initial-jobless-claims-294)):
`(444+473+498)%3=471.666666666666667`. Probably less, because US mostly
vaccinated. Trend decreasing as well.

Date administered doses/capita >0.5 in NL
------------------------------------------

[Link](https://www.metaculus.com/questions/6779/date-administered-dosescapita-05-in-nl/).

Data in Klong array (I should learn R) ([source](https://ourworldindata.org/covid-vaccinations)):

		nlvaccperc::[[15 0.2][17 0.45][24 0.97][31 2.04][38 3.20][45 4.06][59 6.5][66 7.73][73 8.9][80 9.41][87 10.59][94 12.59][101 15.6][108 19.71][115 22.74][122 26.04][129 29.21][136 33.05][142 33.5]]

Linear regression:

		lr(221;lreg(nlvaccperc))
	50.0988848758083841

Calculating back (by hand, `date` couldn't do what I wanted it to),
this gives 2021-07-09 as the date for >50% vaccinations. I'm not sure
whether to be more pessimistic or optimistic, while there hasn't been
any growth in the last week, the overall trend looks kind of superlinear
(maybe because of systems for vaccine distribution being put in place &
optimized over time).

How many NASA "space launch system" (SLS) launches before 2030?
----------------------------------------------------------------

[Link](https://www.metaculus.com/questions/1503/how-many-nasa-space-launch-system-sls-launches-before-2030/).

Feels like a "too big to fail halfway through" situation. Either they
scrap it before anything launches, or they carry out at least one mission
with it before stopping the program.

I want to look up how often (& how early) NASA cancels projects like
these.  Being a big organisation, I expect them to fall prey to sunk-cost
thinking, but on the other hand, it's still a bunch of engineers.

When will India send their first own astronauts to space?
---------------------------------------------------------

[Link](https://www.metaculus.com/questions/1434/when-will-india-send-their-first-own-astronauts-to-space/).

COVID-19 hitting India hard reduces GDP growth (though there is a
question of how long-term this reduction is), and also slows down highly
collaborative projects (such as sending people to space).

We probably can't expect widespread vaccinations for a while
(at the time of writing, [India has a vaccination rate of
10.81%](https://ourworldindata.org/covid-vaccinations)).

I wish I had an equivalent of the [Musk forecast correction
function](https://web.archive.org/web/20210302224031/https://anthony.boyles.cc/Essays/portfolio/ElonMuskFor
ecastCorrectionFunction.html) for announcements by the average politician.

Elon Musk's Net Worth at the End of 2021
-----------------------------------------

[Link](https://www.metaculus.com/questions/4790/elon-musks-net-worth-at-the-end-of-2021/).

According to the [Bloomberg
index](https://www.bloomberg.com/billionaires/), Musk's networth currently
is $167b.

If we predict 2.5% more economic growth this year, and Musk's networth
tracks with that, we can expect his networth to be ~$171b.

Date COVID-19 epidemic subsides in Russia.
------------------------------------------

[Link](https://www.metaculus.com/questions/4737/when-will-the-covid-19-epidemic-subside-in-russia/).

[WHO](https://covid19.who.int/region/euro/country/ru) says that the last
week with <1000 cases of COVID-19 was March 30 2020.

Extremely naively starting with the [Lindy
effect](https://en.wikipedia.org/wiki/Lindy_effect), we assume it's going
to take as long to subside as it took to get to this point, we calculate:

		$ date -d '2020-03-30' '+%s'
	1585519200
		$ date '+%s'
	1622222618
		$ bc
	1622222618+(1622222618-1585519200)
	1658926036
		$ date -d '@1658926036' --iso-8601
	2022-07-27

WHO also states that ~26.5m vaccine doses have been administered.
Russia has a population of ~150m people, so that would be at ~15%
vaccination rate.

They probably started vaccinating beginning of March (+15% vaccination
rate in 3 months), so to reach ~75% vaccination rate (gut-estimate for
what vaccination rate is necessary for <1k cases per week, probably
more). Assuming they vaccinate at similar rate as previously, this gives
`((75-15)/15)*3=12` more months.

This is too pessimistic: vaccine dose prices will fall when richer
countries have more vaccinations, & also over time with economies of
scale and other optimizations. Infection rates will shrink as there's
less cross-infection from other countries with better vaccination rates,
the russian government will figure out how to distribute vaccines faster
and to more people.

Still, I think Russia will need at median 9 more months before they
reach this level of immunity (and after that a relatively long tail,
because 1k cases per week is actually really fricking low, and there's
still the scenario of COVID-19 becoming endemic).

2025 Price of a Crunchwrap Supreme?
-----------------------------------

[Link](https://www.metaculus.com/questions/6344/2025-price-of-a-crunchwrap-supreme/).

Assuming 2% inflation per year, it comes out at `\$3.89*1.02^3.5=\$4.16`.

Lives saved by #SecondDoseDelay for vaccine
-------------------------------------------

[Link](https://www.metaculus.com/questions/6000/lives-saved-by-seconddosedelay-for-vaccine/).

Unfortunately, this hinges a lot on how motivated Metaculites are to
dig up studies & compare the numbers (including all kinds of weird
selection effects, KBCs and factors of laziness). On the level above,
there's the usual p<0.05 conservatism of the scientific community to
"accept a hypothesis", which places a burden on showing that a delay of
the second dose helps (by implicitely assuming that it probably doesn't).
(This is not a critique of the resolution criteria, I have *some* idea of
how hard these kinds of questions are to write, and this one is especially
finicky.  Compared to what I would have done, it's pretty good).

All these considerations would push my estimate down way further than
my actual belief that a delay of second vaccine dose would save lives.

I'm conflicted about whether to predict to maximize my points (and take
the question literally), or to estimate whether delaying a second dose
**would actually save lives**. I'm interested in how other Metaculites
interpret this.

Tenth Sabaton Album
--------------------

[Link](https://www.metaculus.com/questions/7204/tenth-sabaton-album/).

The timespan between new albums being released seems to be increasing:

		yrs::[2005 2006 2007 2008 2010 2012 2014 2016 2019]
		#'-:'yrs
	[1 1 1 2 2 2 2 3]

This indicates that the album will come out in 2022 rather than 2021.
