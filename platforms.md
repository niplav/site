[home](./index.md)
------------------

*author: niplav, created: 2023-08-28, modified: 2023-12-04, language: english, status: in progress, importance: 7, confidence: certain*

> __There are too many possible quantified self experiments to run. Do
hobbyist prediction platforms[^1] make priorisation easier? I test this by
setting up [multiple markets](#Markets), in order to run two experiments
(the best one, and a random one), mostly for the effects of various
[nootropics](https://en.wikipedia.org/wiki/Nootropics) on absorption
in meditation.__

Using Prediction Platforms to Select Quantified Self Experiments
=================================================================

[dynomight 2022](https://dynomight.net/prediction-market-causation/#7)
has a cool proposal:

> Oh, and by the way are you THE NSF or DARPA or THE NIH or A BILLIONAIRE
WHO WANTS TO SPEND LOTS OF MONEY AND BRAG ABOUT HOW YOU ADVANCED THE
STATE OF HUMAN KNOWLEDGE MORE THAN ALL THOSE OTHER LAME BILLIONAIRES
WHO WOULDN’T KNOW A HIGH ROI IF IT HIT THEM IN THE FACE? Well how
about this:

> 1. Gather proposals for a hundred RCTs that would each be really expensive but also really awesome. (E.g. you could investigate `SALT → MORTALITY` or `ALCOHOL → MORTALITY` or `UBI → HUMAN FLOURISHING`.)
> 2. Fund highly liquid markets to predict the outcome of each of these RCTs, conditional on them being funded.
> 	* If you have hangups about prison, you might want to chat with the [CFTC](https://en.wikipedia.org/wiki/Commodity_Futures_Trading_Commission) before doing this.
> 3. Randomly pick 5% of the proposed projects, fund them as written, and pay off the investors who correctly predicted what would happen.
> 4. Take the other 95% of the proposed projects, give the investors their money back, and use the SWEET PREDICTIVE KNOWLEDGE to pick another 10% of the RCTs to fund for STAGGERING SCIENTIFIC PROGRESS and MAXIMAL STATUS ENHANCEMENT.

*—[dynomight](https://dynomight.net/prediction-market-causation/), [“Prediction market does not imply causation”](https://dynomight.net/prediction-market-causation/), 2022*

Well, I'm neither a billionaire nor the NSF or DARPA, but I
__have__ run [two](./nootropics.html#Experiment_B_SelfBlinded_RCT)
[shitty](./nootropics.html#Experiment_A_SelfBlinded_RCT) self-blinded
RCTs on myself already, and I'm certainly not afraid of the
[CFTC](https://en.wikipedia.org/wiki/Commodity_Futures_Trading_Commission).
And indeed I don't have a shortage of ideas on things I
[could](./todo.html#Quantified_Self) run RCTs on, but the time is scarce
(I try to collect m=50 samples in each RCT, which (with buffer-days off)
is usually more than 2 months of data collection).

So I'll do what [@saulmunn](https://nitter.net/saulmunn/) pointed [out
to me](https://nitter.net/saulmunn/status/1671923161695240192)
is a possibility: I'm going to do [futarchy (on)
myself](https://www.lesswrong.com/posts/qZXy8kGkNFyqCfHEJ/you-can-do-futarchy-yourself)
by setting up a set of markets of Manifold Markets with respect to the
outcomes of some pre-specified self-blinded RCTs, waiting until the prices
on them equilibriate, and then running two of those RCTs (the "best" one,
by my standards, and a random one) and using the results as resolutions,
while resolving the others as ambiguous.

### Timeline

If the markets receive enough liquidity, I'll start the first experiment
early in 2024, and the second one sometime in 2024 (depending on the
exact experiment), hopefully finishing both before 2025.

Markets
--------

Some experiments can be self-blinded, especially ones that involve
substances, others can not because they require me to engage in an
activity or receive some sensory input, so I distinguish the two, and
will slightly prioritise the experiments that can be blinded.

In all experiments, I will be using the statistical method
detailed [here](./nootropics.html#Statistical_Method), code for it
[here](./code/experiments/load.py), unless someone points out that I'm
doing my statistics wrong.

I will be scoring the markets based on the variables specified in the
prediction market title, but I'll of course be collecting [a lot of
other data](./data.html) during that time that will also be analyzed.

### Self-Blinded Experiments

In general, by *meditative absorption* I mean
the concentration/tranquility (in Buddhist terms
[samatha](https://en.wikipedia.org/wiki/Samatha-vipassana)) during
a ≥30 minute meditation session in the morning, ~45 minutes
after waking up and taking the substance (less if the substance
starts working immediately). I will be doing at least 15 minutes of
[anapanasati](https://en.wikipedia.org/wiki/Anapanasati) during that
meditation session, but might start (or end) with another practice).

Past meditation data can be found [here](./data/meditations.csv).

1. [__L-Theanine + Caffeine__ vs. __Sugar__ → *Meditative Absorption*](https://manifold.markets/NiplavYushtun/by-how-much-does-caffeine-ltheanine): 50 samples in the morning after waking up, 25 intervention with 500mg l-theanine & 200mg caffeine and 25 placebo (sugar pills). Expected duration of trial: ~2½ months (one sample every day, but with possible pauses).
2. [__Nicotine__ vs. __Normal chewing gum__ → *Meditative Absorption*](https://manifold.markets/NiplavYushtun/by-how-much-does-nicotine-improve-m): 40 samples, with [blocking](https://en.wikipedia.org/wiki/Blocking_\(statistics\)) after waking up, 20 intervention with 2mg nicotine, 20 placebo (similar-looking square chewing gum). Expected duration of trial: ~4½ months (two samples/week, to avoid getting addicted to nicotine).
3. [__Modafinil__ vs. __Sugar__ → *Meditative Absorption*](https://manifold.markets/NiplavYushtun/by-how-much-does-modafinil-improve): 40 samples, again with [blocking](https://en.wikipedia.org/wiki/Blocking_\(statistics\)) directly after waking up, 20 intervention with 100mg modafinil and 20 placebo (sugar pills). Expected duration of trial: Also ~4½ months with two samples per week, as to prevent becoming dependent on modafinil.
4. [__Vitamin D__ vs. __Sugar__ → *Meditative Absorption*](https://manifold.markets/NiplavYushtun/by-how-much-does-vitamin-d-improve): 50 samples, taken after waking up, 25 intervention (25μg Vitamin D₃) and 25 placebo (sugar pills). Expected duration of trial: ~2½ months (taken ~every day, with possible pauses).
5. [__Vitamin B12__ vs. __Sugar__ → *Meditative Absorption*](https://manifold.markets/NiplavYushtun/by-how-much-does-vitamin-b12-improv): 50 samples, taken after waking up, 25 intervention (500μg Vitamin B12 + 200μg [folate](https://en.wikipedia.org/wiki/Folate)) and 25 placebo (sugar pills). Expected duration of trial: 2½ months (short interruptions included).
6. [__LSD Microdosing__ vs. __Water__ → *Meditative Absorption*](https://manifold.markets/NiplavYushtun/by-how-much-does-microdosed-lsd-imp): 50 samples in the morning, 25 intervention (10μg LSD), and 25 placebo (distilled water). Expected duration of trial is ~4 months (4 samples per week, with some time left as a buffer).
7. [__CBD Oil__ vs. __Similar-Tasting Oil__ → *Meditative Absorption*](https://manifold.markets/NiplavYushtun/by-how-much-does-cbd-improve-medita): 50 samples in the morning, 25 intervention (240mg CBD in oil, orally), and 25 placebo (whatever oil I can find that is closest in taste to the CBD oil). Expected duration of the trial: ~2½ months (taken ~every day, with possible pauses).
8. [__L-Phenylalanine__ vs. __Sugar__ → *Meditative Absorption*](https://manifold.markets/NiplavYushtun/by-how-much-does-lphenylalanine-imp): 50 samples, taken directly after waking up, 25 intervention (750mg L-Phenylalanine), and 25 placebo (sugar pills). Duration of trial: 2½ months (one sample a day).
9. [__Bupropion__ vs. __Sugar__ → *Happiness*](https://manifold.markets/NiplavYushtun/by-how-much-does-bupropion-improve): 50 samples taken after waking up, 25 intervention (150mg [Bupropion](https://en.wikipedia.org/wiki/Bupropion)), and 25 placebo (sugar pills). Duration is typical 2½ months again.
10. [__THC Oil__ vs. __Similar-Tasting Oil__ → *Meditative Absorption*](https://manifold.markets/NiplavYushtun/by-how-much-does-thc-oil-improve-me): 50 samples in the morning, 25 intervention (4mg THC in oil, orally), and 25 placebo (whatever oil I can find that is closest in taste to the THC oil). Expected duration of the trial: ~2½ months (taken ~every day, with possible pauses).

### Non-Blinded Experiments

Some experiments can't be blinded, but they can still be randomized. I
will focus on experiments that can be blinded, but don't want to exclude
the wider space of interventions.

1. [__Intermittent Fasting__ vs. __Normal Diet__ → *Happiness*](https://manifold.markets/NiplavYushtun/by-how-much-does-intermittent-fasti): 50 samples, 25 intervention (eating only between 18:00 and midnight), 25 non-intervention (normal diet, which is usually 2 meals a day, spaced ~10 hours apart), chosen randomly via `echo -e "fast\ndon't fast" | shuf | tail -1`. Expected duration of the trial: ~2 months.
2. [__Pomodoro Method__ vs. __Nothing__ → *Productivity*](https://manifold.markets/NiplavYushtun/by-how-much-does-the-pomodoro-metho): 50 samples, 25 intervention (I try to follow the [Pomodoro method](https://en.wikipedia.org/wiki/Pomodoro_technique) as best as I can, probably by installing a [TAP](https://www.lesswrong.com/posts/wJutA2czyFg6HbYoW/what-are-trigger-action-plans-taps) of some sort), 25 non-intervention (I just try to do work as normally), chosen randomly via `echo -e "pomodoro\nno pomodoro" | shuf | tail -1`. Expected duration of trial: 2 months.
3. [__Bright Light__ vs. __Normal Light__ → *Happiness*](https://manifold.markets/NiplavYushtun/by-how-much-does-very-bright-light): 50 samples, 25 intervention (turning on my [lumenator](https://arbital.com/p/lumenators/) of ~30k lumen in the morning), 25 non-intervention (turning on my normal desk lamp of ~1k lumen), selected via `echo -e "lamp\nno lamp" | shuf | tail -1`. Expected duration of trial: 4 months, as I often don't spend all my day at home.
4. [__Meditation__ vs. __No Meditation__ → *Sleep duration*](https://manifold.markets/NiplavYushtun/by-how-much-does-2-hours-of-meditat): 50 samples, 25 intervention (2 consecutive days of ≥2h/day of meditation), 25 non-intervention (no meditation), selected via `echo -e "meditation\nno meditation" | shuf | tail -1`. Expected duration of trial: 5 months, as I might not always find a 2-day interval in which I'm sure I can meditative 2h/day.

#### Further Ideas

I have a couple more ideas on possible experiments that I could run,
and will put them up as I acquire more mana.

Blindeable:

1. __Semaglutide__ vs. __Sugar__ → *Productivity* (tracking conscientiousness)

Not blindeable:

5. __Binaural Beats__ vs. __Silence__ → *Meditative Absorption*
6. __Brown Noise__ vs. __Silence__ → *Meditative Absorption*
7. __Brown Noise__ vs. __Music__ → *Productivity*
8. __Silence__ vs. __Music__ → *Productivity*
9. __Time Since Last Masturbation__ → *Productivity*
10. __Starting Work Standing__ vs. __Starting Work Sitting__ → *Productivity*

Pleas
------

This little exercise may need __your__ participation! I have three pleas
to you, dear reader:


1. __Please predict on the markets!__ If people predict on the markets, I *both* get more information about the value of the different experiments, and I also get mana back. It would be cool to know whether hobbyist prediction markets *can* be used for choosing experiments, and the worst result would be a "well, we can't really tell because liquidity on the markets was too small".
2. __Maybe send me mana for me to create more markets or subsidise existing ones.__ I'd love to subsidise my markets on Manifold a whole bunch, but don't have enough mana for that at the moment. [clippy](https://manifold.markets/anonymous) and [Tetraspace](https://manifold.markets/Tetraspace) both already send me mana, which I greatly appreciate. With more mana, I could also put up more markets, and thereby explore a larger space of possible experiments. However, maybe the value of another market isn't so high, so this one is way less urgent.<!--TODO: acknowledge other mana gifters-->
3. __Give me ideas for more experiments to run.__ If you have an idea you're enthusiastic about and which you've always wanted to have tested, but you're kind of lazy about actually doing it, I might be able to jump in. Most interesting to me are experiments that are:
	1. *Affordable*: Expensive substances, high-end devices etc. are too prohibitive (unless you want to buy the thing for me to perform the experiment).
	2. *Safe*: Sorry, I'm not going to take methamphetamine, even though it might make me much more productive.
	3. *Measurable*: The variable the intervention is supposed to affect should be measurable in at least *one* of the ways [I currently collect data](http://niplav.site/data.html), or at least easily measurable. In particular cognitive performance is hard to get a grip on: [IQ test](https://en.wikipedia.org/wiki/Iq_test) can't be repeated very often, but maybe there's a game that measures cognitive performance reliably?
	4. *Fast*: I can't do 50 samples of an intervention where one sample takes 2 weeks to take effect. Daily is best, but for *really good* options I might be willing to tolerate 2 samples a week.

Other than that, I also welcome all critiques at any level of detail of
this undertaking.

Further Ideas
--------------

If I could create more markets, I might be able to put up markets on
different variables I measure during the day. That way, I could select
interventions that dominate others across multiple dimensions.

If there were prediction platforms that supported them,
combinatorial prediction markets or [latent-variable prediction
markets](https://www.lesswrong.com/posts/ufW5LvcwDuL6qjdBT/latent-variables-for-prediction-markets-motivation-technical)
could be incredibly cool, but we don't live in that world (yet).

Results
--------

To be done.

Acknowledgements
-----------------

Many thanks to [clippy](https://manifold.markets/anonymous)
([twitter](https://twitter.com/12leavesleft)) for 500
Mana and [Tetraspace](https://manifold.markets/Tetraspace)
([twitter](https://twitter.com/TetraspaceWest)) for 1000 Mana — your
funding of the sciences is greatly appreciated.

See Also
---------

* [Replication Markets](https://replicationmarkets.com/)

Appendix A: Explanations for the Experiments I Chose
-----------------------------------------------------

Over time, I'll put some explanations on why these specific experiments
interest me. Not yet fully, though.

### __L-Theanine + Caffeine__ vs. __Sugar__ → *Meditative Absorption*

My [l-theanine experiment](./nootropics.html#LTheanine) gave disappointing
results, but people have (rightfully) pointed out<!--TODO: where?-->
that l-theanine is best taken together with caffeine: one gets energy
*and* relaxation at the same time.

This points at a broader possibility: Why not set up
markets for all possible combinations of nootropics? But
alas, this runs into problems with [combinatorial
explosion](https://en.wikipedia.org/wiki/Combinatorial_explosion).

### __Nicotine__ vs. __Normal chewing gum__ → *Meditative Absorption*

### __Modafinil__ vs. __Sugar__ → *Meditative Absorption*

### __Vitamin D__ vs. __Sugar__ → *Meditative Absorption*

### __Vitamin B12__ vs. __Sugar__ → *Meditative Absorption*

### __LSD Microdosing__ vs. __Water__ → *Meditative Absorption*

Inspired by [Gwern 2019)](https://www.gwern.net/LSD-microdosing).

### __CBD Oil__ vs. __Similar-Tasting Oil__ → *Meditative Absorption*

### __L-Phenylalanine__ vs. __Sugar__ → *Meditative Absorption*

* [Diet Coke probably isn't a cognitive performance enhancer (dynomight, 2022)](https://dynomight.net/diet-coke-nootropic/)
* [Contra Dynomight contra me, but also kinda contra me and in support of Dynomight, on Diet Coke (Aaron Bergman, 2022)](https://www.aaronbergman.net/p/contra-dynomight-contra-me-but-also)

### __Bupropion__ vs. __Sugar__ → *Happiness*

* [My positive experience taking the antidepressant Wellbutrin/Bupropion, & why maybe you should try it too (Robert Wiblin, 2019)](https://docs.google.com/document/d/1niiV8I4cgk_xZ1Blou15ImPmqXU4eb_li9eRVp5NgYo/)

### __THC Oil__ vs. __Similar-Tasting Oil__ → *Meditative Absorption*

### __Intermittent Fasting__ vs. __Normal Diet__ → *Happiness*

### __Pomodoro Method__ vs. __Nothing__ → *Productivity*

> The Pomodoro technique also uses the concept of rhythm, breaking up
the day into twenty-five-minute segments of work and five minutes of
a break. Interestingly, though, I found no academic study that tested
the technique.

*—Gloria Mark, “Attention Span” p. 66, 2023*

It'd be cool if I were the first person to *actually test* this widespread
technique.

### __Bright Light__ vs. __Normal Light__ → *Happiness*

See [all the things people have written about
lumenators](./notes.html#All_Things_People_Have_Written_About_Lumenators).

### __Meditation__ vs. __No Meditation__ → *Sleep duration*

* [O'Hara et al. 2010)](./meditation/science/meditation_acutely_improves_psychomotor_vigilance_and_may_decrease_sleep_need_kaul_et_al_2010.pdf)

[^1]: I find it odd to call any platform on which people functionally give probabilities, but without staking real money, "prediction markets". Neither [Metaculus](https://www.metaculus.com/) not [Manifold Markets](https://manifold.markets/) are prediction markets, but [PredictIt](https://www.predictit.org/) and [Kalshi](https://kalshi.com/) are.
