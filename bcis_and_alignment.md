[home](./index.md)
------------------

*author: niplav, created: 2021-08-17, modified: 2021-08-21, language: english, status: notes, importance: 6, confidence: possible*

> __.__

Brain-Computer Interfaces and AI Alignment
===========================================

Epistemic Status
-----------------

I am neither a neuroscientist nor an AI alignment researcher (although I
have read some blogposts about the latter), and I know very little about
brain-computer interfaces (from now on abbreviated as “BCIs”). I have
done a cursory internet search for a resource laying out the case for the
utility of BCIs in AI alignment, but haven't been able to find anything
that satisfies my standards (I have also asked on the LessWrong open
thread and the AI alignment channel on the Eleuther AI discord channel,
and not gotten any answers that provide such a resource (although I was
told some useful arguments)).

I have tried to make the best case for and against BCIs,
stating some tree of arguments that I think many AI alignment
researchers tacitly believe, mostly taking the Bostrom/Yudkowsky
story of AI risk (although it might be generalizable to a
[Christiano-like](https://www.lesswrong.com/posts/HBxe6wdjxK239zajf/what-failure-looks-like
"What failure looks like") story; I don't know enough about CAIS or
ARCHES to make a judgment about the applicability of the arguments).

Arguments For the Utility of Brain-Computer Interfaces in AI Alignment
-----------------------------------------------------------------------

### Improving Human Cognition

Just as writing or computers have improved the quality and speed of
human cognition, BCIs could improve the quality and the speed of human
thinking. These advantages could arise out of several different advantages
of BCIs over traditional perception:

* Quick lookup of facts (e.g. querying Wikipedia while in a conversation)
* Augmented long-term memory (with more reliable and resilient memory freeing up capacity for thought)
* Augmented working memory (i.e. holding 11±2 instead of 7±2 items in mind at the same time) (thanks to janus#0150 for this point)
* Exchange of mental models (instead of explaining a complicated model, one would be able to simply “send” the model to another person, saving a lot of time explaining)
* Outsourcing simple cognitive tasks to external computers

<!--TODO: how much more intelligent? How much faster?-->

### Understanding the Human Brain

Neuroscience seems to be blocked by not having good access to human
brains while they are alive, and would benefit from shorter feedback
loops and better data. A better understanding of the human brain might
be quite useful in e.g. finding the location of human values in the brain
(even though it seems like there is no one such location <!--TODO: link to
the downloaded paper-->). Similarly, a better understanding of the human
brain might aid in better understanding and interpreting neural networks.

#### Path Towards Whole-Brain Emulation or Human Imitation

Whole-brain emulation (henceforth WBE) (with the emulations being faster
or cheaper to run than physical humans) would likely be useful for AI
alignment if used differentially for alignment over capabilities – human
WBEs would to a large part share human values, and could subjectively
slow down timelines while searching for AI alignment solutions. Fast
progress in BCIs could make WBEs more likely before an AI [point of no
return](https://www.lesswrong.com/posts/JPan54R525D68NoEt/the-date-of-ai-takeover-is-not-the-day-the-ai-takes-over "The date of AI Takeover is not the day the AI takes over")
by improving the understanding of the human brain.

A similar but weaker argument would apply to
[Ai systems that imitate human behavior](https://www.alignmentforum.org/posts/LTFaD96D9kWuTibWr/just-imitate-humans "Just Imitate Humans?").

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
"Approval-directed agents"), since they might be able
to follow he cognition of the AI system in real-time,
and spot undesirable thought processes (akin to [cognitive
steganography](https://arbital.com/p/cognitive_steganography/ "Cognitive steganography")).

#### Input of Cognition

Related to the aspect of augmenting humans using BCIs by outsourcing
parts of cognition, the inverse is also possible: identifying modules
of AI systems that are most likely to be misaligned to humans or produce
such misalignment, and replacing them with human cognition.

For example the part of the AI system that formulates long-term plans
could be most likely to be engaged in formulating misaligned plans,
and the AI system could be made more myopic by replacing the long-term
planning modules by humans, while short-term planning would be left to
AI systems.

Alternatively, if humanity decides it wants to prevent AI systems from
forming [human models](https://www.lesswrong.com/posts/BKjJJH2cRpJcAnP7T),
modeling humans & societies could be outsourced to actual humans, whose
human models would be used by the AI systems.

#### Input of Policies

### Side-note: A Spectrum from Humans to Human Imitations

There seems to be a spectrum from biological humans to human imitations,
roughly along the axes of integration with digital systems/speed/:
Biological humans – humans with BCIs – whole-brain emulations –
human imitations. This spectrum also partially tracks how aligned
these human-like systems can be expected to act: a human imitation
off-distribution seems much less trustworthy than a whole-brain emulation
of a human.

Arguments Against the Utility of Brain-Computer Interfaces in AI Alignment
---------------------------------------------------------------------------

### Possibly Unaligned Systems Have Direct Access to Human Brains

### Opportunity Cost

If work on BCIs is net-positive in expectation for making AI go well,
it might be the case that other approaches are more promising, and that
focusing on BCIS might leave those approaches underdeveloped.

For example, one can posit neural network interpretability as the
[GiveDirectly](https://www.givedirectly.org/) of AI alignment: reasonably
tractable, likely helpful in a large class of scenarios, with basically
unlimited scaling and only slowly diminishing returns. And just as any
new EA cause area must pass the first test of being more promising than
GiveDirectly, so every alignment approach could be viewed as a competitor
to interpretability work.

### “Merging” is Just Faster Interaction

### Problems Arise with Superhuman Systems

#### Performance Problems

#### Transparency Problems

### Speed Differences are Problematic

### Successful Alignment via BCIs Depends on Knowing Details

Subjective Conclusion
----------------------
