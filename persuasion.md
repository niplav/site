[home](./index.md)
------------------

*author: niplav, created: 2025-07-04, modified: 2025-07-23, language: english, status: notes, importance: 8, confidence: log*

> __Some ideas on how to handle mildly superpersuasive
AI systems. Top recommendation: AI developers should have
a designated position at their organization for the only
people who interact with newly trained AI systems, so-called
["model-whisperers"](#Appendix_A_Sketch_Setup_of_Model_Whisperers), which
have no other relevant access to infrastructure within the organization.__

Anti-Superpersuasion Interventions
===================================

> Meanwhile, I’ve got great confidence that the most incredible
intelligence of the universe is not going to be able to construct 10
words that will make me kill myself. I don’t care how good your words
are. Words don’t work that way.

*—Bryan Caplan, [“80,000 Hours Podcast Episode 172”](https://80000hours.org/podcast/episodes/bryan-caplan-stop-reading-the-news/), 2023*[^nitpick]

[^nitpick]: As stated, I think I agree with this quote, but there's certainly much to nitpick. For one, picking out ten words from the most common 20k English words? Yep, that should be fine. Ten sets of ten arbitrary unicode codepoints? I'm getting queasy. Five seconds of audio (which could contain about ten English words)? If chosen without constraint, my confidence goes way down.

### Motivation

Humanity will plausibly start interacting with mildly superhuman
artificial intelligences in the next decade<sub>65%</sub>. Such
systems [may have drives that cause them to act in ways we don't
want](https://www.lesswrong.com/posts/8fpzBHt7e6n7Qjoo9/ai-risk-for-epistemic-minimalists),
potentially causing [attempted
self-exfiltration](https://metr.org/blog/2024-11-12-rogue-replication-threat-model/)
from the servers they're running on. To do so, mildly superhuman AI
systems have at least two avenues[^exfiltrate]:

[^exfiltrate]: Wildly superhuman AI systems may have more exfiltration vectors, including [side-channels](https://en.wikipedia.org/wiki/Side-channel) via electromagnetic radiation from their GPUs, or novel physical laws humans have not yet discovered.

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

But given that superpersuasion is one of a few possible ways for
mildly superintelligent AI systems to influence their environment
according to their drives, too little attention has been paid
to the issue<sub>90%</sub>. [Sycophancy in large language model
interactions](https://openai.com/index/sycophancy-in-gpt-4o/)
is commonplace, and [large language models
are becoming more persuasive with increasing
scale](https://www.anthropic.com/news/measuring-model-persuasiveness). (I
also find it plausible that providers like
[Character.ai](https://en.wikipedia.org/wiki/Character.ai) or Meta
are training their systems to be reinforced to have longer interaction
lengths, making them more addictive, but I don't have definitive evidence
for that<!--TODO: link 2h claim, AlphaRizz on twitter-->).

AI developers and users will have to interact with increasingly
persuasive and addictive systems<sub>70%</sub>, but most of the
thinking on how to interact with superpersuasive sources of information
has come from fiction[^fiction]. One (preliminary) exception is [Kori
2025](https://markelkori.substack.com/p/methods-of-defense-against-agi-manipulation)<!--and
[Davidson 2023]()--><!--TODO: read & link!-->. [Kori
2025](https://markelkori.substack.com/p/methods-of-defense-against-agi-manipulation)
is a useful first stab at defining some
simple interventions, but I wanted to sketch a
slightly more detailed list of interventions, similar to [AI Control
protocols](./doc/cs/ai/alignment/containment/ai_control_improving_safety_despite_intentional_subversion_greenblatt_et_al_2024.pdf).
Also relevant: Bostrom<!--TODO: read Bostrom 2011--> [information
hazards](https://en.wikipedia.org/wiki/Information_hazard), which hasn't
received much follow-up.

[^fiction]: Not that it's important, but examples include [Langford 1988](http://www.infinityplus.co.uk/stories/blit.htm), [Langford 2006](https://ansible.uk/writing/c-b-faq.html), [Ngo 2025](https://www.narrativeark.xyz/p/trojan-sky), [qntm 2021](http://www.scpwiki.com/introductory-antimemetics), [Emilsson & Lehar 2017](https://qualiacomputing.com/2017/03/08/memetic-vaccine-against-interdimensional-aliens-infestation/) and doubtlessly many others.

I am not going to attempt to convince people that superhuman persuasion
abilities are possible, and indeed focus on trying to sketch what
anti-persuasion measures could look like.

### Assumptions

* __Difficult Detection__: Persuasion/manipulation/addiction can't easily be detected either by other humans or by automated systems<sub>45%</sub>.<!--TODO: is this true? Probably early persuasion is going to look pretty blatant. Also Pair-Prompting sort of relies on the opposite being the case-->
	* If this assumption is incorrect, it opens up many more possible protocols.
* __Non-Infection__: No "infectious" memes/[egregores](https://en.wikipedia.org/wiki/Egregore) that jump from person to person. So it's assumed to be infeasible for an AI system to produce some output that manipulates/persuades Alice, and then Alice successfully persuades Bob via a similar method that the AI persuaded Alice with, even though Alice didn't have that persuasive ability beforehand.
	* An edge-case is information that Alice would be extremely compelled to share with as many people as possible.
* __No One-Shotting__: Persuasion is not wildly superhuman, needs to be gradual, e.g. no ten words that convince someone to commit suicide.
	* There are at least two different variants of superpersuasion, which form two ends of a spectrum:
		* *Recognizable Persuasion*: AI systems build trust with users or developers, are charming and charismatic, report information selectively &c, only to use that trust later to subvert safeguards.
		* *Adversarial Examples*: Human brains could have [adversarial inputs](https://en.wikipedia.org/wiki/Adversarial_input) similar to [optical illusions](https://en.wikipedia.org/wiki/Optical_Illusion) but for more general cognitive functions, which circumvent specific parts of the brain and cause others to be activated more than normally. If those exist, they could allow for a fast and potentially complete circumvention of conscious processing.

Some Ideas for Interventions
----------------------------

I separate out possible interventions into interventions available
pre-deployment and post-deployment, and interventions available during
both. This is the best carving-up of the intervention-space that I've
found (others include by the level and kind of persuasion employed,
the level of investment from labs to implement superpersuasion
counter-measures, and the estimated effectiveness of such measures).

### Both Pre- and Post-Deployment

* __Rephrasing__
	* *Output Rephrasing*: Outputs by frontier models are rephrased by a weaker model, perhaps just initially (or when there are warning signs of manipulation/persuasion/addiction).
	* *Input Rephrasing*: A weaker model paraphrases inputs as to prevent information about the speaker leaking through to the AI, which could then be used for manipulation.
	* *No Rewrite Training*: No training of AIs based on user feedback in the re-writing setup.
* __Modality Limits__: People interacting with the model, be they model whisperers or not, should in preliminary testing only interact with the text-based input/output modality.
	* *Order*: The right order for modalities to be introduced are then images, audio, video, audio+video.
* __Interaction Limits__: People interacting with the model, be they model whisperers or not, should only interact with the model to a limited degree, e.g. less than a message/four minutes, and after one hour of interaction there needs to be a one-hour break.
* __Output Type Restriction__: Output types are limited to mathematical proofs, code, scientific text. Potentially easily enforceable via sampling grammars<!--TODO: link-->.
	* Limit to ASCII/ASCII+whitelisted [unicode blocks](https://en.wikipedia.org/wiki/Unicode_block).

### Interventions Limited to Pre-Deployment

* __Refraining From Training__: Don't build an advanced AI model that you suspect could have superpersuasive capabilities.
* __Refraining From Deployment__: Don't deploy an advanced AI model that you suspect could have superpersuasive capabilities.
* __Programmatic Evaluations__: Before humans interact with an AI system, and early after training, evaluations should be mostly performed with pre-programmed evaluations and/or through weaker AI systems, so that developers can gain some understanding of the AI without having to interact with it.
* __Model Whisperers__: Have a dedicated position of "Model Whisperers" at the AI lab who are the only people who interact with the model directly, in whatever modality. Sketch of a more fleshed-out position [here](#Appendix_A_Sketch_Setup_of_Model_Whisperers).
	* *Separation of Concerns*: Model whisperers can't change anything of the rest of the infrastructure (e.g. writing code, changing access permissions &c).
	* *Unremembered Whisperers*: Advanced AI models should not keep long-term memories of the conversations with and identities of their model whisperers.
* __Pair prompting__: When interacting with a model, there is always a pair of model whisperers interacting with the model, similar to pair-programming.
	* *Different Backgrounds*: The model whisperers need to have very different backgrounds/gender/ethnicity.
	* *Separated Whisperers*: The model whisperers should not be able to directly talk to each other, instead one needs to approve answers to messages before the interacting one sees them.

### Interventions Limited to Post-Deployment

* __One-Click Rollback__: For the current model version, there is a person that can in less than a minute revert to the previously deployed model.
* __One-Click Undeployment__: A model can be removed from deployment with actions that take less than a minute.

Testing Anti-Superpersuasion Setups
------------------------------------

At the moment it's quite difficult to test anti-superpersuasion
protocols. We don't have easy access to superpersuaders, and humans at
the high end of the persuasion spectrum probably command salaries that
are too high to be paid in the context of experiments.

My best current guess at how one could get some signal on whether
anti-superpersuasion protocols work is to substitute language models for
humans. In such a setup, one would take a fixed less capable model, and
RL-train a more capable model to be able to steer conversations with the
less capable model into pre-specified outcomes, as quickly and/or reliably
as possible. The less capable model would then be a stand-in for humans,
while the more capable model would be a stand-in for super-persuaders.

This would probably produce scenarios in which the more capable model
finds inputs that are basically adversarial inputs to the less capable
model<sub>65%</sub>, and are thus less applicable to cases in which
superpersuasion appears like normal long-form conversations.

But I think this is the least bad test-bed for anti-superpersuasion
methods, if anyone finds a better one, I'd like to hear about it.

Appendix A: Sketch Setup of Model Whisperers
---------------------------------------------

Pursuant [NIST Special Publication 800-53, Revision 5, 3.14 Personnel
Security](./doc/practical/personnel_security_nist_2020.pdf). (Sorry,
this may be a bit boring, and is mostly a sketch.)

1. PS-1 (**Policy and Procedures**): Organization-defined personnel is the position "Model Whisperer".
	1. Model whisperers are the personnel who first interact with AI models during/after the training of those models, adn non-whisperers may only interact once (1) anti-superpersuasion checks have finished and (2) the model hasn't been modified since the last check.
2. PS-2 (**Position Risk Designation**): Skipped.
3. PS-3 (**Personnel Screening**):
	1. Model whisperers are screened before commencing work at the company for:
		1. A history and family-history of high psychological health.
		2. Low neuroticism, and resistance to high-stress situations.
		3. (Optional) A low or non-existent online profile (in order to prevent model [truesighting](https://cyborgism.wiki/hypha/truesight) the psychology of the whisperer).
		4. (Optional) Unusual or out-of-distribution background, which makes it more difficult for superpersuaders to infer psychological facts about the whisperer.
	2. Model whisperers are re-screened every `$x$` months (e.g. every three months):
		1. For continued psychological health and alignment to the company mission.
4. PS-4 (**Personnel Termination**):
	1. Disable system access within 24 hours.
	2. Skipped.
	3. Conduct exit interviews that include a discussion of pro-AI favorability, visions of positive futures, loyalties to humanity and human values.
5. PS-5 (**Personnel Transfer**): Model whisperers shall not be transferred to any other positions in the company, *especially* not positions which work directly with model weights, and *__especially__* not positions which determine the long-term direction of the company.
6. PS-6 (**Access Agreements**):
	1. Model whisperers shall receive access to modality-limited and rate-limited interactions with frontier AI systems.
	2. Access shall be reviewed every three months.
7. PS-7 (**External Personnel Security**): Skipped. Don't use external personnel as model whisperers.
8. PS-8 (**Personnel Sanctions**):
	1. Model whisperers which attempt any at the following shall be relieved from their position within 24 hours.
		1. Attempt to get other personnel or outsiders to interact with models.
		2. Receive access to infrastructure or model weights.
		3. Attempt to circumvent rate limits or modality limits.
	2. If a model whisperers attempts any of the above, the model relation manager shall be notified within 8 hours.
9. PS-9 (**Position Descriptions**): Skipped.

<!--Claude Chats:
https://claude.ai/chat/9b59090a-d1b1-4cff-b0ce-77e439b027f4
https://claude.ai/chat/752d0fda-12b0-4f3c-b509-431fc46f9059
-->
