[home](./index.md)
------------------

*author: niplav, created: 2023-01-17, modified: 2023-01-28, language: english, status: notes, importance: 7, confidence: unlikely*

> __I investigate whether the attention span of individual humans has
been falling over the last two decades (prompted by curiosity about
whether the introduction of the internet may be harmful to cognitive
performance). I find little direct work on the topic, despite its wide
appeal, but reviewing related research indicates that individual attention
spans might have been declining`$_{75\%}$`.__

Have Attention Spans Been Declining?
=====================================

In what might be just the age-old regular
[ephebiphobia](https://en.wikipedia.org/wiki/Ephebiphobia),
claims have been raised that individual attention spans [have been
declining](#Appendix_A_Claims_That_Attention_Spans_Have_Been_Declining)—not
just among adolescents but also among the general population. If so,
this would be quite worrying: Much of the economy in industrialized
societies is compromised of knowledge work, and knowledge work depends
on attention to the task at hand; switching between tasks too often
might prevent progress on complicated and difficult tasks.

I became interested in the topic after seeing several claims that
e.g. [Generation Z](https://en.wikipedia.org/wiki/Generation_Z) allegedly
has lower attention spans, observing myself and how I struggled to get
any work done when having an internet connection, and reports of others
online of having the same problem.<!--I was finally convinced to actually
investigate the topic™ by a comment on LessWrong asking the question
(TODO: link) receiving a surprisingly large amount of upvotes.-->

The exact question being asked is

__"Have the attention spans of individuals on neutral tasks (that is,
tasks that are not specifically intended to be stimulating) declined
from 2000 to the present?"__

(One might also formulate it as "Is there an equivalent of the “Negative
Flynn Effect” for attention span?".) I am not particularly wedded to
the specific timeframe, though the worries mentioned above assert that
this has become most stark during the last decade or so, attributing the
change to widespread social media/smartphone/internet usage. Data from
before 2000 or just the [aughts](https://en.wikipedia.org/wiki/Aughts)
would be less interesting. The near-global [COVID-19
lockdows](https://en.wikipedia.org/wiki/COVID-19_lockdowns)
could provide an especially enlightening [natural
experiment](https://en.wikipedia.org/wiki/Natural_experiment): Did
social media usage increase (my guess: yes`$_{90\%}$`, and if so, did
attention spans decrease at the same time (or with a lag) (my guess:
also yes`$_{70\%}$`, but I don't think anyone has the data on that *and*
wants to share it).

Ideally want to have experiments from up to 2019: close enough
to the present to see whether there is a downward trend (a bit
more than a decade after the introduction of the [iPhone in
2007](https://en.wikipedia.org/wiki/iPhone_\(1st_generation\))),
but before the [COVID-19
pandemic](https://en.wikipedia.org/wiki/COVID-19_pandemic) which might
be a huge confounder, or just have accelerated existing trends (which
we can probably check in another 2 years).

I am interested in the attention
span of individual humans: [Lorenz-Spreen et al.
2019](./doc/psychology/attention_span/accelerating_dynamics_of_collective_attention_lorenz-spreen_et_al_2019.pdf
"Accelerating dynamics of collective attention") investigate the
development of a construct they call "collective attention" (and indeed
find a decline), but that seems less economically relevant than individual
attention span. I am also far less interested in self-perception of
attention span, give me data from a proper power- or speed-test<!--TODO:
links-->, cowards!

So the question I am asking is not

* "Does more social media/internet usage cause decreased attention spans?"
* "Does more social media/internet usage correlate with decreased attention spans?"
* "Does more social media/internet usage correlate with people reporting having shorter attention spans?"
* "Did collective attention spans decrease?"

How Is Attention Span Defined?
-------------------------------

[Attention](https://en.wikipedia.org/wiki/Attention) is generally
divided into three distinct categories: **sustained attention**,
which is the consistent focus on a specific task or piece of
information over time (Wikipedia states that the span for sustained
attention has a [leprechaun](https://www.gwern.net/Leprechauns)
figure of 10 minutes floating around, elaborated on in [Wilson &
Korn 2007](./doc/psychology/attention_span/attention_during_lectures_beyond_ten_minutes_wilson_korn_2007.pdf)); **selective attention**, which is
the ability to resist distractions while focusing on important
information while performing on a task (the thing trained during
[mindfulness meditation](https://en.wikipedia.org/wiki/Mindfulness));
and **alternating** or **divided attention**, also known as the ability to
[multitask](https://en.wikipedia.org/wiki/Human_multitasking).

<!--Alternative partitioning in *arousal*, *capacity* and *selectity*. See
Plude et al., 1994 p. 4-->

When asking the question "have attention spans been declining",
we'd ideally want the same test measuring all those three aspects of
attention (and not just asking people about their [perception via
surveys](https://guzey.com/statistics/dont-believe-self-reported-data/)),
performed anually on large random samples of humans over decades,
ideally with additional information such as age, sex, intelligence (or
alternatively educational attainment), occupation etc. I'm personally
most interested in the development of sustained attention, and less so
in the development of selective attention. But I have not been able to
find such research, and in fact there is apparently no agreed upon test
for measuring attention span in the first place:

> She studies attention in drivers and witnesses to crime and says the
idea of an "average attention span" is pretty meaningless. "It's very
much task-dependent. How much attention we apply to a task will vary
depending on what the task demand is."

*— Simon Maybin quoting Dr. Gemma Briggs, [“Busting the attention span myth”](https://www.bbc.com/news/health-38896790), 2017*

(So, [similar to
comas](https://slatestarcodex.com/2014/08/11/does-the-glasgow-coma-scale-exist-do-comas/),
attention span doesn't exist…sure, [super-proton things come in
varieties](https://unremediatedgender.space/2019/Dec/on-the-argumentative-form-super-proton-things-tend-to-come-in-varieties/index.html "On the Argumentative Form "Super-Proton Things Tend to Come In Varieties"),
but **_which varieties_**?? And how??? Goddamn,
psychologists, do your job and don't just
[worship](https://www.lesswrong.com/rationality/explain-worship-ignore "Explain/Worship/Ignore?")
complexity.)

How Do We Measure Attention Span?
----------------------------------

One of my hopes was that there is a canonical and well-established (and
therefore, ahem, *tested*) test for attention span (or just attention)
à la the IQ test for *g*: If so, I would've been able to laboriously go
through the literature on attention, extract the individual measurements
(and maybe even acquire some datasets) and perform a meta-analysis.

* [Wilson & Korn 2007](./doc/psychology/attention_span/attention_during_lectures_beyond_ten_minutes_wilson_korn_2007.pdf) report several different measures of attention span during lectures: the amount of notes taken over time<!--TODO: McKeachie (1986, 1999)-->, observation of the students by an author of one study<!--TODO: Lloyd 1968--> or two independent observers in another study<!--TODO: Johnstone and Percival (1976)-->, retention of material after the lecture<!--TODO: McLeish 1986-->, self-report in 5-minute intervals during the lecture<!--TODO: Stuard & Rutherford 1978-->, and heart rate<!--TODO: Bligh 2000-->. They also note that "Researchers use behaviors such as fidgeting, doodling, yawning, and looking around as indicators of inattentiveness (e.g., Frost, 1965; Johnstone & Percival, 1976)."
* [Plude et al. 1994]() review how selective attention develops during a human life. For measuring attentino, they mainly focus on studies using reaction time as a metric—the speed at which an action occurs as a result of a changing stimulus: eye movement patterns of infants, simple tests such as pressing a button on a changing (often visual) stimulus, the influence of irrelevant visual stimuli at the periphery on a task performed at the centre of the visual field, judging similarity of stimuli at various distances in the visual field!--Enns and Girgus, 1985-->, responding to a target stimulus surrounded by interfering distractor stimuli, and determining whether a visual target item is present or absent<!--TODO: continue-->. They also mention skin conductance (measuring arousal)<!--TODO: continue-->.
	* They also mention studies investigating the time required for attentional switching in acoustic contexts: "Pearson and Lane (1991a) studied the time course of the attention-shifting process between lists and also found large age-related improvements between 8 and 11 years. Whereas 8-year-olds required more than 3.5 s to completely switch from monitoring one list to another, 11-year-olds and adults appeared to complete the switch in less than 2.5 seconds."

But, as it stands, I don't think that such a metric exists`$_{35\%}$`:
The set of listed measures I found appears to be too heterogenous and
mostly not quantitative enough for me to pick and drill down on.

What Are the Existing Investigations?
-------------------------------------

* [Gausby 2015](./doc/psychology/attention_span/attention_spans_gausby_et_al_2015.pdf)
	* Methods for assessing attention span:
		* Three online tests (probably devised by the authors (?), since no source is given) (n≈2000 Canadians). Very little information about the exact nature of the tests.
			* Sustained attention span: "Counting the number of times responds correctly identified an X occurring after an A."
			* Selective attention span: "Counting the number of times respondents correctly identified a change in the orientation of the rectangles"
			* Alternating attention span: "Calculating the difference in the time lapsed to perform a series of consecutive number or letter classification, compared to a mixture of number and letter classifications."
		* Neurological research: The same games/tests as above with the participants being measured with an EEG ("Results were reported as ACE (Attention, Connectivity, Encoding) scores, as well as the number of attention bursts") (n=112 Canadians)
	* Questions answered:
		* Sustained attention:
			* *Do younger people perform worse on the sustained attention span test?*, Yes (31% high sustained attention for group aged 18-34, 34% for group aged 35-54, and 35% group aged 55+) (the methodology is wholly unclear here, though: how do we determine the group that has "high sustained attention span"? Did they perform any statisitical tests? If yes, which?).
			* *Do people who report more technology usage (web browsing/multi-screen usage while online/social media usage/tech adoption) perform worse on the sustained attention span test?*, Yes. Light:medium:heavy usage for web browsing has 39%:33%:27% users with high sustained attention span, 36%:33%:27% for light:medium:heavy multi-screen usage, 36%:29%:23% for light:medium:heavy social media usage and 35%:31%:25% for light:medium:heavy tech adoption (though these numbers are basically not elaborated on).
		Selective attention:
			* *Do younger people perform worse on the selective attention span test?* No (34% high selective attention for group aged 18-34, 30% for group aged 35-54, and 35% group aged 55+).
			* *Do people with high selective attention use fewer devices at the same time?* Yes (details p. 31).
		* Alternating attention:
			* *Do younger people perform worse on the alternating attention span test?* No (36% high selective attention for group aged 18-34, 28% for group aged 35-54, and 36% group aged 55+).
			* *Do people who report more technology usage (tech adoption/web browsing/multi-screen usage while online) perform worse on the alternating attention span test?* No, they seem to perform better: Light:medium:heavy tech adoption corresponds to 31%:39%:40% having high alternating attention spans, light:medium:heavy web browsing to 29%:34%:37% and multi-screening while online to 27%:32%:37%.
			* *Do people who use social media more have higher Attention/Connection/Encoding scores on EEG measurements?*, Not quite: "Moderate users of social media are better at multi-tasking than lower users. But, when crossing into the top quartile of social media usage, scores plummet."
	* This is a marketing statement wearing the skinsuit of a previously great paper, it would be awesome if they released their exact methodology (tests performed, data collected, exact calculations & code written). I can smell that they actually put effort into the research: Creating an actual test instead of just asking respondents about their attention spans, doing EEG measurements of over 100 people, for 3 different types of attention…come on! Just put out there what you did!
* [Carstens et al. 2018](./doc/psychology/attention_span/social_media_impact_on_attention_span_carstens_et_al_2018.pdf) (n=209 American respondents to a survey)
	* Questions answered:
		* *Is self-reported attention span related to the number of social media accounts?*, No, not statistically significant (F(2, 206)=0.1223, p>0.05) (via a one-way ANOVA)
		* *Is self-reported attention span related to whether a respondent mainly uses a mobile phone or a computer?*, No, not statistically significant (P(2,713)=0.923, p>0.05) (via a one-way ANOVA)
	* Method for assessing attention span: Questionnaire developed by the authors based on Conners 2004 (reliability: α=0.786)
	* I do **not** trust this paper: Calling (what I think is) Generation Z "Generation D" (without source for the term), being clearly written in Word, and bad grammar (I *think* the authors are all Americans, so no excuse here):

> Users that are older such as late adolescents and emerging adults
average approximately 30-minutes daily for just Facebook that does not
calculate the time spent on all social media networks

*—Carstens et al., [“Social Media Impact on Attention Span”](./doc/psychology/attention_span/social_media_impact_on_attention_span_carstens_et_al_2018.pdf) p. 2, 2018*

> Bakardjieva and Gaden (2012) examined the field of social interaction
in general to the everyday chatter of unstructured and spontaneous
interactions among individuals to highly structured and regulated
interaction consisting of the military or the stock exchange.

*—Carstens et al., [“Social Media Impact on Attention Span”](./doc/psychology/attention_span/social_media_impact_on_attention_span_carstens_et_al_2018.pdf) p. 3, 2018*

* [Lorenz-Spreen et al. 2019](./doc/psychology/attention_span/accelerating_dynamics_of_collective_attention_lorenz-spreen_et_al_2019.pdf "Accelerating dynamics of collective attention")
	* Questions answered:
		* *How long does any particular hashtag stay in the group of the top 50 most used hashtags? Specifically, how has that number developed from 2013 to 2016?*, "in 2013 a hashtag stayed within the top 50 for 17.5 hours on average, a number which gradually decreases to 11.9 hours in 2016", and "The average maximum popularity `$\langle L(t_{\hbox{peak}}) \rangle$` on one day `$t_{\hbox{peak}}$` stays relatively constant, while the average gradients `$\langle ΔL \rangle$` in positive and negative direction become steeper over the years."
		* *Do things become more popular faster over time? That is, when e.g. a movie is gaining popularity, did it take longer to become popular in 1985 than it did in 2018?*, Broadly yes (the trends holds for popularity of hashtags in tweets (2013-2016)/[n-grams](https://en.wikipedia.org/wiki/n-gram) in books (1900-2004)/number of theaters that movies were screened in (1985-2018)/topics for search queries on Google (2010-2017)/Reddit comments on posts (2010-2015)/citations of publications (1990-2015)/daily traffic for Wikipedia articles (2012-2017)). Again the length of the time at the peak mostly didn't change (except in the case of Wikipedia articles, where the time at the peak *shrunk*)
	* Method for assessing attention span: Time that specific pieces of information (hashtags/n-grams/Reddit submissions &c) were popular
	* While it investigates a question different from the one I have, this paper seems good and trustworthy to me, while supporting a suspicion I've had (observing that the lifecycle of e.g. memes has apparently sped up significantly). I'd be interested in seeing whether the same process holds for internet communities I'm part of (for example on votes [LessWrong](https://www.lesswrong.com/) and the [EA Forum](https://forum.effectivealtruism.org/) or forecasts on [Metaculus](https://www.metaculus.com/)).

![Chart indicating how the speed at which hashtags become popular changed over the years. Four plots (yellow, green, blue and purple) which form a peak in the middle and fall off at the sides. The yellow line is highest around the peak, the green one is lower, blue even lower and purple the lowest.](./img/spans/popularity_ascent.png "Chart indicating how the speed at which hashtags become popular changed over the years. Four plots \(yellow, green, blue and purple\) which form a peak in the middle and fall off at the sides. The yellow line is highest around the peak, the green one is lower, blue even lower and purple the lowest.")

<!--
What Would the Ideal Study Look Like?
--------------------------------------

### How Might One Measure Attention Span Best?

Power/speed test, maybe track eye movement. Internal/retest validity, of course.

Why Are Existing Studies So Inadequate?
----------------------------------------

------
-->

<!--
* `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4567490`
* `https://doi.org/10.1177%2F0956797615594896`
* `https://web.archive.org/web/20100601192507/http://blogs.suntimes.com/ebert/2010/05/the_french_word_frisson_descri.html`
* `http://blogs.suntimes.com/ebert/2010/05/the_french_word_frisson_descri.html#more`
* `https://www.wired.com/2010/05/ff-nicholas-carr/`
* `https://www.wired.com/beyond-the-beyond/2016/08/nicholas-carr-world-wide-cage/`
* `https://web.archive.org/web/20100601192507/http://blogs.suntimes.com/ebert/2010/05/the_french_word_frisson_descri.html`
* `https://www.digitalinformationworld.com/2020/02/report-shows-that-attention-spans-are-shortening.html`
* `https://www.euruni.edu/blog/the-truth-about-decreasing-attention-spans-in-university-students/`
* `https://www.dtu.dk/english/news/all-news/nyhed?id=246BBED3-8683-4012-A294-20DB7F0015F4`
* `https://www.brainbalancecenters.com/blog/normal-attention-span-expectations-by-age`
* `https://www.dtu.dk/english/news/all-news/nyhed?id=246BBED3-8683-4012-A294-20DB7F0015F4`
* `https://lsf.org/grammar/are-attention-spans-getting-shorter/`
* `https://statenews.com/article/2022/01/having-the-attention-span-of-a-goldfish-may-no-longer-be-the-the-joke-you-think-it-is?ct=content_open&cv=cbox_latest`
* `https://www.kcl.ac.uk/news/are-attention-spans-really-collapsing-data-shows-uk-public-are-worried-but-also-see-benefits-from-technology`
* `https://www.brainbalancecenters.com/blog/normal-attention-span-expectations-by-age`

For television & children:

* `http://pediatrics.aappublications.org/cgi/content/abstract/113/4/708`
* `https://doi.org/10.1542%2Fpeds.113.4.708`
-->

Appendix A: Claims That Attention Spans Have Been Declining
------------------------------------------------------------

Most of these are either unsourced or cite [Gausby
2015](./doc/psychology/attention_span/attention_spans_gausby_et_al_2015.pdf "Attention spans")
[fallaciously](https://www.bbc.com/news/health-38896790).

> Today, individuals are constantly on an information overload from
both the quantity of information available and the speed of which
information gets into the hands of individuals through advertising and
multimedia. Attention deficits tend to be increasing as it is challenging
to attract individuals and hold their attention long enough for people
to read or watch messages such as work memos, advertisements, etc.

*—Carstens et al., [“Social Media Impact on Attention Span”](./doc/psychology/attention_span/social_media_impact_on_attention_span_carstens_et_al_2018.pdf) p. 2, 2018*

> Big data plays an important role in the development of microlearning. In
the age of big data, human’s attention span is decreasing. As per Hebert
(1971), “what information consumes is rather obvious: it consumes the
attention of its recipients. Hence a wealth of information creates a
poverty of attention and a need to allocate that attention efficiently
among the overabundance of information sources that might consume it”
(p. 41). An example of short attention span in the age of big data can
be found in the music industry, as per (Gauvin, 2017), the average time
that passed before the audience would hear the vocals on any radio song
was 23 s, today the average intro is just 5 s long. Wertz (2017) also
suggested that 40% of users are likely to abandon a website if it does
not load within three seconds or less. Furthermore, a survey (Gausby,
2015) conducted by Microsoft indicated that the average attention span
of a human dropped from 12 to eight seconds, which means shorter than
a goldfish. Given the average human attention span is decreasing,
microlearning becomes more and more important because it emphasises
short learning duration.

*—Leong et al., “A review of the trend of microlearning”<!--TODO: perhaps link--> p. 2, 2020*
