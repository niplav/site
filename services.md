[home](./index.md)
------------------

*author: niplav, created: 2023-07-17, modified: 2024-03-05, language: english, status: finished, importance: 5, confidence: other*

> __My services (research, programming, experimental design and
implementation) can be acquired for money.__

Services
=========

I am available for hire to do consulting, especially research consulting
and to a lesser degree software engineering and data science.

Contact me [here](./about.html#Contact) for inquiries.

Examples of my past paid work include [a library of forecasting
datasets](./iqisa.html) [an analysis of range and forecasting
accuracy](./range_and_forecasting_accuracy.html), and a literature review
on [transfer learning in humans](./transfer.html).

<!--TODO: add Raymond feedback. Ask Yagudin & Leech?-->

### Rates

My rates are determined via the
following procedure via a two-sided [sealed-bid
auction](https://en.wikipedia.org/wiki/First-price_sealed-bid_auction),
splitting the difference in bids[^1]:

* You explain your project (scope, problem &c) to me in a call for ≤10 minutes.
* I decide on my minimum acceptable rate `$r_{\text{min}}$` per hour.
* You decide on your maximum acceptable payment `$r_{\text{max}}$` per hour.
* We both reveal `$r_{\text{min}}$` and `$r_{\text{max}}$`, either first through [hashsums](https://en.wikipedia.org/wiki/Hash_sum) of the numbers (with random text appended) and then the cleartext, or simply at the same time.
	* If `$r_{\text{max}} \ge r_{\text{min}}$`, then my rate is `$\frac{r_{\text{max}}+r_{\text{min}}}{2}$` (i.e. the [mean](https://en.wikipedia.org/wiki/Mean) of the two bids).
	* If `$r_{\text{max}}<r_{\text{min}}$`, then no agreement takes place and we fall back to our [BATNA](https://en.wikipedia.org/wiki/BATNA)s.

I am also open to implementing the [VCG
mechanism](https://en.wikipedia.org/wiki/Vickrey-Clarke-Groves_mechanism)
in a negotiation, which would be more effort (needing to report full
utility functions for salaries, and deciding on `$h_i$`) but also
more fun.

<!--My past rates are available [here](#Past_Rates).-->

#### Why Do This?

The [current state of the art for salary
negotiations](https://www.kalzumeus.com/2012/01/23/salary-negotiation/)
is really bad. It rewards disagreeableness, stubornness and social skills,
and is just so unelegant.

Me posting fixed rates online is slightly better, but allows me
less flexibility: There are projects I think are hugely important
and/or interesting, which I'd like to prioritise above unimportant
and uninteresting projects, as well as situations when I'm busy,
and situations in which I'm not busy. But fixed rates only allow
this to a limited amount, and having a complicated multi-stage
payment structure is a bit ugly. It also doesn't allow for [price
discrimination](https://sideways-view.com/2016/11/03/the-best-kind-of-discrimination/index.html)—in
some cases I might suspect that most of the [gains from
trade](https://en.wikipedia.org/wiki/Gains_from_Trade) are going to the
other party, and I'm selfish, so I'd like to have some of that :-).

So the system outlined achieves multiple goals: It allows me to bring
a potentially better salary negotiation mechanism into the world, in
a low-stakes context (since I don't depend on this for my livelihood),
it allows for a better distribution of gains from trade, and it allows
me to adjust my rates depending on my situation.

Also, `$r_{\text{min}}$` and `$r_{\text{max}}$` do *not* need to be
positive! It might be that I like your project *so much* that I set
`$r_{\text{min}}$` to zero or even negative—I have in the past just
[started projects other people proposed because I thought the idea was
awesome](./platforms.html), and an exceptionally great idea might be
worth paying for. Or `$r_{\text{max}}$` might be negative, in that case
you would be selling *me* something. Because this is a new and system,
I welcome inquiries (silly and serious) [here](./about.html#Contact).

I'm not aware of anyone proposing this kind of auction for salary
negotiation in particular, Claude 3.5 Sonnet states that it's similar to
[Vickrey auctions](https://en.wikipedia.org/wiki/Vickrey_Auction), but
in this case there is no second price, and both parties are symmetrical.

<!--#### Past Rates-->

### See Also

* [Other research consultants](./notes.html#Research_Consultants_List)

[^1]: I think that the setup described is probably not [incentive-compatible](https://en.wikipedia.org/wiki/Incentive-compatible) due to the [Myerson-Satterthwaite theorem](https://en.wikipedia.org/wiki/Myerson-Satterthwaite_theorem), like the [first-price sealed-bid auction](https://en.wikipedia.org/wiki/First-price_sealed-bid_auction). (I still think it's a vast improvement over the current state of the art, however). For an incentive-compatible [truthful mechanism](https://en.wikipedia.org/wiki/Truthful_mechanism) the [Vickrey-Clark-Groves mechanism](https://en.wikipedia.org/wiki/Vickrey-Clarke-Groves-Mechanism) can be used. If you want to use the VCG mechanism instead of I'm absolutely down to do that, and would try to figure it out for free.
