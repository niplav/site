[home](./index.md)
-------------------

*author: niplav, created: 2019-12-25, modified: 2019-01-24, language: english, status: in progress, importance: 4, confidence: remote*

> __Is daygame worth it, and if yes, how much? I present a point-estimate
> cost-benefit value estimation written in Klong and find that daygame
> is probably worth ~\$2500 maximum, at ~2000 approaches, though the
> number varies under different assumptions. I then perform a Monte-Carlo
> estimation to determine the uncertainty around the expected value and
> find that _.__

Daygame Cost-Benefit Analysis
=============================

<!--How to hyphenate the title?-->

<!--Stats:
Roy Walker:

[2019](https://roywalkerdaygame.wordpress.com/2020/01/07/2019-the-year-of-meh/)
[2018](https://roywalkerdaygame.wordpress.com/2019/01/09/2018-a-year-of-change/)
[2017](https://roywalkerdaygame.wordpress.com/2018/01/06/2017-the-year-of-ups-and-downs/)
[2016](https://roywalkerdaygame.wordpress.com/2017/01/02/2016-the-year-of-1000-sets/)
[Before 2016](https://roywalkerdaygame.wordpress.com/2016/08/07/the-journey-two-years-in/)

Seven:

[2018](https://sevendaygame.wordpress.com/2019/01/20/2018-review-well/)
[2017](https://sevendaygame.wordpress.com/2018/01/15/2017-review-a-year-in-st-petersburg/)
[2016](https://sevendaygame.wordpress.com/2017/01/21/dec-2016-report-2016-review-and-kicking-off-2017/) (July to December)

Mr. White:

[2019](https://mrwhitedaygame.wordpress.com/2020/01/02/2019-daygame-results-stats-and-overview/)
[2018](https://mrwhitedaygame.wordpress.com/2019/01/02/2018-daygame-results-stats-and-overview/)

Thomas Crown:

[2019](https://thomascrownpua.wordpress.com/2020/01/03/2019-in-review/)
[2018](https://thomascrownpua.wordpress.com/2018-statistics/)
[2016/2017](https://thomascrownpua.wordpress.com/2016-17/)

Runner:

[2019](http://daygamenyc.com/2020/01/01/im-now-an-intermediate-level-daygamer/)
[First 2 years](http://daygamenyc.com/2019/08/06/2-years-on-is-daygame-worth-it/)
[First 2000 approaches](http://daygamenyc.com/2019/05/31/approaching-2000-approaches/)

More stats:

https://tddaygame.com/daygame-stats-blatant-lies/
https://project-tusk.com/blogs/the-tusk-diaries/realistic-daygame-statistics
https://daygamersbible.wordpress.com/2018/05/23/daygame-statistics-and-what-they-tell-your-daygame/

Other analysis:
https://freenortherner.wordpress.com/2012/06/12/economic-analysis-of-casual-sex-prostitution-vs-game/
-->

<!--
> Daygame is the art of meeting and attracting women during the daytime
> in different locations and at different times of the day.

Source: https://www.globalseducer.com/daygame/
-->

Cost
----

Daygame has many different costs: opportunity costs<!--TODO: wiki link-->
from the time spent approaching and dating women who then flake (one could
be doing better things in the same time, like pursuing other hobbies,
learning a language or musical instrument), mental strain from approach
anxiety, and simply the cost of paying for dates.

### Approaching Opportunity Cost

It seems like<!--TODO: [citation needed]--> most daygamers do around 4
approaches an hour, so 15 minutes for one approach.

The opportunity cost<!--TODO: wiki--> of daygame is unclear – what would
one be doing instead? One could dream of daygamers instead cultivating
friendships, learning languages or instruments and meditating, and while
that could certainly sometimes be the case, a lot of that time would also
be spent on mindlessly browsing the internet, watching series or doing
other things that aren't terribly fulfilling or valuable. Economists
often assume that the opportunity cost of an activity to be the money
one could have earned with a minimum wage job during that time<!--TODO:
[citation needed]-->, but that seems to go too far: an additional hour
spent working might be net negative, even with taking wage into account
(working hours have diminishing and at some point negative marginal
returns<!--TODO: link--> because of exhaustion).

<!--TODO: minimum wage in different western countries-->

And daygame is generally an activity with comparatively much value:
one spends time outside, moving around and interacting with other people.

I will tentatively set the opportunity cost of an hour of daygame to \$5,
but would be interested in further input:

	oppcost::5

Daygamers who could earn more with their day job might want to adjust
this number up.

### Dating Opportunity Cost

### Mental Cost (or Benefit?)

### Paying for Dates

Benefit
-------

### Value of Having Sex

#### Value of the Sex Itself

#### A Sense of Pride and Accomplishment

#### Long-term Partners

### Flowthrough Benefits

Conclusion
----------

This way, we can calculate the optimal number of approaches and the
cumulative dollar value of these approaches:

	vals::{benefit(x)-cost(x)}'!10000
	*>vals
	vals@*>vals

Appendix A: A Guesstimate Model of the Value
--------------------------------------------
