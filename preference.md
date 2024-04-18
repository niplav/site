[home](./index.md)
------------------

*author: niplav, created: 2023-12-04, modified: 2023-12-04, language: english, status: maintenance, importance: 3, confidence: certain*

> __I remain unconvinced by preference utilitarianism. Here's why.__

Arguments Against Preference Utilitarianism
=============================================

<div>
        $$\text{argmax} \sum ☺-☹$$
</div>

*—Anders Sandberg, [FHI Final Report](https://static1.squarespace.com/static/660e95991cf0293c2463bcc8/t/661a3fc3cecceb2b8ffce80d/1712996303164/FHI+Final+Report.pdf#page=52) p. 52, 2024*

[Preference
utilitarianism](https://en.wikipedia.org/wiki/Preference_utilitarianism)
enjoys great popularity among utilitarians<!--TODO: citation
needed? How does it compare to other utilitarianisms?-->,
and I tend to agree that it is a [very good pragmatic
compromise](./notes_on_politics_especially_economics.html#What_Politics_Is_For)
especially in the context of politics.

However, most formulations I have encountered bring up some problems
that I have not seen mentioned or addressed elsewhere.

The Identification Argument
----------------------------

One issue with preference utilitarianism concerns the word
“preference”, and especially where in the world these preferences
are located and how they can be identified. What kinds of physical
structures can be identified as having preferences (we might call this
the *identification problem*), and where exactly are those preferences
located (one might call this the *location problem*)? If one is purely
behavioristic about this question, then every physical system can be said
to have preferences, with the addition that if it is in equilibrium, it
seems to have achieved those prefereneces. This is clearly nonsensical,
as also explored in [Filan
2018](https://www.lesswrong.com/posts/26eupx3Byc8swRS7f/bottle-caps-aren-t-optimisers "Bottle Caps Aren't Optimisers").

If we argue that this is pure distinction mongering, and that we "know
an agent when we see one", it might still be argued that evolution is
agent-like enough to fall into our category of an agent, but that we are
not necessarily obligated to spend a significant part of our resources
on copying and storing large amounts of DNA molecules.

Even restricting ourselves to humans, we still have issue with identifying
the computation inside human brains that could be said to be those
preferences, see e.g. [Hayden & Niv
2021](https://nivlab.princeton.edu/publications/case-against-economic-values-brain "The case against economic values in the orbitofrontal cortex (or anywhere else in the brain)").
If we instead go with revealed preferences, unless we assume a
certain level of irrationality, we wouldn't be able to ascertain which
preferences of humans were *not* fulfilled (since we could just assume
that at each moment, each human is [perfectly fulfilling their own
preferences](https://arxiv.org/abs/1712.05812)).

These are, of course, standard problems in value learning [Soares
2018](./doc/cs/ai/alignment/value_learning/the_value_learning_problem_soares_2016.pdf "The Value Learning Problem").

Preference-Altering Actions Disallowed
---------------------------------------

Even if agents bearing preferences can be identified and the preferences
they bear can be located, ethical agents are faced with a dubious
demand: Insofar only the preferences of existing agents matter (i.e. our
population axiology is person-affecting), the ethical agent is forced
to stabilize existing consistent prefereneces (and perhaps also to
[make inconsistent preferences consistent](./turning.html)), because
every stable preference implies a "meta-preference" of its own continued
existence [Omohundro
2008](./doc/cs/ai/alignment/the_basic_ai_drives_omohundro_2008.pdf "The Basic AI Drives").

However, this conflicts with ethical intuitions: We would like to allow
ethical patients to undergo moral growth and reflect on their values.

(I do not expect this to be a practical issue, since at least in
human brains, I expect there to be no actually consistent internal
preferences. With simpler organisms or very simple physical systems, this
might become an issue, but one wouldn't expect them to have undergone
significant moral growth in any case.)

<!--What did I mean by this?

TODO

#### Second-Order Preference

#### Reflective Equilibrium
-->

Possible People
----------------

If we allow the preferences of possible people to influence our decision
procedure, we run into trouble *very quickly*.

In the most realistic case, imagine we can perform genetic editing
(or [embryo selection](https://www.gwern.net/Embryo-selection)) to
select for traits in new humans, and assume that the psychological
profile of people who really want to have been born is at least
somewhat genetically determined, and we can identify and modify
those genes. (Alternatively, imagine that we have found out how
to raise people so that they have a great preference for having
been born, perhaps by an unanticipated leap in [developmental
psychology](https://en.wikipedia.org/wiki/Developmental_psychology)).

Then it seems like preference utilitarianism that includes possible
people demands that we try to grow humanity as quickly as possible,
with most people being modified in such a way that they strongly prefer
being alive and having been born (if they are unusually inept in one or
more ways, we would like to have some people around who can support them).

However, this *preference* for having been born doesn't guarantee
an *enjoyment of life* in the commonsense way. It might be that
while such people really prefer being alive, they're not really
happy while being alive. Indeed, since most of the time [the tails
come apart](https://www.lesswrong.com/posts/asmZvCPHcB4SkSCMW "The Tails Coming Apart As Metaphor For Life"),
I would make the guess that those people wouldn't be much
happier than current humans (an example of [causal
Goodhart](./doc/cs/ai/alignment/agent_foundations/categorizing_variants_of_goodharts_law_manheim_garrabrant_2019.pdf "Categorizing Variants of Goodhart's Law")).

Preference utilitarians who respect possible preferences might just bite
this bullet and argue that this indeed the correct thing to do.

But, depending on the definition of an ethical patient [who displays
preferences](./notes_on_ethics.html#The_Identification_Argument), the
moral patient who maximally prefers existing might look nothing like a
typical human, and more like an intricate e-coli-sized web of diamond
or a very fast rotating blob of strange matter. The only people I can
imagine willing to bite this bullet probably are too busy running around
robbing ammunition stores.

### Side-Note: Philosophers Underestimate the Strangeness of Maximization

Often in arguments with philosophers, especially about consequentialism,
I find that most of them underappreciate the strangeness of
results of very strong optimization algorithms. Whenever there's
an `$\text{argmax}$` in your function, the result is probably
going to look *nothing like* what you imagine it looking like,
especially if the optimization doesn't have [conservative concept
boundaries](https://arbital.com/p/inductive_ambiguity/).

### Preference-Creating Preferences

If you restrict your preference utilitarianism to currently existing
preferences, you might get lucky and avoid this kind of scenario. But
also maybe you won't: If there are any currently existing preferences
of the form P="I want there to be as many physically implemented
instances of P to exist as possible" (these are possible to represent as
[quines](https://en.wikipedia.org/wiki/Quine_\(computing\))), you have
two choices:

* Either you weight preferences by how strong they were at a single point in time `$t$`, and just maximize the preferences existing at `$t$`.
* Or you maximize *currently existing preferences*, weighted by how strong they are right now.

In the latter case, you land in a universe filled with physical systems
implementing the preference P.

Summary
--------

All forms of preference utilitarianism face the challenge of identifying
which systems have preferences, and how those preferences are implemented.

* Preference utilitarianisms
	* Face the challenge of identifying which systems have preferences, and how those preferences are implemented.
	* That don't respect possible preferences:
		* Will attempt to "freeze" current preferences and prevent any moral progress.
		* If they always maximize the currently existing preferences, and self-replicating preferences exist in the universe, they will tile the universe with those preferences.
	* That respect possible preferences:
		* Will get mercilessly exploited by the strongest preferences they include in the domain of moral patients.
