[home](./index.md)
-------------------

*author: niplav, created: 2021-01-21, modified: 2021-01-23, language: english, status: in progress, importance: 2, confidence: likely*

> __[“Artificial Intelligence: A Modern
Approach”](https://en.wikipedia.org/wiki/Artificial_Intelligence:_A_Modern_Approach),
written by [Stuart
Russell](https://en.wikipedia.org/wiki/Stuart_J._Russell) and [Peter
Norvig](https://en.wikipedia.org/wiki/Peter_Norvig), is probably the most
well-known textbook on artificial intelligence. Here, I write down my
solutions to exercises in that book. I use the 2010 edition, because the
exercises for the 2020 edition were moved online.__

Solutions to “Artificial Intelligence: A Modern Approach”
=========================================================

Chapter 1
----------

### 1.1

> Define in your own words: (a) intelligence, (b) artificial intelligence,
(c) agent, (d) rationality, (e) logical reasoning

#### Intelligence

The word “intelligence” is mostly used to describe a property of
systems. Roughly, it refers to the ability of a system to make decisions
that result in consequences are graded high according to some metric,
as opposed to decisions that result in consequences that are graded low
according to that metric.

#### Artificial Intelligence

“Artificial intelligence” refers to systems designed and implemented
by humans with the aim of these systems displaying intelligent behavior.

#### Agent

An “agent” is a part of the universe that carries out goal-directed
actions.

#### Rationality

The usage of the word “rationality” is difficult to untangle from
the usage of the word “intelligence”. For humans, “rationality”
usually refers to the ability to detect and correct cognitive errors
that hinder coming to correct conclusions about the state of the world
(epistemic rationality), as well as the ability to act on those beliefs
according to ones values (instrumental rationality). However, these
seem very related to “intelligence”, maybe only being separated by a
potentiality–intelligence being the potential, and rationality being
the ability to fulfill that potential. One could attempt to apply the
same definition to artificial intelligences, but it seems unclear how
a lawful process could be more intelligent, but is not.

#### Logical Reasoning

“Logical reasoning” refers to the act of deriving statements from
other statements according to pre-defined rules.

<!--
### 1.2

> Read Turing’s original paper on AI (Turing, 1950). In the paper, he discusses several
objections to his proposed enterprise and his test for intelligence. Which objections still carry
weight? Are his refutations valid? Can you think of new objections arising from develop-
ments since he wrote the paper? In the paper, he predicts that, by the year 2000, a computer
will have a 30% chance of passing a five-minute Turing Test with an unskilled interrogator.
What chance do you think a computer would have today? In another 50 years?

TODO

-->

### 1.3

A reflex action is not intelligent, as it is not the result of a
deliberate reasoning process. According to my personal definition above
(and also the definition given in the text), it is also not rational
(since the action is not guided by a belief).

Common usage of the term “rational” indicates that
people would describe this reflex as a rational action. I
believe this is fine, and words are just pointers to [clusters in
thing-space](https://www.lesswrong.com/posts/jMTbQj9XB5ah2maup/similarity-clusters)
anyway.

### 1.4

> Suppose we extend Evans’s ANALOGY program so that it can score 200
on a standard IQ test. Would we then have a program more intelligent
than a human? Explain.

No. (At least not for any useful definition of intelligence). IQ
tests as they currently exist measure a proxy for the actual ability
to perform complex tasks in the real world. For humans, geometry
puzzles correlate (and predict) well with such tests ([Sternberg et al.
2001](./doc/aima_solutions/the_predictive_value_of_iq_sternberg_2001.pdf "The Predictive Value of IQ")).

However, this proxy breaks down once we start optimising for it (as
in the case on extending ANALOGY). We can now not predict real-world
performance on arbitrary goals given the result of the IQ test performed
on ANALOGY anymore.

### 1.5

> The neural structure of the sea slug Aplysia has been widely studied
(first by Nobel Laureate Eric Kandel) because it has only about 20,000
neurons, most of them large and easily manipulated. Assuming that the
cycle time for an Aplysia neuron is roughly the same as for a human
neuron, how does the computational power, in terms of memory updates
per second, compare with the high-end computer described in Figure 1.3?

<!--TODO: un-fuck the dimensional analysis here-->

Given the cycle time of `$10^{-3}$` seconds, we can expect

<div>
	$$\frac{2*10^{4} \hbox{ neurons}}{10^{-3}\frac{\hbox{s}}{\hbox{update}}}=2*10^{7} \frac{\hbox{neuron updates}}{s}$$
</div>

which is seven orders of magnitude lower than a supercomputer. Aplysia
won't be proving any important theorems soon.

<!--
If Aplysia has 20k neurons, then it can be expected to have

`$2*10^{4}\hbox{ neurons }*\frac{10 \hbox{ to } 10^{5} \hbox{ synapses }}{\hbox{neuron}}=2*10^{5}\hbox{ to } 2*10^{9} \hbox{ neurons}$`
-->

<!--
TODO: do exercises 6 through 15

### 1.6

> How could introspection—reporting on one’s inner thoughts—be
inaccurate? Could I be wrong about what I’m thinking? Discuss.

### 1.7

> To what extent are the following computer systems instances of artificial intelligence:
* Supermarket bar code scanners.
* Web search engines.
* Voice-activated telephone menus.
* Internet routing algorithms that respond dynamically to the state of the network.

### 1.8

> Many of the computational models of cognitive activities that have been proposed in-
volve quite complex mathematical operations, such as convolving an image with a Gaussian
or finding a minimum of the entropy function. Most humans (and certainly all animals) never
learn this kind of mathematics at all, almost no one learns it before college, and almost no
one can compute the convolution of a function with a Gaussian in their head. What sense
does it make to say that the “vision system” is doing this kind of mathematics, whereas the
actual person has no idea how to do it?

### 1.9

> Why would evolution tend to result in systems that act rationally? What
goals are such systems designed to achieve?

### 1.10

> Is AI a science, or is it engineering? Or neither or both? Explain.

### 1.11

> “Surely computers cannot be intelligent—they can do only what
their programmers tell them.” Is the latter statement true, and does
it imply the former?

### 1.12

> “Surely animals cannot be intelligent—they can do only what their
genes tell them.” Is the latter statement true, and does it imply
the former?

### 1.13

> “Surely animals, humans, and computers cannot be intelligent—they
can do only what their constituent atoms are told to do by the laws of
physics.” Is the latter statement true, and does it imply the former?

### 1.14

> Examine the AI literature to discover whether the following tasks
can currently be solved by computers

> a. Playing a decent game of table tennis (Ping-Pong).
b. Driving in the center of Cairo, Egypt.
c. Driving in Victorville, California.
d. Buying a week’s worth of groceries at the market.
e. Buying a week’s worth of groceries on the Web.
f. Playing a decent game of bridge at a competitive level.
g. Discovering and proving new mathematical theorems.
h. Writing an intentionally funny story.
i. Giving competent legal advice in a specialized area of law.
j. Translating spoken English into spoken Swedish in real time.
k. Performing a complex surgical operation.

> For the currently infeasible tasks, try to find out what the
difficulties are and predict when, if ever, they will be overcome.

### 1.15

> Various subfields of AI have held contests by defining a standard task
and inviting re- searchers to do their best. Examples include the DARPA
Grand Challenge for robotic cars, The International Planning Competition,
the Robocup robotic soccer league, the TREC infor- mation retrieval event,
and contests in machine translation, speech recognition. Investigate five
of these contests, and describe the progress made over the years. To
what degree have the contests advanced toe state of the art in AI? Do
what degree do they hurt the field by drawing energy away from new ideas?

-->
