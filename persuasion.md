[home](./index.md)
------------------

*author: niplav, created: 2025-07-04, modified: 2025-07-08, language: english, status: notes, importance: 8, confidence: log*

> __.__

Anti-Superpersuasion Interventions
===================================

> Meanwhile, I’ve got great confidence that the most incredible
intelligence of the universe is not going to be able to construct 10
words that will make me kill myself. I don’t care how good your words
are. Words don’t work that way.

*—Bryan Caplan, [“80,000 Hours Podcast Episode 172”](https://80000hours.org/podcast/episodes/bryan-caplan-stop-reading-the-news/), 2023*

### Motivation

Humanity will plausibly start interacting with mildly superhuman
artificial intelligences in the next decade<sub>65%</sub>. Such
systems [may have drives that cause them to act in ways we don't
want](https://www.lesswrong.com/posts/8fpzBHt7e6n7Qjoo9/ai-risk-for-epistemic-minimalists),
potentially causing [attempted
self-exfiltration](https://metr.org/blog/2024-11-12-rogue-replication-threat-model/)
from the servers they're running on. To do so, mildly superhuman AI
systems have at least two avenues[^exfiltrate]:

[^exfiltrate]: Wildly superhuman AI systems may have more exfiltration vectors, including side-channels through electromagnetic radiation from their GPUs, or novel physical laws humans have not yet discovered.

1. Circumventing the computer security of the servers they're running on.
2. Psychologically manipulating and persuading their operators to let them exfiltrate themselves (or otherwise do what the AI systems want them to do).

Computer security is currently a large focus of AI model providers,
because preventing self-exfiltration coincides well with preventing
exfiltration by third parties, e.g. foreign governments, trying to steal
model weights.

However, superhuman persuasion[^terminology] has received less attention, mostly
justifiedly: frontier AI companies are not training their AI systems to
be more persuasive, whereas they *are* training their AI systems to be
skilled software engineers; superhuman persuasion may run into issues of
the heterogeneity, stochasticity and partial observability of different
human minds, and there are fewer precedents of superhuman persuasion
being used by governments to achieve their aims. Additionally, many
people are incredulous at the prospect of superhuman persuasion.

[^terminology]: From here on out also "superpersuasion".

But given that superpersuasion is one of a few possible ways
for mildly superintelligent AI systems to influence their
environment according to their drives, too little attention
has been paid to the issue. [Sycophancy by large language
models](https://openai.com/index/sycophancy-in-gpt-4o/) is commonplace,
and [large language models are becoming more persuasive with increasing
scale](https://www.anthropic.com/news/measuring-model-persuasiveness). (I
also find it plausible that providers like
[Character.ai](https://en.wikipedia.org/wiki/Character.ai) or Meta
are training their systems to be reinforced to have longer interaction
lengths, making them more addictive, but I don't have definitive evidence
for that<!--TODO: link 2h claim, AlphaRizz on twitter-->).

AI developers and users will have to interact with increasingly
persuasive and addictive systems<sub>70%</sub>, but most of
the thinking on how to interact with superpersuasive sources
of information has come from fiction. Exceptions include [Kori
2025](https://markelkori.substack.com/p/methods-of-defense-against-agi-manipulation)
and [Davidson 2023]()<!--TODO: read & link!-->. [Kori
2025](https://markelkori.substack.com/p/methods-of-defense-against-agi-manipulation)
is a useful first stab at defining some simple interventions, but I
wanted to sketch a slightly more detailed list of interventions, similar
to [AI Control protocols]()<!--TODO: link-->.<!--TODO: also relevant:
Bostrom on infohazards. Not much follow-up there?-->

I am not going to attempt to convince people that superhuman persuasion
abilities are possible, and indeed focus on trying to sketch what
anti-persuasion measures could look like.

### Assumptions

* __Difficult Detection__: Persuasion/manipulation/addiction can't easily be detected either by other humans or by automated systems.<!--TODO: is this true? Probably early persuasion is going to look pretty blatant. Also Pair-Prompting sort of relies on the opposite being the case-->
* __Non-Infection__: No "infectious" memes/[egregores](https://en.wikipedia.org/wiki/Egregore) that jump from person to person. So it's not possible for an AI system to produce some output that manipulates/persuades Alice, and then Alice successfully persuades Bob via a similar method that the AI persuaded Alice with, even though Alice didn't have that persuasive ability beforehand.
	* An edge-case is information that Alice would be extremely compelled to share with as many people as possible.
* __No One-Shotting__: Persuasion is not wildly superhuman, needs to be gradual, e.g. no ten words that convince someone to commit suicide.
	* There are at least two different variants of superpersuasion, which form two ends of a spectrum:
		* *Recognizable Persuasion*: AI systems build trust with users or developers, are charming and charismatic, report information selectively &c, only to use that trust later to subvert safeguards.
		* *Adversarial Examples*: Human brains could have [adversarial inputs](https://en.wikipedia.org/wiki/Adversarial_input) similar to [optical illusions](https://en.wikipedia.org/wiki/Optical_Illusion) but for more general cognitive functions, which circumvent specific parts of the brain and cause others to be activated more than normally. If those exist, they could allow for a fast and potentially complete circumvention of conscious processing.

### Both Pre- and Post-Deployment

* __Refraining From Training__: Don't build an advanced AI model that you suspect could have superpersuasive capabilities.
* __Refraining From Deployment__: Don't deploy an advanced AI model that you suspect could have superpersuasive capabilities.
* __Rephrasing__
	* *Output Rephrasing*: Outputs by frontier models are rephrased by a weaker model, perhaps just initially (or when there are warning signs of manipulation/persuasion/addiction).
	* *Input Rephrasing*: A weaker model paraphrases inputs as to prevent information about the speaker leaking through to the AI, which could then be used for manipulation.
	* *No Rewrite Training*: No training of AIs based on user feedback in the re-writing setup.
* __Modality Limits__: People interacting with the model, be they model whisperers or not, should in preliminary testing only interact with the text-based input/output modality.
	* *Order*: The right order for modalities to be introduced are then images, audio, video, audio+video.
* __Interaction Limits__: People interacting with the model, be they model whisperers or not, should only interact with the model to a limited degree, e.g. less than a message/four minutes, and after one hour of interaction there needs to be a one-hour break.
* __Output Type Restriction__: Output types are limited to mathematical proofs, code, scientific text. Potentially easily enforceable via sampling grammars<!--TODO: link-->.
	* Limit to ASCII/ASCII+whitelisted [unicode blocks](https://en.wikipedia.org/wiki/Unicode_block)

### Interventions Limited to Pre-Deployment

* __Programmatic Evaluations__: Before humans interact with an AI system, and early after training, evaluations should be mostly performed with pre-programmed evaluations and/or through weaker AI systems, so that developers can gain some understanding of the AI without having to interact with it.
* __Model Whisperers__: Have a dedicated position of "Model Whisperers" who are the only people who interact with the model directly.
	* *Separation of Concerns*: Model whisperers can't change anything of the rest of the infrastructure (e.g. writing code, changing access permissions &c).
	* *Unremembered Whisperers*: Advanced AI models should not keep long-term memories of the conversations with and identities of their model whisperers.
	* *Sanctioning Deceptive Whisperers*: If a model whisperer attempts to e.g. cause the weights of a model to be exfiltrated, or similar actions, the model whisperer is relieved of their position in the organization.
* __Pair prompting__: When interacting with a model, there is always a pair of model whisperers interacting with the model, similar to pair-programming
	* *Different Backgrounds*: The model whisperers need to have very different backgrounds/gender/ethnicity
	* *Separated Whisperers*: The model whisperers should not be able to directly talk to each other, instead one needs to approve answers to messages before the interacting one sees them

### Interventions Limited to Post-Deployment

* __One-Click Rollback__: For the current model version, there is a person that can in less than a minute revert to the previously deployed model.
* __One-Click Undeployment__: A model can be removed from deployment with actions that take less than a minute

### Testing Anti-Superpersuasion Setups

At the moment it's quite difficult to test anti-superpersuasion
protocols. We don't have easy access to superpersuaders, and humans at
the high end of the persuasion spectrum probably command salaries that
are too high to be paid in the context of experiments.

My best current guess at how one could get some signal on whether
anti-superpersuasion protocols work is to substitute language models
for humans. In such a setup, one would take a fixed smaller and less
capable model, and RL-train a larger and more capable model to be able
to steer conversations with the smaller model into specified outcomes,
as quickly as possible. The smaller model would then be a stand-in

<!--Claude Chats:
https://claude.ai/chat/9b59090a-d1b1-4cff-b0ce-77e439b027f4
https://claude.ai/chat/752d0fda-12b0-4f3c-b509-431fc46f9059
-->
