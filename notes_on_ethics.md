[home](./index.md)
------------------

*author: niplav, created: 2021-03-31, modified: 2022-03-15, language: english, status: notes, importance: 3, confidence: highly unlikely*

> __This page contains my notes on ethics, separated from my regular
notes to retain some structure to the notes.__

Notes on Ethics
================

> Aber was wollen denn die Fragen, ich bin ja mit ihnen gescheitert,
wahrscheinlich sind meine Genossen viel klüger als ich und wenden
ganz andere vortreffliche Mittel an, um dieses Leben zu ertragen,
Mittel freilich, die, wie ich aus eigenem hinzufüge, vielleicht ihnen
zur Not helfen, beruhigen, einschläfern, artverwandelnd wirken, aber
in der Allgemeinheit ebenso ohnmächtig sind, wie die meinen, denn,
soviel ich auch ausschaue, einen Erfolg sehe ich nicht.

*— [Frank Kafka](https://en.wikipedia.org/wiki/Franz_Kafka), “Forschungen eines Hundes”, 1922*

My general ethical outlook is one of high [moral
uncertainty](./doc/philosophy/ethics/moral_uncertainty_macaskill_et_al_2020.pdf "Moral Uncertainty (William MacAskill/Krister Bykvist/Toby Ord, 2020)"),
with my favourite theory being consequentialism. I furthermore favour
hedonic, negative-leaning, and act-based consequentialisms.

However, most notes on this page don't depend on these assumptions.

Note that while I am interested in ethics, I haven't read as much about
the topic as I would like. This probably leads to me re-inventing a large
amount of jargon, and making well-known (and already refuted) arguments.

Converging Preference Utilitarianism
------------------------------------

One problem with [preference
utilitarianism](https://en.wikipedia.org/wiki/Preference_utilitarianism)
is the difficulty of aggregating and comparing preferences
interpersonally, as well as a critique that some persons have very
altruistic and others very egoistic preferences.

### Method

A possible method of trying to resolve this is to try to hypothetically
calculate the aggregate preferences of all persons in the following
way: For every existing person pₐ, this person learns about the
preferences of all other persons pₙ. For each pₙ, pₐ learns about
their preferences and experiences pₙ's past sensory inputs. pₐ then
updates their preferences according to this information. This process
is repeated until the maximal difference between preferences has shrunk
to a certain threshold.

### Variations

One possible variation in the procedure is between retaining knowledge
about the identity of pₐ, the person aggregating the preferences. If
this were not done, the result would be very akin to the [Harsanyian
Veil of Ignorance](https://en.wikipedia.org/wiki/Veil_of_ignorance).


Another possible variation could be not attempting to achieve convergence,
but only simply iterating the method for a finite amount of times. Since
it's not clear that more iterations would contribute towards further
convergence, maybe 1 iteration is desirable.

### Problems

This method has a lot of ethical and practical problems.

#### Assumptions

The method assumes a bunch of practical and theoretical premises,
for example that preferences would necessarily converge upon
experiencing and knowing other persons qualia and preferences.
It also assumes that it is in principle possible to make a person
experience other persons qualia.

#### Sentient Simulations

Since each negative experience would be experienced by every
person at least one time, and negative experiences could
considered to have negative value, calculating the converging
preferences would be unethical in practice (just as [simulating the
experience](https://foundational-research.org/risks-of-astronomical-future-suffering/#Sentient_simulations)
over and over).

#### Genuinely Selfish Agents

If an agent is genuinely selfish (has no explicit term for the welfare of
another agent in its preferences), it might not adjust its own preferences
upon experiencing other lifes. It might even be able to circumvent the
veil of ignorance to locate itself.

#### Lacking Brain Power

Some agents might lack the intelligence to process all the information
other agents perceive. For example, an ant would probably not be able
to understand the importance humans give to art.

### See Also

* [Yudkowsky 2004](./doc/cs/ai/alignment/cev/coherent_extrapolated_volition_yudkowsky_2004.pdf "Coherent Extrapolated Volition")

Humans Implement Ethics Discovery
----------------------------------

Humans sometimes change their minds about what they consider to be good,
both on a individual and on a collective scale. One obvious example is
slavery in western countries: although our wealth would make us more
prone to admitting slavery (high difference between wages & costs of
keeping slaves alive), we have nearly no slaves. This used to be different,
in the 18th and 19th century, slavery was a common practice.

This process seems to come partially from learning new facts about
the world (e.g., which ethical patients respond to noxious stimuli,
how different ethical patients/agents are biologically related to each
other, etc.), let's call this the *model-updating process*. But there also
seems to be an aspect of humans genuinely re-weighting their values when
they receive new information, which could be called the *value-updating
process*. There also seems to be a third value-related process
happening, which is more concerned with determining inconsistencies
within ethical theories by applying them in thought-experiments (e.g. by
discovering problems in population axiology, see for example [Parfit
1986](./doc/philosophy/ethics/population/overpopulation_and_the_quality_of_life_parfit_1986.pdf "Overpopulation and the Quality of Life")).
This process might be called the *value-inference process*.

One could say that humans implement the *value-updating*
and the *value-inference* process—when they think about
ethics, there is an underlying algorithm that weighs trade-offs,
considers points for and against specific details in theories,
and searches for maxima. As far as is publicly known, there is no crisp
formalization of this process (initial attempts are [reflective
equilibrium](https://plato.stanford.edu/entries/reflective-equilibrium/)
and [coherent extrapolated
volition](./doc/cs/ai/alignment/cev/coherent_extrapolated_volition_yudkowsky_2004.pdf) "Coherent Extrapolated Volition").

If we accept the [complexity of human
values](https://arbital.com/p/complexity_of_value/) hypothesis, this
absence of a crisp formalism is not surprising: the algorithm for
*value-updating* and *value-inference* is probably too complex to
write down.

However, since we know that humans are existing implementations of this
process, we're not completely out of luck: if we can preserve humans
"as they are" (and many of the notes on this page try to get at what
this fuzzy notion of "as they are" would mean), we have a way to further
update and infer values.

This view emphasizes several conclusions: preserving humans "as they
currently are" becomes very important, perhaps even to the extent of
misallowing self-modification, the loss of human cultural artifacts
(literature, languages, art) becomes more of a tragedy than before
(potential loss of information about what human values are), and making
irreversible decisions becomes worse than before.

<!--Often, change in values seems forseeable. Why? How?-->

See Also
--------

* [Yudkowsky 2017](https://arbital.com/p/meta_unsolved/ "Meta-rules for (narrow) value learning are still unsolved")

I Care About Ethical Decision Procedures
-----------------------------------------

Or, why virtue ethics alone feels misguided.

In general, ethical theories want to describe what is good and what
is bad. Some ethical theories also provide a decision-procedure: what
to do in which situations. One can then differentiate between ethical
theories that give recommendations for action in every possible situation
(we might call those *complete theories*), and ethical theories that
give recommendations for action in a subset of all possible situations
(one might name these *incomplete theories*, although the name might be
considered unfair by proponents of such theories).

<!--Add stuff about partial orderings of actions, with multiple maximal elements?-->

It is important to clarify that incomplete theories are not necessarily
indifferent between different choices for action in situations they have
no result for, but that they just don't provide a recommendation for action.

Prima facie, complete theories seem more desirable than incomplete
theories—advice in the form of "you oughtn't be in this situation
in the first place" is not very helpful if you are confronted with such
a situation!

Virtue ethics strikes me as being such a theory—it defines what is
good, but provides no decision-procedure for acting in most situations.

At best, it could be interpreted as a method for developing such a
decision-procedure for each individual agent, recognizing that an attempt
at formalizing an ethical decision-procedure is a futile goal, and instead
focussing on the value-updating and value-inference process itself.

Deference Attractors of Ethical Agents
---------------------------------------

When I'm angry or stressed (or tired, very horny, high, etc), I would
prefer to have another version of myself make my decisions in that
moment—ideally a version that is well rested, is thinking clearly,
and is not under very heavy pressure. One reason for this is that my
rested & clear-headed self is in general better at making decisions –
it is likely better at playing chess, programming a computer, having
a mutually beneficial discussion etc. But another reason is that even
when I'm in a very turbulent state, I usually still find the *values*
of my relaxed and level-headed self (let's call that self the **deferee
self**) better than my current values. So in some way, my values in
that stressful moment are not [reflectively stable](https://arbital.com/p/reflective_stability/).

Similarly, even when I'm relaxed, I usually still can imagine a
version of myself with even more desired values—more altruistic,
less time-discounting, less parochial. Similarly, that version of
myself likely wants to be even more altruistic! This is a [Murder-Ghandi
problem](https://www.lesswrong.com/posts/SdkAesHBt4tsivEKe/gandhi-murder-pills-and-mental-illness "Gandhi, murder pills, and mental illness"):
It likely leads to a perfectly altruistic, universalist version of myself
that just wants to be itself and keep its own values. Let's call that
self a **deference attractor**.

But I don't always have the same deferee self. Sometimes I actually want
to be more egoistic, more parochial, perhaps even more myopic (even
though I haven't encountered that specific case yet. The deferee self
likely also wants to be even more egoistic, parochial and (maybe?) myopic.
This version of myself is again a deference attractor.

These chains of deference are embedded in a [directed
graph](https://en.wikipedia.org/wiki/Graph_\(discrete_mathematics\))
of selves, many of which are likely reflectively stable. Some
aren't, and perhaps form such chains/paths which either form
[cycles](https://en.wikipedia.org/wiki/Cycle_\(graph_theory\)), or lead
to attractors.

### Deceptive Deference-Attractors?

These graphs don't have to be
[transitive](https://en.wikipedia.org/wiki/Transitivity_\(mathematics\)),
so a deference attractor of myself now could look extremely unappealing
to me. Could one be mistaken about such a judgement, and if yes, when
would one be?

That is, when one would judge a deference attractor to be undesirable,
could it be in fact desirable? Or, if one were to judge in desirable,
could it in fact be undesirable?

Arguments Against Preference Utilitarianism
--------------------------------------------

Moved [here](./preference.html).

Stating the Result of “An Impossibility Theorem for Welfarist Axiologies”
-------------------------------------------------------------------------

<!--TODO: More impossibility theorems?-->

[Arrhenius
2000](./doc/philosophy/ethics/population/an_impossibility_theorem_for_welfarist_axiologies_arrhenius_2000.pdf "An Impossibility Theorem for Welfarist Axiologies")
gives a proof that basically states that the type of population axiology
we want to construct is impossible. However, the natural-language
statement of his result is scattered throughout the paper.

> The primary claim of this paper is that any axiology that satisfies the
Dominance, the Addition, and the Minimal Non-Extreme Priority Principle
implies the Repugnant, the Anti-Egalitarian, or the Sadistic Conclusion.

*— [Gustaf Arrhenius](https://www.iffs.se/en/research/researchers/gustaf-arrhenius/), [“An Impossibility Theorem for Welfarist Axiologies”](./doc/philosophy/ethics/population/an_impossibility_theorem_for_welfarist_axiologies_arrhenius_2000.pdf) p. 15, 2000*

### Requirements

> The Dominance Principle: If population A contains the same number of
people as population B, and every person in A has higher welfare than
any person in B, then A is better than B.

*— [Gustaf Arrhenius](https://www.iffs.se/en/research/researchers/gustaf-arrhenius/), [“An Impossibility Theorem for Welfarist Axiologies”](./doc/philosophy/ethics/population/an_impossibility_theorem_for_welfarist_axiologies_arrhenius_2000.pdf) p. 11, 2000*

> The Addition Principle: If it is bad to add a number of people, all
with welfare lower than the original people, then it is at least as bad
to add a greater number of people, all with even lower welfare than the
original people.

*— [Gustaf Arrhenius](https://www.iffs.se/en/research/researchers/gustaf-arrhenius/), [“An Impossibility Theorem for Welfarist Axiologies”](./doc/philosophy/ethics/population/an_impossibility_theorem_for_welfarist_axiologies_arrhenius_2000.pdf) p. 11, 2000*

> The Minimal Non-Extreme Priority Principle: There is a number n such
that an addition of n people very high welfare and a single person with
slightly negative welfare is at least as good as an addition of the same
number of people but with very low positive welfare.

*— [Gustaf Arrhenius](https://www.iffs.se/en/research/researchers/gustaf-arrhenius/), [“An Impossibility Theorem for Welfarist Axiologies”](./doc/philosophy/ethics/population/an_impossibility_theorem_for_welfarist_axiologies_arrhenius_2000.pdf) p. 11, 2000*

### Conclusions

> The Repugnant Conclusion: For any perfectly equal population
with very high positive value, there is a population with very
low positive welfare which is better.

*— [Gustaf Arrhenius](https://www.iffs.se/en/research/researchers/gustaf-arrhenius/), [“An Impossibility Theorem for Welfarist Axiologies”](./doc/philosophy/ethics/population/an_impossibility_theorem_for_welfarist_axiologies_arrhenius_2000.pdf) p. 2, 2000*

> The Anti-Egalitarian Conclusion: A population with perfect equality can
be worse than a population with the same number of people, inequality,
and lower average (and thus lower total) positive welfare.

*— [Gustaf Arrhenius](https://www.iffs.se/en/research/researchers/gustaf-arrhenius/), [“An Impossibility Theorem for Welfarist Axiologies”](./doc/philosophy/ethics/population/an_impossibility_theorem_for_welfarist_axiologies_arrhenius_2000.pdf) p. 12, 2000*

> The Sadistic Conclusion: When adding people without
affecting the original people's welfare, it can be better to
add people with negative welfare than positive welfare.

*— [Gustaf Arrhenius](https://www.iffs.se/en/research/researchers/gustaf-arrhenius/), [“An Impossibility Theorem for Welfarist Axiologies”](./doc/philosophy/ethics/population/an_impossibility_theorem_for_welfarist_axiologies_arrhenius_2000.pdf) p. 5, 2000*

All of these are stated more mathematically on page 15.

Possible Surprising Implications of Moral Uncertanity
------------------------------------------------------

Preserving languages & biospheres might be really important, if the
continuity of such processes is morally relevant.

We should try to be careful about self-modification, lest we fall into
a molochian attractor state we don't want to get out of. Leave a line
of retreat in ideology-space!

For a rough attempt to formalize this, see [TurnTrout & elriggs
2019](https://www.lesswrong.com/s/7CdoznhJaLEKHwvJW/p/6DuJxY8X45Sco4bS2 "Seeking Power is Often Robustly Instrumental in MDPs").

### We Should Kill All Mosquitoes

If we assign a non-miniscule amount of credence to [retributive theories
of justice](https://en.wikipedia.org/wiki/Retributive_justice)
that include invertebrates as culpable agents, humanity might
have an (additional) duty to exterminate mosquitoes. Between
[5% and 50%](https://en.wikipedia.org/wiki/Mosquito)<!--TODO:
this is incorrect, change!--> of all humans that have ever
lived have been killed by mosquito-born diseases—if humanity
wants to restore justice for all past humans that have died at the
[proboscis](https://en.wikipedia.org/wiki/Proposcis) of mosquito, the
most sensible course of action is to exterminate some or all species of
mosquito that feed on human blood and transmit diseases.

There are of course also additional reasons to exterminate some species
of mosquito: 700k humans die per year from mosquito-borne diseases, and
it might be better for mosquitos themselves to not exist at all (with
[gene drives being an effective method of driving them to
extinction](https://reducing-suffering.org/will-gene-drives-reduce-wild-animal-suffering/ "Will Gene Drives Reduce Wild-Animal Suffering?"), see [Tomasik
2017](https://foundational-research.org/the-importance-of-wild-animal-suffering/ "The Importance of Wild-Animal Suffering")
and [Tomasik
2016](https://reducing-suffering.org/the-importance-of-insect-suffering/ "The Importance of Insect Suffering")
as introductions):

> the cost-effectiveness of the \\$1 million campaign to eliminate
mosquitoes would be (7.5 * 10¹⁴ insect-years prevented) *
(0.0025) / \\$1 million = 1.9 * 10⁶ insect-years prevented per
dollar [by increasing human population]. As one might expect,
this is much bigger than the impact on mosquito populations
directly as calculated in the previous section.

*— [Brian Tomasik](https://reducing-suffering.org), [Will Gene Drives Reduce Wild-Animal Suffering?](https://reducing-suffering.org/will-gene-drives-reduce-wild-animal-suffering/), 2018*

A mild counterpoint to this view is that we have an obligation to help
species that thrive on mosquitoes, since they have helped humanity
throughout the ages, but we'd hurt them by taking away one of their
food sources.

<!--
Why Death is Bad
-----------------

Under moral uncertainty with evolving preferences, you want to keep
options open, but death closes all options but one, potentially losing
a lot of future value.

In a sense, it's unfair towards all other ethical systems you embody
to kill yourself.

Monotonic Convergence or Not of Moral Discovery Process
--------------------------------------------------------

Conditions for Neither Repugnant nor Monstrous Utilitarianism
--------------------------------------------------------------

Diminishing or increasing returns on investments for well-being
of a single agent?

If we're really lucky, initially there are increasing returns, but at
some point they start diminishing.

What Use Ethics For?
---------------------

Everyday life, or problems that arise in the limit?

C.f. High Energy Ethics.

The Two Urgent Problems are: How Don't We Die and How Do We Become Happy?
--------------------------------------------------------------------------

A Very Subjective Ranking of Types of Ethical Theories
-------------------------------------------------------

Consequentialism, Contractualism, Deontology, Virtue Ethics

What Is Wrong With the Unwilling Organ-Donor Thought Experiment?
-----------------------------------------------------------------

Problems with game-theoretical ethical intuitions.

Better framing: Create universe, make decision, destroy universe after
payoff time.

For most people, there's a point where they kill the unwilling organ
donor, so we're basically haggling over the price. Maybe just a Sorites
paradox?
-->
