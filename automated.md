[home](./index.md)
------------------

*author: niplav, created: 2025-05-30, modified: 2025-06-20, language: english, status: notes, importance: 7, confidence: likely*

> __An unstructured, unfinished braindump.__

Automated AI Alignment Research
================================

### I. Type Signature of Output

When we create scaffolds for/train/create training environments for
automated AI alignment researchers, what is the type signature of the
outputs of those researchers?

* Model weights of new, presumably aligned, more powerful AI systems?
* New architectures for AI systems?
* Proofs of convergence or OOD generalization of new architectures?
* Enumerative safety through mechanistic interpretability?
	* That seems hard, there are probably exponentially many meaningful circuits in large neural networks
* New AI paradims that side-step inner optimizers?
	* Neo-GOFAI?
	* Infra-Bayesian physicalism implementations?
* Control techniques that allow for better supervision of the next generation of automated alignment researchers?
* Just ask the automated alignment researchers what the type signature should be?

### II. Condition Number of Succession Process

### III. Generator-Verifier Gap Broken/Unusual For Alignment

There are different perspectives on this.

### IV. Goal-Guarding + Adversarial Examples

### V. Training Imitators

[Clymer
2025](https://www.lesswrong.com/posts/TTFsKxQThrqgWeXYJ/how-might-we-safely-pass-the-buck-to-ai)
suggests to train AIs that imitate human alignment researchers. His
proposal lacks some detail, namely on whether one __trains against
alignment researcher feedback__ or __trains against alignment researcher
behavior__.

__Training against alignment researcher feedback__: An alignment
researcher formulates a task (i.e. an experiment, a conceptual question
&c). The AI model generates an output to solve the task. The researcher
then samples and observes the output, and then grades the results
according to how much they liked the output of the AI model with respect
to the task. The model is trained on that feedback.

__Training against alignment researcher behavior__: An alignment
researcher formulates a task. The AI model, as in the previous case,
tries to solve the task and produces some output `$O_A$`. For some tasks,
the alignment researcher *separately* tries to solve the task themselves,
and produces some output `$O_R$`, without any access to `$O_A$`. A third
person (which could be a different AI model, or another researcher) then
goes over `$O_A$` and `$O_R$` and grades the AI model on how similar
`$O_A$` is to `$O_R$`.

Training against alignment researcher behavior is much more bona-fide
[imitation learning](https://en.wikipedia.org/wiki/Imitation_learning),
whereas training against alignment researcher feedback is much more
similar in spirit to e.g. RLHF.
