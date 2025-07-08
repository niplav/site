[home](./index.md)
------------------

*author: niplav, created: 2025-07-04, modified: 2025-07-07, language: english, status: notes, importance: 8, confidence: log*

> __.__

Anti-Superpersuasion Interventions
===================================

> Meanwhile, I’ve got great confidence that the most incredible
intelligence of the universe is not going to be able to construct 10
words that will make me kill myself. I don’t care how good your words
are. Words don’t work that way.

*—Bryan Caplan, [“80,000 Hours Podcast Episode 172”](https://80000hours.org/podcast/episodes/bryan-caplan-stop-reading-the-news/), 2023*

### Motivation

### Assumptions

* __Difficult Detection__: Persuasion/manipulation/addiction can't easily be detected.
* No "infectious" memes/egregores that jump from person to person
* __No One-Shotting__: Persuasion is not wildly superhuman, needs to be gradual, e.g. no ten words that convince someone to commit suicide.

### Both Pre- and Post-Deployment

* __Refraining From Training__: Don't build an advanced AI model that you suspect could have superhuman persuasive capabilities.
* __Rephrasing__
	* *Output Rephrasing*: Outputs by frontier models are rephrased by a weaker model, perhaps just initially (or when there are warning signs of manipulation/persuasion/addiction).
	* *Input Rephrasing*: A weaker model paraphrases inputs as to prevent information about the speaker leaking through to the AI, which could then be used for manipulation.
	* *No Rewrite Training*: No training of AIs based on user feedback in the re-writing setup.
* __Modality Limits__: People interacting with the model, be they model whisperers or not, should in preliminary testing only interact with the text-based input/output modality.
	* *Order*: The right order for modalities to be introduced are then images, audio, video, audio+video.
* __Interaction Limits__: People interacting with the model, be they model whisperers or not, should only interact with model to a limited degree, e.g. less than a message/four minutes, and after one hour of interaction there needs to be a one-hour break.
* __Output Type Restriction__: Output types are limited to mathematical proofs, code, scientific text. Potentially easily enforceable via sampling grammars<!--TODO: link-->.
	* Limit to ASCII/ASCII+whitelisted [unicode blocks](https://en.wikipedia.org/wiki/Unicode_block)

### Interventions limited to pre-deployment

* __Model Whisperers__: Have a dedicated position of "Model Whisperers" who are the only people who interact with the model directly.
	* *Separation of Concerns*: Model whisperers can't change anything of the rest of the infrastructure (e.g. writing code, changing access permissions &c).
	* *Unremembered Whisperers*: Advanced AI models should not keep long-term memories of the conversations with and identities of their model whisperers.
	* *Sanctioning Deceptive Whisperers*: If a model whisperer attempts to e.g. cause the weights of a model to be exfiltrated, or similar actions, the model whisperer is relieved of their position in the organization.
* __Pair prompting__: When interacting with a model, there is always a pair of model whisperers interacting with the model, similar to pair-programming
	* *Different Backgrounds*: The model whisperers need to have very different backgrounds/gender/ethnicity
	* *Separated Whisperers*: The model whisperers should not be able to directly talk to each other, instead one needs to approve answers to messages before the interacting one sees them

### Interventions limited to post-deployment

* __One-Click Rollback__: For the current model version, there is a person that can in less than a minute revert to the previously deployed model.
* __One-Click Undeployment__: A model can be removed from deployment with actions that take less than a minute

### Testing Anti-Superpersuasion Setups

<!--Claude Chats:
https://claude.ai/chat/9b59090a-d1b1-4cff-b0ce-77e439b027f4
https://claude.ai/chat/752d0fda-12b0-4f3c-b509-431fc46f9059
-->
