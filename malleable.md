[home](./index.md)
-------------------

*author: niplav, created: 2025-12-06, modified: 2025-12-09, language: english, status: in progress, importance: 6, confidence: possible*

> __.__

Malleable Human Minds and AI
=============================

Human values are physically instantiated, and those physical
instantiations can be changed by processes in the world around them. This
is a problem when you have systems around that can steer reality very
well, for example advanced AI systems.

This kind of issue sometimes appears in interactions
between humans, for example between [mentally
disabled people and their caretakers in the context of
voting](https://en.wikipedia.org/wiki/Suffrage_for_Americans_with_Disabilities).
The disabled person might lack the mental tools to form an opinion on
who to vote for on their own, and every action their caretaker takes to
help them form their opinion could steer the process the disabled person
takes to form their opinion by a large amount. In some sense it
might be under-defined what the "correct" way of trying them help
find a party to vote for is.

I think that advanced AI systems could be in a similar relation to
us as caretakers are to people with mental disabilities: They will
be able to easily[^1] influence us by presenting us with [selected
information](https://www.lesswrong.com/s/uLEjM2ij5y3CXXW6c/p/fhJkQo34cYw6KqpH3),
find it hard to communicate the consequences of different decisions so
that we'd find them comprehensible, and see multiple equally valuable
pathways that involve human modification.

The problem of human malleability has several aspects, (1) direct value
modification, (2) addiction/superstimuli, (3) humans becoming unable to
understand AI reasoning, (4) the philosophical problem that "what humans
really want" might be underdefined. Worth disentangling and finding
different interventions?

[^1]: By some global yardstick, such as how many resources they would have to expend relative to how many they have available.

The worry of human minds being malleable wrt the optimization
exerted by AIs would apply in multiple scenarios, both when AIs are
[intent-aligned](https://www.lesswrong.com/s/EmDuGeRw749sD3GKd/p/ZeE7EKHTFMBs8eMxn)
vs. not, where they steer beliefs vs. values, whether they are attempting
take-over or they are not.

1. In AI takeover scenarios, highly persuasive AIs might manipulate the developers or operators of their deployment environment and enable them to give those AIs more power.
2. Resulting in the world becoming optimized towards being a [siren world](https://www.lesswrong.com/posts/nFv2buafNc9jSaxAH/siren-worlds-and-the-perils-of-over-optimised-search), see also [Neyman 2025](https://www.lesswrong.com/posts/c7kZKGswtLkjFbszg/balancing-exploration-and-resistance-to-memetic-threats)
3. Intent alignment becomes fuzzy, much more complicated (see the [Do-What-I-Mean hierarchy](https://arbital.com/p/dwim/)).
4. The future might be very addictive, similar to how modern humans are addicted to many superstimuli compared to hunter-gatherers.

> Some people work makeshift government jobs; others collect a generous
basic income. Humanity could easily become a society of superconsumers,
spending our lives in an opium haze of amazing AI-provided luxuries
and entertainment.

*—Kokotajlo et al., [“AI 2027”](https://ai-2027.com/slowdown#slowdown-2029-12-31), 2025*

I'll mostly focus on situations where AIs are more or less intent-aligned
to some humans, and have looked at non-intent-aligned AI persuasion risks
[elsewhere](https://niplav.site/persuasion.html).

### How Big of a Problem Is It

Ignoring persuasion as a means that AIs could use for take-over, how
disvaluable would worlds be in which human preferences are being shaped
by well-intentioned AIs?

My intuition is that it wouldn't be as bad as the proverbial
[paperclip maximizer](https://arbital.com/p/paperclip_maximizer/)
(to which one can assign a value of zero). Would it be better than
a world in which humans never build superintelligence? If humans
are too distracted by superstimuli to settle and use the [cosmic
endowment](https://arbital.com/p/cosmic_endowment/), then we'd be better
off not building AIs which are powerful enough to influence malleable
human minds.

Two considerations that flow into how much worse futures with these
kinds of influenced human minds would be are (1) how malleable human
minds are, and (2) the classic consideration about [fragility of
values](https://www.lesswrong.com/posts/xzFQp7bmkoKfnae9R).

In general, influenceable human minds are a risk factor for not reaching
near-optimal futures, and the standard questions on the ease of reaching
near-optimal futures apply, e.g. whether it is sufficient for a small
part of the universe to be near-optimal so that the whole future is
near-optimal.

If more time available: Try to build a
[squiggle](https://forum.effectivealtruism.org/posts/t6FA9kGsJsEQMDExt/what-is-estimational-programming-squiggle-in-context)
model that tries to estimate the disvalue compared to (1) paperclipper,
(2) near-optimal future for a single human who has grabbed power, (3)
near-optimal future.

#### Current Evidence

Events that are somewhat indicative of strange human-AI interactions
that also somewhat steer the human:

1. Recommender systems causing their users to be addicted or otherwise changed, see also [Aligning Recommender Systems as Cause Area (Ivan Vendrov/Jeremy Nixon, 2019)](https://forum.effectivealtruism.org/posts/xzjQvqDYahigHcwgQ/aligning-recommender-systems-as-cause-area)
	1. I haven't looked into this much, how overblown are e.g. polarization worries?
2. [Sycophancy in GPT-4o: what happened and what we’re doing about it (OpenAI, 2025)](https://openai.com/index/sycophancy-in-gpt-4o/), though it's unclear how much this is related to training on human feedback vs. mild misalignment on the side of the models. My guess is that the lack of continual learning by AIs also reduces the amount they change their users.
	1. Plausibly related: [The Rise of Parasitic AI (Adele Lopez, 2025)](https://www.lesswrong.com/posts/6ZnznCaTcbGYsCmqu/the-rise-of-parasitic-ai).
3. *Anecdotal & subjective evidence*: My guess is that my interactions with Claude over the past 1⅔ years have slightly changed the way I write, and maybe the way I interact with other people. (I think I've caught myself saying "You're absolutely right" a few times in conversations with people :-D). I'd guess that change has been small and positive.

### Counter-Arguments

__Intent-alignment is a strong enough attractor that this is solved
"automatically"__: AIs will have learned a latent generator of what
ultimately endorsed and unendorsed modifications to human minds are,
and try to follow what these generators specify. Alternatively, at least
the modifications ultimately judged as very disvaluable are excluded,
and the remaining possible modifications to humans are benign enough to
still be very valuable.

This might not work if this generator can't be learned from the training
data because humans haven't made enough philosophical progress so that
it is present in the training data.

Reinforcement learning on human feedback won't learn which modifications
are acceptable and which aren't<sub>80%</sub>.

__The Good is already represented enough in the training data or the model
spec for this to be solved automatically__: All the actions implied by
the model spec point at what is morally good, and AIs will enact that.
This is a stronger claim since it assumes some variant of moral realism?

__Value change≠Corruption__: Humans already accept a lot of
modifications to their values, so it could be that most of the
modifications that will fine-ish. Similarly, it could be that
humans should be indifferent to most modifications to their values.

__Humans are already hardened against value corruption__: Humans are
exposed to tons of propaganda, persuasion attempts, advertising,
with people very much trying to change their values, yet this doesn't
happen very often, especially with untargeted attempts.

Although: It seems to me that humans mostly do form their opinions
based on their long-term interactions with other humans, though maybe
this mostly happens during a formative period in the teens and twenties.

Question: When do humans form their values, do they "lock in" after some point in their life?

### How Malleable Are Human Minds

Human preferences seem to be distributed around the brain ([Hayden & Niv
2021](https://pubmed.ncbi.nlm.nih.gov/34060875/ "The case against economic values in the orbitofrontal cortex (or anywhere else in the brain)"))
and built using learned representations ([(TurnTrout
2022)](https://www.lesswrong.com/s/nyEFg3AuJpdAozmoX/p/CQAMdzA4MZEhNRtTp)).

The human brain [has 8.7×10¹⁰
neurons](https://en.wikipedia.org/wiki/List_of_animals_by_number_of_neurons),
[10¹⁴ synapses](https://aiimpacts.org/scale-of-the-human-brain/),
encoding ~26 distinguishable states per synapse (which then ballparks the
information content at *very roughly* to 10TB-100TB), takes in ~10⁷
bits per second (10⁷ of those visual, 10⁶ of those proprioceptive,
10⁴ auditory, the rest via other modalities), of which only 10-60 bits
go through attention ([Zheng & Meister 2024](https://arxiv.org/pdf/2408.10234)).

One can use this to estimate a very rough lower bound on how quickly
human brains could be overwritten (ignoring consolidation and many other
factors): [8\*10¹³, 8\*10¹⁴] bits/(10⁸ bits/second)≈[10, 100]
days.  If the information is limited to what passes through attention
it'd take [~250k, 2.5M] years.

Relevant factual questions:

1. How much perceived information is consolidated how quickly?
	1. Claude 4.5 Sonnet tells me we don't have a great idea of how much of the perceived information is consolidated per second, and most research on this is on how memory is consolidated, not the amount.
2. Does most of the perceived information have to pass through attention to be consolidated, or is unconsciously perceived information consolidated as well? How much?
3. How much are different parts of brain "fire-walled" from having processed information be consolidated in them?
4. How uniformly throughout the brain are new patterns consolidated?

### How Might We Solve It

Ways to prevent these kinds of problems that arise when AIs interact
with malleable human minds:

1. [STEM AI](https://www.lesswrong.com/posts/fRsjBseRuvRhMPPE5/an-overview-of-11-proposals-for-building-safe-advanced-ai#6__STEM_AI) that doesn't know much about humans/doesn't interact much with humans, and instead focuses purely on solving engineering problems with clear specifications. This way we'd have useful AIs that still don't need to interact with malleable human minds, humans reap many benefits of advanced AI, and humans take their time to engage in moral epistemology/value formation/philosophy on their own.
	1. Downsides: Many useful applications such as therapy, geopolitics & international coordination, augmentation with impact on psychological traits, everyday personal advice requires some knowledge of psychology and interaction with humans, and AI companies are less likely to leave those on the table (given how much they are currently focused on consumers and very interaction-heavy applications).
	2. How much value would STEM AI leave on the table?
	3. See also the [Safeguarded AI](https://www.aria.org.uk/programme-safeguarded-ai/) program that also tries to address takeover risk.
2. Solve moral epistemology? As in, find the correct reasoning procedure to discover what humans (should) want in the limit of reflection, in a form that is not itself malleable.
	1. Downsides: Humans don't seem to have made enough progress in philosophy for a solution to moral epistemology, so this looks intractable.
	2. See also the [Automation of Philosophy and Wisdom](https://www.lesswrong.com/posts/52ygLry5KCdvxY6zn/essay-competition-on-the-automation-of-wisdom-and-philosophy) research agenda.
3. Empower a principal similar to newer conceptualizations of [corrigibility](https://niplav.site/doc/cs/ai/alignment/corrigibility/corrigibility_soares_et_al_2015.pdf) as I understand the newer research program by Max Harms to focus on. Focusing on such empowerment would at least prevent enfeeblement[^2] situations.
	1. Downsides: This may not prevent situations where empowering the principal modifies them and their values in ways that are not optimal (and plausibly not endorsed upon sufficient reflection by the unmodified principal).
4. More focus on human augmentation, especially around [cognitive](https://tsvibt.blogspot.com/2024/10/overview-of-strong-human-intelligence.html) and moral enhancement (if that is possible?).

[^2]: Term from “Human Compatible (Stuart Russell, 2019)”; describes situations in which humans have given up on influencing the future and let AIs take care of them.

### Related Research

* [AI Alignment with Changing and Influenceable Reward Functions (Micah Carroll/Davis Foote/Anand Siththaranjan/Stuart Russell/Anca Dragan, 2024)](https://arxiv.org/pdf/2405.17713?)
* [Cooperative Inverse Reinforcement Learning (Dylan Hadfield-Menell/Anca Dragan/Pieter Abbeel/Stuart Russell, 2016)](./doc/cs/ai/alignment/cirl/cooperative_inverse_reinforcement_learning_hadfield_menell_et_al_2016.pdf), somewhat.
* [Coherent Extrapolated Volition (Eliezer Yudkowsky, 2004)](https://niplav.site/doc/cs/ai/alignment/cev/coherent_extrapolated_volition_yudkowsky_2004.pdf)
