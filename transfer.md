[home](./index.md)
------------------

*author: niplav, created: 2024-02-28, modified: 2024-02-28, language: english, status: notes, importance: 6, confidence: certain*

> __I examine the literature on transfer learning in humans<!--, and find that-->.__

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

What I Am Looking For
-----------------------

Given a broad set of skills `$S$`, I was looking for an intervention/a
set of interventions `$I$` which has the following properties:

1. After applying `$I$`, an average adult can now learn skills from `$S$` is on average much faster counterfactually to not having applied `$I$`
2. Applying `$I$` is easier than learning all skills `$S$`
3. Optional: `$I$` is *relatively* easy to apply, that is it doesn't need a lot of institutional setup
4. Optional: `$I$` can be applied to itself, and to find better interventions `$I'$` that have the same properties as `$I$`

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

Candidates
-----------

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
		for each one". Works better on mathematics.

[^1]: Judging from [Dunlosky et al. 2017](https://www.wku.edu/senate/documents/improving_student_learning_dunlosky_2013.pdf) the participants in the various studies were asked to verbally explain their reasoning. It's not said how writing the explanation instead of saying it compares.
[^2]: These two techniques are treated separately in the paper, but as far as I can tell mostly for historical reasons.

### "Far Transfer"

### Pólya Method

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

The relevant papers are:

1. [Nasir & Syartina 2021](https://jurnal.syekhnurjati.ac.id/index.php/eduma/article/viewFile/8700/3969): n=32 Indonesian high-school students, non-RCT, only observational. Effect size d=0.71, but that's not super impressive given it's not an RCT.
2. [Widiana et al. 2018](http://edulearn.intelektual.org/index.php/EduLearn/article/viewFile/4526/5353): n=138 elementary school children, RCT. I'm not *entirely* sure about this, but based on their Table 1 and [this calculator](https://www.socscistatistics.com/effectsize/default3.aspx) I get __d=2.4__, which I find really hard to believe. I think I'm making a mistake`$_{60\%}$` or the paper is fraudulent`$_{40\%}$`.
3. [Hayati et al. 2022](https://jestec.taylors.edu.my/Special%20Issue%20ICMScE2022/ICMScE2022_04.pdf): n=40 Indonesian high-school children. This paper is so confusingly written I can't extract any meaning from it.

### Training Spatial Cognition

### Dual N-Back

### Increasing Intelligence

Creating Self-Improving Institutions
--------------------------------------

Double-loop learning.
