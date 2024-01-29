[home](./index.md)
------------------

*author: niplav, created: 2024-01-30, modified: 2024-01-30, language: english, status: draft, importance: 5, confidence: certain*

> __I collect [civilizational
inadequacies](https://www.lesswrong.com/s/oLGCcbnvabyibnG9d/p/yPLr2tnXbiFXkMWvk)
and perform an [inadequacy
analysis](https://www.lesswrong.com/s/oLGCcbnvabyibnG9d/p/pRibkeqBa2AxrpgT6)
on some of them.__

Some Civilizational Inadequacies
=================================

<!--TODO: Fermi estimates for all of these-->

* Cookie warnings in the EU, caused by the GDPR
	* Civilizational cost Fermi estimate
		* 1 warning per day, which takes 2 seconds to close, with ~400 mio. people use the internet regularly, for the 4 years since GDPR was instituted
		* `$\frac{1 \text{ warning}}{\text{person} \cdot \text{day}} \cdot \frac{2 \text{ unskilled labor seconds}}{\text{warning}} \cdot \frac{1 \text{ unskilled labor hour}}{3600 \text{ unskilled labor seconds}} \cdot \frac{365 \text{ days}}{\text{year}} \cdot 4 \text{ years} \cdot 4 \cdot 10^8 \text{ persons} \approx 3.25 \cdot 10^8 \text{ unskilled labor hours}$`
		* Which at `$\frac{5€}{\text{unskilled labor hour}}$` is ~1.6 bio. €
		* Can the benefit compare to this?
* Gear sticks for manual gear shifting (which are much more common in the EU, I think)
	* Civilizational cost Fermi estimate
		* Let's assume that ~half of the population of Europe learned to drive with manual (manual might not have been available beforehand), which took them ~5 hours more on average.
		* That gives `$\frac{5 \text{ unskilled labour hours}}{\text{person}} \cdot 3 \cdot 10^8 \text{ persons}=1.5 \cdot 10^8 \text{ unskilled labour hours}$`
		* At `$\frac{5€}{\text{unskilled labor hour}}$` this is ~7.5 bio. €
		* Although maybe this isn't a civiliational inadequacy (since there is not *really* an equilibrium we're caught in), or at least we're in the process of transitioning [out of it](https://www.nytimes.com/2021/06/24/business/stick-shift-collector-cars.html).
		* Disregarding
			* Any costs from increased numbers of crashes.
			* Increased crash probabilities from higher cognitive load.
		* Further relevant numbers
			* It seems like automatic cars [are now *more* fuel efficient than manual ones](https://20somethingfinance.com/manual-transmission-savings/), at ~\$60 per 1000 kilometers.<!--TODO: maybe use http://www.fueleconomy.
gov/ -->
			* On the other hand, automatic gearshifting mechanisms [are far more expensive to repair](https://www.fbfs.com/learning-center/automatic-vs-manual-cars-costs-to-consider), at a cost of ~\\$2k-\\$4k, whereas manual transmission replacement costs ~\\$1.5k-\\$3k.
			* Additionally, [this page](https://20somethingfinance.com/manual-transmission-savings/) states that manual cars are still ~\\$1k cheaper than automatic ones.
			* The world produces about [100 mio. cars per year](https://en.wikipedia.org/wiki/Car_production#World_motor_vehicle_production).
* Non-velcro shoes
* Courses at university are not 3blue1brown + Q&A + extensive quizzes (or automated tutoring à la DARPA)
* TSA security theater
* A lot of terminology in mathematics, for example using "numerator"/"denominator" instead of "upper number"/"lower number" when talking about [fractions](https://en.wikipedia.org/wiki/Fraction) (which would be vastly easier to understand/remember *and* in one case even has fewer syllables)
* Recycling
* People wear glasses and usually clean the *lenses*, but I've never heard of anyone who washes the *frame* of their glasses, despite wearing them on their face nearly the entire day.
* Instead of writing Bachelor's theses, students could simply improve or write Wikipedia articles

### Fragile Tableware

Ceramic/porcelain plates and cups made of glass break easily, while the
æsthetics we have around them seem mostly path-dependent (and perhaps
even *caused* by their fragility, leftovers from a time where fragile
tableware signaled wealth).

__Cooling__: Generally, porcelain plates have the advantage
that food placed on them cools less quickly. Wikipedia [states
that](https://en.wikipedia.org/wiki/List_of_thermal_conductivities)
porcelain has a thermal conductivity of ~1.4 to 1.9
`$\frac{W}{K \cdot m}$` at ~400 Kelvin, and [pyrex
glass](https://en.wikipedia.org/wiki/Pyrex) variants have thermal
conductivities of 1-2 in the the range 273-373 Kelvin, while Aluminium
(a contender for a substance out of which to make plates, glasses &
cups) has a thermal conductivity of ~100 `$\frac{W}{K \cdot m}$` at
273 Kelvin — which leads to faster cooling, and colder food is less
enjoyable to eat. However, we don't *have* to be stupid about this:
plastics lose heat even more slowly than porcelain (generally with
thermal conductivities <1).


__Æsthetics__: The other advantage of porcelain and glass is that they
just *look so much nicer*. I don't have any strong rejoinders here,
my æsthetics rejoice in knowing that I'm doing a thing that is more
economical—but I acknowledge that I'm in the minority there. The
only guidepost I can offer is to look at the price and then ask: "Are
the æsthetics worth this price?" If yes, go ahead! If not, I may have
pointed out something interesting.

Code for a slightly more complicated Fermi
estimate, (mis)using the [probabilistic programming
language](https://en.wikipedia.org/wiki/Probabilistic_programming_language)
Turing.jl:

        using Turing, Plots

        @model function ceramic_glass()
                people ~ Normal(8*10^9, 0.05)
                meals_per_day ~ truncated(Normal(2.5, 1), lower=0)
                proportion_tableware_users ~ Beta(5, 2.5) # Mean ⅔
                breakage_per_meal ~ Beta(1.5, 1000) # Mean ~0.0015
                cost_per_tableware ~ truncated(Normal(2, 0.5), lower=0) # In dollars
        end

        chains = sample(ceramic_glass(), IS(), 10000)
        sampled=get(chains, [:people, :meals_per_day, :proportion_tableware_users, :breakage_per_meal, :cost_per_tableware])
        total_cost_per_day=sampled[:people] .* sampled[:meals_per_day] .* sampled[:proportion_tableware_users] .* sampled[:breakage_per_meal] .* sampled[:cost_per_tableware]
        mean(total_cost_per_day)
        4.00195809996674e7
        gui(histogram(total_cost_per_day, label="samples", xlabel="cost", ylabel="number of samples"))

![](./img/civilizational_inadequacies/cost_histogram.png)

I'm aware that this code is ugly, and I'll fix it<!--TODO: look at how
to do this properly in Turing, maybe download documentation-->.

Note that this code only estimates the costs of fragile tableware, and
makes no statements about the costs of e.g. switching to alternative
materials.
