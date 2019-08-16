[home](./index.md)
------------------

*author: niplav, created: 2019-04-10, modified: 2019-08-15, language: english, status: in progress, importance: 2, confidence: log*

> __A while ago, I became interested in personal estimations
> of life expectancy. I wanted to know how accurate people are
> at estimating their own life expectancy (by checking [actuarial
> tables](https://en.wikipedia.org/wiki/Life_table) and whether accuracy
> correlates with age or gender). I went out and collected data, which is
> shared and analysed here.__

Subjective Estimates of Life Expectancy
======================================

Abstract
--------

<!--TODO: at ≥1000 data points, put results into the abstract.-->

Actuarial tables are of great interest to statisticians, gerontologists
and policymakers. In this piece, data about subjective life expectancy
of urban germans is presented, analyzed using linear regression and
compared to actuarial tables. Gender and age differences in accuracy of
assessing ones own life expectancy are also considered.

Terminology
-----------

This text uses the terms "subjective life expectancy" and "estimated
life expectancy" interchangeably.

Data Collection Method
----------------------

192 random people were approached during the day in the streets of the
center of a major german city. They were asked the following questions
(in the presented order):

1. "Entschuldigung, darf ich Ihnen kurz zwei Fragen stellen?"
2. "Wie alt, schätzen Sie, werden sie werden?"
3. "Und wie alt sind Sie?"
4. "Vielen Dank, schönen Tag noch."

If the respondent was unsure after the second question, they were told:
"Nur eine grobe Schätzung" to indicate that they weren't expected to make
a perfect estimate. If at any point the respondent seemed uncomfortable,
the interrogation was stopped with step 4 directly.

If after the first question the respondent didn't seem able to understand,
they were asked the following questions (in that order):

1. "Do you speak English?"
2. "How old, do you think, will you become?"
3. "And how old are you?"
4. "Thank you very much, have a nice day."

Similarly, if the respondent seemed unsure after step 2, they were told
to only give "a rough estimate" of the number.

The perceived gender of the respondent was then noted together with
their age and estimated age.

Data was collected in the time from February 2019 to August 2019<!--(TODO:
Finish, collect at least 1000 data points, then do analysis)-->.

The raw data is available in CSV
[here](./data/estimated_life_expectancy.csv).

Analysis
--------

<!--TODO: Add p-values!-->

Code to load the data from the CSV file:

		.l("csv")
		.l("nstat")
		.fc(.ic("./data/estimated_life_expectancy.csv"));data::csv.load()
		m::1:$'{1_x}'flr({"m"~*x};data)
		f::1:$'{1_x}'flr({"f"~*x};data)
		data::1:$'{1_x}'1_data

### Age

Of the 192 respondents, 96 of which were male and 96 were female. The
mean age was 37.94 years (37.06 years for men and 38.83 years for women)
with the youngest respondents being 16 years old and the oldest being
82 years old (youngest/oldest male: 16/82, youngest/oldest female: 17/74).
The standard deviation for age was 17.13 (16.7 for men, 17.38 for women).

		dm::mu(*+data)
	37.9479166666666666
		fm::mu(*+f)
	38.8333333333333333
		mm::mu(*+m)
	37.0625
		ages::(*+data)@<*+data
		mages::(*+m)@<*+m
		fages::(*+f)@<*+f
		*ages
	16
		*|ages
	82
		*mages
	16
		*|mages
	82
		*fages
	16
		*|fages
	74
		sd(ages)
	17.1261196098769183
		sd(mages)
	16.7088337105538922
		sd(fages)
	17.3724740308938622

Code for the image:

	.l("nplot")
	.l("./load.kg")

	cgrid("age (female red, male blue)                      (N=",($#data),")";[0 100 20])
	fillrgb(0;0;1)
	scplot(mages)
	fillrgb(1;0;0)
	scplot(fages)

	setrgb(0;0;0)
	segplot(100:^dm)
	setrgb(0;0;1)
	segplot(100:^mm)
	setrgb(1;0;0)
	segplot(100:^fm)

	draw()

![The ages of the participants](./img/estimated_life_expectancy/ages.png)

<!--TODO: there is an annoying red line at the border of the image here
and in est_ages.png. Fix that.-->

As one can see in the image, the ages of the respondents by gender
follow a very similar pattern, except a lack of women aged 40 to 50
and a lack of women older than 75. Perhaps a bias on my side? But I
remember to have noticed that older women are less likely to answer,
especially questions about age.

### Subjective Life Expectancy

Estimates of life expectancy were interesting: The mean estimate was
83.49 years, 82.29 years for men and 84.69 years for women.  The lowest
estimate of life expectancy was only 30 years, the highest was 200 years
(lowest/highest for males: 30/120, lowest/highest for females: 39/200).

On average, respondents estimated that they had 45.54 years left in
their life, women estimating having 45.85 left in their lifes, men with
45.23 years. The lowest estimate for years of life left was 1, the highest
was 169 (lowest/highest for males: 1/82, lowest/highest for females: 6/169).

The standard deviation for the estimated age was 14.46 (13.84 for men,
14.96 for women).

		estages::(*|+data)@<*|+data
		mu(estages)
	83.4895833333333333
		mestages::(*|+m)@<*|+m
		festages::(*|+f)@<*|+f
		mu(mestages)
	82.2916666666666667
		mu(festages)
	84.6875
		*estages
	30
		*|estages
	200
		*mestages
	30
		*|mestages
	120
		*festages
	39
		*|festages
	200
		:"yl: years left"
		yl::{(*|x)-*x}'data
		yl::yl@<yl
		muyl::mu(yl)
	45.5416666666666666
		fyl::{(*|x)-*x}'f
		fyl::fyl@<fyl
		mufyl::mu(fyl)
	45.8541666666666667
		myl::{(*|x)-*x}'m
		myl::myl@<myl
		mumyl::mu(myl)
	45.2291666666666667
		*yl
	1
		*|yl
	169
		*myl
	1
		*|myl
	82
		*fyl
	6
		*|fyl
	169
		sd(estages)
	14.4566526421722967
		sd(mestages)
	13.8422517635064537
		sd(festages)
	14.9593731281680085

Code for the image:

	.l("nplot")
	.l("./load.kg")

	cgrid("estimated age (female red, male blue)           (N=",($#data),")";[0 200 20])
	fillrgb(0;0;1)
	scplot(mestages)
	fillrgb(1;0;0)
	scplot(festages)

	setrgb(0;0;0)
	segplot(100:^dem)
	setrgb(0;0;1)
	segplot(100:^mem)
	setrgb(1;0;0)
	segplot(100:^fem)

	setwidth(1)
	setrgb(0;0;0)

	draw()

![Subjective life expectancies of the participants](./img/estimated_life_expectancy/est_ages.png)

The black line between the blue line for the male average estimated age
and the red line for female average estimated age is for the overall
average estimated age.

### Linear Regression & Correlation

One can now do a linear regression on the data and try to find out what
the relation between estimated age and real age is.

		lreg(data)
	[0.151862914982186082 77.7986935564643823]
		lreg(f)
	[0.0608377197820622489 82.4196005451742221]
		lreg(m)
	[0.236555690251618827 73.5777002454096563]

The regression shows a positive relation between age and subjective life
expectancy, which is stronger for men than for women.

One can now also calculate the correlation between age and estimated
age, which is 0.1519 for the whole data set, 0.0608 for women and 0.2366
for men, indicating that men become more optimistic when growing older.

		cor@+data
	0.151862914982186104
		cor@+f
	0.0608377197820622755
		cor@+m
	0.23655569025161882

This can be shown in a scatter plot of the data.

	.l("nplot")
	.l("./load.kg")

	grid([0 100 20];[0 220 20])
	fillrgb(0;0;1)
	scplot2(m)
	fillrgb(1;0;0)
	scplot2(f)
	xtitle("age")
	ytitle("estimated age")

	setrgb(0;0;1)
	plot(lr(;lreg(m)))
	setrgb(1;0;0)
	plot(lr(;lreg(f)))
	setrgb(0;0;0)
	plot(lr(;lreg(data)))

	draw()

![A scatter plot of the whole data, with linear regression](./img/estimated_life_expectancy/all_scatter.png)

The red dots represent data points from women, the blue ones are from
men. The red line is the linear regression for the data by women, the
black line is the linear regression for the whole data, and the blue
line is the linear regression for the data by men.  Outliers are clearly
visible, and the difference between the linear regressions is also visible.

### Comparison With Actuarial Tables

One can also compare the data collected to existing actuarial tables,
and determine if there is a systematic deviation between subjective life
expectancy and the values given by actuarial tables.

For this, one can calculate averages for a given age, both separately
for genders and for the whole data set:

		grf::=*+f
		abaf::mu'(*|+f)@grf
		:"female averages, by age"
		rf::(*'(*+f)@grf),'abaf
		grm::=*+m
		abam::mu'(*|+m)@grm
		"male averages, by age"
		rm::(*'(*+m)@grm),'abam
		gr::=*+data
		aba::mu'(*|+data)@gr
		"averages, by age"
		r::(*'(*+data)@gr),'aba

Next, one needs actual actuarial tables for information to compare
the collected data to. Because the data was collected in Germany,
the actuarial tables were taken from the [Federal Statistical Office of
Germany](https://en.wikipedia.org/wiki/Federal_Statistical_Office_of_Germany).
The [actuarial
tables](https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Sterbefaelle-Lebenserwartung/_inhalt.html)
were downloaded, converted from [ISO/IEC
8859](https://en.wikipedia.org/wiki/ISO/IEC_8859) to
[UTF-8](https://en.wikipedia.org/wiki/UTF-8) and arranged in the
following form:

	age,life expectancy m,life expectancy f

The resulting data can be viewed [here](./data/de_actuarial_tables.csv).

Now, one can start comparing the collected estimates to the actuarial
tables. To do this, one first loads the data into Klong:

		known::{(1:$*x),(1.0:$x@1),(1.0:$x@2)}'1_known
		mk::{x@[0 1]}'known
		fk::{x@[0 2]}'known
		kr::{(*x),((x@1)+x@2)%2}'known

The variable `kr` contains the mean of the female and male actuarial values.

Since one has already calculate the average estimates for life
expectancy by age (the variables `grm`, `grf` and `gr`), one can now
compute correlations between the estimates and the actuarial tables. The
correlation between the estimates and the actuarial values is 0.0732,
0.0799 for men and 0.0032 for women.

		cord::cor(aba;*|+kr@*'(*+data)@gr)
	0.0732435875628164249
		corm::cor(abam;*|+mk@*'(*+m)@grm)
	0.0799339532720909585
		corf::cor(abaf;*|+fk@*'(*+f)@grf)
	0.00321245137729511554

One can now also visualize the estimates and actuarial values.

For the mean estimate:

	.l("nplot")
	.l("nstat")
	.l("./load.kg")

	grid([0 100 20];[0 150 20])

	setdot(3)

	fillrgb(0;0;0)
	scplot2(mk)

	fillrgb(0;0;1)
	scplot2(rm)

	xtitle("age")
	ytitle("male: average estimated life expectancy (blue), average life expectancy (black)")

	draw()

![Mean estimate per year to actuarial table](./img/estimated_life_expectancy/avg_est.png)

For men:

	.l("nplot")
	.l("nstat")
	.l("./load.kg")

	grid([0 100 20];[0 150 20])

	setdot(3)

	fillrgb(0;0;0)
	scplot2(mk)

	fillrgb(0;0;1)
	scplot2(rm)

	xtitle("age")
	ytitle("male: average estimated life expectancy (blue), average life expectancy (black)")

	draw()

![Mean estimate per year to actuarial table for men](./img/estimated_life_expectancy/m_res.png)

For women:

	.l("nplot")
	.l("nstat")
	.l("./load.kg")

	grid([0 100 20];[0 150 20])

	setdot(3)

	fillrgb(0;0;0)
	scplot2(fk)

	fillrgb(1;0;0)
	scplot2(rf)

	xtitle("age")
	ytitle("female: average estimated life expectancy (red), average life expectancy (black)")

	draw()

![Mean estimate per year to actuarial table for men](./img/estimated_life_expectancy/f_res.png)

<!--TODO: difference between estimated age and actuarial value, is there
a correlation? Would that even be a useful measure?-->

Problems
---------

As with most self-reported data, there are numerous problems with this
approach. The data presented here represents estimates often made in a
very short amount of time, and is prone to misunderstandings.

### Hope Instead of Estimates

It seemed like very often people misunderstood that the estimate they were
asked for was not asking for the age they hoped for, but the age they
estimated. It would not have been practical explaining this to people,
since the response rate already was quite low and there were sometimes
severe difficulties in understanding, but this seems to be the strongest
bias in the data. Interestingly, a surprising number of people seemed
to hope to die earlier than the average person, especially a woman aged
29 who hoped to die at 39.

### Joke Answers

Keeping in line with the [lizardman
constant](http://slatestarcodex.com/2013/04/12/noisy-poll-results-and-reptilian-muslim-climatologists-from-mars/),
there was a number of joke answers and sometimes even straight lies. Most
of the people who answered that they estimated to become 120 years old
fit into this category (the woman who estimated that she would become
200 years old seemed convinced of that, though). There was also a number
of people who either looked way too old or lied about their age.

### Some Ages are Missing

The visualisation of the data shows a clear lack of women aged between
40-50 in the data set, as well as a lack of people older than 70. One
possible explanation for this observation is an age-related bias by the
interrogator. Another possible explanation could be that people older
than 70 don't like to answer questions in the street, don't go outside
very often, are rare, or lie about their age regularly.  I note that it
seemed to me that older women were most reluctant to answer my questions,
but that may just be another manifestation of personal bias.

### Selection Bias and Non-Representative Data

As with any street poll, this interrogation got responses from
people willing to answer questions from strangers on the street. This
could select for high openness, which could function as a proxy for
optimism. Also, all people were interrogated in a big city, which
could have biased the data (I am not sure which direction this bias
woul tend).  One could also argue that self-reported data is [notoriously
unreliable](https://guzey.com/statistics/dont-believe-self-reported-data/),
but since the point of this data collection was to aggregate subjective
estimates, this should not be an issue here.

Conclusion
-----------

See Also
--------

<!--
TODO: read:

/usr/local/doc/unread/sle/*
-->
