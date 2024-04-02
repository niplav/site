[home](./index.md)
------------------

*author: niplav, created: 2024-02-28, modified: 2024-03-31, language: english, status: in progress, importance: 6, confidence: certain*

> __I examine the literature on transfer learning in humans<!--, and find that-->.__

<!--TODO: section n negative transfer?-->

Transfer Learning in Humans
============================

When learning, one would like to progress faster, and learn things
faster. So it makes sense to search for interventions that speed up
learning (effective learning techniques), enable using knowledge
and knowledge patterns from one learned domain in a new domain if
appropriate (transfer learning), and make it easier to find further
learning-accelerating techniques (meta-learning).

Summary of the Results
-----------------------

If you're already using spaced repetition a bunch,

1. If you want to [learn faster](#Straightforward_Stuff)
	1. Do [spaced repetition](https://www.gwern.net/Spaced-repetition) when possible
		1. In general, revisit basics of a field while you're learning
	2. Spend a lot of time on practice problems
	3. Explain why you're doing what you're doing, while you're doing it
	4. If errors are cheap and obvious, [make and seek out errors during learning/training](#Error_Management_Theory)
1. If you want to solve problems
	1. Try to get feedback on both the process and the outcomes of what you're doing
		1. Explicitly [analyse errors after you've made them](#Inducing_Transfer)[^4]
	2. If there are already experts at the problem you're trying to solve, [interview them in a systematic fashion](https://commoncog.com/accelerated-expertise/) to [extract](https://commoncog.com/an-easier-method-for-extracting-tacit-knowledge/) their [tacit knowledge](https://commoncog.com/the-tacit-knowledge-series/)
		1. With enough institutional support this can be turned into a training program
	3. If there are no experts in the domain where you're trying to solve a problem:
		1. Search for related domains and extract existing tacit knowledge there, or learn those domains—the closer the better
		2. Apply the [Pólya method](#Pólya_Method)<!--Add four steps-->

If you think that these recommendations are kind of unsatisfying,
[I agree with you](#My_Impression_of_the_Literature).

[^4]: Since everything is judgmental-forecasting-shaped, one could test this by letting forecasters elaborate on their forecasts and at resolution time analyse their elaborations. I've [tried doing this](http://niplav.site/notes_on_predictions.html) but it fell off for other projects.

What I Am Looking For
-----------------------

Given a broad set of skills `$S$`, I was looking for an intervention/a
set of interventions `$I$` which has the following properties:

1. After applying `$I$`, an average adult can now learn skills from `$S$` is on average much faster counterfactually to not having applied `$I$`
2. Applying `$I$` and learning `$S$` is easier than just learning all skills `$S$`
3. `$S$` is large (or actually encompasses all skills humans have)
4. Optional: `$I$` is *relatively* easy to apply, that is it doesn't need a lot of institutional setup
5. Optional: `$I$` can be applied to itself, and to find better interventions `$I'$` that have the same properties as `$I$`

The question about transfer learning in humans isn't clearly
differentiated from the research into effective learning techniques.
Transfer learning and meta-learning are more focused on crossing the
theory-practice gap and making progress in domains where we don't yet
have detailed knowledge.

Therefore, I tried to find more information from well-performing
institutions such as the military and large corporations, de-emphasizing
research done in universities and schools (I found this difficult because
those places tend to have more incentive to publish their techniques,
and also strive to quantify their benefits).

Candidate Interventions
------------------------

### Straightforward Stuff

I found several studies from psychology, especially educational
psychology.

[Dunlosky et al.
2017](https://www.wku.edu/senate/documents/improving_student_learning_dunlosky_2013.pdf)
reviewed the evidence on ten proposed effective learning techniques,
and singled out two interventions as having high utility and three
interventions as having moderate utility:

1. High utility:
	1.	__Practice testing__: Testing oneself on the target domain
		in a low-stakes context, ideally repeatedly. Think [spaced
		repetition](https://www.gwern.net/Spaced-repetition) with
		flashcards, or preparing for exams by doing exams from previous
		years. They mention that practice testing generalizes across
		formats (e.g. from simple recall to short answer inference tests).
		Can generate *far transfer*.
		1.	p. 30: "practice testing a subset of information
			influences memory for related but untested information"
	2.	__Distributed practice__: Practice that happens
		spread out over a longer amount of time, instead
		of cramming. This gain is also captured via [spaced
		repetition](https://www.gwern.net/Spaced-repetition). They do
		not mention any transfer benefits here.
2. Moderate utility:
	1.	__Elaborative interrogation__ and __Self-explanation__[^2]:
		Generating and saying[^1] an explanation for why an
		explicitly stated fact or concept is true. This most helps
		learners who already know a lot about the target domain, and
		works best if it is done *during* the learning process.
		1. ![](./img/transfer/practice_transfer.png)
	2.	__Interleaved practice__: When learning, repeat basic
		material while learning more advanced material. The
		advantages over distributed practice testing seems
		moderate, but (p. 38): "interleaved practice helped
		students to discriminate between various kinds of
		problems and to learn the appropriate formula to apply
		for each one". Works better on mathematics[^3].

[^1]: Judging from [Dunlosky et al. 2017](https://www.wku.edu/senate/documents/improving_student_learning_dunlosky_2013.pdf) the participants in the various studies were asked to verbally explain their reasoning. It's not said how writing the explanation instead of saying it compares.
[^2]: These two techniques are treated separately in the paper, but as far as I can tell mostly for historical reasons.
[^3]: This is supported by the theory of [transfer-appropriate processing](https://en.wikipedia.org/wiki/Transfer-appropriate_processing), which puts an especially strong emphasis on the encoding and retrieval of learned information. As far as I understand, the recapitulation of basic knowledge in the context of more advanced knowledge allows for a more accurate re-encoding of the basic knowledge. This also tracks with my experience of learning mathematics: I've gotten more mileage out of understanding basic concepts deeply (e.g. how probabilities, logits and bits fit together), than understanding more advanced concepts shallowly.

### "Far Transfer"

__Summary__: Far transfer occurs if one puts in a lot of effort,
e.g. after doing semester- or year-long courses on decision-making and
such. The effect sizes on general abilities tests are medium (d≈0.3).

Far transfer is:

> improved performance at problems that are similar to but also
substantially different from ones experienced during training (e.g.,
fault diagnosis in process control to fault diagnosis in telecommunication
networks).

*—Hoffman et al., “Accelerated Expertise”, 2014*

The relevant papers are:

* [Herrnstein et al. 1986](https://www.researchgate.net/profile/Raymond-Nickerson/publication/232424806_Teaching_Thinking_Skills/links/564b3d0408ae3374e5dd841b/Teaching-Thinking-Skills.pdf): n=895 Venezuelan high-school students (mean age 13.22 years), controlled trial. Intervention was a year-long course on decision-making (four days a week), others received a control course (it's not clear what this control course was about). Effect sizes on various general intelligence tests are d=0.35 (General Abilities Test), d=0.43 ([OLSAT](https://en.wikipedia.org/wiki/Otis-Lennon_School_Ability_Test)), d=0.11 ([CATTELL](https://en.wikipedia.org/wiki/Cattell_Culture_Fair_Intelligence_Test)), all at statistical significance.
* [Fong et al. 1986](https://deepblue.lib.umich.edu/bitstream/handle/2027.42/26118/0000194.pdf;sequence=1): n=347 adults and high-school students were instructed on the [law of large numbers](https://en.wikipedia.org/wiki/Law_Of_Large_Numbers), from just reading a description (control) to working through examples where the law was and was not applicable (intervention). They were then tested on the application of the law to new problems. Effect size was 1 logit (which corresponds to d≈0.55 [IIUC](https://en.wiktionary.org/wiki/IIUC)).

### Error Management Theory

__Summary__: Making errors during training, if it is obvious an error
has occurred, and errors are affordable, transfers the learned knowledge
pretty well (d=0.8).

[Error Management
Training](https://en.wikipedia.org/wiki/Error_management_theory) (EMT) is a
type of training in which making errors during exploration while learning
is actively encouraged. Trainers encourage learners during learning to
make errors and reflect on those errors while learning, but don't give
much guidance beyond that.

[Keith & Frese
2008](http://fox.leuphana.de/portal/files/607254/Keith_frese_Error_Manag_Train_Metacongition_Em_control_JAP05.pdf)
perform a meta-analysis analysing studies training participants to use
software tools or learn programming languages (n=2183), comparing EMT
to training that encourages error-avoidance, and find that EMT has a
medium-sized advantage over error-avoiding training methods (d=0.44).

EMT shows *larger* effect sizes over error-avoiding methods with more
demanding transfer: d=0.56 for performance after training, and d=0.8 for
transfer that requires modifying learned procedures to fit news contexts
(adaptive transfer). However, Keith & Frese also provide evidence that
this advantage only occurs if there is clear feedback on whether an
error has occurred or not.

One is reminded of [Umeshisms](https://www.scottaaronson.com/blog/?p=40):
If you never fail, you're underperforming. (Also, you're not going to
be able to use it.)

When I tried tutoring someone in programming for fun, I tried to give
the person assignments that they would only be able to solve 50% of
the time. I don't know whether this is optimal, but *mumble mumble*
entropy *mumble* dense reward *mumble*.

### Pólya Method

__Summary__: Evidence is not great, but one paper looks suspiciously
good. Worth investigating, especially since it's often recommended by
research mathematicians.

Another interesting-seeming strand of research were tests of the
[Pólya method](https://en.wikipedia.org/wiki/How_To_Solve_It). The
Pólya method is a four-step problem-solving method, with the [four
steps being](https://math.berkeley.edu/~gmelvin/polya.pdf)

1. Understand the problem
2. Devise a plan
	1.	The book "How to Solve It"
		also has a list of [problem solving
		strategies](https://en.wikipedia.org/wiki/How_to_Solve_It#Second_principle:_Devise_a_plan)
3. Carry out the plan
4. Look back

This is a variant of the [OODA
loop](https://en.wikipedia.org/wiki/OODA_Loop), with the difference that
a lessened time pressure allows forming a whole plan (not just a decision)
and for reflection after carrying out the plan.

For some weird reason, the only scientists who have investigated the
Pólya method experimentally are Indonesian. I have no idea why.

The relevant papers all test on learning basic
mathematical problem solving skills in [plane
geometry](https://en.wikipedia.org/wiki/Plane_Geometry) and
[fractions](https://en.wikipedia.org/wiki/Fractions):

1. [Nasir & Syartina 2021](https://jurnal.syekhnurjati.ac.id/index.php/eduma/article/viewFile/8700/3969): n=32 Indonesian high-school students, non-RCT, only observational. Effect size d=0.71, but that's not super impressive given it's not an RCT.
2. [Widiana et al. 2018](http://edulearn.intelektual.org/index.php/EduLearn/article/viewFile/4526/5353): n=138 elementary school children, RCT. I'm not *entirely* sure about this, but based on their Table 1 and [this calculator](https://www.socscistatistics.com/effectsize/default3.aspx) I get __d=2.4__, which I find really hard to believe. I think I'm making a mistake`$_{60\%}$` or the paper is fraudulent`$_{40\%}$`.
3. [Hayati et al. 2022](https://jestec.taylors.edu.my/Special%20Issue%20ICMScE2022/ICMScE2022_04.pdf): n=40 Indonesian high-school children. This paper is so confusingly written I can't extract any meaning from it.

### Accelerated Expertise

__Summary__: With a lot of institutional support, one can extract
knowledge from experts and use it to create better training programs.
This requires a large institution to be worth it.

Accelerated Expertise ([Hoffman et al.,
2014](https://www.goodreads.com/book/show/17399473-accelerated-expertise))
was motivated by getting military recruits up to speed quickly before
moving them to deployment.  It focuses on the case in which there are
already experts for a given domain, and one aims to move the skills from
domain experts into the mind of new recruits as quickly as possible. [Chin
2024](https://commoncog.com/accelerated-expertise/) summarizes the goals
of the research project that lead to the book as attempting to speed
up the time from being a beginner at a specific task or set of tasks to
being proficient at that task (hence the name "Accelerated Expertise").

![](./img/transfer/accelerated.jpg)

They are skeptical that any training can make trainees dramatically
better at the domain than experts with a lot of training.

For this, Hoffman et al. have developed a series of multiple steps for
creating training programs for new recruits.

1. Identify domain experts
2. Use [Cognitive Task Analysis](https://commoncog.com/an-easier-method-for-extracting-tacit-knowledge/) to extract expert knowledge
3. Build a case library of difficult cases
4. Turn case library into a set of training simulations
5. Optional: Include introspection & reflection in the program
6. Optional: Teach abstract/generalized principles
7. Test the program

The book contains a literature review on transfer in chapter 5, which I
didn't manage to completely read, but which afaik is the best collected
resource on transfer learning in humans. They summarize the chapter by
remarking that not artificially "dumbing down" a domain when a beginner
tries to learn it can delay learning in the beginning, but speed up
learning in the long run because it prevents misunderstandings from
becoming entrenched.

#### Inducing Transfer

They also summarize the methods for inducing transfer:

> Transferring a skill to new situations is often difficult but can
be promoted by following a number of training principles: employing
deliberate practice, increasing the variability of practice, adding
sources of contextual interference, using a mixed practice schedule,
distributing practice in time, and providing process and outcome feedback
in an explicit analysis of errors.

*—Hoffman et al., [“Accelerated Expertise”](https://www.goodreads.com/book/show/17399473-accelerated-expertise) p. 176, 2014*

I'd also have liked to dive deeper on extracting expert knowledge,
which looks important especially in novel domains like AI alignment.

### Dual N-Back

__Summary__: Increases working memory, but probably not IQ.

I re-read parts of [Gwern 2019](https://gwern.net/dnb-faq) and [Gwern
2018](https://gwern.net/dnb-meta-analysis), and come away with believing
that if one is bottlenecked by working memory, n-back is worth it,
but it doesn't work well for increasing intelligence.

### Judgmental Forecasting

__Summary__: I didn't find anything on whether learned forecasting
ability transfers across domains. I now want to analyze some data to
find out whether it does.

The evidence from the judgmental forecasting research is confusing. On
the one hand, it's widely known that domain-level experts are [not
very good](https://en.wikipedia.org/wiki/Expert_Political_Judgment)
at making predictions about their own domain, and are outcompeted by
[superforecasters](https://en.wikipedia.org/wiki/Superforecasting)
who are just generally good at predicting.

On the other hand, the vibe given by forecasters and forecasting
researchers is similar to the following statement:

> By the way, there are no shortcuts. Bridge players may develop
well-calibrated judgment when it comes to bidding on tricks, but research
shows that judgment calibrated in one context transfers poorly, if at
all, to another. So if you were thinking of becoming a better political
or business forecaster by playing bridge, forget it.

*—Philip E. Tetlock & Dan Gardner, “Superforecasting” p. 179, 2015*

I tried to find the research this paragraph is talking about by asking
in a couple of discord servers and messaging the [Forecasting Research
Institute](https://forecastingresearch.org/), but I didn't get any
responses that were satisfying to me.

I now want to analyze my [own judgmental forecasting
datasets](./iqisa.html) to figure out how much forecasting ability
generalizes across domains.

<!--
TODO:

### Training Spatial Cognition
-->

Creating Self-Improving Institutions
--------------------------------------

__Summary__: Organizations can become organizations that improve their
governing variables. Inducing this is very tricky. Events that can
induce double-loop learning in an organization include a change to
leaders which value reflection and dialogue, and the introduction of
software tools, such as systems which are used for prediction, which
then provide feedback.

*Double-loop learning* is a method to improve learning of organizations,
taking into account the learning process itself.

[Auqui-Caceres & Furlan
2023](https://onlinelibrary.wiley.com/doi/pdf/10.1111/emre.12615) review
the evidence on double-loop learning.

![](./img/transfer/double_loop.png)

They report on several interventions:

* Tested:
	* [Integrative Double-Kaizen Loop](https://ieeexplore.ieee.org/document/8345680) → implemented and saw improvements, but no controls
	* Writing and iterating on simulation software ("simulation modeling"/machine learning models) → Induced double-loop learning in two different papers
* Tested, didn't work:
	* PIER (Problem-based learning, Interactive multimedia, Experiential learning, and Role-playing) → Allegedly failed because leadership didn't participate
	* Briefing-debriefing sessions → Allegedly failed because the tested protocol didn't include communicating up the hierarchy
	* Incident-reporting systems → No change observed
* Proposed but, as far as I understand, not tested:
	* [DMAIC](https://asq.org/quality-resources/dmaic)
	* ["Circular organization"](https://www.proquest.com/docview/197599398)

> […] these studies maintain that the most prominent barrier to generate
DLL is defensive reasoning and routines (Bochman & Kroth, 2010; Clarke,
2006; Kwon & Nicolaides, 2017; Sisaye & Birnberg, 2010; Stavropoulou et
al., 2015; Sterman, 1994; Wong, 2005), which are produced by participants
in DLL processes, whenever assumptions underlying taken-for-granted
procedures, practices, or policies are challenged. Although people are
aware that they should not use defensive reasoning to deal with daily work
difficulties and challenges (Thornhill & Amit, 2003), they still use them
to avoid losing control and dealing with embarrassment (Mordaunt, 2006).

*—Auqui-Caceres & Furlan, [“Revitalizing double-loop learning in organizational contexts: A systematic review and research agenda”](https://onlinelibrary.wiley.com/doi/pdf/10.1111/emre.12615) p. 14, 2023*

Questions
-----------

1. Is it better to perform elaborative interrogation verbally, or is it as good to write things down?
2. What is the optimal amount of "going back to the basics" to deepen understanding over time?
	1. Spaced repetition schedules are one suggestion, but they're only geared towards remembering, not deepening understanding.
3. Do people generalize within judgmental forecasting, across question asking domains?
4. Why do all papers I've found to gravitate to the "better learning techniques" bucket?
5. Which techniques do really successful consultancies or investment firms use for problem-solving ability?

My Impression of the Literature
--------------------------------

After spending a dozen hours researching this area, my current impression
is that this is something that too many different fields are interested
in; among them are business people, military psychologists, education
researchers, neuroscientists, cognitive psychologists…

This results in a wild outgrowth of terminology: "transfer of learning",
"learning to learn", "deutero-learning", "double-loop learning", "design
thinking", "adaptive learning" &c. In my research I don't think I've
encountered a paper being cited by two different papers, which suggests
there's more than a thousand papers grasping at the same question of
transfer learning.

<!--Have people figured anything out, did they do obvious or just
seemingly obvious things-->

I've created an (incomplete)
[spreadsheet](https://docs.google.com/spreadsheets/d/1-_EuaLf1Fau7hhH-9lvzec-hhiswmRM2rey2bfbp8mA/edit?usp=sharing)
with the relevant papers from the literature that I could find.

See Also
---------

* [Ricón 2020](https://nintil.com/bloom-sigma/#darpa-s-study) on a DARPA study with a digital tutor for a specific domain, showing __d=2.81__ improvement
