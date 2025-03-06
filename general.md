[home](./index.md)
------------------

*author: niplav, created: 2024-03-23, modified: 2025-02-15, language: english, status: finished, importance: 3, confidence: unlikely*

> __I don't think that humans are (equivalent to) Turing machines,
but people who defend the view are barking up the right tree.__

Trying to Disambiguate Different Questions about Whether Humans are Turing Machines
====================================================================================

<!--TODO: Check where the linear bounded automata are more appropriate
than finite-state machines-->

I often hear the sentiment that humans are [Turing
machines](https://en.wikipedia.org/wiki/Turing_Machine), and that this
sets humans apart from other pieces of matter.<!--TODO: link twitter-->

Examples are [this
thread](http://nitter.poast.org/tmdanis/status/1769471661001109979)
and a short section in [an interview with David
Deutsch](https://www.dwarkeshpatel.com/i/52511224/will-ais-be-smarter-than-humans):

> So all hardware limitations on us boil down to speed and memory
capacity. And both of those can be augmented to the level of any other
entity that is in the universe. Because if somebody builds a computer
that can think faster than the brain, then we can use that very computer
or that very technology to make our thinking go just as fast as that. So
that's the hardware.
[…]
So if we take the hardware, we know that __our brains are Turing-complete
bits of hardware__, and therefore can exhibit the functionality of
running any computable program and function.

[and](https://www.dwarkeshpatel.com/i/52511224/can-you-simulate-the-whole-universe):

> So the more memory and time you give it, the more closely it could
simulate the whole universe. But it couldn't ever simulate the whole
universe or anything near the whole universe because it is hard for it
to simulate itself. Also, the sheer size of the universe is large.

I've always found those statements a bit strange and confusing, so it
seems worth it to tease apart what they could mean.

The question "is a human a Turing machine" is probably meant to
convey "can a human mind execute arbitrary programs?", that is
"are the languages the human brain emit at least [recursively
enumerable](https://en.wikipedia.org/wiki/Recursively_enumerable)?",
as opposed to e.g.
[context-free](https://en.wikipedia.org/wiki/Context-free_grammar)
languages.

1.	My first reaction is that humans are definitely not Turing
	machines, because we lack the infinite amount
	of memory the Turing machine has in form of
	an (idealized) tape. Indeed, in the [Chomsky
	hierarchy](https://en.wikipedia.org/wiki/Chomsky_Hierarchy)
	human aren't even at the level of [pushdown
	automata](https://en.wikipedia.org/wiki/Push-down_automata)
	(since we lack an infinitely deep stack),
	instead we are nothing more than [finite state
	automata](https://en.wikipedia.org/wiki/Finite-state_automaton).
	(I remember a professor pointing out to us that all physical
	instantiations of computers are merely finite-state automata).
	1.	Depending on one's [interpretation of quantum
		mechanics](https://en.wikipedia.org/wiki/Interpretations_of_Quantum_Mechanics),
		one might instead argue that
		we're at least [nondeterministic finite
		automata](https://en.wikipedia.org/wiki/Nondeterministic_finite_automata)
		or even [Markov
		chains](https://en.wikipedia.org/wiki/Markov-Chain). However,
		every nondeterministic finite automaton
		can be [transformed into a deterministic finite
		automaton](https://en.wikipedia.org/wiki/Nondeterministic_finite_automata#Equivalence_to_DFA),
		albeit at an exponential increase in the
		number of states, and Markov chains aren't more
		computationally powerful (e.g. they can't recognize [Dyck
		languages](https://en.wikipedia.org/wiki/Dyck_language), just
		as DFAs can't).
	2. It might be that [Quantum finite
		automata](https://en.wikipedia.org/wiki/Quantum_finite_automata)
		are of interest, but I don't know enough about quantum physics
		to make a judgment call.
2.	The above argument only applies if we regard humans as closed systems
	with clearly defined inputs and outputs. When probed, many proponents
	of the statement "humans are Turing machines" indeed fall back to
	a [motte](https://en.wikipedia.org/wiki/Motte-and-Bailey) that *in
	principle* a human could execute every algorithm, given enough [time,
	pen and paper](https://xkcd.com/505/).
	1.	This seems true to me, assuming that the matter in universe
		does not have a limited amount of computation it can perform.
		1.	In a [finite
			universe](https://arxiv.org/pdf/quant-ph/0110141.pdf)
			we are [logically
			isolated](https://www.lesswrong.com/posts/JWeA8PHnRNQYGWw6Q/aaboyles-s-shortform?commentId=P3NmzPzKHpBXFFZbm)
			from [almost
			all](https://en.wikipedia.org/wiki/Almost_all) computable
			strings, which seems pretty relevant.
		2.	Another constraint is from computational
			complexity; [should we treat things that
			are not polynomial-time computable as basically
			unknowable](https://www.scottaaronson.com/papers/philos.pdf)?
			Humans certainly can't solve [NP-complete
			problems](https://en.wikipedia.org/wiki/NP-complete)
			efficiently.
	2. I'm not sure this is a very useful notion.
		1.	On the one hand, I'd argue that, by orchestrating
			the exactly right circumstances, a tulip could
			receive specific stimuli to grow in the right
			directions, knock the correct things over, lift
			other things up with its roots, create offspring
			that perform subcomputations &c to execute arbitrary
			programs. [Conway's Game of Life certainly manages
			to](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Undecidability)!
			One might object that this is set up for the tulip
			to succeed, but we also put the human in a room with
			unlimited pens and papers.
		2.	On the other hand, those circumstances would have to
			be *very exact*, much more so than with humans. But that
			again is a difference in degree, not in kind.

### Conclusion

After all, I'm coming down with the following belief: Humans are
*certainly not* Turing machines, however there might be a (much weaker)
notion of generality that humans fulfill and other physical systems don't
(or don't as much). But this notion of generality is purported to be
stronger than the one of *life*:

<div>
	$$\text{Turing-completeness} \Rightarrow \text{Context-sensitive} \Rightarrow \text{Context-free} \overset{?}{\Rightarrow} \text{Proposed-generality} \overset{?}{\Rightarrow} \text{Life} \overset{?}{\Rightarrow} \text{Finite-state automata}$$
</div>

I don't know of any formulation of such a criterion of generality,
but would be interested in seeing it fleshed out.

### See Also

* [Are there cognitive realms? (Tsvi Benson-Tilsen, 2022)](https://tsvibt.blogspot.com/2022/11/are-there-cognitive-realms.html)
