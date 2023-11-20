[home](./index.md)
------------------

*author: niplav, created: 2023-08-28, modified: 2023-08-28, language: english, status: finished, importance: 7, confidence: certain*

> __There are too many possible quantified self experiments to run. Do
hobbyist prediction platforms[^1] make priorisation easier? I test this
by setting up multiple markets and running two experiments on nootropics
for meditation.__

Using Prediction Platforms to Select Quantified Self Experiments
=================================================================

[dynomight 2022](https://dynomight.net/prediction-market-causation/#7)
has a good proposal:

> Fortunately, there’s a good (and well-known) alternative, which is
to randomize decisions sometimes, at random. You tell people: “I will
roll a 20-sided die. If it comes up 1-19, everyone gets their money back
and I do what I want. If it comes up 20, the bets activate and I decide
what to do using a coinflip.”

> What’s nice about this is that you can do whatever you want when 1-19
come up, including making your decisions using the market prices. But you
must make decisions randomly sometimes, because if bets never activate,
no one will waste their time betting in your market.

> This is elegant. Oh, and by the way are you THE NSF or DARPA or THE
NIH or A BILLIONAIRE WHO WANTS TO SPEND LOTS OF MONEY AND BRAG ABOUT
HOW YOU ADVANCED THE STATE OF HUMAN KNOWLEDGE MORE THAN ALL THOSE OTHER
LAME BILLIONAIRES WHO WOULDN’T KNOW A HIGH ROI IF IT HIT THEM IN THE
FACE? Well how about this:

> 1. Gather proposals for a hundred RCTs that would each be really expensive but also really awesome. (E.g. you could investigate `SALT → MORTALITY` or `ALCOHOL → MORTALITY` or `UBI → HUMAN FLOURISHING`.)
> 2. Fund highly liquid markets to predict the outcome of each of these RCTs, conditional on them being funded.
> 	* If you have hangups about prison, you might want to chat with the [CFTC](https://en.wikipedia.org/wiki/Commodity_Futures_Trading_Commission) before doing this.
> 3. Randomly pick 5% of the proposed projects, fund them as written, and pay off the investors who correctly predicted what would happen.
> 4. Take the other 95% of the proposed projects, give the investors their money back, and use the SWEET PREDICTIVE KNOWLEDGE to pick another 10% of the RCTs to fund for STAGGERING SCIENTIFIC PROGRESS and MAXIMAL STATUS ENHANCEMENT.

*[dynomight](https://dynomight.net/prediction-market-causation/), [“Prediction market does not imply causation”](https://dynomight.net/prediction-market-causation/), 2022*

Well, I'm neither a billionaire nor the NSF or DARPA, but I
__have__ run [two](./nootropics.html#Experiment_B_SelfBlinded_RCT)
[shitty](./nootropics.html#Experiment_A_SelfBlinded_RCT) self-blinded
RCTs on myself already, and I'm certainly not afraid of the
[CFTC](https://en.wikipedia.org/wiki/Commodity_Futures_Trading_Commission).
And indeed I don't have a shortage of ideas on things I
[could](./todo.html#Quantified_Self) run RCTs on, but the time is scarce
(I try to collect m=50 samples in each RCT, which (with days off) is
usually more than 2 months of data collection).

So I'll do what [@saulmunn](https://twitter.com/saulmunn/) pointed [out
to me](https://twitter.com/saulmunn/status/1671923161695240192)
is a possibility: I'm going to do [futarchy
myself](https://www.lesswrong.com/posts/qZXy8kGkNFyqCfHEJ/you-can-do-futarchy-yourself)
by setting up a set of markets of Manifold Markets with respect to the
outcomes of some pre-specified self-blinded RCTs, waiting until bets
on them accumulate, and then running two of those RCTs (the "best" one,
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
activity or receive some sensory input), so I distinguish the two,
and will slightly prioritise the experiments that can be blinded.

In all experiments, I will be using the statistical method
detailed [here](./nootropics.html#Statistical_Method), code for it
[here](./code/experiments/load.py).

### Self-Blinded Experiments

1. __L-Theanine + Caffeine__ vs. __Sugar__ → *Meditative absorption*: 50 samples in the morning after waking up, 25 intervention with 500mg l-theanine & 200mg caffeine and 25 placebo (sugar pills). Expected duration of trial: ~2½ months (one sample every day, but with possible pauses).
2. __Nicotine__ vs. __Normal chewing gum__ → *Meditative absorption*: 40 samples, with [blocking](https://en.wikipedia.org/wiki/Blocking_\(statistics\)) after waking up, 20 intervention with 2mg nicotine, 20 placebo (similar-looking square chewing gum). Expected duration of trial: ~4½ months (two samples/week, to avoid getting addicted to nicotine).
3. __Modafinil__ vs. __Sugar__ → *Meditative absorption*: 40 samples, again with [blocking](https://en.wikipedia.org/wiki/Blocking_\(statistics\)) directly after waking up, 20 intervention with 100mg modafinil and 20 placebo (sugar pills). Expected duration of trial: Also ~4½ months with two samples per week, as to prevent becoming dependent on modafinil.
4. __Vitamin D__ vs. __Sugar__ → *Meditative absorption*: 50 samples, taken after waking up, 25 intervention (25μg Vitamin D₃) and 25 placebo (sugar pills). Expected duration of trial: ~2½ months (taken ~every day, with possible pauses).
5. __Vitamin B12__ vs. __Sugar__ → *Meditative absorption*
6. __LSD Microdosing__ vs. __Water__ → *Meditative absorption*
7. __CBD__ → *Meditative absorption*
8. __THC__ → *Meditative absorption*
9. __Aspartame__ → *Meditative absorption*
10. __Phenylalanine__ → *Meditative absorption*
11. __Bupropion__ → *Happiness*

### Non-Blinded Experiments

1. __Intermittent fasting__ → *Happiness*
2. __Meditation__ → *Sleep duration*
3. __Binaural beats__ → *Meditative absorption*
4. __Brown noise__ vs. __Music__ → *Productivity*
5. __Silence__ vs. __Music__ → *Productivity*
6. __Pomodoro method__ → *Productivity*
7. __Time since last masturbation__ → *Productivity*
8. __Time since last masturbation__ → *Happiness*

Plea
-----

I would love to subsidise my markets on Manifold a whole bunch, but
don't have enough mana for that (I've subsidised them best I could).

So here is my plea: __Please predict on the markets!__

It would be cool to know whether hobbyist prediction markets *can* be
used for choosing experiments, and the worst result would be a "well,
we can't really tell because liquidity on the markets was too small".

Further Ideas
--------------

Combinatorial prediction markets, [latent-variable prediction
markets](https://www.lesswrong.com/posts/ufW5LvcwDuL6qjdBT/latent-variables-for-prediction-markets-motivation-technical).

Results
--------

[^1]: I refuse to call any platform on which people functionally give probabilities, but without staking real money, "prediction markets". Neither [Metaculus](https://www.metaculus.com/) not [Manifold Markets](https://manifold.markets/) are prediction markets, but [PredictIt](https://www.predictit.org/) and Kalshi are.
