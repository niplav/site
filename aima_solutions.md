[home](./index.md)
-------------------

*author: niplav, created: 2021-01-21, modified: 2021-02-11, language: english, status: in progress, importance: 2, confidence: likely*

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
> b. Driving in the center of Cairo, Egypt.  
> c. Driving in Victorville, California.  
> d. Buying a week’s worth of groceries at the market.  
> e. Buying a week’s worth of groceries on the Web.  
> f. Playing a decent game of bridge at a competitive level.  
> g. Discovering and proving new mathematical theorems.  
> h. Writing an intentionally funny story.  
> i. Giving competent legal advice in a specialized area of law.  
> j. Translating spoken English into spoken Swedish in real time.  
> k. Performing a complex surgical operation.

> For the currently infeasible tasks, try to find out what the
difficulties are and predict when, if ever, they will be overcome.

### 1.15

> Various subfields of AI have held contests by defining a standard task
and inviting researchers to do their best. Examples include the DARPA
Grand Challenge for robotic cars, The International Planning Competition,
the Robocup robotic soccer league, the TREC information retrieval event,
and contests in machine translation, speech recognition. Investigate five
of these contests, and describe the progress made over the years. To
what degree have the contests advanced toe state of the art in AI? Do
what degree do they hurt the field by drawing energy away from new ideas?

-->

Chapter 2
---------

### 2.1

> Suppose that the performance measure is concerned with just the first
T time steps of the environment and ignores everything thereafter. Show
that a rational agent’s action may depend not just on the state of
the environment but also on the time step it has reached.

Example: Let's say that we are in an environment with a button,
and pressing the button causes a light to go on in the next timestep.
The agent cares that the light is on (obtaining 1 util per timestep the
light is on for the first T timesteps).

However, pressing the button incurs a cost of ½ on the agent.

Then, at timestep T, the agent will not press the button, since it does
not care about the light being on at timestep T+1, and wants to avoid
the cost ½. At timesteps `$<T$` it will press the button, with the light
currently being on, at timestep T it will not press the button, under
the same environmental conditions.

<!--

### 2.2

> Let us examine the rationality of various vacuum-cleaner agent
functions.

> a. Show that the simple vacuum-cleaner agent function described in
Figure 2.3 is indeed rational under the assumptions listed on page 38.  
> b. Describe a rational agent function for the case in which each movement
costs one point. Does the corresponding agent program require internal
state?  
> c. Discuss possible agent designs for the cases in which clean squares
can become dirty and the geography of the environment is unknown. Does it
make sense for the agent to learn from its experience in these cases? If
so, what should it learn? If not, why not?

-->

### 2.3

> For each of the following assertions, say whether it is true or
false and support your answer with examples or counterexamples where
appropriate.

> a. An agent that senses only partial information about the state cannot
be perfectly rational.  

False. An agent that senses only partial information about the state could
infer missing information by making deductions (logical or statistical)
about the state of the environment, coming to full knowledge of the
environment, and making perfectly rational choices using that information.

For example, a chess-playing agent that can't see exactly one square
could infer the piece standing on that square by observing which piece
is missing from the rest of the board.

> b. There exist task environments in which no pure reflex agent can
behave rationally.  

True. In an environment in which the next reward depends on the current
state and the previous state, a simple reflex agent will get outperformed
by agents with an internal world-model.

An example for this is a stock-trading agent: The future prices of stocks
doesn't just depend on the current prices, but on the history of prices.

> c. There exists a task environment in which every agent is rational.  

True. It is the environment where the agent has no options to act.

> d. The input to an agent program is the same as the input to the
agent function.  

Not sure. Both the agent function and the agent program receive percepts,
but sometimes the agent program also needs information that is not a
percept (e.g. priors for bayesian agents). Is that counted as input,
or simply as program-specific data?

> e. Every agent function is implementable by some program/machine
combination.  

