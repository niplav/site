[home](./index.md)
------------------

*author: niplav, created: 2025-04-03, modified: 2025-04-03, language: english, status: notes, importance: 9, confidence: log*

> __.__

Orexin And Sleep Deprivation
===============================

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
	* Dissolve Orexin powder in the saline solution in *one* spray bottle
	* Put saline solution in the other bottle
	* Put the Orexin-filled spray bottle in one container, together with the 'O' piece of paper
	* Put the saline solution spray bottle in the other container, together with the 'P' piece of paper
	* Shuffle the containers until you don't remember which is which, put them in the fridge
* During the block:
	* Day 1:
		* Sleep only 5-6 hours
		* Pick a container at random, take out only the bottle, administer nasal spray
		* Mark the container so that you know that you took it on day one of the block
		* Wait ~30 minutes
		* Run [a bunch of measurements](#Measurements)
	* Day 2:
		* Sleep a normal amount
	* Day 3:
		* Sleep only 5-6 hours
		* Pick the other container, take out only the bottle, administer nasal spray
		* Mark the container so that you know that you took it on day three of the block
		* Wait ~30 minutes
		* Run [a bunch of measurements](#Measurements)
	* Day 4:
		* Sleep a normal amount
		* Look into the containers, write down whether you took placebo/orexin on days one and three

It doesn't matter when a block starts, it can be any day of the week,
and one can take a couple of days off from the experiment when something
(e.g. a holiday) comes in the way.

#### Measurements

I would like to keep the measurements manageable and scalable: There
is a core of measurements performed in each block, but if I feel like I
have slack I might decide to do more extensive measurements for one block.

If done per block, this will not impact the quality of the data, but
please don't decide within a block to switch the detail of measurements.

* Active measurements
	* Reaction speed: ≥10 datapoints, collected via TODO
	* Digit span: ≥10 datapoints, collected via TODO
	* Subjective well-being: ≥10 datapoints, collected via TODO (maybe MoodPatterns?)
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

### Open Questions

* Is there a way to store Orexin in a dissolved form without it degrading?
* How long should we wait after taking Orexin before starting measurements?

Power Calculation
------------------

[^1]: Even demonstrating one-off effectiveness would be cool: It's often the case that people have short-term sleep deprivation, and would like to ameliorate the effects.
