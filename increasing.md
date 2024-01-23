[home](./index.md)
------------------

*author: niplav, created: 2023-07-06, modified: 2024-01-17, language: english, status: notes, importance: 6, confidence: possible*

> __Humans get around 80 years of life. How can that time be made to
feel as long as possible?__

Increasing Subjective Lifespan
================================

[Existing](http://theoryengine.org/life/tips-for-a-longer-life/)
[investigations](https://www.wikihow.com/Slow-Down-Time)
are not well cited, don't consider trade-offs and costs
or effect sizes, given that subjective time is all one has,
it'd be good to have a reliable guide to lengthening it. [Ethan
2023](https://210ethan.github.io/research/slow.html) is the best resource
I currently know of, but a more comprehensive resource including effect
sizes, costs and benefits appears worthwhile to create.

This is *not* about extending healthspan, either by prosaic or
medical interventions, or curing aging, for overview into that see [JackH
2020](https://www.lesswrong.com/posts/RcifQCKkRc9XTjxC2/anti-aging-state-of-the-art)
and [Ricón 2021](https://nintil.com/longevity).

| Intervention | [Net present value](https://en.wikipedia.org/wiki/Net_Present_Value) | State of evidence | Papers | Notes |
| ----------------------------- | -------------------------------------------------------------------- | -------------------------------- | -------| ----- |
| Meditating 2.5 hours per day → Reduces sleep need | \$33k | Poor, a single case study (n=7) | [Kaul et al. 2010](./doc/meditation/science/meditation_acutely_improves_psychomotor_vigilance_and_may_decrease_sleep_need_kaul_et_al_2010.pdf) | Can also confer [other benefits](https://en.wikipedia.org/wiki/Research_on_Meditation), but multiple hours of meditation per day [could be risky](https://harpers.org/archive/2021/04/lost-in-thought-psychological-risks-of-meditation/) | <!--TODO: maybe link MCTB here?-->
| Taking melatonin → Reduces sleep need | \$7.5k | Data collected from two individuals (n=2) | [Gwern 2019](https://www.gwern.net/Melatonin#tempus-fugit), [Niplav 2024](./nootropics.html#Reducing_Sleep_Duration) | Low risk |


Reducing Time Slept
--------------------

[Harsimony 2021](https://harsimony.wordpress.com/2021/02/05/why-sleep/)
argues that we should reduce sleep need, pointing out that these ~30%
of our lives might be better spent on other activities, be they conscious
leisure or work.

Beliefs are for action, all statistics is decision theory. In choosing
how (much) to sleep, and in what way, we want to trade off benefits
against costs. The benefit of sleeping less is quite straightforward:
More time spent awake, either in leisure or working, making more use of
the limited amount of time we have before dying.

The costs are more subtle: Some intervention we're considering might have
negative side effects, either only on the hours gained or on all of the
hours spent awake, or having an effect on expected lifespan.  So we have
to decide how much we (e.g.) (dis)value spending an additional hour awake,
but being 5% more dizzy during those 17 waking hours.

<!--https://www.healthline.com/health/how-to-sleep-8-hours-in-4-hours-->

### Drugs

#### Melatonin

<!--TODO: incorporate info from two meta-analyses linked in twitter replies-->

##### Gwern 2019

[Gwern 2019](https://www.gwern.net/Melatonin#tempus-fugit):

> My rule of thumb is melatonin subtracts an hour [of sleep
time]. (I originally guessed at this value, but my Zeo
sleep recordings seem to suggest the value is [more like 50
minutes](https://www.gwern.net/Zeo.html#melatonin-analysis).) That is:
if one slept for 7 hours, one awakes as refreshed as if one had slept
for 8 hours etc. From comparing with others, I think I benefit more than
around two-thirds of people.

##### Niplav 2024

I [analyze](./nootropics.html#Reducing_Sleep_Duration) my own data,
and (weakly) conclude that melatonin reduces my sleep duration by ~25
minutes, although I have not checked whether melatonin simply makes my
body go into sleep debt which is then paid off the next night.

##### Cost-Benefit

Assuming a (conservative) 15 minutes of sleep time saved, at a price of
~4 cent per pill, assuming the benefit does not taper off, we get a net
present value (over the next 40 years) of

`$\sum_{i=0}^{40} \frac{365 \cdot (0.25 \text{hr} \cdot 5 \frac{\$}{\text{hr}})}{1.05^i} \approx \$7578$`.

#### Orexin-A

> If you are a naive reader, you might expect that we give people
with narcolepsy type 1 orexin-A as a supplement because that would be
obvious. We don’t. You might expect that someone tried to bring it to
market as a drug and ran a clinical trial. They didn’t.  
> The problem seems to be that the solution is too obvious. The patent
office likely decided that the solution would be too obvious to give
out a [patent for it](https://qr.ae/pvWJAr), and thus the narcoleptic
patients are without orexin-A supplementation unless they go through
[efforts](https://forum.biohack.me/index.php?p=/discussion/1075/orexin-a-group-purchase)
to procure it themselves.

*—[ChristianKl](https://www.lesswrong.com/users/christiankl), [“Orexin and the quest for more waking hours”](https://www.lesswrong.com/posts/sksP9Lkv9wqaAhXsA/orexin-and-the-quest-for-more-waking-hours), 2022*

<!--TODO: check up on Orexin agonists!-->

#### Others

Selected from [Harsimony 2023](https://harsimony.wordpress.com/2023/01/20/research-areas-for-reducing-sleep-need/):

* Modafinil
* Neuropeptide S
* S-Adenosyl methionine
* Sodium Oxybate

### Meditation

> While it may be true that, when doing intensive practice, the need
for sleep may go down to perhaps four to six hour or less at a time,
try to get at least some sleep every night.

*—Daniel Ingram, “Mastering the Core Teachings of the Buddha”, p. 179*

> Meditation in dreams and lucid dreaming is common in this territory
[of the Arising and Passing away]. The need for sleep may be greatly
reduced. […] The big difference between the A&P and Equanimity is that this
stage is generally ruled by quick cycles, quickly changing frequencies
of vibrations, odd physical movements, strange breathing patterns, heady
raptures, a decreased need for sleep, strong bliss, and a general sense
of riding on a spiritual roller coaster with no brakes.

*—Daniel Ingram, “Mastering the Core Teachings of the Buddha”, p. 275*

> Need for sleep tends to increase in the Three Characteristics, mostly
due to how tiring pain can be. Sleep need can drop dramatically in the
stage of the A&P, suddenly peak in dissolution, drop a bit again in Fear
as our energy returns, and increase during the Dark Night, mostly due
to how mentally fatiguing that stage can be.

> ![](./img/increasing/ingram_sleep_chart.png)

*—Daniel Ingram, “Mastering the Core Teachings of the Buddha”, p. 379*

Note: as far as I know, this chart is not based on any data collected,
but on the personal experience of Ingram and his acquaintances.

> The interesting thing is that all four of these people within a year
or so of having started this practice claimed to have done it, and by
“it” I mean eliminated all emotions entirely, replacing them with a
perpetually wonderful perception of the freshness of the sensate world,
a lack of time pressure, a reduced need for sleep, and some other benefits
and odd side effects.

*—Daniel Ingram, “Mastering the Core Teachings of the Buddha”, p. 462*

> The sleep models generally relate to either sleeping less or being
awake in some way while asleep. Sleeping less is common during retreats,
particularly in some stages such as the A&P. I also know some people who,
because of spiritual attainments, have reduced their need for sleep,
and this has happened to me at points, but it hasn't been sustained in
my case.

*—Daniel Ingram, “Mastering the Core Teachings of the Buddha”, p. 470*

#### Kaul et al. 2010

[Kaul et al.
2010](./doc/meditation/science/meditation_acutely_improves_psychomotor_vigilance_and_may_decrease_sleep_need_kaul_et_al_2010.pdf)
find that long-term meditators sleep ~2.5h less at 2.3h meditation/day,
which suggests that one can reap the benefits of meditation while also
increasing the time spent lucid, if one values time in meditation half
as much as other waking time at \$2.5/hr. This gives a [net present
value](https://en.wikipedia.org/wiki/Net_Present_Value) over the next
40 years of

`$\sum_{i=0}^{40} \frac{365 \cdot \$5/\text{hr} \cdot 2 \text{hr} \cdot 0.5}{1.05^i} \approx \$33140$`.

The quality of the evidence here is very slim, but anecdotes point
towards sleep durations decreasing during meditation retreats. It would
be quite interesting to know the relation between time spent meditating
and amount of time slept.

### Behavioral Interventions

* Sleep Hygiene
* Cognitive Behavioral Therapy
* Polyphasic Sleep
* Unihemispheric Sleep
* Going to Bed Later and Waking Up At The Same Time
* Going to Bed At The Same Time And Waking Up Earlier

> There are two plausible ways to cut sleep duration without harming
cognition: increasing the proportion of slow wave sleep that is spent
in deep sleep and reducing REM sleep.

*—[Angela Pretorius](https://www.lesswrong.com/users/angela-pretorius), [LessWrong comment](https://www.lesswrong.com/posts/sksP9Lkv9wqaAhXsA/orexin-and-the-quest-for-more-waking-hours?commentId=L6HTekbs6hrCdATAv), 2022*

### Other Interventions

#### Reducing Sleep Inertia

#### Stimulation

* Transcranial Direct-Current Stimulation
* Transcranial Magnetic Stimulation

### Genes

<!--https://forum.effectivealtruism.org/posts/nSwaDrHunt3ohh9Et/cause-area-short-sleeper-genes-->
<!--https://harsimony.wordpress.com/2021/02/05/why-sleep/-->
<!--https://harsimony.wordpress.com/2022/07/14/cause-exploration-prize-application/-->

> Sleep takes up a sizeable fraction of our lives and has major effects on
life quality, making improvements in quality or wakefulness an ethically
relevant topic [2392]. It appears that mutations in the genes DEC2 [1332,
1372], ADRB1[2639], NPSR1 [3113], GRM1 [2640] can enable reductions in
sleep without negative consequences [3137, 3167].][sic]

* [2392] An Ravelingien and A Sandberg. Sleep better than medicine? ethical issues related to “wake enhancement”. Journal of Medical Ethics, 34(9):e9–e9, 2008.
* [1332]: [He et al. 2009](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2884988/ "Ying He, Christopher R Jones, Nobuhiro Fujiki, Ying Xu, Bin Guo, Jimmy L Holder Jr, Moritz J Rossner, Seiji Nishino, and Ying-Hui Fu. The transcriptional repressor dec2 regulates sleep length in mammals. Science, 325(5942):866–870, 2009")
* [1372] Arisa Hirano, Pei-Ken Hsu, Luoying Zhang, Lijuan Xing, Thomas McMahon, Maya Yamazaki, Louis J Ptáček, and Ying-Hui Fu. Dec2 modulates orexin expression and regulates sleep. Proceedings of the National Academy of Sciences, 115(13):3434–3439, 2018.
* [2639] Guangsen Shi, Lijuan Xing, David Wu, Bula J Bhattacharyya, Christopher R Jones, Thomas McMahon, SY Christin Chong, Jason A Chen, Giovanni Coppola, Daniel Geschwind, et al. A rare mutation of β1-adrenergic receptor affects sleep/wake behaviors. Neuron, 103(6):1044–1055, 2019.
* [3113] Lijuan Xing, Guangsen Shi, Yulia Mostovoy, Nicholas W Gentry, Zenghua Fan, Thomas BMcMahon, Pui-Yan Kwok, Christopher R Jones, Louis J Ptáˇcek, and Ying-Hui Fu. Mutant neuropeptide s receptor reduces sleep duration with preserved memory consolidation. Science translational medicine, 11(514):eaax2014, 2019.
* [2640] Guangsen Shi, Chen Yin, Zenghua Fan, Lijuan Xing, Yulia Mostovoy, Pui-Yan Kwok, Liza H Ashbrook, Andrew D Krystal, Louis J Ptáˇcek, and Ying-Hui Fu. Mutations in metabotropic glutamate receptor 1 contribute to natural short sleep trait. Current Biology, 31(1):13–24, 2021.
* [3137] Ji Hyun Yook, Muneeba Rizwan, Noor ul ain Shahid, Noreen Naguit, Rakesh Jakkoju, Sadia Laeeq, Tiba Reghefaoui, Hafsa Zahoor, and Lubna Mohammed. Some twist of molecular circuitry fast forwards overnight sleep hours: A systematic review of natural short sleepers’ genes. Cureus, 13(10), 2021.
* [3167] Liubin Zheng and Luoying Zhang. The molecular mechanism of natural short sleep: A path towards understanding why we need to sleep. Brain Science Advances, 2022.

See also [JohnBoyle
2022](https://forum.effectivealtruism.org/posts/nSwaDrHunt3ohh9Et/cause-area-short-sleeper-genes),
and a [skeptical
comment](https://forum.effectivealtruism.org/posts/nSwaDrHunt3ohh9Et/cause-area-short-sleeper-genes?commentId=GCQf5qjG4LyEdEJov)
on the state of research on these genes.

Slowing Down Subjective Experience of Time
-------------------------------------------

### Behavioral Interventions

### Drugs

* [The Pseudo-Time Arrow: Explaining Phenomenal Time With Implicit Causal Structures In Networks Of Local Binding (Andrés Gomez Emilsson, 2018)](https://qualiacomputing.com/2018/11/28/the-pseudo-time-arrow-explaining-phenomenal-time-with-implicit-causal-structures-in-networks-of-local-binding/): Inducing exotic states of time experience.

### Meditation

### Other

* Being scared: <http://www.livescience.com/2117-time-slow-emergencies.html>

Making Sleep More Lucid
------------------------

### Dreams

#### Lucid Dreaming

##### Behavioral Interventions

> While self-assessed numbers of awakenings, polyphasic sleep and
physiologically validated wake-REM sleep tran- sitions were associated
with lucid dreaming, neither self-assessed sleep quality, nor physiologi-
cally validated numbers of awakenings were.

*–Gott et al., “Sleep fragmentation and lucid dreaming”, 2019*

##### Drugs

* Galantamine (h/t [Chapin](https://twitter.com/sashachapin/status/1743332700143174124))