False. An agent function could be uncomputable
(e. g. [AIXI](https://en.wikipedia.org/wiki/AIXI)), and therefore not
be implementable on a real-world machine.

> f. Suppose an agent selects its action uniformly at random from the
set of possible actions. There exists a deterministic task environment
in which this agent is rational.  

True, that would be the environment in which every action scores equally
well on the performance measure.

> g. It is possible for a given agent to be perfectly rational in two
distinct task environments.  

True. Given two agents `$A_X$` and `$A_Y$`, and two task environments
`$X$` (giving percepts from the set `$\{x_1, \dots, x_n\}$`) and `$Y$`
(giving percepts from the set `$\{y_1, \dots, y_n\}$`), with `$A_X$` being
perfectly rational in `$X$` and `$A_Y$` being perfectly rational in `$Y$`
an agent that is perfectly rational in two distinct task environments
could be implemented using the code:

	p=percept()
	if p∈X
		A_X(p)
		while p=percept()
			A_X(p)
	if p∈Y
		A_Y(p)
		while p=percept()
			A_Y(p)

> h. Every agent is rational in an unobservable environment.  

False. Given an unobservable environment in which moving results in
the performance measure going up (e.g. by knocking over ugly vases),
agents that move a lot are more rational than agents that do not move.

> i. A perfectly rational poker-playing agent never loses.

False. Given incomplete knowledge, a rational poker-playing agent can
only win in expectation.

<!--

### 2.4

> For each of the following activities, give a PEAS description of the
task environment and characterize it in terms of the properties listed
in Section 2.3.2.

> * Playing soccer.
> * Exploring the subsurface oceans of Titan.
> * Shopping for used AI books on the Internet.
> * Playing a tennis match.
> * Practicing tennis against a wall.
> * Performing a high jump.
> * Knitting a sweater.
> * Bidding on an item at an auction.

### 2.5

> Define in your own words the following terms: agent, agent function,
agent program, rationality, autonomy, reflex agent, model-based agent,
goal-based agent, utility-based agent, learning agent.

### 2.6

> This exercise explores the differences between agent functions and
agent programs.

> a. Can there be more than one agent program that implements a given
agent function? Give an example, or show why one is not possible.  
> b. Are there agent functions that cannot be implemented by any agent
program?  
> c. Given a fixed machine architecture, does each agent program implement
exactly one agent function?  
> d. Given an architecture with n bits of storage, how many different
possible agent programs are there?  
> e. Suppose we keep the agent program fixed but speed up the machine
by a factor of two. Does that change the agent function?

### 2.7

> Write pseudocode agent programs for the goal-based and utility-based
agents. The following exercises all concern the implementation of
environments and agents for the vacuum-cleaner world.

### 2.8

> Implement a performance-measuring environment simulator for
the vacuum-cleaner world depicted in Figure 2.2 and specified on
page 38. Your implementation should be modular so that the sensors,
actuators, and environment characteristics (size, shape, dirt placement,
etc.) can be changed easily. (Note: for some choices of programming
language and operating system there are already implementations in the
online code repository.)

### 2.9

> Implement a simple reflex agent for the vacuum environment in Exercise
2.8. Run the environment with this agent for all possible initial dirt
configurations and agent locations. Record the performance score for
each configuration and the overall average score.

### 2.10

> Consider a modified version of the vacuum environment in Exercise 2.8,
in which the agent is penalized one point for each movement.

> a. Can a simple reflex agent be perfectly rational for this
environment? Explain.  
> b. What about a reflex agent with state? Design such an agent.  
> c. How do your answers to a and b change if the agent’s percepts
give it the clean/dirty status of every square in the environment?

### 2.11

> Consider a modified version of the vacuum environment in Exercise 2.8,
in which the geography of the environment—its extent, boundaries,
and obstacles—is unknown, as is the initial dirt configuration. (The
agent can go Up and Down as well as Left and Right.)

> a. Can a simple reflex agent be perfectly rational for this
environment? Explain.  
> b. Can a simple reflex agent with a randomized agent function outperform
a simple reflex agent? Design such an agent and measure its performance
on several environments.  
> c. Can you design an environment in which your randomized agent will
perform poorly? Show your results.  
> d. Can a reflex agent with state outperform a simple reflex
agent? Design such an agent and measure its performance on several
environments. Can you design a rational agent of this type?

### 2.12

> Repeat Exercise 2.11 for the case in which the location sensor
is replaced with a “bump” sensor that detects the agent’s
attempts to move into an obstacle or to cross the boundaries of the
environment. Suppose the bump sensor stops working; how should the
agent behave?

### 2.13

> The vacuum environments in the preceding exercises have all been
deterministic. Discuss possible agent programs for each of the following
stochastic versions:

> a. Murphy’s law: twenty-five percent of the time, the Suck action
fails to clean the floor if it is dirty and deposits dirt onto the floor
if the floor is clean. How is your agent program affected if the dirt
sensor gives the wrong answer 10% of the time?  
> b. Small children: At each time step, each clean square has a 10%
chance of becoming dirty. Can you come up with a rational agent design
for this case?  

-->

Chapter 13
-----------

### 13.1

> Show from first principile that `$P(a|b \land a) = 1$`.

I'm not sure whether this counts as "from first principles", but

`$P(a|b \land a)=\frac{P(a \land a \land b)}{P(a \land b)}=\frac{P(a \land b)}{P(a \land b)}=1$`

is my solution.

### 13.2

> Using the axioms of probability, prove that any probability distribution
on a discrete random variable must sum to 1.

We know that `$\sum_{\omega \in \Omega} P(\omega)=1$`.

Given a discrete random variable X (X is discrete (and therefore also
countable?)), and a probability distribution `$P: X \rightarrow [0;1]$`.

Then, setting `$\Omega=X$`, one can see that `$\sum_{x \in X} P(x)=1$`.

<!--Possible problem: What about other variables & their distributions?
Conditional on those in joint, the result is still 1, but would be
worthwhile to write down.-->

### 13.3

> For each of the following statements, either prove it is true or give
a counterexample.

> a. If `$P(a|b,c)=P(b|a,c)$`, then `$P(a|c)=P(b|c)$`

<div>
	$$P(a|b,c)=P(b|a,c) \Leftrightarrow \\
	\frac{P(a,b,c)}{P(b,c)}=\frac{P(a,b,c)}{P(a,c)} \Leftrightarrow \\
	P(a,c)=P(b,c) \Leftrightarrow \\
	\frac{P(a,c)}{P(c)}=\frac{P(b,c)}{P(c)} \Leftrightarrow \\
	P(a|c)=P(b|c)$$
</div>

True.

> b. If `$P(a|b,c)=P(a)$`, then `$P(b|c)=P(b)$`

False: If
`$P(a)=P(a|b,c)=P(a|\lnot b,c)=P(a|b, \lnot c)=P(a|\lnot b,\lnot c)=0.1$`
(`$P(\lnot a)$` elided for brevity), then still can b be dependent on c,
for example `$P(b|c)=0.2$`, `$P(\lnot b|c)=0.8$`, `$P(b|\lnot c)=0.3$`,
`$P(\lnot b|\lnot c)=0.7$`, and `$P(c)=P(\lnot c)=0.5$` (which would
make `$P(b)=\sum_{c \in C} P(b|c)*P(c)=0.5*0.2+0.5*0.3=0.25$` and
`$P(\lnot b)=\sum_{c \in C} P(\lnot b|c)*P(c)=0.5*0.8+0.5*0.7=0.75$`).

> c. If `$P(a|b)=P(a)$`, then `$P(a|b,c)=P(a|c)$`

`$a$` and `$b$` are independent. However, this does not imply conditional
independence given `$c$`. E.g.:

`$P(a)=0.5, P(b)=0.5, P(c|a, b)=1, P(c|\lnot a, \lnot b)=0, P(c|\lnot a, b)=1, P(c|a, \lnot b)=1$`

So this is false.

<!--
### 13.4

> Would it be rational for an agent to hold the three beliefs `$P(A)=0.4, P(B)=0.3$`,
and `$P(A \lor B)=0.5$`? If so, what range of probabilities
would be rational for the agent to hold for `$A \land B$`? Make up
a table like the one in Figure 13.2, and show how it supports your
argument about rationality. Then draw another version of the table where
`$P(A \lor B)=0.7$`. Explain why it is rational to have this probability,
even though the table shows one case that is a loss and three that just
break even. (*Hint*: what is Agent 1 commited to about the probability
of each of the four cases, especially the case that is a loss?)

It is rational for an agent to believe `$P(A)=0.4, P(B)=0.3$` and
`$P(A \lor B)=0.5$`, if
`$P(A \land B)=P(A)+P(B)-P(A \lor B)=0.4+0.3-0.5=0.2$`.

<table>
<thead>
	<tr>
		<td>Proposition</td>
		<td>Belief</td>
	</tr>
</thead>
<tbody>
	<tr>
	</tr>
</tbody>
</table>
-->

### 13.5

> This question deals with the properties of possible worlds, defined
on page 488 as assignments to all random variables. We will work with
propositions that correspond to exactly one possible world because they
pin down the assignments of all the variables. In probability theory,
such propositions are called **atomic events**. For example, with Boolean
variables `$X_1, X_2, X_3$`, the proposition `$x_1 \land \lnot x_2 \land \lnot x_3$`
fixes the assignment of the variables,; in the language of
propositional logic, we would say it has exactly one model.

> a. Prove, for the case of `$n$` Boolean variables, that any two distinct
atomic events are mutually exclusive; that is, their conjunction is
equivalent to *false*.

Let `$s_1, s_2$` be two distinct atomic events. That means there exists at
least one `$x_i$` so that `$x_i$` is part of the conjunction in `$s_1$`
and `$\lnot x_i$` is part of the conjunction in `$s_2$`.

Then:

<div>
	$$s_1 \land s_2 = \\
	s_1(1) \land \dots \land s_1(i-1) \land x_i \land s_1(i+1) \land \dots \land s_1(n) \land s_2(1) \land \dots \land s_2(i-1) \land \lnot x_i \land s_2(i+1) \land \dots \land s_2(n)=\\
	s_1(1) \land \dots \land s_1(i-1) \land s_1(i+1) \land \dots \land s_1(n) \land s_2(1) \land \dots \land s_2(i-1) \land s_2(i+1) \land \dots \land s_2(n) \land x_i \land \lnot x_i=\\
	s_1(1) \land \dots \land s_1(i-1) \land s_1(i+1) \land \dots \land s_1(n) \land s_2(1) \land \dots \land s_2(i-1) \land s_2(i+1) \land \dots \land s_2(n) \land false=\\
	false$$
</div>

> b. Prove that the disjunction of all possible atomic events is logically
equivalent to *true*.

For every atomic event `$s$`, there is an atomic event
`$s'=\lnot s=\lnot s(1) \land \dots \lnot s(n)$`. Then the
disjunction of all atomic events contains `$s \lor s' \lor \dots=true$`.

> c. Prove that any proposition is logically equivalent to the disjunction
of the atomic events that entail its truth.

Let `$\mathcal{A}$` be the set of `$n$` assignments that make the proposition
true. Then each assignment `$A_i \in \mathcal{A}$` corresponds to exactly
one atomic event `$a_i$` (e.g. assigning true to `$x_1$`, false to `$x_2$` and
false to `$x_3$` corresponds to `$x_1 \land \lnot x_2 \land \lnot x_2$`).
The set of these atomic events exactly entails the proposition.

One can then simply create the conjunction of sentences
`$\bigwedge_{i=1}^{n} a_i$` that is true only if we use an assignment
that makes the proposition true.

Chapter 15
----------

### 15.13

> A professor wants to know if students are getting enough sleep. Each
day, the professor observes whether the students sleep in class, and
whether they have red eyes. The professor has the following domain theory:

>* The prior probability of getting enough sleep, with no observations, is 0.7.
*	The probability of getting enough sleep on night t is 0.8 given
	that the student got enough sleep the previous night, and 0.3
	if not.
* The probability of having red eyes is 0.2 if the student got enough sleep, and 0.7 if not.
* The probability of sleeping in class is 0.1 if the student got enough sleep, and 0.3 if not.

> Formulate this information as a dynamic Bayesian network that
the professor could use to filter or predict from a sequence of
observations. Then reformulate it as a hidden Markov model that has only
a single observation variable. Give the complete probability tables for
the model.

There are three variables: `$E_t$` for getting enough sleep in night t,
`$S_t$` for sleeping in class on day t, and `$R_t$` for having red eyes
on day t.

<!--TODO: Make diagram of bayes network-->

The conditional probabilities tables for the dynamic Bayesian network are:

`$P(E_{t+1}|E_t)$`:

<table>
<thead>
	<tr>
		<td>`$E_t$`</td>
		<td>`$e_{t+1}$`</td>
		<td>`$\lnot e_{t+1}$`</td>
	</tr>
</thead>
<tbody>
	<tr>
			<td>1</td>
			<td>0.8</td>
			<td>0.2</td>
	</tr>
	<tr>
			<td>0</td>
			<td>0.3</td>
			<td>0.7</td>
	</tr>
</tbody>
</table>

`$P(S_t|E_t)$`:

<table>
<thead>
	<tr>
		<td>`$E_t$`</td>
		<td>`$s_t$`</td>
		<td>`$\lnot s_t$`</td>
	</tr>
</thead>
<tbody>
	<tr>
			<td>1</td>
			<td>0.1</td>
			<td>0.9</td>
	</tr>
	<tr>
			<td>0</td>
			<td>0.3</td>
			<td>0.7</td>
	</tr>
</tbody>
</table>

`$P(R_t|E_t)$`:

<table>
<thead>
	<tr>
		<td>`$E_t$`</td>
		<td>`$r_t$`</td>
		<td>`$\lnot r_t$`</td>
	</tr>
</thead>
<tbody>
	<tr>
			<td>1</td>
			<td>0.2</td>
			<td>0.8</td>
	</tr>
	<tr>
			<td>0</td>
			<td>0.7</td>
			<td>0.3</td>
	</tr>
</tbody>
</table>

For the hidden Markov model, the table for `$P(E_{t+1}|E_t)$` stays
the same. For `$P(S_t, R_t | E_t)$` we assume that `$S_t$` and `$R_t$`
are conditionally independent given `$E_t$`:


<table>
<thead>
	<tr>
		<td>`$E_t$`</td>
		<td>`$r_t, s_t$`</td>
		<td>`$r_t, \lnot s_t$`</td>
		<td>`$\lnot r_t, s_t$`</td>
		<td>`$\lnot r_t, \lnot s_t$`</td>
	</tr>
</thead>
<tbody>
	<tr>
			<td>1</td>
			<td>0.02</td>
			<td>0.18</td>
			<td>0.08</td>
			<td>0.72</td>
	</tr>
	<tr>
			<td>0</td>
			<td>0.21</td>
			<td>0.49</td>
			<td>0.09</td>
			<td>0.21</td>
	</tr>
</tbody>
</table>

### 15.14

> For the DBN specified in Exercise 15.13 and for the evidence values

>* e1 = not red eyes, not sleeping in class
* e2 = red eyes, not sleeping in class
* e3 = red eyes, sleeping in class

> perform the following computations:

> a. State estimation: Compute `$P(EnoughSleep_t|e_{1:t})$` for each of t = 1, 2, 3.

Note: In the previous exercise, I used e as a symbol for getting enough
sleep. This collides with the abstract symbol for evidence variables,
but I'm too lazy to change it back (I will use `$ev$` for the evidence
variables instead). I will not mix abstract variables and concrete
variables (here R, S and E) to keep the confusion minimal.

For t=1:

<div>
	$$P(E_1|e_{1:1})=\\
	E(E_1|\lnot r, \lnot s)=\\
	\alpha P(\lnot r, \lnot s| E_1)*(P(E_1|e_0)*P(e_0)+P(E_1|\lnot e_0)*P(\lnot e_0)=\\
	\alpha \langle 0.72, 0.21 \rangle * (\langle 0.8, 0.2 \rangle * 0.7 + \langle 0.2, 0.8 \rangle * 0.3)=\\
	\alpha \langle 0.4464, 0.0798 \rangle \approx \\
	\langle 0.8483, 0.151653 \rangle $$
</div>

For t=2:

<div>
	$$P(E_2|e_{1:2})=\\
	E(E_2|r, \lnot s)=\\
	\alpha P(r, \lnot s| E_2)*(P(E_2|e_1)*P(e_1)+P(E_2|\lnot e_1)*P(\lnot e_1)=\\
	\alpha \langle 0.18, 0.49 \rangle * (\langle 0.8, 0.2 \rangle * 0.8483 + \langle 0.3, 0.7 \rangle * 0.151653)=\\
	\alpha \langle 0.13034446, 0.13515 \rangle \approx \\
	\langle 0.490949, 0.50905 \rangle $$
</div>

For t=3:

<div>
	$$P(E_3|e_{1:3})=\\
	E(E_3|r, s)=\\
	\alpha P(r, s| E_3)*(P(E_3|e_2)*P(e_2)+P(E_3|\lnot e_2)*P(\lnot e_2)=\\
	\alpha \langle 0.02, 0.21 \rangle * (\langle 0.8, 0.2 \rangle * 0.490949 + \langle 0.3, 0.7 \rangle * 0.50905)=\\
	\alpha \langle 0.0109095, 0.09545 \rangle \approx \\
	\langle 0.1025715, 0.89742846\rangle $$
</div>

> b. Smoothing: Compute `$P(EnoughSleep_t|e_{1:3})$` for each of t = 1, 2, 3.

I'll use k instead of t for the point of smoothing here, because, let's
be real, I don't need more double-usage of symbols:

For k=1:

<div>
	$$P(E_1|ev_{1:t}=\alpha P(E_1|ev_{1:1})\times P(ev_{2:3}|E_1)=\alpha f_{1:1} \times b_{2:3}=\\
	\alpha \langle 0.8483, 0.151653 \rangle \times b_{2:3}=\\
	\alpha \langle 0.8483, 0.151653 \rangle \times P(ev_{2:3}|E_1)=\\
	\alpha \langle 0.8483, 0.151653 \rangle \times P(r, \lnot s | e_2)*P(ev_{3:3}|e_2)*P(e_2|E_1)+P(r, \lnot s| \lnot e_2)*P(ev_{3:3}|\lnot e_2) * P(\lnot e_2 | E_1)=\\
	\alpha \langle 0.8483, 0.151653 \rangle \times P(r, \lnot s | e_2)*P(r,s|e_2)*P(e_2|E_1)+P(r, \lnot s| \lnot e_2)*P(r,s|\lnot e_2) * P(\lnot e_2 | E_1)=\\
	\alpha \langle 0.8483, 0.151653 \rangle \times 0.18*0.02*\langle 0.8, 0.3 \rangle + 0.49*0.21*\langle 0.2, 0.7 \rangle=
	\alpha \langle 0.8483, 0.151653 \rangle \times \langle 0.02346, 0.07311 \rangle=\\
	\langle 0.64221, 0.3577896 \rangle $$
</div>

For k=2:

<div>
	$$P(E_2|ev_{1:t}=\alpha P(E_2|ev_{1:2})\times P(ev_{3:3}|E_2)=\alpha f_{1:2} \times b_{3:3}=\\
	\alpha  \langle 0.490949, 0.50905 \rangle \times \langle 0.490949, 0.50905\rangle \times b_{3:3}=\\
	\alpha  \langle 0.490949, 0.50905 \rangle \times \langle 0.490949, 0.50905\rangle \times P(ev_{3:3}|E_2)=\\
	\alpha  \langle 0.490949, 0.50905 \rangle \times P(r, s | e_3)*P(ev_{4:3}|e_3)*P(e_3|E_2)+P(r, s| \lnot e_3)*P(ev_{4:3}|\lnot e_3) * P(\lnot e_3 | E_2)=\\
	\alpha  \langle 0.490949, 0.50905 \rangle \times P(r, s | e_3)*P(e_3|E_2)+P(r, s| \lnot e_3) * P(\lnot e_3 | E_2)=\\
	\alpha  \langle 0.490949, 0.50905 \rangle \times 0.02*\langle 0.8, 0.3 \rangle + 0.21*\langle 0.2, 0.7 \rangle=
	\alpha  \langle 0.490949, 0.50905 \rangle \times \langle 0.058, 0.153\rangle=\\
	\langle 0.2677723998, 0.732276 \rangle $$
</div>

Since I don't know `$e_{4:3}$` (I think nobody does), I assign it
probability 1. Should I assign it probability 0? I don't know!

For k=3:

The number is the same as for filtering, since k=t.

> c. Compare the filtered and smoothed probabilities for t = 1 and t = 2.

As a reminder,
`$P(E_1|ev_{1:1})=\langle 0.8483, 0.151653 \rangle, P(E_2|ev{1:2)=\langle 0.490949, 0.50905 \rangle$`,
and
`$P(E_1|ev_{1:3})=\langle 0.64221, 0.3577896 \rangle, P(E_2|ev{1:3)=\langle 0.2677723998, 0.732276 \rangle$`.

The probabilities don't disagree sharply at any point. Interestingly,
`$P(E_1|ev_{1:1})$` is more confident than `$P(E_1|ev_{1:3})$`, but
it's the other way around for `$E_2$`.

Otherwise, what's there to compare further?
