[home](./index.md)
------------------

*author: niplav, created: 2021-08-17, modified: 2021-12-23, language: english, status: in progress, importance: 6, confidence: possible*

> __I discuss arguments for and against the usefulness of brain-computer
interfaces in relation to AI alignment, and conclude that the path to
AI going well using brain-computer interfaces hasn't been explained in
sufficient detail.__

<!--
Original TODO:

* BCIs and AI Alignment

> Unfortunately, I don't know of a good write-up of the argument for why
BCIs wouldn't be *that* useful for AI alignment (maybe I should go and
try to write it out – so many things to write). Superintelligence
ch. 2 by Bostrom explains why it seems unlikely that we will create
superintelligence by BCIs, but doesn't explain why, even if they existed,
they would be unhelpful for alignment.

> Arguments against why BCIs might be use/helpful:

> *	There doesn't seem to be a clear notion of what it would mean for
	humans to merge with AI systems/no clear way of stating how having
	*	Humans [likely don't have fully specified coherent utility
		functions](https://nivlab.princeton.edu/publications/case-against-economic-values-brain),
		and there also doesn't seem to be an area in the brain
		that is the *value module* so that we could plug it into
		the AI system as a utility function
	*	Human augmentation with AI systems of [infrahuman
		capability](https://arbital.com/p/relative_ability/) might
		work, but might carry the risk of causing amounts of value
		drift large enough to count as human values being lost
	*	Human augmentation with [superhuman (or even
		par-human)](https://arbital.com/p/relative_ability/) AI
		systems seems pretty bad: if the AI system is unaligned to
		begin with, it probably doesn't help you if it has *direct
		access to your brain and therefore your nervous system*
	*	Using humans in AI systems as
		[approvers/disapprovers](https://www.lesswrong.com/posts/7Hr8t6xwuuxBTqADK/approval-directed-agents-1)
		works just as fine with screens & keyboards
*	To re-emphasise: It seems really really bad to have an unaligned
	AI system plugged into your brain, or to provide attack vectors
	for possible unaligned future AI systems

> Arguments for why BCIs might be useful:

> *	Humans would become effectively a bit more intelligent (though I'd
	guess that functional intelligence would be <2x what we have now)
*	Reaction times compared to AI systems would be sped up (maybe
	by around 10x – BCIs seem faster than typing on a keyboard,
	but not *that* much, since we're limited by processing speed
	(brain at 200 Hz, CPUs at 2000000000 Hz, and GPUs/TPUs with
	similar orders of magnitude), not reaction speed)
*	BCIs might help with human
	imitation/[WBEs](https://www.fhi.ox.ac.uk/brain-emulation-roadmap-report.pdf):
	the more information you have about the human brain, the easier
	it is to imitate/emulate it.
*	BCIs and human augmentation might lessen the pressure to create
	AGI due to high economic benefits, especially if coupled with
	[KANSI](https://arbital.com/p/KANSI/) infrahuman systems

> My intuition is that the pro-usefulness arguments are fairly weak (if
more numerous than the anti arguments), and that there is no really
clear case *for* BCIs in alignment, especially if you expect AI growth
to speed up (at least, I haven't run across it, if someone knows one,
I'd be interested in reading it). They mostly rely on a vague notion of
humans and AI systems merging, but under closer inspection, so far they
don't really seem to respond to the classical AI risk arguments/scenarios.

> My tentative belief is that direct alignment work is probably more useful.
-->

<!--
Suggestions comment 2 (https://old.reddit.com/r/ControlProblem/comments/pfb8ze/braincomputer_interfaces_and_ai_alignment/hb6gg89):

The obvious argument against BCI is that human brains aren't designed
to be extensible. Even if you have the hardware, writing software that
interfaces with the human brain to do X is harder than writing software
that does X on its own.

If you have something 100x smarter than a human, if there is a human
brain somewhere in that system, its only doing a small fraction of the
work. If you can make a safe substantially superhuman mind with BCI,
you can make the safe superhuman mind without BCI.

Alignment isn't a magic contagion that spreads into any AI system
wired into the human brain. If you wire humans to algorithms, and the
algorithm on its own is dumb, you can get a human with a calculator in
their head. Which is about as smart as a human with a calculator in their
hand. If the algorithm on the computer is itself smart, well if its smart
enough it can probably manipulate and brainwash humans with just a short
conversation, but the wires do make brainwashing easier. You end up with
a malevolent AI puppeting around a human body.
-->

<!--
Suggestions comment 3:

Agree with your point about such merging just being faster
interaction. The concept seems confused, merging wholesale to the
point where you just have a separate AI agent inside your head solves
nothing. But i'm guessing that isn't what people usually mean?

If we can substitute the AI's goal-oriented part with human reward
mechanisms, feelings, beliefs and goals, then that may solve the intent
alignment problem. I think it would be different to eg. human-in-the-loop
type alignment, where reward is trained on abstracted human
input. Instead, rather than just being closer interaction, the brain's
reward function IS the AI's reward function, in the same way that it's
the brain's reward function. In other words since we already have an
intelligent agent with goals, we simply need to upgrade its capabilities.

So the question is how far can we increase human intelligence by expanding
the brain's capabilities while leaving goal structures intact. What are
the other components of (super)intelligence?

Better algorithms: As far as we know the brain's algorithms are
already superior to what we can do artificially, since we're generally
intelligent. But maybe we can add on modules with different architectures
for specific types of processing (like maybe the way the brain works is
inefficient for eg. some kinds of math or thinking)

More compute:

Feels like this might be the real bottleneck. Imagine what you could do
with upgraded working memory, upgraded attention, upgraded processing
speed. When I try to imagine what it's like to be a superintelligence,
this is part of what I think of, alongside maybe better ways of thinking,
less reliance on language, etc. Like imagine being able to hold even 20
items in working memory with perfect attention.

It seems like any safe increases to the limits of intelligence could help
us substantially to solve alignment, but I don't think we have time if
there's only a decade or two left, considering we don't know how to do
this and might not figure it out without a lot of human experimentation.
-->

<!--
Resources from this comment:
https://www.lesswrong.com/posts/rpRsksjrBXEDJuHHy/brain-computer-interfaces-and-ai-alignment?commentId=t9n35ss9nhW2gJBg5
-->

Brain-Computer Interfaces and AI Alignment
===========================================

As a response to Elon Musk declaring that [NeuraLink's purpose is to
aid AI alignment](https://www.youtube.com/watch?v=ycPr5-27vSI&t=1447s),
[Muehlhauser
2021](https://lukemuehlhauser.com/musks-non-missing-mood "Musk's non-missing mood")
cites [Bostrom 2014 ch.
2](https://en.wikipedia.org/wiki/Superintelligence:_Paths,_Dangers,_Strategies)
for reasons why brain-computer interfaces seem unlikely to be helpful
with AI alignment. However, the chapter referenced concerns itself
with building superintelligent AI using brain-computer interfaces,
and not specifically about whether such systems would be aligned or
especially alignable.

Arguments against the usefulness for brain-computer interfaces
in AI alignment have been raised, but mostly in short form on
twitter (for example [here](https://twitter.com/robbensinger/status/1405878940149944332)).
This text attempts to collect arguments for and against brain-computer
interfaces from an AI alignment perspective.

Epistemic Status
-----------------

I am neither a neuroscientist nor an AI alignment researcher (although I
have read some blogposts about the latter), and I know very little about
brain-computer interfaces (from now on abbreviated as “BCIs”). I have
done a cursory internet search for a resource laying out the case for the
utility of BCIs in AI alignment, but haven't been able to find anything
that satisfies my standards (I have also asked on the [LessWrong open
thread](https://www.lesswrong.com/posts/QqnQJYYW6zhT62F6Z/?commentId=dMpstgZ3gQnGBbRhh)
and the AI alignment channel on the AI alignment channel on the Eleuther
AI discord server, and not received any answers that provide such a
resource (although I was told some useful arguments about the topic)).

I have tried to make the best case for and against BCIs, stating some tree
of arguments that I think many AI alignment researchers tacitly believe,
mostly taking as a starting point the Bostrom/Yudkowsky story of AI risk
(although it might be generalizable to a
[Christiano-like](https://www.lesswrong.com/posts/HBxe6wdjxK239zajf/what-failure-looks-like
"What failure looks like") story; I don't know enough about
[CAIS](https://www.lesswrong.com/posts/x3fNwSe5aWZb5yXEG "Reframing Superintelligence: Comprehensive AI Services as General Intelligence")
or ARCHES to make a judgment about the applicability of the arguments).
This means that AI systems will be assumed to be maximizers, as
[mathematical descriptions of other optimization idioms are currently
unsatisfactory](https://arbital.com/p/otherizer/ "Other-izing (wanted: new optimization idiom)").

Existing Texts
---------------

The most thorough argument for the usefulness of BCIs for AI alignment is
[Urban
2017](https://waitbutwhy.com/2017/04/neuralink.html "Neuralink and the Brain’s Magical Future")
(which I was pointed to by []() in [this comment](), thanks!).

The text mostly concerns itself with the current status of BCI technology,
different methods of reading and writing information from and to the
brain, and some of the implication on society if such a technology
were developed.

The section where the text explains the relation of BCIs to AI alignment
is as follows:

> That AI system, he believes, will become as present a character in your
mind as your monkey and your human characters—and it will feel like you
every bit as much as the others do. He says: I think that, conceivably,
there’s a way for there to be a tertiary layer that feels like it’s
part of you. It’s not some thing that you offload to, it’s you.

> This makes sense on paper. You do most of your “thinking” with your
cortex, but then when you get hungry, you don’t say, “My limbic
system is hungry,” you say, “I’m hungry.” Likewise, Elon thinks,
when you’re trying to figure out the solution to a problem and your AI
comes up with the answer, you won’t say, “My AI got it,” you’ll
say, “Aha! I got it.” When your limbic system wants to procrastinate
and your cortex wants to work, a situation I might be familiar with, it
doesn’t feel like you’re arguing with some external being, it feels
like a singular you is struggling to be disciplined. Likewise, when you
think up a strategy at work and your AI disagrees, that’ll be a genuine
disagreement and a debate will ensue—but it will feel like an internal
debate, not a debate between you and someone else that just happens to
take place in your thoughts. The debate will feel like thinking.

> It makes sense on paper.

> But when I first heard Elon talk about this concept, it didn’t really
feel right. No matter how hard I tried to get it, I kept framing the
idea as something familiar—like an AI system whose voice I could hear
in my head, or even one that I could think together with. But in those
instances, the AI still seemed like an external system I was communicating
with. It didn’t seem like me.

> But then, one night while working on the post, I was rereading some of
Elon’s quotes about this, and it suddenly clicked. The AI would be
me. Fully. I got it.

*– [Tim Urban](https://waitbutwhy.com/), “[Neuralink and the Brain’s Magical Future](https://waitbutwhy.com/2017/04/neuralink.html)”, 2017*

However, this paragraph is not wholly clear on how this merging with AI
systems is supposed to work.

It could be interpreted as describing [input of
cognition](./#Input-of-Cognition) from humans
into AI systems and vice versa, or simply non-AI [augmentation of human
cognition](./#Improving-Human-Cognition).

Assuming the interaction with an unaligned
AI system, these would enable [easier neural
takeover](./#Direct-Neural-Takeover-Made-Easy)
or at least induce the removal of humans
from the [centaur](https://en.wikipedia.org/wik/Advanced_chess) [due to convergent instrumental
strategies](./#Removing-Merged-Humans-is-a-Convergent-Instrumental-Strategy-for-AI-Systems)—well
known failure modes in cases where [merging is just faster
interaction](/#Merging-is-Just-Faster-Interaction)
between humans and AI systems.

The comparison with the limbic system is leaky, because the limbic system
is not best modeled as a more intelligent optimizer than the cortex with
different goals.

Aligning an already aligned AI system using BCIs is, of course, trivial.

Arguments For the Utility of Brain-Computer Interfaces in AI Alignment
-----------------------------------------------------------------------

### Improving Human Cognition

Just as writing or computers have improved the quality and speed of human
cognition, BCIs could do the same, on a similar (or larger) scale. These
advantages could arise out of several different advantages of BCIs over
traditional perception:

* Quick lookup of facts (e.g. querying Wikipedia while in a conversation)
*	Augmented long-term memory (with more reliable and resilient
	memory freeing up capacity for thought)
*	Augmented working memory (i.e. holding 11±2 instead of 7±2
	items in mind at the same time) (thanks to janus#0150 on the
	Eleuther AI discord server for this point)
*	Exchange of mental models between humans (instead of explaining
	a complicated model, one would be able to simply “send” the
	model to another person, saving a lot of time explaining)
*	Outsourcing simple cognitive tasks to external computers
* [Adding additional emulated cortical columns to human brains](https://www.lesswrong.com/posts/QqnQJYYW6zhT62F6Z/open-and-welcome-thread-august-2021?commentId=bkPAbLDDDhjR3wyYm)

It would be useful to try to estimate whether BCIs could make as much of
a difference to human cognition as language or writing or the internet,
and to perhaps even quantify the advantage in intelligence and speed
given by BCIs.

<!--TODO: how much more intelligent? How much faster?-->

#### Scaling far Beyond Human Intelligence

If BCIs could allow to scale the intelligence of biological humans
far beyond normal human intelligence, this might either

*	enable a [pivotal act](https://arbital.com/p/pivotal/), in which
	looming catastrophes are avoided
*	make artificially superintelligent systems unneccessary because
	of sufficiently intelligent biological humans (this might be
	caused by BCIS enabling sufficient access to the human brain that
	self-modification with resulting recursive self-improvement is
	enacted by a human)

### Understanding the Human Brain

Neuroscience seems to be blocked by not having good access to human brains
while they are alive, and would benefit from shorter feedback loops and
better data. A better understanding of the human brain might be quite
useful in e.g. finding the location of human values in the brain (even
though it seems like there might not be one such location [Hayden & Niv
2021](https://nivlab.princeton.edu/publications/case-against-economic-values-brain "The case against economic values in the orbitofrontal cortex (or anywhere else in the brain)")).
Similarly, a better understanding of the human brain might aid in better
understanding and interpreting neural networks.

#### Path Towards Whole-Brain Emulation or Human Imitation

Whole-brain emulation (henceforth WBE) (with the emulations being
faster or cheaper to run than physical humans) would likely be useful
for AI alignment if used differentially for alignment over capabilities
research – human WBEs would to a large part share human values, and
could subjectively slow down timelines while searching for AI alignment
solutions. Fast progress in BCIs could make WBEs more likely before an AI
[point of no
return](https://www.lesswrong.com/posts/JPan54R525D68NoEt/the-date-of-ai-takeover-is-not-the-day-the-ai-takes-over "The date of AI Takeover is not the day the AI takes over")
by improving the understanding of the human brain.

A similar but weaker argument would apply to
[AI systems that imitate human behavior](https://www.alignmentforum.org/posts/LTFaD96D9kWuTibWr/just-imitate-humans "Just Imitate Humans?").

### “Merging” AI Systems With Humans

A notion often brought forward in the context of BCIs and AI alignment
is the one of “merging” humans and AI systems<!--TODO: [citation
neeeded]-->.

Unfortunately, a clearer explanation of how exactly this would work or
help with making AI go well is usually not provided (at least I haven't
managed to find any clear explanation). There are different possible
ways of conceiving of humans “merging” with AI systems: using human
values/cognition/policies as partial input to the AI system.

#### Input of Values

The most straightforward method of merging AI systems and humans could be
to use humans outfitted with BCIs as part of the reward function of an AI
system. In this case, a human would be presented with a set of outcomes
by an AI system, and would then signal how desirable that outcome would
be from the human's perspective. The AI would then search for ways to
reach the states rated highest by the human with the largest probability.

If one were able to find parts of the human brain that hold the human
utility function, one could use these directly as parts of the AI systems.
However, it seems unlikely that the human brain has a clear notion of
terminal values distinct from instrumental values and policies<!--TODO:
link the case against economic values in the brain--> in a form that
could be used by an AI system.

##### Easier Approval-Directed AI Systems

Additionally, a human connected to an AI system via a BCI would
have an easier time evaluating the cognition of [approval-directed
agents](https://www.lesswrong.com/s/EmDuGeRw749sD3GKd/p/7Hr8t6xwuuxBTqADK
"Approval-directed agents"), since they might be able to follow he
cognition of the AI system in real-time, and spot undesirable thought
processes (like e.g. attempts at [cognitive
steganography](https://arbital.com/p/cognitive_steganography/ "Cognitive steganography")).

#### Input of Cognition

Related to the aspect of augmenting humans using BCIs by outsourcing parts
of cognition to computers, the inverse is also possible: identifying
modules of AI systems that are most likely to be misaligned to humans
or produce such misalignment, and replacing them with human cognition.

For example the part of the AI system that formulates long-term
plans could be most likely to be engaged in formulating
misaligned plans, and the AI system could be made more
[myopic](https://www.alignmentforum.org/tag/myopia) by replacing the
long-term planning modules with BCI-augmented humans, while short-term
planning would be left to AI systems.

Alternatively, if humanity decides it wants to prevent AI systems from
forming [human
models](https://www.lesswrong.com/posts/BKjJJH2cRpJcAnP7T "Thoughts on Human Models"),
modeling humans & societies could be outsourced to actual humans, whose
human models would be used by the AI systems.

#### Input of Policies

As a matter of completeness, one might hypothesize about an AI
agent that is coupled with a human, where the human can overwrite
the policy of the agent (or, alternatively, the agent samples
policies from some part of the human brain directly). In this case,
however, when not augmented with other methods of “merging”
humans and AI systems, the agent has a strong [instrumental
pressure](https://arbital.com/p/instrumental_convergence/ "Instrumental Convergence")
to remove the ability of the human to change its policy at a whim.

### Aid to Interpretability Work

By increasing the speed of interaction and augmenting human intelligence,
BCIs might aid the quest of improving the interpretability of AI systems.

### Side-note: A Spectrum from Humans to Human Imitations

There seems to be a spectrum from biological humans to human imitations,
roughly along the axes of integration with digital systems/speed:
Biological humans – humans with BCIs – whole-brain emulations –
human imitations. This spectrum also partially tracks how aligned
these human-like systems can be expected to act: a human imitation
off-distribution seems much less trustworthy than a whole-brain emulation
of a human acting off distribution.

Arguments Against the Utility of Brain-Computer Interfaces in AI Alignment
---------------------------------------------------------------------------

> And so we boldly go—into the whirling knives.

*–[Nick Bostrom](https://en.wikipedia.org/wiki/Nick_Bostrom), “Superintelligence: Paths, Dangers, Strategies” p. 143, 2014*

### Direct Neural Takeover Made Easy

A common observation about AI alignment is that initially AI systems
would be confined to computers, hopefully only with indirect contact
to the outside world (i.e. no access to roboters, nanotechnology
or factories). While there are some responses to these arguments
(see i.e. [Yudkowsky 2016a](https://arbital.com/p/user_manipulation/ "User manipulation"),
[Yudkowsky 2016b](https://arbital.com/p/30b/ "User maximization"),
[Bostrom 2014 pp. 117-122]("Superintelligence: Paths, Dangers, Strategies")<!--TODO: link to
Superintelligence-->), the proposal of connecting humans to potentially
unaligned AI systems offers these counterarguments more weight.

Given direct write-access to the nervous system of a human, an AI system
would be more likely to be able to hijack the human and use them to
instantiate more instances of itself in the world (especially on computers
with more computing power or access to manufacturing capabilities). Even
if the access to the human brain is severely restricted to few bits
and very specific brain regions (therewhile making the connection less
useful in the first place), the human brain is not modular, and as far
as I understand not designed to withstand adversarial interaction on the
neural level (as opposed to attacks through speech or text, which humans
are arguably more optimized against through constant interaction with
other humans who tried to manipulate them in the ancestral environment).

However, if the AI were restricted to read-only access to the human brain,
this particular scenario would be of no concern (except for AI systems
gaining information about human psychology more quickly).

<!--TODO: use yudkowsky screaming image here?-->

### Opportunity Cost

If work on BCIs is net-positive in expectation for making AI go well,
it might be the case that other approaches are more promising, and that
focusing on BCIS might leave those approaches underdeveloped.

For example, one can posit [neural network
interpretability](https://www.lesswrong.com/posts/X2i9dQQK3gETCyqh2 "Chris Olah’s views on AGI safety")
as the [GiveDirectly](https://www.givedirectly.org/) of AI alignment:
reasonably tractable, likely helpful in a large class of scenarios, with
basically unlimited scaling and only slowly diminishing returns. And
just as any new EA cause area must pass the first test of being more
promising than GiveDirectly, so every alignment approach could be viewed
as a competitor to interpretability work. Arguably, work on BCIs does
not cross that threshold.

### “Merging” is Just Faster Interaction

Most proposals of “merging” AI systems and humans using BCIs
are proposals of speeding up the interaction betwen humans and
computers (and possibly increasing the amount of information that
humans can process): A human typing at a keyboard can likely
perform all operations on the computer that a human connected
to the computer via a BCI can, such as giving feedback in a [CIRL
game](doc/bcis_and_alignment/cooperative_inverse_reinforcement_learning_hadfield_mendell_et_al_2016.pdf "Cooperative Inverse Reinforcement Learning"),
interpreting a neural network, analysing the policy of a reinforcement
learner etc. As such, BCIs offer no qualitatively new strategies for
aligning AI systems.

While this is not negative (after all, quantity (of interaction) can have
a quality of its own), if we do not have a type of interaction that makes
AI systems aligned in the first place, faster interaction will not make
our AI systems much safer. BCIs seem to offer an advantage by a constant
factor: If BCIs give humans a 2x advantage when supervising AI systems
(by making humans 2x faster/smarter), then if an AI system becomes
2x bigger/faster/more intelligent, the advantage is nullified. Even
though he feasibility of rapid capability gains is a matter of debate,
an advantage by only a constant factor does not seem very reassuring.

Additionally, supervision of AI systems through fast interaction should
be additional to a genuine solution to the AI alignment problem: Ideally
[niceness is the first line of
defense](https://arbital.com/p/niceness_defense/ "Niceness is the first line of defense")
and [the AI would tolerate our safety
measures](https://arbital.com/p/nonadversarial_safety/ "The AI must tolerate your safety measures"),
but most arguments for BCIs being useful already assume that the AI
system is not aligned.

<!--TODO: think about serial vs. parallel in AI systems and humans
with BCIs, think about frequency (200 Hz for human brain, >2 GHz for
computers-->

### Problems Arise with Superhuman Systems

When combining humans with BCIs and
[superhuman](https://arbital.com/p/relative_ability/ "Infrahuman, par-human, superhuman, efficient, optimal")
AI systems, several issues might arise that were no problem with
infrahuman systems.

When infrahuman AI systems are “merged” with humans in a way
that is nontrivially different from the humans using the AI system,
the performance bottleneck is likely going to be the AI part of the
tandem. However, once the AI system passes the human capability threshold
in most domains necessary for the task at hand, the bottleneck is going
to be the humans in the system. While such a tandem is likely not going
to be strictly only as capable as the humans alone (partially because the
augmentation by BCI makes the human more intelligent), such systems might
not be competitive against AI-only systems that don't have a human part,
and could be outcompeted by AI-only approaches.

These bottlenecks might arise due to different speeds of cognition
and increasingly alien abstractions by the AI systems that need to be
translated into human concepts.

### “Merging” AI Systems with Humans is Underspecified

To my knowledge, there is no publicly written up explanation of what it
would mean for humans to “merge” with AI systems. I explore some of
the possibilities in [this section](#Merging-AI-Systems-With-Humans),
but these mostly boil down faster interaction.

It seems worrying that a complete company has been built on a vision
that has no clearly articulated path to success.

#### Removing Merged Humans is a Convergent Instrumental Strategy for AI Systems

If a human being is merged with an unaligned AI system,
the unaligned AI system has a [convergent instrumental
drive](https://arbital.com/p/convergent_self_modification/ "Convergent strategies of self-modification")
to remove the (to it) unaligned human: If the human can interfere with
the AI systems' actions or goals or policies, the AI system will not be
able to fully maximize its utility. Therefore, for merging to be helpful
with AI alignment, the AI system must already be aligned, or [not a
maximizer](https://arbital.com/p/otherizer/ "Other-izing (wanted: new optimization idiom)"),
the exact formulation of which is currently an open problem.

### BCIs Speed Up Capabilities Research as Well

If humanity builds BCIs, it seems not certain that the AI alignment
community is going to be especially privileged over the AI capabilities
community with regards to access to these devices. Unless BCIs increase
human wisdom as well as intelligence, widespread BCIs that only enhance
human intelligence would be net-zero in expectation.

On the other hand, if an alignment-interested company like NeuraLink
acquires a strong lead in BCI technology and provides it exclusively to
alignment-oriented organisations, it appears possible that BCIs will
be a [pivotal tool](https://arbital.com/p/pivotal/ "Pivotal event")
for helping to secure the development of AI.

#### How Important Is Wisdom?

If the development of unaligned AI systems currently poses an
existential risk, then AI capabilities researchers, most of which are
very intelligent and technically capable, are currently engaging in an
activity that is on reflection not desirable. One might call this lacking
property of reflection “wisdom”, similar to the usage in [Tomasik
2017](./doc/thoughts_on_open_borders/differential_intellectual_progress_as_a_positive_sum_project_tomasik_2017.pdf "Differential Intellectual Progress as a Positive-Sum Project").

It is possible that such a property of human minds, distinct from
intelligence, does not really exist, and it is merely by chance and
exposure to AI risk arguments that people become aware and convinced
these arguments (also dependent, of course, on the convincingness of
these arguments). If that is the case, then intelligence-augmenting BCIs
would help to aid AI alignment, by giving people the ability to survey
larger amounts of information and engage more quickly with the arguments.

### Superintelligent Human Brains Seem Dangerous (Although Less So)

Increasing the intelligence of a small group of humans
appears to be the most likely outcome if one were to aim
for endowing some humans with superintelligence. [Bostrom 2014
ch.2](https://en.wikipedia.org/wiki/Superintelligence:_Paths,_Dangers,_Strategies)
outlines some reasons why this procedure is unlikely to
work, but even the case of success still carries dangers with
it: the augmented humans might not be sufficiently [metaphilosophically
competent](https://www.lesswrong.com/posts/CCgvJHpbvc7Lm8ZS8/metaphilosophical-competence-can-t-be-disentangled-from "Metaphilosophical competence can't be disentangled from alignment")
to deal with much greater insight the
structure of reality (e.g. by being unable to cope with [ontological
crises](./doc/bcis_and_alignment/ontological_crises_in_artificial_agents_value_systems_de_blanc_2011.pdf "Ontological Crises in Artificial Agents' Value Systems")
(which appear not infrequently in normal humans), or becoming "drunk
with power" and therefore malevolent).

Subjective Conclusion
----------------------

Before collecting these arguments and thinking about the topic, I was
quite skeptical that BCIs would be useful in helping align AI systems: I
believed that while researching BCIs would be in expectation net-positive,
there are similarly tractable approaches to AI alignment with a much
higher expected value (for example work on interpretability).

I still basically hold that belief, but have shifted my expected value of
researching BCIs for AI alignment upwards somewhat (if pressed, I would
give an answer of a factor of 1.5, but I haven't thought about that number
very much). The central argument that prevents me from taking BCIs as an
approach to AI alignment seriously is the argument that BCIs per se offer
only a constant interaction speedup between AI systems and humans, but no
clear qualitative change in the way humans interact with AI systems, and
create no differential speedup between alignment and capabilities work.

The fact that that there is no writeup of a possible path to AI going well
that is focused on BCIs worries me, given that a whole company has been
founded based on that vision. An explanation of a path to success would be
helpful in furthering the discussion and perhaps moving work to promising
approaches to AI alignment (be it towards or away from focusing on BCIs).
