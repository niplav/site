[home](./index.md)
-------------------

*author: niplav, created: 2019-10-18, modified: 2019-10-18, language: english, status: in progress, importance: 4, confidence: remote*

> __.__

Considerations on Cryonics
==========================

Many would-be cryonicists cryocrastinate <!--TODO: link for the use of
the word-->, i.e they put off signing up for cryonics until a later point
in their life. This has often been explained by the fact that signing up
for cryonics requires high conscientiousness<!--TODO: source for this-->
and can be easily put off to another point in life. However, it hasn't
yet been explored whether this procrastination might not be rational:
Many cryonics organisations have high membership fees, which might be
avoided by waiting.

To find this out, I present a point-estimate model of whether (and if yes,
when) to sign up for cryonics. The model is written in Lua.<!--TODO: link-->

Cost-Benefit Calculation for Cryonics
-------------------------------------

To find out whether to sign up for cryonics at all, one needs
to make a cost-benefit calculation. This has been [attempted
before](http://www.overcomingbias.com/2009/03/break-cryonics-down.html)<!--TODO:
quote the last paragraph from this blog-post-->, but it might be
productive to approach the topic independently.

Costs are comparatively easy to calculate and contain little uncertainty:
The costs of cryopreservation and life-insurance are widely known, and
can be easily added. The benefits of cryopreservation, however, contain
a lot more uncertainty: It is not at all clear that the technology for
reuscitation will be developed, cryonics organizations (or humanity)
survive to develop such technology, or that the future will be interested
in reuscitating people from cryopreservation.

The model presented makes the assumption that a person has a given age
and has the option of waiting for signing up for cryonics every year
up to their expected year of death. So, for example, a person that is
20 years old now is able to plan signing up when they are 20 years old,
21 years, 22 years and so on up to 78 years. The value of cryonics is
calculated, and the value of a regular death is tacitly assumed to be
\$0.

	curage=20
	actval={78.36, 78.64, 78.66, 78.67, 78.68, 78.69, 78.69, 78.70, 78.71, 78.71, 78.72, 78.72, 78.73, 78.73, 78.74, 78.75, 78.75, 78.77, 78.79, 78.81, 78.83, 78.86, 78.88, 78.91, 78.93, 78.96, 78.98, 79.01, 79.03, 79.06, 79.09, 79.12, 79.15, 79.18, 79.21, 79.25, 79.29, 79.32, 79.37, 79.41, 79.45, 79.50, 79.55, 79.61, 79.66, 79.73, 79.80, 79.87, 79.95, 80.03, 80.13, 80.23, 80.34, 80.46, 80.59, 80.73, 80.88, 81.05, 81.22, 81.42, 81.62, 81.83, 82.05, 82.29, 82.54, 82.80, 83.07, 83.35, 83.64, 83.94, 84.25, 84.57, 84.89, 85.23, 85.58, 85.93, 86.30, 86.68, 87.08, 87.49, 87.92, 88.38, 88.86, 89.38, 89.91, 90.47, 91.07, 91.69, 92.34, 93.01, 93.70, 94.42, 95.16, 95.94, 96.72, 97.55, 98.40, 99.27, 100.14, 101.02, 101.91}

	for age=curage,math.floor(actval[curage]) do
		print(value(age) .. ": " .. age)
	end

`curage` contains the current age of the user of the program. `actval` is
an actuarial table that contains at the nth position the life expectancy
of a person that is n years old at the moment for a westernn nation
(in this case Germany)<!--TODO: source-->.

The Disvalue of Waiting
-----------------------

Two important factors play into the value (or disvalue) of waiting
to sign up for cryonics: [Motivation drift](./notes.html#Value-Drift)
and the possibility of dying before signing up.

	function value(age)
		return prob_signup(age)*prob_liveto(age)*(benefit(age)-cost(age))
	end

### Motivation Drift

<!--TODO: find out whether there has been any research into the concrete shape
of motivation drift-->

`prob_signup` is a function that calculates the probability of signing up
for cryonics after waiting up to having a certain age. It seems clear
that people loose motivation to perform certain actions, especially
if they are unpleasant or complex. A good example for this is people
being motivated at the start of the year to do regular exercise: How
many of those actually keep their promises to themselves? They might
start off exercising, but after the first few weeks the first people
drop out, and and a couple of months there is nearly nobody left still
keeping the promises. It seems like there is a strong regression to the
mean<!--TODO: link--> in regards to action: Most regular actions are
replaced by inaction, most strong values are replaced by apathy over time.
A similar phenomenon seems likely for signing up for cryonics: At first,
people are very enthusiastic about signing up, but then loose interest
as time progresses.

It doesn't seem obvious how strong motivation drift is and how it develops
over time (some people regain motivation after some time), but intuitively
it seems like a geometric distribution<!--TODO: source-->. The reasoning
is as follows: Imagine that a thousand people have the motivation to
perform a given action n years into the future. Every year, a certain
percentage p of the people still motivated loses interest in performing
that action and drop out. After n years, the number of people who
perform the action is `$1000*p^n$` (the percentage of people motivated is
`$p^n$`).

When trying to find out what the value of p is for oneself, one can
imagine a thousand independent identical copies of oneself planning a
complex plan one year ahead. What would the percentage of selves actually
going through with the plan be? Intuitively, it can't be much higher
than 95%, possibly much lower, especially for something as complex as
signing up for cryonics.

	decay=0.95
	function prob_signup(age)
	        return decay^(age-curage)
	end

Interestingly, this does not mean that the decision of whether to be
cryonically preserved or not should be set in stone as soon as possible:
Cryonics memberships are very easy to cancel, in nearly all cases a
simple email and a cessation of paying membership fees suffices. Signing
up for cryonics earlier protects against regression to the mean, which
means apathy or lack of motivation towards cryonics, but does not protect
against changing ones mind about cryonics: If one becomes convinced it's
bullshit later, one can easily get out (much more easily than getting in).
On the other hand, there might be a considerable sunk cost due to already
paid membership fees and the acquired life insurance.

### Dying Before Signing Up

Mortality rates are often calculated using a so-called Gompertz
distribution<!--TODO: link-->.

	b=0.108
	eta=0.0001

	function gompertz(age)
	        return math.exp(-eta*(math.exp(b*age)-1))
	end

	function prob_liveto(age)
	        return gompertz(age)/gompertz(curage)
	end

Value of a Lifeyear in the Future
---------------------------------

Much ink and pixels have been spilled on the question of the quality
of the future, very little of it trying to make accurate predictions.
One way to look at the question could be to create clear criteria that
encapsulate the most important human values and ask a prediction market
to start betting. This could include the power of humanity to make most
important decisions regarding its development and resource management,
diversity among human beings, average happiness and lifespans and other
variables such as inequality regarding resources.

1. Most future scenarios seem merely "alien", not really positive/negative
2. Most negative future scenarios don't lead to reuscitation (civilisational collapse, stable totalitarianism, existential catastrophes like AI failure, nuclear war, biotechnological disaster, natural catastrophe). Exceptions:
	*	ascended economy where the cryonics contract is fulfilled by the
		economy, but the resulting world has few/no humans & living
		conditions are insanity-inducingly boring
	* malevolent AI, either through acausal trade or because of sign error in CEV
3.	There are some people working on long-term positive outcomes, and
	most people work on long-term neutral projects, but no or very
	few people working on long-term hellish conditions
