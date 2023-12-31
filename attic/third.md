[home](./index.md)
-------------------

*author: niplav, created: 2022-02-03, modified: 2022-02-03, language: english, status: draft, importance: 1, confidence: fiction*

Third Variable
===============

> __*IC\* Algorithm*__ (__Inductive Causation with Latent Variables__)  
__Input:__ `$\hat{P}$`, a stable distribution (with respect to some latent structure).  
__Output__: core (`$\hat{P}$`), a marked pattern.  
1. For each pair of variables `$a$` and `$b$`, search for a set `$S_{ab}$` such that `$a$` and `$b$` are independent in `$\hat{P}$`, conditioned on `$S_{ab}$`. If there is no such `$S_{ab}$`, place an undirected link between the two variables, `$a—b$`.  
2. For each pair of nonadjacent variables `$a$` and `$b$` with a common neighbor `$c$`, check if `$c \in S_{ab}$`.  
&nbsp; &nbsp; &nbsp; &nbsp; If it is, then continue.  
&nbsp; &nbsp; &nbsp; &nbsp; If it is not, then add arrowheads pointing at `$c$` (i.e., `$a \rightarrow c \leftarrow b$`).  
3. In the partially directed graph that results, add (recursively) as many arrowheads as possible, and mark as many edges as possible, according to the following two rules:  
&nbsp; &nbsp; &nbsp; &nbsp; R₁: For each pair of nonadjacent nodes `$a$` and `$b$` with a common neighbor `$c$`, if the link between `$a$` and `$c$` has an arrowhead into `$c$` and if the link between `$c$` and `$b$` has no arrowhead into `$c$`, then the arrowhead on the link between `$c$` and `$b$` and the mark that link to obtain `$c \overset{*}{\rightarrow} b$`.  
&nbsp; &nbsp; &nbsp; &nbsp; R₂: If `$a$` and `$b$` are adjacent and there is a directed path (composed strictly of marked links) from `$a$` to `$b$` […], then add an arrowhead pointing toward `$b$` on the link between `$a$` and `$b$`.

*— [Judea Pearl](https://en.wikipedia.org/wiki/Judea_Pearl), “Causality: Models, Reasoning, And Inference” p. 52-53, 2009*

So apparently the boyfriend of a woman I have been sleeping with has
commited suicide.

She had been the sixth of eight women I had talked to on a February
evening, there had been a tease of rain the whole day (but no actual
rain, not even a drizzle). I don't even remember what opener I'd used,
I had hit that mental state where it feels like your eyes have turned
so that they only show white, and you bang out one approach after another.

She neither gave me a Russian Minute nor giggled weirdly, but kept a
close coolness that I appreciated, since it wound me down a bit after two
blowouts and four awkward sets. Of course she mentioned her boyfriend,
and of course I neglected to react to it—standard human mating tactics,
as far as I was concerned. I didn't think she would give me her number,
but her end-twenties eyes showed no hesitation as I awkwardly pulled
out my phone and handed it to her.

Related Texts
--------------

* [Why Men NEED To Learn Game – A Case Study](https://cassidydaygame.wordpress.com/2022/02/23/why-men-need-to-learn-game-a-case-study/) by craigcassidy1<!--TODO: add link for craigcassidy1, and is the en dash in the original title?-->
