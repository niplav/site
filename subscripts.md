[home](./index.md)
------------------

*author: niplav, created: 2023-12-21, modified: 2024-04-18, language: english, status: finished, importance: 3, confidence: certain*

> __Subscripts in text can be used to attach explicit probabilities to claims<sub>99%</sub>.__

Subscripts for Probabilities
==============================

Gwern has wondered about a use-case for subscripts in hypertext. While
they have settled on a specific use-case, namely [years for
citations](https://www.gwern.net/Subscripts.html), I propose a different one:
reporting explicit probabilities.

Explicitely giving for probabilities in day-to-day English text is usually
quite clunky: "I assign 35% to North Korea testing an intercontinental
ballistic missile until the end of this year" reads far less smoothly
than "I don't think North Korea will test an intercontinental ballistic
missile this year".<!--TODO: what's the normal English problem with
multiple statements?-->

And since subscripts are a solution in need of a problem, one can wonder
how well those two fit together: Quite well, I claim.

In short, I propose to append probabilities in subscript after a statement
using standard HTML subscript notation (or `$\LaTeX$` as a fallback if
it's available), with the probability possibly also being a link to a
relevant forecasting platform with the same question:

> I think Donald Trump is going to be incarcerated before 2030<sub>[65%](https://www.metaculus.com/questions/10832/donald-trump-jailed-by-2030/)</sub>.

This is *almost* as readable as the sentence without the probability.

There are some complications with negations in sentences or multiple
statements. For the most part, I'll simply avoid such cases ("Doctor,
it hurts when I do this!" "Don't do that, then."), but if I had to,
I'd solve the first problem by declaring that the probability applies to
the literal meaning of the previous sentence, including all negations;
the problem with multiple statements is solved by delimiters.

As an example for the different kinds of negation: "The train won't
come more than 5 minutes late<sub>90%</sub>" would (arguendo) mean the
same thing as "I don't think the train will come more than 5 minutes
late<sub>90%</sub>" means the same as "The train will take more than 5
minutes to arrive<sub>10%</sub>" equivalent to "I assign 90% probability
to the train arriving within the next 5 minutes".

With multiple statements, my favorite way of delimiting is currently
half brackets: "I think ⸤it'll rain tomorrow⸥<sub>55%</sub>, but
⸤Tuesday is going to be sunny⸥<sub>80%</sub>, but I don't think
⸤your uncle is going to be happy about that⸥<sub>15%</sub>."

The probabilities in this context aren't quite
[evidentials](https://en.wikipedia.org/wiki/Evidentiality), but neither
are they [veridicals](https://en.wikipedia.org/wiki/Veridicality) nor
[miratives](https://en.wikipedia.org/wik/Mirativity), I propose the world
"credal" for this category.

### Enumerating Possible Notations

The exact place of insertion is subtle: In sentences with a
single central statement, there are multiple locations one could place
the probability.

* After the verb related to belief: "I think<sub>55%</sub> it'll rain tomorrow."
	* Advantage: Close to the word relating to the belief (which could reflect the strength of belief in itself, using "guess"/"wager"/"think"/"believe").
	* Disadvantages:
		* Conflicts with assigning probabilities to multiple statements.
		* Puts visual clutter before the statement in question.
* At the end of the statement: "I think it'll rain tomorrow<sub>55%</sub>."
	* Advantages:
		* Allows assigning probabilities to simple statements ("It'll rain tomorrow<sub>55%</sub>") and to multiple statements (see below).
		* Allows distinguishing the beliefs of different people. "I think<sub>55%</sub> it'll rain tomorrow, but [Cú Chulainn](https://en.wikipedia.org/wiki/Cú_Chulainn) disagrees<sub>22%</sub>."
	* Disadvantage: If the probability is intended to contextualise the statement, this context is weaker if it is introduced *after* the statement in question.
* At the subject of the sentence: "I<sub>55%</sub> think it'll rain tomorrow."
	* Advantage: This can be used to distinguish the beliefs of different people. "I<sub>55%</sub> think it'll rain tomorrow, but [Cú Chulainn](https://en.wikipedia.org/wiki/Cú_Chulainn)<sub>22%</sub> is skeptical about it."
	* Disadvantage: Putting the probability before the statement the probability is about feels quite unnatural.

This becomes trickier in sentences with multiple statements.

* Probabilities after each subclaim: "I think it'll rain tomorrow<sub>55%</sub>, but Tuesday is going to be sunny<sub>80%</sub>, but I don't think your uncle is going to be happy about that<sub>15%</sub>.
	* Adding in delimiters to denote a specific subclaim the probability is about. I wonder whether there are better unicode characters for this, corner brackets might be a good candidate.
		* Lower [half brackets](https://en.wikipedia.org/wiki/Half_Bracket) (or [Quine corners](https://en.wikipedia.org/wiki/Bracket#Quine_corners_⌜⌝_and_half_brackets_⸤_⸥_or_⸢_⸣) which look almost the same): "I think ⸤it'll rain tomorrow⸥<sub>55%</sub>, but ⸤Tuesday is going to be sunny⸥<sub>80%</sub>, but I don't think ⸤your uncle is going to be happy about that⸥<sub>15%</sub>."
		* Upper half brackets to the left, lower half brackets to the right: "I think ⸢it'll rain tomorrow⸥<sub>55%</sub>, but ⸢Tuesday is going to be sunny⸥<sub>80%</sub>, but I don't think ⸢your uncle is going to be happy aboutthat⸥<sub>15%</sub>."
		* Subscripted [parentheses](https://en.wikipedia.org/wiki/Parenthesis): "I think <sub>(</sub>it'll rain tomorrow<sub>)</sub><sub>55%</sub>, but <sub>(</sub>Tuesday is going to be sunny<sub>)</sub><sub>80%</sub>, but I don't think <sub>(</sub>your uncle is going to be happy about that<sub>)</sub><sub>15%</sub>."
		* Subscripted half [guillemets](https://en.wikipedia.org/wiki/Guillemet): "I think <sub>‹</sub>it'll rain tomorrow<sub>›</sub><sub>55%</sub>, but <sub>‹</sub>Tuesday is going to be sunny<sub>›</sub><sub>80%</sub>, but I don't think <sub>‹</sub>your uncle is going to be happy about that<sub>›</sub><sub>15%</sub>."
		* And subscripted full guillemets: "I think <sub>«</sub>it'll rain tomorrow<sub>»</sub><sub>55%</sub>, but <sub>«</sub>Tuesday is going to be sunny<sub>»</sub><sub>80%</sub>, but I don't think <sub>«</sub>your uncle is going to be happy about that<sub>»</sub><sub>15%</sub>."
* I basically rule out lists of probabilities after the verb relating to each subclaim, as it's very mentally taxing to relate each probability to each claim:
	* "I think<sub>55%, 80%, 15%</sub> ⸤it'll rain tomorrow⸥, but ⸤Tuesday is going to be sunny⸥, but I don't think ⸤your uncle is going to be happy about that⸥.

#### Variants

A variant of the notation could use decimal notation instead
of percentages, and leave out trailing zeroes. "I think it'll
rain tomorrow`$_{50\%}$`" would then become the more compact "I
think it'll rain tomorrow`$_{.5}$`". This has the advantage of
being compatible with plain text through the [combining dot below
diacritic](https://en.wikipedia.org/wiki/Dot_\(diacritic\)), which would
yield "I think it'll rain tomorroẉ₅". However, the meaning of the
combining dot can be ambiguous to uninformed readers.

On [LessWrong](www.lesswrong.com), one can also use [reacts signifying
probabilities](https://www.lesswrong.com/posts/ByqKwsYK6rH6AYNDY/reacts-now-enabled-on-100-of-posts-though-still-just)
on one's own text. While it's restricted to LessWrong, it also allows
other people to easily assign different probabilities to your statements.

Since the people writing the text
reporting probabilities are probably [logically
non-omniscient](./doc/cs/ai/alignment/agent_foundations/embedded_agency_demski_garrabrant_2020.pdf)
[bounded agents](https://arbital.com/p/bounded_agent/), it might as
well be useful to report the time or effort one has spent on refining
the reported probability: "I reckon humanity will survive the 21st
century<sub>55%:20h</sub>", indicating that the speaker has reflected
on this question for 20 hours to arrive at their current probability
(something akin to reporting an "epistemic effort" for a piece of
information). I fear that this notation is getting into cumbersome
territory and won't be using it.

### Notation Options and Difficulties

There are three available options: Either ones writing platform supports
HTML, in which case one can use the `<sub>18%</sub>` tags (giving
<sub>18%</sub>), or it supports `$\LaTeX$`, which creates a sligthly
fancier looking but also more fragile notation using `_{18\%}` (resulting
in `$_{18\%}$`), or ones platform directly supports subscripting, such
as [pandoc](https://en.wikipedia.org/wiki/Pandoc) with `~18%~`, but not
Reddit Markdown (which *does* support superscript). More info about other
platforms [here](https://www.gwern.net/Subscripts.html#technical-support).

Ideally one would simply use [Unicode
subscripts](https://en.wikipedia.org/wik/Unicode_subscripts), which are
available for all digits, but tragically not for the percentage sign
'%' or a simple dot '.'. Perhaps a project for the future: After all,
they did include a subscript '+'₊, a subscript '-'₋, equality sign
'='₌ and parentheses '()'₍₎, but many subscript letters (b, c, d,
f, g, j, q, r, u, v, w, y and z) are still missing…

### Applications

I've used this notation sparingly but
increasingly, a good example of a first exploration is
[here](./range_and_forecasting_accuracy.html#Appendix_A_Replicating_Metaculus_Findings_With_Full_Data)
and interspersed in the text [here](./spans.html).

[Fischer
2023](https://forum.effectivealtruism.org/s/y5n47MfgrKvTLE3pw/p/Qk3hd6PrFManj8K6o)
uses a different notation:

> * Given hedonism and conditional on sentience, we think (credence: 0.7) that none of the vertebrate nonhuman animals of interest have a welfare range that’s more than double the size of any of the others. While carp and salmon have lower scores than pigs and chickens, we suspect that’s largely due to a lack of research.
* Given hedonism and conditional on sentience, we think (credence: 0.65) that the welfare ranges of humans and the vertebrate animals of interest are within an order of magnitude of one another.
* Given hedonism and conditional on sentience, we think (credence 0.6) that all the invertebrates of interest have welfare ranges within two orders of magnitude of the vertebrate nonhuman animals of interest. Invertebrates are so diverse
and we know so little about them; hence, our caution.

The notation proposed here would change the text:

> * Given hedonism and conditional on sentience, we think that none of the vertebrate nonhuman animals of interest have a welfare range that’s more than double the size of any of the others<sub>70%</sub>. While carp and salmon have lower scores than pigs and chickens, we suspect that’s largely due to a lack of research.
* Given hedonism and conditional on sentience, we think that the welfare ranges of humans and the vertebrate animals of interest are within an order of magnitude of one another<sub>65%</sub>.
* Given hedonism and conditional on sentience, we think that all the invertebrates of interest have welfare ranges within two orders of magnitude of the vertebrate nonhuman animals of interest<sub>60%</sub>. Invertebrates are so diverse a
nd we know so little about them; hence, our caution.

### "Share Likelihood Ratios, not Beliefs"

For sharing a likelihood ratio, we need to talk about both the hypothesis
`$H$` *and* the evidence `$E$`. If I then want to say that `$E$` updates
`$H$` by `$k$` [shannon](https://en.wikipedia.org/wiki/Shannon_\(unit\)),
how could I write that?

1. No need to invent special notation, saying "`$E$` provides `$k$` bits for/against `$H$`" is enough.
2. `$E⇅_{k}H$`, specifically `$E↑_{k}H$` if `$E$` is evidence for `$H$`, and `$E↓_{k}H$` if `$E$` is evidence *against* `$H$`.
	1. The variants `$E⇈_{k}H$` and `$E⇊_{k}H$` in cases where `$E$` is *strong* evidence.

### Discussions

* [LessWrong](https://www.lesswrong.com/posts/Tmz6ucxDFsdod2QLd/subscripts-for-probabilities)

### See Also

* [Creating a Text Shorthand for Uncertainty (Ozzie Gooen, 2013)](https://www.lesswrong.com/posts/jsfSXH8mGrLy9pPqr/creating-a-text-shorthand-for-uncertainty)
* [Interrocolon (xefer, 2008)](https://xefer.com/2008/03/interrocolon)
