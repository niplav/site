[home](./index.md)
-------------------

*author: niplav, created: 2026-03-29, modified: 2026-06-28, language: english, status: maintenance, importance: 6, confidence: likely*

> __I try to square the agent-structure problem with LLMs.__

LLMs as Giant Lookup-Tables of Shallow Circuits
------------------------------------------------

Early 2026 LLMs in scaffolds, from simple ones
such as giving the model access to a scratchpad/"[chain of
thought](https://blog.research.google/2022/05/language-models-perform-reasoning-via.html)"
up to [MCP servers](https://en.wikipedia.org/wiki/Model_Context_Protocol),
[skills](https://claude.com/skills) and [context
compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)
&c are *quite* capable. ([Obligatory meme link to the METR
graph](https://metr.org/time-horizons/).)

Yet: If someone had told me in 2019 that systems with
such capability would exist in 2026, I would strongly
predict that they would be almost uncontrollable optimizers,
ruthlessly & tirelessly pursuing their goals and finding [edge
instantiations](https://arbital.com/p/edge_instantiation/) in everything.
But they don't seem to be doing that. Current-day LLMs are just not *that*
optimizer-y, they appear to have capable behavior without apparent [agent
structure](https://www.lesswrong.com/posts/osxNg6yBCJ4ur9hpi/does-agent-like-behavior-imply-agent-like-architecture).

Discussions from the time either ruled out giant lookup-tables ([Altair 2024](https://www.lesswrong.com/posts/oxsBpx9v3bgxraiPj/towards-a-formalization-of-the-agent-structure-problem)):

> One obvious problem is that there could be a policy which is the
equivalent of a giant look-up table it's just a list of key-value pairs
where the previous observation sequence is the look-up key, and it returns
a next action. For any well-performing policy, there could exist a table
version of it. These are clearly not of interest, and in some sense they
have no "structure" at all, let alone agent structure. A way to filter
out the look-up tables is to put an upper bound on the description length
of the policies […].

or specified that the optimizer must be in the causal
history of such a giant lookup-table ([Garrabrant
2019](https://www.lesswrong.com/posts/osxNg6yBCJ4ur9hpi/does-agent-like-behavior-imply-agent-like-architecture)):

> First a giant look-up table is not (directly) a counterexample. This
is because it might be that the only way to produce an agent-like GLUT
is to use agent-like architecture to search for it. Similarly a program
that outputs all possible GLUTs is also not a counterexample because you
might have to use your agent-like architecture to point at the specific
counterexample. A longer version of the conjecture is “If you see a
program impelements agent-like behavior, there must be some agent-like
architecture in the program itself, in the causal history of the program,
or in the process that brought your attention to the program.”

The most fitting rejoinder to the observation
of capable non-optimizer AIs is probably [*"Just you
wait"*](https://www.allmusicals.com/lyrics/hamilton/alexanderhamilton.htm)—current
LLMs are *capable*, sure, but they're not wildly superhuman
to an extent comparable to the original worries about extreme
optimization pressure. In this view, they're molting into
full agency right now, and we should see the problems of high
optimization pressure show up by the end of 2026 or the five years
after`$_{50\%}$`[^report] if they're not hidden from us by [deceptive
AIs](https://www.lesswrong.com/s/r9tYkB2a8Fp4DN8yB/p/zthDPAjh9w6Ytbeks)`$_{35\%}$`.
Indeed, current LLMs [*do*
reward-hack](https://metr.org/blog/2025-06-05-recent-reward-hacking/),
though the developers have been decent at suppressing the tendency down
to a consumer-acceptable level.

[^report]: Someone wrote a [long report](https://ai-2027.com/) about this.

But I have [a different model
of](https://www.lesswrong.com/posts/yeADMcScw8EW9yxpH/a-sketch-of-good-communication)
how LLMs can be capable without being agentic/pernicioulsy optimizing:

**LLMs are superlinear-in-network-width
[lookup-table](https://en.wikipedia.org/wiki/Lookup_table)-like
collections of _depth-limited_, _composeable_ and
_[error-correcting](https://www.lesswrong.com/posts/nWRj6Ey8e5siAEXbK/simple-versus-short-higher-order-degeneracy-and-error-1)_
[circuits](https://en.wikipedia.org/wiki/Circuit_\(computer_theory\)),
[computed in superposition](https://www.lesswrong.com/w/comp-in-sup)**.

One could call this the GLUT-of-circuits model of LLMs.

To elaborate:

1. "[lookup-table](https://en.wikipedia.org/wiki/Lookup_table)-like": A common issue in [proving theorems about agent structure](https://www.lesswrong.com/posts/oxsBpx9v3bgxraiPj/towards-a-formalization-of-the-agent-structure-problem) is to avoid including giant lookup tables where each sequence of previous percepts and actions is matched to an optimal next action. Such a giant lookup table is infeasible in the real world, but I think something _similar_ to a giant lookup table might be possible, namely through computation in superposition.
2. "circuits": Turing machines aren't a great model for the type of computation that neural networks use (namely because they assume an infinite tape and arbitrary serial depth); a slightly better one is [circuits](https://en.wikipedia.org/wiki/Circuit_\(computer_science\)), which have limited depth, though in computer science circuits are usually defined for booleans or integers. See also [Olah et al. 2020)](https://distill.pub/2020/circuits/zoom-in/) on the relatedly defined concept in mechanistic interpretability.
3. "computed in superposition": Current LLMs [represent features in superposition](https://transformer-circuits.pub/2022/toy_model/index.html), that is, they exploit the fact that high-dimensional spaces can have exponentially many almost-orthogonal vectors relative to the number of dimensions (a consequence of the [Johnson-Lindenstrauss lemma](https://en.wikipedia.org/wiki/Johnson-Lindenstrauss_lemma)). The idea of [computation in superposition](https://www.lesswrong.com/w/comp-in-sup) generalizes this observation to cram more computation into a neural network.
4. "superlinear-in-network-width": Computation in superposition allows for running many circuits at the same time. E.g. [Hänni et al. 2024](https://arxiv.org/abs/2408.05451) construct (shallow) neural networks of witdh `$\tilde{O}(m^{\frac{2}{3}}s^2)$` that are able emulate an `$s$`-sparse[^sparse] boolean circuit of width `$m$` (__Theorem 8__).
	1. This result gestures at the possibility that one *can* put a superlinear number of circuits[^number] into a single neural network, making the neural network more of a lookup-table than an example of [general-purpose search](https://www.lesswrong.com/posts/6mysMAqvo9giHC4iX/what-s-general-purpose-search-and-why-might-we-expect-to-see).
5. "depth-limited": A forward pass in SOTA language models has a limited number of steps of [serial computation](https://en.wikipedia.org/wiki/Serial_computation); [gpt-3-davinci](./doc/cs/ai/language_models_are_few_shot_learners_brown_et_al_2020.pdf) had 96 layers, which results in a circuit depth of 78-83 steps per layer, impliying in `$96 \cdot [78, 83]=[7488, 7968]$` serial steps per forward pass. Current LLMs might look different due to sparse attention and other developments in architecture, no to speak of increased model size, but I'd guess that current frontier models don't have a circuit depth of more than 20000`$_{65\%}$`, unless I really messed something up in my calculation. Claude Sonnet 4.5 estimates that Kimi K2.5 Thinking has slightly less than 5000 serial steps of computation, mostly due to being only 61 layers deep.
6. "composeable": If the neural network just contained an unrelated collection of circuits, the network wouldn't be effective at solving difficult math problems. Instead, my best guess is that the circuits are selected by reinforcement learning, especially RLVR, to be *composeable*, that is each circuit takes inputs of the same type as outputs of other circuits in the network. (Maybe this explains the some of the "sameness"/"slop"-factor of LLM outputs, the "semantic type" has to match?)
7. "error-correcting": If a forward pass executes many circuits in superposition, there will be some interference between individual circuits, so circuits will be selected to be either robust to small errors or error-correcting. This is oddly similar to results from singular learning theory, which imply that (very roughly) [Bayesian inference selects for error-correcting programs](https://www.lesswrong.com/posts/nWRj6Ey8e5siAEXbK/simple-versus-short-higher-order-degeneracy-and-error-1). I don't know which implications this would have.

[^sparse]: The details of `$s$`-sparsity are beyond the purview of this short note.
[^number]: [Hänni et al. 2024](https://arxiv.org/abs/2408.05451) prove polynomial scaling, the [Johnson-Lindenstrauss lemma](https://en.wikipedia.org/wiki/Johnson-Lindenstrauss_lemma), taken too seriously, could imply exponential scaling. Polynomial scaling makes this picture more more feasible but less likely, since it's not clear a merely-polynomial number of circuits can deal with the complexity of the world with its exponentially growing observation-action sequences.

Estimate on the circuit depth of gpt-3-davinci:

1. Self-attention
	1. `$Q, K, V$` projections: single step
	2. Compute `$QK^T$`: `matmul` of square matrix with size 12288, at logarithmic circuit depth for `matmul`s we get 13-14 steps
	3. `softmax` over an array of length `$l$` has depth `$\mathcal{O}(\log_2 l)$` (summation of a list can be done via a summation in a binary tree), for a vector size of 2048 we get 11 steps
	4. Multiply by `$V$`, one `matmul`, 13-14 steps
	5. Output projection, another `matmul`, 13-14 steps
4. Feed-forward
	1. First linear layer: one `matmul`, 13-14 steps
	2. [GELU](https://en.wikipedia.org/wiki/Activation_function): single step
	3. Second linear layer: another `matmul`, 13-14 steps

Inferences from this model:

__Circuit selection__: This model would imply that circuits are
selected mostly by another algorithm with very small serial depth,
relying on features of a problem that can be determined by very parallel
computations.

That somewhat matches my observations from looking at LLMs trying to
tackle problems: It often looks to me like they try one strategy after
another, and less often use detailed information from the past failed
attempt to form a complicated new strategy.

It *also* matches what we've seen from LLMs
[self-preserving](https://palisaderesearch.org/blog/shutdown-resistance)/[black-mailing](https://www.anthropic.com/research/agentic-misalignment)/reward-hacking:
The actions seem opportunistic, not carefully hidden once they've been
performed, not embedded in larger plans; they look mostly like "another
strategy to try, oops, I guess that didn't quite work".

__Alignment__: My guess is that most or almost all of
these circuits are _individually aligned_ through bog-standard
[RLHF](https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback)/[Constitutional
AI](https://en.wikipedia.org/wiki/Constitutional_AI).
This works because the standard problems of [edge
instantiation](https://arbital.com/p/edge_instantiation/) and [Goodhart's
law](./doc/cs/ai/alignment/agent_foundations/categorizing_variants_of_goodharts_law_manheim_garrabrant_2019.pdf)
don't show up as strongly, because the optimization mainly occurs
by either:

1. Selecting one circuit from the giant lookup table that is all the circuits in superposition in the LLM
2. Running many circuits in superposition and selecting the best result or aggregating the best results.

In this model every circuit is individually "aligned" (insofar such a
shallow program can be misaligned at all). Chain of "thought" composes
calls to related circuits (though more on CoT below).

If this view is correct, a folk view of alignment as simply
"deleting/downweighting the bad parts of a model" would be *mostly
correct*: There would be a large but finite number of circuits embedded
in the model, which can be upweighted, downweighted or outright
deleted by gradient descent. My extremely speculative guess is that
there is less than a quadrillion circuits stored in superposition in a
trillion-parameter model`$_{85\%}$`, which which thorough-enough safety
training could exhaustively or near-exhaustively check and select. In
this view, AI alignment really *would* be purely bottlenecked on the
amount of computation spent on whac-a-moling unaligned circuits.

People might not spend enough compute on alignment training, and that
would still be a problem (though a lesser one, since the model wouldn't be
actively working against the developers), but the problem of alignment
would've been turned from a [category I problem into a category II
problem](https://musingsandroughdrafts.wordpress.com/2021/04/05/on-category-i-and-category-ii-problems/).

__Chain of thought__: The obvious wrinkle in this story is that I haven't
talked about chain-of-"thought"/"reasoning" LLMs. It goes with saying that
long chains of thought enable vastly more serial computation to be done,
and I haven't yet quite teased apart how this impacts the overall picture
(besides "it makes it worse").

Still, some guesses at implications from the GLUT-of-circuits models
for alignment and chain-of-"thought":

1. The token bottleneck is *real*. Every <10k serial steps the entire state needs to be compressed down to one of 50k-200k tokens, resulting in at most 16-20 bits of state to be passed between each circuit. My guess is that it's actually closer to ~8-10 bits (given [~1 bit per character in English](https://en.wikipedia.org/wiki/Entropy_\(information\)#Introduction)), so maybe 2 bits per character in an optimized chain of "thought", at four to five characters per token. A vector of a thousand floats becomes a token of a dozen bits.
	1. This may allow us to estimate an upper limit on the optimization power of an LLM outputting `$n$` tokens?
2. Continuous chains of "thought" would be quite bad, since they'd increase the serial depth without information bottlenecks by a lot.
3. It now matters that all the circuits are aligned even when composed with each other, which is not guaranteed at all, and even having to extend the guarantees for alignment from every circuit to every ordered pair of circuits increases the size of the search space quadratically.
	1. Though, I'm still not convinced this would give us ruthless optimizers. You gotta chain together *a lot* of short circuits in a semi-related fashion to result in strong optimization pressure/Goodharting/edge instantiation.

Most of the other things (backtracking in a forward pass is really hard
&c) I'd otherwise say here have already been said by others.

__Training process__: If we see this whole model as being about amortized
optimization, maybe it's the training process that takes up all the
optimization power? Are LLMs the most dangerous during training, or is
it rather the whole training process which is dangerous?

----------------------------------------------------------------------

I think this model is mostly correct`$_{50\%}$`, and also has implications
for capabilities progress/the need to switch to another paradigm/overhaul
parts of the current paradigm to reach wildly superhuman capabilities. I
think it predicts we'll see some gains from training but that we'll
plateau, or trade hard to measure capabilities for easily measurable
capabilities. I think I want to point to 55% "LLMs are agents" and 45%
"LLMs are stochastic parrots", but there's tons of AI capabilities
forecast questions I'm not yet able to answer (e.g. the infamous "which
concrete capability would you expect an LLM-based system not to have in
$YEAR?"). And plausibly the whole thing is just moot because long chains
of thought just enable enough chaining together to get the capabilities.

or smth idk

(Thanks to Claude 4.5 Sonnet for help and feedback)

See Also
---------

Related/prior work/inspirations:

1. [The shard theory of human values (Quintin Pope/TurnTrout, 2022)](https://www.lesswrong.com/s/nyEFg3AuJpdAozmoX/p/iCfdcxiyr2Kj8m8mT): This post may as well be a recasting of the shard theory perspective on neural networks, with computation in superposition as a possible mechanism for *how* shard theory could work.
2. [Simulators (janus, 2022)](https://generative.ink/posts/simulators/): The simulators perspective is *related*, but slightly distinct, it is more interested in the behavior of pretrained base models, but similarly asks questions about where the agency of LLMs is.
