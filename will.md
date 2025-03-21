[home](./index.md)
------------------

*author: niplav, created: 2025-02-27, modified: 2025-03-21, language: english, status: notes, importance: 1, confidence: joke*

> __New philosophical position/Effective Altruism cause area
dropped. Benefits of pursuing the creation of libertarian free will
likely not worth the costs, based on a Monte-Carlo estimate.__

Creating Libertarian Free Will
================================

The philosophical literature is rich in discussions about [free
will](https://en.wikipedia.org/wiki/Free-Will): Whether beings (usually
humans[^1]) can make choices that are not, in some sense, "completely
determined" by the causal forces of nature. I won't take
any position in that debate here, but instead will ask a
far less explored question:

__If [libertarian free
will](https://en.wikipedia.org/wiki/Libertarian_free_will) *does not*
exist, would it be good to bring it into existence?__

Clearly, humans value freedom in various:
[Libertarianism](https://en.wikipedia.org/wiki/Libertarianism) makes
it the central tenet of its political philosophy, mundane forms of
unfreedom (slavery, imprisonement, social pressure &c) are usually
regarded as undesirable, at least in WEIRD morality; the [capability
approach](https://en.wikipedia.org/wiki/Capability_Approach) and the
[will to power](https://en.wikipedia.org/wiki/Will_To_Power) both take
as central object the value of expanded actions and some theories of
life and artificial intelligence take expanded empowerment/control over
the environment as *the* feature defining successful existence.

Therefore, it's just natural to extend the desire for an expanded
action space to the ontological level; if we could, would we
not want to be able to act *counter* to the laws of physics,
peskily constraining each of us to a single future? ([Many
worlds](https://en.wikipedia.org/wiki/Many-Worlds_Interpretation)
notwithstanding, since it also produces a pre-defined multiverse, and
[quantum randomness](https://en.wikipedia.org/wiki/Quantum_randomness)
(if it exists) also does not count, as outlined in the debate around
the existence of libertarian free will.)

One can call this the __constructive axiological free will hypothesis__
(CAFWH): "*If libertarian free will doesn't (yet) exist, it would be
good to create it and imbue humans with it*".

Fermi Cost-Benefit Estimate
----------------------------

The ITN framework<!--TODO: link--> is ready-to-hand for evaluating whether
working on the CAWFH is a good idea.

### Tractability

Starting with the weakest point. It is currently not clear how to bring
about new ontological entities. One can weakly estimate the cost from
taking the number of basic ontological categories in existence and
dividing them by the work that was involved in bringing them about.

As for basic ontological categories,
my estimate ranges from 0 ([ontological
nihilism](https://en.wikipedia.org/wiki/Ontological_nihilism))
to ~10 (list: mathematical objects, God and/or gods, qualia,
[matterenergy](https://en.wikipedia.org/wiki/Matter-energy_relation),
[spacetime](https://en.wikipedia.org/wiki/Spacetime), [abstract
objects](https://en.wikipedia.org/wiki/Abstract_object),
[souls](https://en.wikipedia.org/wiki/Soul), [moral
facts](https://en.wikipedia.org/wiki/Moral_Realism) and likely others
I have forgotten to consider).

The total work needed to bring those about is difficult to estimate, as
it may range from no work (in the case of ontological nihilism) up to
[absolute infinity](https://en.wikipedia.org/wiki/Absolute_Infinite)
if supernatural beings created existence. I'll take as a mean the
matter-energy content of the observable universe multiplied by four
(since matter-energy and spacetime are only two of the eight basic
ontological categories listed above).

The amount of [baryonic
matter](https://en.wikipedia.org/wiki/Baryonic_matter)
in the observable universe is [estimated
at](https://en.wikipedia.org/wiki/Observable_Universe) ~`$10^{53}$` kg,
but since baryonic matter only makes up 4.5% of the total mass-energy
in the universe, I'll adjust the estimate (not leaving out dark energy &
dark matter).

Using [squigglepy](https://github.com/rethinkpriorities/squigglepy):

	import squigglepy as sq
	num_ontological_categories=sq.to(0, 10)
	cost_new_entity=sq.lognorm(lognorm_mean=(1/0.045)*10**53, lognorm_sd=20)
	prop_universe_entities=num_ontological_categories/sq.to(1, 3)
	new_entity_cost=cost_new_entity/prop_universe_entities

Usually, a new ontological entity costs the mass-energy of `$10^{53}$` kg:

	>>> sq.sample(new_entity_cost, 10)
	array([2.96996124e+53, 7.18535888e+53, 2.98417566e+54, 1.11103257e+54,
	       6.09266737e+53, 8.39602018e+53, 4.08215136e+53, 5.01485048e+53,
	       4.63852243e+53, 3.93717114e+53])

### Importance

It would likely be valuable to create libertarian free will. (Though
see the list of [possible risks](#Risks) below.)

As a proxy, one can try to estimate how much time and energy humans
expand on broadening the list of possible choices available to them;
examples include education, migration to more democratic and liberal
countries, buying transport, many health interventions &c. Philosophical
intuition points me to ~10% of human effort being spent on pure expansion
of mundane freedoms.

Assuming that libertarian free will would be ~5× more valuable, and a
~20% chance that humans already have libertarian free will, together with
a [gross world product](https://en.wikipedia.org/wiki/Gross_World_Product)
of ~\$100T, we can arrive at the value humanity should be willing to
pay for libertarian free will:

	gwp=sq.norm(mean=10**14, sd=1)
	prop_spent_on_freedom=sq.beta(a=2, b=8)
	real_freewill_mult=sq.to(4, 20)
	chance_freewill_exists=sq.beta(a=1, b=4)
	total_value=prop_spent_on_freedom*gwp*real_freewill_mult*(1-chance_freewill_exists)

Sampling, we usually get a few tens of trillions of dollars in value:

	>>> sq.sample(total_value, 10)
	array([9.96797785e+13, 4.23572584e+13, 8.24106658e+13, 4.32935165e+14,
	       2.43818602e+14, 1.26017517e+14, 1.86109674e+14, 1.43918708e+14,
	       4.01545018e+13, 2.40841431e+14])

### Neglectedness

As far as I know, no being is working on creating libertarian free will
de novo, and philosophers have not yet discussed the possibility and
desirability[^2]. It is possible that hidden supernatural entities are
engaged in the process, but that seems unlikely<sub>4%</sub>, and it's
not clear they would imbue humans specifically with the capability if
they created it.

---------------------------------

Unfortunately, it seems like the cost for new ontological basic entities
is too high: It is implausible that we will be able to bring up the
equivalent of ~`$10^{53}-10^{54}$` kg of massenergy with an investment
of ~\$`$10^{13}-10^{14}$`.

However, due to the small amount of thought that has gone into ontological
engineering, there is the potential that creating new ontological
categories is much cheaper than estimated here, and the neglectedness
leaves space for a few experimental philosophers.

Risks
------

Drastic changes to the structure of existence are not without their
risks. Creating libertarian free will may induce multiple hazards:

1. *Choosing evil*: Imbuing humans with free will may cause them to deliberately choose evil (instead of simply being compelled to by the laws of physics), leaving them uniquely culpable of their harmful deeds.
2. *Making the world less predictable*: Free agents interacting with the world may make it less stable and predictable, leading to overall lower welfare.
3. *Being smitten by God for choosing evil*: If God or other supernatural beings have a plan that involves Him or them keeping control over which entities have free will, or if entities are only smitten if they actively choose evil, then giving humans free will may cause God or gods to smite humans, potentially even as a collective. Thus introducing libertarian free will poses a small existential risk.

Other Ontological Entities It Would Potentially Be Good To Create
-------------------------------------------------------------------

* Moral Facts (…)
* God, which would pose novel alignment challenges.
* [Dasein](https://en.wikipedia.org/wiki/Dasein)
* Qualia
* [Hypercomputation](https://en.wikipedia.org/wiki/Hypercomputation), if it is not already possible via [Malament-Hogarth spacetimes](https://en.wikipedia.org/wiki/Malament-Hogarth_spacetime).

See Also
---------

* [Some Unattractive Meta-Ethical Positions, Free to a Good Home (Cosma Shalizi, 2024)](http://bactra.org/notebooks/some-meta-ethical-positions.html)
* [Zombie is to Human as Human is to XXX? (Eric Schwitzgebel, 2025)](https://schwitzsplinters.blogspot.com/2025/02/zombie-is-to-human-as-human-is-to-xxx_26.html)

[^1]: Though even here we may consider possibilities similar to the ones [Shalizi](http://bactra.org/notebooks/some-meta-ethical-positions.html) dicusses: What if free will is possible, but only a few species in the past had it, or only a few species in the future will have it, but not *homo sapiens*? What if there are inanimate objects that *have* free will, but choose not to exercise it? What if some humans<!--TODO: link Aaronson anecdote--> have free will, but others don't, or if all humans have free will as a latent ability, but have failed to notice and deploy it? How about the hypothesis that figuring out whether something/someone has free will is [undecidable](https://en.wikipedia.org/wiki/Undecidable), or at least [EXPTIME-complete](https://en.wikipedia.org/wiki/EXPTIME-complete)? Humans may not have free will themselves, but be theoretically able to create beings with free will… it's just that, by the way the universe is structured, we never will.
[^2]: Based on a short websearch using Google Scholar & Perplexity, and a conversation with ChatGPT with web search enabled.
