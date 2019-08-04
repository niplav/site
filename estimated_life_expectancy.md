[home](./index.md)
------------------

*author: niplav, created: 2019-04-10, modified: 2019-08-03, language: english, status: notes, importance: 2, confidence: log*

> __A while ago, I became interested in personal estimations
> of life expectancy. I wanted to know how accurate people are
> at estimating their own life expectancy (by checking [actuarial
> tables](https://en.wikipedia.org/wiki/Life_table) and whether accuracy
> correlates with age or gender. I went out and collected data, which is
> shared and analysed here.__

Personal Estimates of Life Expectancy
======================================

Abstract
--------

Actuarial tables are of great interest to statisticians, gerontologists
and policymakers. In this piece, data about subjective life expectancy
of urban germans is presented and analyzed using linear regression and
compared to actuarial tables. Gender and age differences in accuracy of
assessing ones own life expectancy are also considered.

Data Collection Method
----------------------

192 random people were approached during the day in the streets of a major german city.
They were asked the following questions (in the presented order):

1. "Entschuldigung, darf ich Ihnen kurz zwei Fragen stellen?"
2. "Wie alt, schätzen Sie, werden sie werden?"
3. "Und wie alt sind Sie?"
4. "Vielen Dank, schönen Tag noch."

If the respondent was unsure after the second question, they were told:
"Nur eine grobe Schätzung" to indicate that they weren't expected to make
a perfect estimate). If at any point the respondent seemed uncomfortable,
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

Data was collected in the time from May 2019 to August 2019 (TODO:
Finish, collect at least 1000 data points, then do analysis).

The raw data is available in CSV
[here](./data/estimated_life_expectancy.csv).

Analysis
--------

Problems
---------

* Hoped for age, not estimated age
* Joke answers
* Interrogator bias (age, gender)

Conclusion
-----------

See Also
--------

TODO: read:

/usr/local/doc/unread/sle/*
