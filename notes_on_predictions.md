[home](./index.md)
------------------

*author: niplav, created: 2021-05-23, modified: 2021-05-23, language: english, status: notes, importance: 3, confidence: highly unlikely*

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
in the 1960s, 10 in the 1970s, 18 in the 1980s, 130 in the 1990s, and 31
between 2000 and 2015. […] five changes of Prime Ministers between
2010 and 2018

Specifically, leadership spills occurred in 2010, 2012, twice in 2013,
twice in 2015, twice in 2018, and once in 2020. That gives 9 leadership
spills in 120 months (~7.5% chance of a spill per month).
