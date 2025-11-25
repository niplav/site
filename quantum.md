[home](./index.md)
-------------------

*author: niplav, created: 2025-10-12, modified: 2025-11-25, language: english, status: finished, importance: 5, confidence: possible*

> __Progress in quantum computing is mostly relevant insofar that it is
progress in Atoms, not progress in Bits. This is because quantum computers
are best suited for simulating quantum-mechanical systems, and because
Shor's algorithm doesn't matter economically, Grover's algorithm only
matters at huge scales, and quantum machine learning hasn't found any
promising algorithms yet.__

Quantum Computing is about Atoms, not Bits
-------------------------------------------

*epistemic status*: Stating impressions, but I don't know much about
quantum physics (or quantum computing!). Someone more qualified please
write the accurate version of this post.

That said: I think people have been hyping quantum computing
backwards. The specific algorithms that are always brought up as
providing a relevant speedup over their classical counterparts are
[Shor's algorithm](https://en.wikipedia.org/wiki/Shor's_Algorithm) and
[Grover's algorithm](https://en.wikipedia.org/wiki/Grover's_algorithm),
but not much relevant economic activity is tied up with
finding the prime factors of numbers, and while getting a
[radical](https://en.wiktionary.org/wiki/radical#Etymology) speedup in
unsorted search is cool, the setup costs may only be worth it except
for extremely large searches:

> Even when considering only problem instances that can be solved within
one day, we find that there are potentially large quantum speedups
available. ... However, the number of physical qubits used is extremely
large, ... . In particular, the quantum advantage disappears if one
includes the cost of the classical processing power required to perform
decoding of the surface code using current techniques.” The most recent
of the references listed above [[11](https://arxiv.org/abs/2307.00523)]
estimates that achieving a quantum advantage via a quadratic speedup
requires at least a month-long computation already if each iteration
contains at least one floating-point operation.

*—Dalzell et al., [“Quantum algorithms: A survey of applications and end-to-end complexities”](https://arxiv.org/pdf/2310.03011#subsection.0.4.1) p. 76, 2023*

Relevantly, with cheaper quantum error correction this may drop, and
I vaguely remember Aaronson claiming that performing unsorted search
with tens of terabytes is a low estimate for when Grover speedups will
be useful.

For cracking 2048-bit RSA and 256-bit ECC:

> The physical resources required to implement these logical
circuits fault tolerantly depends on many details of the
hardware, including the error rate, the physical gate speed,
and the available connectivity. In both cases (2048-bit RSA
[[10](https://arxiv.org/pdf/2310.03011#cite.21@gidney2021HowToFactor),
[29](https://arxiv.org/pdf/2310.03011#cite.21@ha2022ShorResources)]
and 256-bit ECC
[[25](https://arxiv.org/pdf/2310.03011#cite.21@webber2022HardwareSpecifications),
[26](https://arxiv.org/pdf/2310.03011#cite.21@gouzien2023catCodeEllipticCurve),
[27](https://arxiv.org/pdf/2310.03011#cite.21@litinski2023EllipticCurvesBaseline)]),
given current hardware schemes restricted to nearest-neighbor 2D
connectivity with logical qubits encoded into surface codes, the number
of physical qubits is estimated to be on the order of 10 million and
the computation runs for at least 3–10 hours (significantly longer
than this for platforms with relatively slower physical gate speeds).

*—Dalzell et al., [“Quantum algorithms: A survey of applications and end-to-end complexities”](https://arxiv.org/pdf/2310.03011#subsection.0.6.1) p. 114, 2023*

which is certainly much faster, but also much less
economically useful, and in some sense economically
*disvaluable* because now we have to find [post-quantum
cryptography](https://en.wikipedia.org/wiki/Post-Quantum_Cryptography)
methods.

I don't have a full picture of the possible applications for quantum
algorithms, but my impression is that for purely bit-focused areas such as
e.g. logistics or supply chain optimization or even machine learning the
algorithms (1) are fairly narrow, (2) usually don't offer an exponential
speedup *or* only offer it if we postulate specific setups (e.g. the [HHL
algorithm](https://en.wikipedia.org/wiki/HHL_algorithm) for estimating
quadratic functions of the solution of a system of linear equations
depends on ["the solution vector, `$|b⟩$`, […] be efficiently
prepared"](https://en.wikipedia.org/wiki/HHL_algorithm#Implementation_difficulties)),
(3) often the best classical algorithms exploit some structure that
makes them comparable in performance to quantum algorithms (such as
sorting an [index](https://en.wikipedia.org/wiki/Database_index)
once and searching in logarithmic time repeatedly) and (4) that
finding exact solutions to computational problems efficiently is not
a large bottleneck on bit-focused parts of the economy, except in
training LLMs. I feel skeptical about quantum machine learning, and my
guess is that if we [read the fine print on quantum machine learning
speedups](https://www.scottaaronson.com/papers/qml.pdf) we'll often not
find them useful in practice:

> So in summary, how excited should we be about the new quantum machine
learning algorithms? To whatever extent we care about quantum computing
at all, I’d say we should be excited indeed: HHL and its offshoots
represent real advances in the theory of quantum algorithms, and in a
world with quantum computers, they’d probably find practical uses. But
along with the excitement, we ought to maintain a sober understanding
of what these algorithms would and wouldn’t do: an understanding
that the original papers typically convey, but that often gets lost in
secondhand accounts.  
The new algorithms provide a general template, showing how quantum
computers might be used to provide exponential speedups for central
problems like clustering, pattern-matching, and principal component
analysis. But for each intended application of the template, one still
needs to invest a lot of work to see whether (a) the application satisfies
all of the algorithm’s “fine print,” and (b) once we include the
fine print, there’s also a fast classical algorithm that provides the
same information.

*—Scott Aaronson, [“Quantum Machine Learning Algorithms: Read the Fine Print”](https://www.scottaaronson.com/papers/qml.pdf), 2015*

Hence: Quantum computing looks quite underwhelming on the side of bits.

My best guess is still that quantum computing is still extremely
promising, because quantum algorithms are really good at simulating
quantum systems, and the world is at its basis quantum.

> Despite the apparent exponential cost of exact classical methods
for this task, scientists have made incredible progress over the last
century via increasingly sophisticated approximate methods. As a result,
quantum chemistry is now a core part of several applications, including
the analyses of chemistry experiments, the pharmaceutical drug discovery
pipeline, and the optimization of materials for catalysts and batteries.

*—Dalzell et al., [“Quantum algorithms: A survey of applications and end-to-end complexities”](https://arxiv.org/pdf/2310.03011#section.0.2) p. 36, 2023*

There's been some speculation that accurate quantum computers can even
help with the construction of next-generation quantum computers

> I wish we had a quantum computer because by the way, the first thing the
quantum computer will allow us to do is build quantum computers, because
it's going to be so much easier to simulate atom-by-atom construction
of these new quantum gates.

*—Dwarkesh Patel & Satya Nadella, [“Satya Nadella — Microsoft’s AGI plan & quantum breakthrough”](https://www.dwarkesh.com/p/satya-nadella), 2025*

but my impression is that these kinds of flywheel-arguments are usually
not applicable and usually some different bottleneck kicks in.

But otherwise, quantum algorithms seem really useful
for simulating the interactions of small molecules and
their formation, figuring out the dynamics of chemical
interactions, maybe even making progress on [atomically precise
manufacturing](https://www.gap-map.org/gaps/inability-to-perform-chemistry-with-direct-positional-control/)
and resolving the [Drexler-Smalley
debate](https://en.wikipedia.org/wiki/Drexler-Smalley_debate_on_molecular_nanotechnology)???

There is also some hope that quantum computing will
allow us to make [progress in nuclear and particle
physics](https://arxiv.org/pdf/2310.03011#section.0.3), but I can't
immediately think of any industrial applications of such progress.

If my understanding here is correct, then that's way cooler
than progress in bits! Humanity hasn't made much [progress in
atoms](https://www.lesswrong.com/posts/Xqcorq5EyJBpZcCrN/thiel-on-progress-and-stagnation)
recently, while making tons of progress in bits, so that might be why
people are hyping quantum computing as a bit-focussed technology—they
can't conceive of anything else? And communicating the advantages of
quantum computing has been extremely backwards, which is usually lead with
"quantum computing will break this strange cryptography thing", *not*
"quantum computing will let us make batteries that are substantially
more efficient", guess which of those is more easily understandeable
to laypeople‽

So, yeah, I think quantum computing is hype-worthy, though my best guess
is that the magnitude of current hype on it is too large relative to
other technologies. But: the current hype is mis-directed, and can be
redirected in the correct direction with a simple message: __Quantum
Computing is About Atoms, Not Bits__.
