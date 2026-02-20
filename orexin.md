[home](./index.md)
------------------

*author: niplav, created: 2025-04-03, modified: 2025-11-24, language: english, status: notes, importance: 9, confidence: log*

> __.__

Orexin And Sleep Deprivation
==============================

Protocol
---------

The rough idea is to have a self-blinded randomized trial with
[blocking](https://en.wikipedia.org/wiki/Blocking_\(statistics\)), where
each block is a period of four days alternating between administration
and recovery days.

### Requirements

* Two undistinguishable [spray bottles](https://en.wikipedia.org/wiki/Spray_Bottle)
* Two identical opaque containers for fitting the bottles
* Two pieces of paper, one marked with 'O', one marked with 'P', folded so that the text is not visible
* Saline solution
* Orexin powder for a sufficient dose<!--TODO: ask Claude/read papers to figure out sufficient dose and dissolution!-->

### Checklist

* Store Orexin powder in the freezer
* Before a block:
	* Dissolve Orexin powder in the saline solution in *one* spray bottle, so that it contains an adequate amount (administration results in ~1μg/kg of bodymass)
	* Put saline solution in the other bottle
	* Put the Orexin-filled spray bottle in one container, together with the 'O' piece of paper
	* Put the saline solution spray bottle in the other container, together with the 'P' piece of paper
	* Shuffle the containers until you don't remember which is which, put them in the fridge
* During the block:
	* Day 1:
		* Sleep only 5-6 hours
		* Pick a container at random, take out only the bottle, administer nasal spray
		* Mark the container so that you know that you took it on day one of the block
		* Wait 20 minutes
		* Run [a bunch of measurements](#Measurements)
		* In the evening (~16:00): Collect the measurements again
	* Day 2:
		* Sleep a normal amount
	* Day 3:
		* Sleep only 5-6 hours
		* Pick the other container, take out only the bottle, administer nasal spray
		* Mark the container so that you know that you took it on day three of the block
		* Wait 20 minutes
		* Run [a bunch of measurements](#Measurements)
		* In the evening (~16:00): Collect the measurements again
	* Day 4:
		* Sleep a normal amount
		* Look into the containers, write down whether you took placebo/orexin on days one and three

It doesn't matter when a block starts, it can be any day of the week,
and one can take a couple of days off from the experiment when something
(e.g. a holiday) comes in the way.

#### Measurements

We'd like to keep the measurements manageable and scalable: There is a
core of measurements performed in each block, but if I feel like I have
slack I might decide to do more extensive measurements for one block.

If done per block, this will not impact the quality of the data, but
please don't decide within a block to switch the detail of measurements.

Measurements were selected according to how much they
degrade with sleep deprivation, informed by [this auto-generated
report](./doc/orexin/impact_of_sleep_deprivation_on_psychological_metrics_elicit_2025.pdf)
using [Elicit](https://elicit.org/).

Most of the datapoints will be collected with an application using
pygame<!--TODO: link-->.

* Active measurements
	* Reaction speed via the [psychomotor vigilance task](https://en.wikipedia.org/wiki/Psychomotor_vigilance_task): ≥10 datapoints/day, collected via the tool
	* Attention via the [digit symbol substitution test](https://en.wikipedia.org/wiki/Digit_symbol_substitution_test): 1 datapoint/day, collected via the tool
	* Digit span: ≥10 datapoints/day, collected via the tool
	* [Stanford Sleepiness Scale](https://en.wikipedia.org/wiki/Stanford_Sleepiness_Scale)
	* Subjective well-being: ≥4 datapoints/day, collected via MoodPatterns
	* Time perception accuracy, collected via the tool
* Passive measurements
	* Whatever is collected by the fitbit

### Complications & Explanation

Ideally, we wouldn't have to re-fill the nasal spray bottles after
every block, instead marking the bottle in an easily blindable way
(e.g. a small dot on the bottom) for being able to figure out which
bottle contains what.

Unfortunately, Claude informs me that Orexin has a half-life of ~2 weeks
when stored at fridge temperatures in a liquid solution, and is best
stored long-term in powder-form in the freezer—hence the plan to be careful
and mix it back for each block.

The blocks reduce unexplained variability. The pause days make sure that
(1) one doesn't suffer from excessive sleep deprivation, and (2) to check
if there is any "catch-up sleep" that needs to happen even after taking
Orexin. Investigating tolerance effects would be interesting, but I just
don't think we have enough statistical power to get there, and it's more
useful to focus on one-off effectiveness instead[^1]. Tolerance effects
can be examined later.

Power Calculation
------------------

*epistemic status*: Doing a [power
analysis](https://en.wikipedia.org/wiki/Power_calculation#Power_analysis)
for the first time. Checked by Claude.

Let's say we will use a
[two-sample](https://en.wikipedia.org/wiki/Two-sample_hypothesis_testing)
[t-test](https://en.wikipedia.org/wiki/Student's_t-test). We can use
[statsmodels](https://www.statsmodels.org/) to do the heavy lifting; we
want to detect a medium effect size (0.5) with a bog-standard significance
level of 0.05 and a power of 0.75:

	import statsmodels.stats.power
	>>> statsmodels.stats.power.tt_ind_solve_power(effect_size=0.5, alpha=0.05, power=0.75, alternative='two-sided')
	56.49860618876443
	>>> statsmodels.stats.power.tt_ind_solve_power(effect_size=0.8, alpha=0.05, power=0.75, alternative='two-sided')
	22.68883256203551

This means that we'll have to collect ~60 Orexin samples to detect a
medium effect size; splitting it over two people means that each takes
Orexin ~30 times and Placebo 30 times, with blocks of a length of four
days that gives us 240 days in total (though half of those don't actually
entail any work in terms of data collection).

We're collecting 24 datapoints.

Literature
-----------

![](./img/orexin/monkeys.png)

*SD stands for "sleep deprivation"*

Experimental Log
------------------

### Batch 1

* Prepared from 2025-09-07T23:10 until 2025-09-08T00:10:00
* Stored 6 samples in the vials in the freezer, 1 in the vials in the fridge, and 1 sample in the syringe+atomizer in the fridge.

#### Sample 1

* Monday night: Taking 0.45mg melatonin before going to sleep at 2025-09-08T01:00, setting alarm for 2025-09-08T06:00
* Monday:
	* Contractions in the face
	* Feel alert but scattered, dull
* Tuesday 2025-09-09: Taking 0.45mg melatonin before going to sleep at 2025-09-10T00:10, setting alarm for 2025-09-10T05:35
* Wednesday:
	* Feel surprisingly refreshed after the dose
	* Administering was a pain, 2.5ml is too much
	* 62% sure this was the Orexin-A

#### Sample 2

* Monday:
	* Slight hit/motivation/boost while administering
	* Little pinchings on the shoulders
	* Feel unmotivated to do anything, slight headache, want to take a nap
	* Took a nap from 13:40 to 17:20, feeling much better afterwards
* Wednesday night: Taking 300mg magnesium at 2025-09-17T00:51:33
* Wednesday:
	* Good meditation, though my nervousness cut it short
	* Feel comparatively awake, especially now around two hours after the dose (the lumenator may be helping)
	* Slightly slower than normal but not as slow as on Monday

### Sample 3

* Monday night: Took melatonin and magnesium
* Monday:
	* Might've deblinded? I think this was placebo<sub>60</sub>, based on how full the syring was.
	* Feeling more alert after taking it, slightly hungry (though that could've been the case beforehand already)
	* Emotional status fine, slightly cold, last dream before waking up was indicative of some interesting trauma related to being clumsy and breaking things that are fragile (I personally now think most things are just too fragile, and we're rich enough to be able to afford robust things)
	* Took stimulants ~45 minutes after Orexin, feeling mostly awake but energetic at ~11:00
* Wednesday night: Took melatonin and magnesium
* Wednesday:
	* Took Orexin-A relatively late, around 08:30. While taking, at first I hade a sort of sharpness in my right nostril, I guess this was just because the liquid was irritating it. Went away after spraying more
	* Feeling refreshed immediately after taking it, might just be the [mammalian dive reflex](https://en.wikipedia.org/wiki/Mammalian_dive_reflex), possibly this was the Orexin<sub>65%</sub>

### Sample 4

* Monday
	* Took the sample relatively late, at 09:36
* Wednesday night: Took 0.5mg melatonin
* Wednesday
	* Felt hungry *immediately* after taking it, started eating chocolate cookies. Orexin??

### Sample 5

* Started first dose on Tuesday
* Tuesday morning: Took melatonin and magnesium before sleep
* Tuesday: Snorting this much water stings
* Thursday morning: Took melatonin and magnesium before sleep
* Thursday:
	* Man 2.5ml is *way* too much. 0.5ml would've been totally fine
	* 09:30: Eating

### Sample 6

* Started first dose on Monday, didn't take any melatonin &c beforehand
* Monday morning: Took early, felt elated, whistling as I walking to work
	* Focused enough to do some reading on [Spencer & Gillen 1899](https://www.goodreads.com/book/show/68126748-the-native-tribes-of-central-australiar)
	* Arrived but didn't find any motivation, didn't work the entire day, instead falling into an addictive loop
	* Felt dirty during the day, unclean because I hadn't done anything I'd set out to do
* Tuesday: Woke up at 09:30, but my fitbit slipped off while i slept

### Sample 7

* Thursday morning: Took melatonin and magnesium before sleep
* Thursday: Feeling refreshed by when snorting the water.
	* Maybe deblinded myself by accidentally looking at how full the syringe was?
	* Good mood immediately after taking
* Sunday night: Took melatonin (powder) and magnesium before sleep
* Sunday: Waking up without motivation to do anything. *Hard time* waking up, had to look directly into my lamp to get any mojo.
	* After taking Orexin: Felt refreshed after taking it, more alert.
	* Went to the gym afterwards. Not that hungry, didn't feel like exercising.

[^1]: Even demonstrating one-off effectiveness would be cool: It's often the case that people have short-term sleep deprivation, and would like to ameliorate the effects.
| Variable | Effect Size | p-value | p-corrected | Orexin | Placebo | Difference |
|----------|------------|---------|------------|--------|---------|------------|
| **[PVT](https://en.wikipedia.org/wiki/Psychomotor_vigilance_task) Mean RT (ms)** | 0.100 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.624 | 1.000 | 256.0 ± 28.0 (n=50) | 253.3 ± 26.2 (n=46) | +2.7 |
| **[PVT](https://en.wikipedia.org/wiki/Psychomotor_vigilance_task) Median RT (ms)** | 0.149 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.469 | 1.000 | 243.6 ± 18.3 (n=50) | 240.8 ± 18.9 (n=46) | +2.8 |
| **[PVT](https://en.wikipedia.org/wiki/Psychomotor_vigilance_task) Slowest 10% (ms)** | -0.024 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.908 | 1.000 | 296.7 ± 59.9 (n=50) | 298.2 ± 68.3 (n=46) | -1.5 |
| **[DSST](https://en.wikipedia.org/wiki/Wechsler_Adult_Intelligence_Scale#Coding_and_Symbol_Search) Correct** | 0.211 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.303 | 1.000 | 69.7 ± 10.6 (n=51) | 67.4 ± 11.3 (n=46) | +2.3 |
| **[Digit Span](https://en.wikipedia.org/wiki/Memory_span#Digit-span) Forward** | 0.175 ([r](https://en.wikipedia.org/wiki/Rank-biserial_correlation)) | 0.148 | 1.000 | 7.86 ± 1.00 (n=42) | 8.10 ± 1.13 (n=40) | -0.24 |
| **[Digit Span](https://en.wikipedia.org/wiki/Memory_span#Digit-span) Backward** | 0.061 ([r](https://en.wikipedia.org/wiki/Rank-biserial_correlation)) | 0.627 | 1.000 | 7.31 ± 0.95 (n=42) | 7.38 ± 1.25 (n=40) | -0.07 |
| **[Digit Span](https://en.wikipedia.org/wiki/Memory_span#Digit-span) Total** | 0.127 ([r](https://en.wikipedia.org/wiki/Rank-biserial_correlation)) | 0.318 | 1.000 | 15.2 ± 1.7 (n=42) | 15.5 ± 2.0 (n=40) | -0.3 |
| **[SSS](https://en.wikipedia.org/wiki/Stanford_Sleepiness_Scale) Rating** | -0.178 ([r](https://en.wikipedia.org/wiki/Rank-biserial_correlation)) | 0.112 | 1.000 | 3.29 ± 1.02 (n=52) | 2.98 ± 0.86 (n=46) | +0.31 |
| **Sleep Duration (hrs)** | 0.212 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.542 | 1.000 | 8.60 ± 1.91 (n=17) | 8.27 ± 1.05 (n=17) | +0.33 |
| **Sleep Time Asleep (min)** | 0.115 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.741 | 1.000 | 459 ± 96 (n=17) | 450 ± 60 (n=17) | +9 |
| **Sleep Efficiency (%)** | -0.257 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.460 | 1.000 | 89.4 ± 5.3 (n=17) | 90.5 ± 3.7 (n=17) | -1.2 |
| **Sleep Deep (min)** | -0.011 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.974 | 1.000 | 74.5 ± 22.9 (n=17) | 74.7 ± 19.3 (n=17) | -0.2 |
| **Sleep Light (min)** | 0.232 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.505 | 1.000 | 283 ± 69 (n=17) | 270 ± 40 (n=17) | +13 |
| **Sleep [REM](https://en.wikipedia.org/wiki/Rapid_eye_movement_sleep) (min)** | -0.150 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.665 | 1.000 | 101.2 ± 27.3 (n=17) | 104.9 ± 21.8 (n=17) | -3.7 |
| **Sleep Wake (min)** | 0.341 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.331 | 1.000 | 56.9 ± 38.0 (n=17) | 46.6 ± 19.6 (n=17) | +10.3 |

-------------

| Variable | Effect Size | p-value | Orexin | Placebo | Difference |
|----------|------------|--------|--------|---------|------------|
| **HRV Daily RMSSD (ms)** | 0.079 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.814 | 32.8 ± 13.0 (n=18) | 31.7 ± 15.1 (n=18) | +1.1 |
| **HRV Deep RMSSD (ms)** | 0.369 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.276 | 31.8 ± 12.2 (n=18) | 27.2 ± 13.0 (n=18) | +4.6 |
| **SpO2 Avg (%)** | -0.286 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.397 | 95.7 ± 1.0 (n=18) | 96.0 ± 1.0 (n=18) | -0.3 |
| **SpO2 Min (%)** | -0.059 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.861 | 93.6 ± 1.4 (n=18) | 93.7 ± 1.6 (n=18) | -0.1 |
| **Breathing Rate (breaths/min)** | 0.314 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.382 | 16.4 ± 2.0 (n=17) | 15.8 ± 1.9 (n=15) | +0.6 |
| **Skin Temp Δ (°C)** | -0.041 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.905 | 0.01 ± 0.65 (n=17) | 0.04 ± 0.49 (n=17) | -0.02 |
| **Steps** | 0.032 ([Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)) | 0.909 | 6478 ± 6403 (n=27) | 6282 ± 5996 (n=26) | +196 |
