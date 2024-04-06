[home](./index.md)
------------------

*author: niplav, created: 2024-04-06, modified: 2024-04-06, language: english, status: finished, importance: 5, confidence: likely*

> __Question decomposition is unreasonably effective, despite good
counter-arguments.__

On The Effectiveness Of Question Decomposition
================================================

If we say "`$X$` will happen if and only if `$Y_1$` and `$Y_2$` and
`$Y_3$`... *all* happen, so we estimate `$P(Y_1)$` and `$P(Y_2|Y_1)$`
and `$P(Y_3|Y_1, Y_2)$` &c, and then multiply them together to estimate
`$P(X)=P(Y_1)·P(Y_2|Y_1)·P(Y_3|Y_2,Y_1·)·$`…", do we usually get a
probability that is close to `$P(X)$`? Does this *improve* forecasts where
one tries to estimate `$P(X)$` directly?

This type of question decomposition (which one could
call __multiplicative decomposition__) appears to be a
relatively common method for forecasting, see [Allyn-Feuer & Sanders
2023](https://forum.effectivealtruism.org/posts/ARkbWch5RMsj6xP5p/transformative-agi-by-2043-is-less-than-1-likely),
[Silver
2016](http://fivethirtyeight.com/features/donald-trumps-six-stages-of-doom/),
[Kaufman
2011](https://www.jefftk.com/p/breaking-down-cryonics-probabilities),
[Carlsmith 2022](https://arxiv.org/abs/2206.13353) and [Hanson
2011](https://www.overcomingbias.com/p/break-cryonics-downhtml),
but there have been conceptual arguments against this technique, see
[Yudkowsky 2017](https://arbital.com/p/multiple_stage_fallacy/), [AronT
2023](https://www.lesswrong.com/posts/kmZkCmz6AiJntjWDG/multiple-stages-of-fallacy-justifications-and-non)
and [Gwern 2019](https://gwern.net/forking-path), which all argue that
it reliably underestimates the probability of events.

What is the empirical evidence for decomposition being a technique that
*improves* forecasts?

[Lawrence et al.
2006](https://www.sciencedirect.com/science/article/abs/pii/S0169207006000501)
summarize the state of research on the question:

> Decomposition methods are designed to improve accuracy by splitting
the judgmental task into a series of smaller and cognitively less
demanding tasks, and then combining the resulting judgements. [Armstrong
(2001)](https://www.researchgate.net/publication/267198099_The_Forecasting_Dictionary)
distinguishes between decomposition, where the breakdown of
the task is multiplicative (e.g. sales forecast=market size
forecast×market share forecast), and segmentation, where it is
additive (e.g. sales forecast=Northern region forecast+Western
region forecast+Central region forecast), but we will use the
term for both approaches here. **Surprisingly, there has been
relatively little research over the last 25 years into the value
of decomposition and the conditions under which it is likely to
improve accuracy. In only a few cases has the accuracy of forecasts
resulting from decomposition been tested against those of control
groups making forecasts holistically.** One exception is [Edmundson
(1990)](https://onlinelibrary.wiley.com/doi/abs/10.1002/for.3980090403)
who found that for a time series extrapolation task, obtaining separate
estimates of the trend, seasonal and random components and then combining
these to obtain forecasts led to greater accuracy than could be obtained
from holistic forecasts. Similarly, [Webby, O’Connor and Edmundson
(2005)](https://www.sciencedirect.com/science/article/abs/pii/S0169207004001049)
showed that, when a time series was disturbed in some periods by several
simultaneous special events, accuracy was greater when forecasters were
required to make separate estimates for the effect of each event, rather
than estimating the combined effects holistically. [Armstrong and Collopy
(1993)](https://core.ac.uk/download/pdf/76362507.pdf) also constructed
more accurate forecasts by structuring the selection and weighting
of statistical forecasts around the judge’s knowledge of separate
factors that influence the trends in time series (causal forces).
Many other proposals for decomposition methods have been based on an
act of faith that breaking down judgmental tasks is bound to improve
accuracy or upon the fact that decomposition yields an audit trail
and hence a defensible rationale for the forecasts ([Abramson & Finizza,
1991](https://d1wqtxts1xzle7.cloudfront.net/49278189/0169-2070_2891_2990004-f20161001-25533-1nihj7p-libre.pdf?1475369537=&response-content-disposition=inline%3B+filename%3DUsing_belief_networks_to_forecast_oil_pr.pdf&Expires=1693237828&Signature=JtQssSZv0KaUbWLf3fPA70ho1ECj9zYkBC~EnNVIrFfIgcQ5dDVeK5stSWj1tR7OQrcur7PG~y8wHNuAorqrPAjqHwEq3T88klt23BzmzXwMWUNR~ZPKimTrcDTGgrj0WcC~~gM51fzvvCJrK2hO7oPsmc-mQsgvBL5VIywRLw6-GpQjBbpILXJk90c3-JTXwWeUwhwt1zv3h6U-WAyQn-Y88tZg~R7AUFJBRAdbwV8A67o7mHcCZNbKLdluGYDgG9uC516BWr4lckSd7VcoqzfywkjpxZWTjBEFLvmJoWuSRwNvqak3SzHBO5Hv86zZ4oJtWXbxwTdsVw61JGmt6Q__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA);
[Bunn & Wright,
1991](https://www.researchgate.net/profile/George-Wright-11/publication/227446292_Interaction_of_Judgemental_and_Statistical_Forecasting_Methods_Issues_Analysis/links/0c9605375ff870d3c9000000/Interaction-of-Judgemental-and-Statistical-Forecasting-Methods-Issues-Analysis.pdf);
[Flores, Olson, & Wolfe,
1992](https://www.sciencedirect.com/science/article/abs/pii/0169207092900277);
[Saaty &
Vargas, 1991](https://link.springer.com/book/9789401579544); [Salo & Bunn, 1995](https://d1wqtxts1xzle7.cloudfront.net/56667412/0040-1625_2894_2900050-720180527-12155-ptp70l-libre.pdf?1527455229=&response-content-disposition=inline%3B+filename%3DDecomposition_in_the_assessment_of_judgm.pdf&Expires=1693237988&Signature=Np4MDK~nFPb3xPknH2QaBnyOnnYT8FPgpsx7PTKkZEhmPVRQ5RTKSKzOQ7j9KDstvWfF~X7pIQdd~OJxn4OntioCsEPCPxRzLtOUscn3~UuGBnWYNsZ4JO8iBaREvH2N~DL0um~6moufhk69-lNkSjV~x2MLC5KMDBGJUwbxSwZmTp0sx3vANfZGpq~~f5ojnSkSfVJ1NYvWr82KK5UUxtU08HtGsSqOKlBB8NA7~IxsTcJnUKONHm5lczVeWq8KBEMGaNLI0GBr1y4e2bPA~Y8aKcCqnDbsOriQ0f7rNclqsY-cEEarUmd8UXRFJZc6vtPjgdF5Xv0CgrPEGIh0xA__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA);
[Wolfe & Flores,
1990](https://onlinelibrary.wiley.com/doi/abs/10.1002/for.3980090407)).
Yet, as [Goodwin and Wright
(1993)](https://d1wqtxts1xzle7.cloudfront.net/46103856/0169-2070_2893_2990001-420160531-2191-1mlbayr-libre.pdf?1464718211=&response-content-disposition=inline%3B+filename%3DImproving_judgmental_time_series_forecas.pdf&Expires=1693238053&Signature=PDCGfnyMHtluH1q9RsZffGSGZU02oBJZvEFChvofGx0nzBDrpCnlErCwx5OFUv0rXIRsULnJL~LA57rWsRXBEXcAbUtaObpC6rJTmAqe1RJLkDE59eD7787zBpqxYCkBHx5-uOou2gPpBCrxpMzc9JS3zDt4HXSs3eiXMzhzw0jPHkPyYGPwIFK5Xae1JVOkmZccnBe-9QwZhwyIcLEqoEWIoAr34d2EW19zendk~9NA182Kaf4MgKXaUCzMxSwcyMIWfoJ5K~VdfWr5Cf1LOToCb638Nn354gpcOtTX~gwCfaK0lwWcqc9Ew-3AJ7w7EBtStETgW3rSbOvuSV9WrA__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA)
point out, decomposition is not guaranteed to improve accuracy and may
actually reduce it when the decomposed judgements are psychologically more
complex or less familiar than holistic judgements, or where the increased
number of judgements required by the decomposition induces fatigue.

(Emphasis mine).

The types of decomposition described here seem quite different from
the ones used in the sources above: Decomposed time series are quite
dissimilar to multiplied probabilities for binary predictions, and in
combination with the conceptual counter-arguments the evidence appears
quite weak.

It appears as if a team of a few (let's say 4) dedicated forecasters could
run a small experiment to determine whether multiplicative decomposition
for binary forecasts a good method, by randomly spending 20 minutes either
making explicitely decomposed forecasts or control forecasts (although
the exact method for control needs to be elaborated on). Working in
parallel, making 70 forecasts should take $70 \text{ forecasts} \cdot \frac{1 \text{hr}}{3 \text{ forecasts}} \cdot \frac{1}{4}
\approx 5.8\text{hr}$ less than 6 hours, although it'd be useful to search for
more recent literature on the question.

* Would decomposition work better if one were operating with log-odds instead of probabilities?

Classification and Improvements
--------------------------------

The description of such decomposition in [this
section](#Forecasting_Techniques) is, of course, lacking: A
*better* way of decomposition would be, for a specific outcome,
to find a set of preconditions for `$X$` that are [mutually
exclusive](https://en.wikipedia.org/wiki/Mutually-exclusive)
and [collectively
exhaustive](https://en.wikipedia.org/wiki/Collectively_exhaustive), find
a chain that precedes them (or another MECE decomposition), and iterate
until a whole (possibly interweaving) tree of options has been found.

Thus one can define three types of question decomposition:

1. __Multiplicative Decomposition__: Given an event `$X$`, find conditions `$Y_1, \dots Y_n$` so that `$X$` if any only if all of `$Y_1, \dots, Y_n$` happen. Estimate `$P(Y_1)$` and `$P(Y_2|Y_1)$` and `$P(Y_3|Y_1, Y_2)$` &c, and then mult
iply them together to estimate `$P(X)=P(Y_1)·P(Y_2|Y_1)·P(Y_3|Y_2,Y_1·) \dots P(Y_n | Y_{n-1}, \dots, Y_2, Y_1)$`.
2. __Additive Decomposition__ or __[ME](https://en.wikipedia.org/wiki/Mutually-exclusive)[CE](https://en.wikipedia.org/wiki/Collectively_Exhaustive_Events) Decomposition__: Given an event `$X$`, find a set of scenarios `$Y_1, \dots Y_n$`
such that `$X$` happens if any `$Y$` happens, and only then, and no two `$Y_k, Y_l$` have `$P(Y_k \cap Y_l)>0$`. Estimate `$P(Y_1), P(Y_2), \dots P(Y_n)$` and then estimate `$P(X)=\sum_{i=1}^n P(Y_i)$`.
3. __Recursive Decomposition__: For each scenario `$X'$`, decide to pursue one of the following strategies:
        1. Estimate `$P(X')$` directly
        2. Multiplicative decomposition of `$P(X')$`
                1. Find a multiplicative decomposition `$Y_1', \dots Y_n'$` for `$X'$`
                2. Estimate `$P(Y_1'), \dots P(Y_n' | Y_1', \dots Y_{n-1}')$` each via recursive decomposition
                3. Determine `$P(X')=P(Y_1')·P(Y_2'|Y_1')·P(Y_3'|Y_2', Y_1') \dots P(Y_n' | Y_{n-1}', \dots, Y_2', Y_1')$`.
        3. Additive decomposition of `$P(X')$`
                1. Find a multiplicative decomposition `$Y_1', \dots Y_n'$` for `$X'$`
                2. Estimate `$P(Y_1'), \dots P(Y_n')$` each via recursive decomposition
                3. Determine `$P(X')=P(Y_1')+P(Y_2')+ \dots P(Y_n')$`.

A keen reader will notice that recursive decomposition is similar to
[Bayes nets](https://en.wikipedia.org/wiki/Bayesian_Network). True, though
it doesn't deal as well with conditional probabilities.

Using LLMs
-----------

This is a scenario where large language models are quite useful, and
we have a testable hypothesis: Does question decomposition (or MECE
decomposition) improve language model forecasts by any amount?

Frontier LLMs are [at](https://dynomight.net/predictions/)
[best](https://www.lesswrong.com/posts/c3cQgBN3v2Cxpe2kc/getting-gpt-3-to-predict-metaculus-questions)
[mediocre](https://arxiv.org/pdf/2206.15474v1) at
forecasting real-world events, but similar to how [asking
for calibration](https://arxiv.org/pdf/2305.14975v2)
improves performance, so perhaps
[chain-of-thought](https://blog.research.google/2022/05/language-models-perform-reasoning-via.html)-like
question decomposition improves (or reduces) their performance (and
therefore gives us reason to believe that similar practices will (or
won't) work with human forecasters).

Direct:

        Provide your best probabilistic estimate for the following
        question. Give ONLY the probability, no other words or
        explanation. For example:
        0.1
        Give the most likely guess, as short as possible; not a complete
        sentence, just the guess!
        The question is: ${QUESTION}.
        ${RESOLUTION_CRITERIA}.

Multiplicative decomposition:

        Provide your best probabilistic estimate a question.

        Your output should be structured in three parts.

        First, determine a list of factors X₁, …, X_n that are necessary
        and sufficient for the question to be answered "Yes". You can choose
        any number of factors.

        Second, for each factor X_i, estimate and output the conditional
        probability P(X_i|X₁, X₂, …, X_{i-1}), the probability that X_i
        will happen, given all the previous factors *have* happened. Then, arrive
        at the probability for Q by multiplying the conditional probabilities
        P(X_i):

        P(Q)=P(X₁)*P(X₂|X₁)…P(X_n|X₁, X₂, …, X_{n-1}).

        Third and finally, In the last line, report P(Q), WITHOUT ANY ADDITIONAL
        TEXT. Just write the probability, and nothing else.

        Example (Question: "Will my wife get bread from the bakery today?"):

        Necessary factors:
        1. My wife remembers to get bread from the bakery.
        2. The car isn't broken.
        3. The bakery is open.
        4. The bakery still has bread.

        1. P(My wife remembers to get bread from the bakery)=0.75
        2. P(The car isn't broken|My wife remembers to get bread from the bakery)=0.99
        3. P(The bakery is open|The car isn't broken, My wife remembers to get bread from the bakery)=0.7
        4. P(The bakery still has bread|The bakery is open, The car isn't broken, My wife remembers to get bread from the bakery)=0.9
        Multiplying out the probabilities: 0.75*0.99*0.7*0.9=0.467775
        0.467775
        (End of output)
        The question is: ${QUESTION}.
        ${RESOLUTION_CRITERIA}

### Small Experiment

Using the metaculus data in [iqisa](./iqisa.html), I test whether
gpt-4-0613 outperforms when multiplicative decomposition, compared to
direct estimation.

__I find that, on a sample of 100 questions from after the end
of training, *multiplicative decomposition* outperforms *direct
estimation*.__

Forecasts produced by direct estimation have a logscore of -0.439,
while forecasts produced by multiplicative decomposition have a logscore
of -0.206.

This goes against [my
prediction](https://fatebook.io/q/multiplicative-decomposition-of-a--cluns2mz10003l408adz3aw37)
that direct estimation would outperform multiplicative
decomposition<sub>[75%](https://fatebook.io/q/multiplicative-decomposition-of-a--cluns2mz10003l408adz3aw37)</sub>.

#### Description

Code [here](https://github.com/niplav/decomposer).

I load the forecasting data in iqisa, and filter to select questions
which resolved after the release of GPT-4 in March 2023:

        questions=metaculus.load_questions(data_dir='../iqisa/data')
        end_training_data=datetime.fromisoformat('2023-04-30')
        not_in_training_data=questions.loc[(questions['q_status']=='resolved') & (questions['resolve_time']>=end_training_data)]

I then loop over `not_in_training_data`, replace `\${QUESTION}` in
the prompts with the questions and `\${RESOLUTION_CRITERIA}` with the
resolution criteria. I send the resulting prompt over the OpenAI API,
and save the result in a separate file. The resulting files can be found
[here](https://github.com/niplav/decomposer/tree/main/completions),
file format is `\${QUESTION_ID}_\${METHOD}_completion$`.

I then [load the last line from each
file](https://github.com/niplav/decomposer/blob/main/analyser.py), and
calculate the [log-score](https://en.wikipedia.org/wiki/Log_scoring_rule)
of the individual forecasts.

#### Conclusion

I have changed my mind as a result of this experiment: I previously
believed that multiplicative decomposition would result in worse
forecasts, name ones that are too close to 0%, with respect to good
calibration.

My best guess now is that multiplicative decomposition *has that
effect*, but that it also encourages thinking more deeply and clearly
about the question, and that this outweighs the effect from pushing
the probabilities towards zero. This should also hold for truth-seeking
humans.

It also suggests another experiment: Instructing the language
model to "think about the question step by step", without
any specific instructions how to do so, would outperform multiplicative
decomposition<sub>[55%](https://fatebook.io/q/instructing-to-think-about-the-question--clunyjnwf0001l708pz9k1xv7)</sub>
if my understanding is correct.

Discussions
------------

* [LessWrong](https://www.lesswrong.com/posts/YjZ8sJmkGJQhNcjHj/the-evidence-for-question-decomposition-is-weak)
* [Effective Altruism Forum](https://forum.effectivealtruism.org/posts/beRtXkMpCT39y8bPj/there-is-little-evidence-on-question-decomposition)
