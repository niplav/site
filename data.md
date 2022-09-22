[home](./index.md)
-------------------

*author: niplav, created: 2022-07-07, modified: 2022-08-07, language: english, status: notes, importance: 2, confidence: log*

> __Notes for myself on the data I track, how to transform it into a
usable shape, data quality and other random assortments.__

Types & Methods of Data Collection I Use
=========================================

I've always collected some data about myself and the world around me,
but not using/analyzing it because of a chronic "I'll get around to it
*eventually*" syndrome. Which is a shame, because that means I've been
putting in a reasonably large amount of effort and have nothing to show
for it, a 1-legged stool:

> The QS cycle is straightforward and flexible:  
>  
1. Have an idea  
2. Gather data  
3. Test the data  
4. Make a change; GOTO 1

> Any of these steps can overlap: you may be collecting sleep data long
before you have the idea (in the expectation that you will have an idea),
or you may be making the change as part of the data in an experimental
design, or you may inadvertently engage in a “natural experiment”
before wondering what the effects were (perhaps the baby wakes you up
on random nights and lets you infer the costs of poor sleep).  
>
> The point is not publishable scientific rigor. If you are the sort of
person who wants to run such rigorous self-experiments, fantastic! The
point is making your life better, for which scientific certainty is not
necessary: imagine you are choosing between equally priced sleep pills
and equal safety; the first sleep pill will make you go to sleep faster
by 1 minute and has been validated in countless scientific trials, and
while the second sleep pill has in the past week has ended the sweaty
nightmares that have plagued you every few days since childhood but alas
has only a few small trials in its favor—which would you choose? I
would choose the second pill! […]
>
> One failure mode which is particularly dangerous for QSers is
to overdo the data collection and collect masses of data they
never use. Famous computer entrepreneur & mathematician [Stephen
Wolfram](https://en.wikipedia.org/wiki/Stephen_Wolfram)
exemplified this for me in March 2012 with his
lengthy blog post ⁠[“The Personal Analytics of My
Life”](https://writings.stephenwolfram.com/2012/03/the-personal-analytics-of-my-life/)
in which he did some impressive graphing and exploration
of data from 1989 to 2012: a third of a million (!) emails,
full keyboard logging, calendar, phone call logs (with missed
calls include), a pedometer, revision history of his tome [A New Kind of
Science⁠](https://www.amazon.com/New-Kind-Science-Stephen-Wolfram/dp/1579550088/?tag=gwernnet-20),
file types accessed per date, parsing scanned documents for dates,
a treadmill, and perhaps more he didn’t mention. […]
>
> One thinks of [a saying](https://deming.org/index.cfm?content=653) of
[W. Edwards Deming](https://en.wikipedia.org/wiki/W._Edwards_Deming):
“Experience by itself teaches nothing.” Indeed. A QS experiment is a
4-legged beast: if any leg is far too short or far too long, it can’t
carry our burdens.

At least I now know that I'm falling into this trap, "Selbsterkenntnis
ist der erste Schritt zur Besserung". And the second step is to bring
all of your data in a usable format.

Anki
-----

I use spaced repetition, and plan to take it as a proxy for cognitive
performance in QS experiments.

The data can be found in the helpfully named `collection.anki2`, which
is actually an sqlite database in disguise.

The [Anki manual]() helpfully informs that the most important table is
`revlog`, one can then export the data to CSV with the following command:

	echo -e '.headers on \n select * from revlog;' |
	sqlite3 anki_2022-07-04T08:43:00.db |
	tr '|' ',' >anki_2022-07-04T08:43:00.csv

The header is to be interpreted as follows:

> The most important table for statistics is the revlog table, which
stores an entry for each review that you conduct. The columns are
as follows:
>  
id  
>  
> The time at which the review was conducted, as the number of milliseconds
that had passed since midnight UTC on January 1, 1970. (This is sometimes
known as Unix epoch time, especially when in straight seconds instead
of milliseconds.)
>  
cid  
>  
The ID of the card that was reviewed. You can look up this value in
the id field of the cards table to get more information about the card,
although note that the card could have changed between when the revlog
entry was recorded and when you are looking it up. It is also the
millisecond timestamp of the card’s creation time.
>  
usn  
>  
This column is used to keep track of the sync state of reviews and
provides no useful information for analysis.
>  
ease  
>  
Which button you pressed at the end of the review (1 for Again, 4 for Easy).
>  
> ivl  
>  
The new interval that the card was pushed to after the review. Positive
values are in days; negative values are in seconds (for learning cards).
>  
lastIvl  
>  
The interval the card had before the review. Cards introduced for the
first time have a last interval equal to the Again delay.
>  
factor  
>  
The new ease factor of the card in permille (parts per thousand). If
the ease factor is 2500, the card’s interval will be multiplied by
2.5 the next time you press Good.
>  
time  
>  
The amount of time (in milliseconds) you spent on the question and answer
sides of the card before selecting an ease button.
>  
type  
>  
This is 0 for learning cards, 1 for review cards, 2 for relearn cards,
and 3 for "cram" cards (cards being studied in a filtered deck when they
are not due).

*— Anki developers, [“Manual Analysis”](https://docs.ankiweb.net/stats.html#manual-analysis) in [“Graphs and Statistics”](https://docs.ankiweb.net/stats.html#manual-analysis), year unknown*

The CSV of the data can be found [here](./data/anki_reviews.csv).

Meditation
-----------

Similarly, one can export meditation data from Meditavo (if one has
coughed up 5€ for the premium version, which I decided was worth it
for the data, after having locked myself in :-|):

	echo -e '.headers on \n select * from History;' |
	sqlite3 meditation_2022-07-02T20:00:00.db |
	tr '|' ',' >meditations.csv

The names for the columns are exceedingly obvious and need no further
explanation.

I didn't rate my sessions in the beginning (and manually inserted
data from meditation retreats with unrated sessions), leading to a
very optimistic default of 4.0 mindfulness and "concentration" (better
called absorption, I claim). So we execute, using the sam language in
vis<!--TODO: links-->:

	/^1,/;/^860,/
	x/4\.0,4\.0,/c/,/
	/^1210,/;/^1308,/
	x/4\.0,4\.0,/c/,/
	/^1594,/;/^1615,/
	x/4\.0,4\.0,/c/,/

The CSV of the meditation data can be found [here](./data/meditations.csv).

Daygame
--------

2 datasets, first containing approaches, 2nd containing approach sessions

1st file datapoints (in CSV):

* Approach index number
* Datetime
* Location
* Blowout
* Contact info ∈{number,instagram,facebook,skype,snapchat etc.,other}
* Idate length (minutes)
* Idate cost (euro)
* Flake before 1st date (boolean)
* Date before first sex [1..10] cost (euro)
* Date before first sex [1..10] length (minutes)
* Sex number of times (approximately)
* Attractiveness (∈[1..10])

2nd file:

* Datetime start
* Datetime end
* Approaches index number range
* Number of approaches

Sanitizing the sessions file:

Converting f\*\*\*ed up Google sheets date format (why does __nobody__
use the perfect [ISO-8601](https://en.wikipedia.org/wiki/ISO-8601) when
it's right there‽), then removing stray spaces after semicolons,
then removing the `^M` from the end of each line, using
[structural regular                                                                                  expressions](./doc/cs/structural_regular_expressions_pike_1990.pdf "Structural Regular Expressions"):

	,x/([0-9]+)\/([0-9]+)\/([0-9]+) /c/\3-\1-\2T/
	,x/; /c/;/
	,x/.$/c//
	,x/(T[0-9]+:[0-9]+),/c/\1:00,/
	,x/-([0-9])-/c/-0\1-/

and some other minor fixes.

Formatting the approaches file:

	,x/.$/d
	,x/ ,/c/,/

Find incorrectly written locations:

	$ awk -F, '{ print($2) }' <daygame_stats_approaches.csv | sort | uniq

and manually correct them (this is useful for the other fields as well,
just to check consistency).

Anonymizing locations and the names of girls:

	$ awk -F,  'BEGIN { OFS="," }
	{
		if(loc[$2]=="" && $2!="Location")
		{
			loc[$2]=""10*rand();
			gsub(/,/, "", loc[$2]);
		}
		if(name[$8]=="" && $8!="Name")
		{
			name[$8]=""10*rand();
			gsub(/,/, "", name[$8])
		}
		if($2!="Location") { $2=loc[$2]; }
		if($8!="Name") { $8=name[$8]; }
		print($0);
	}' <daygame_stats_approaches.csv >daygame_stats_approaches_anon.csv
	$ mv daygame_stats_approaches.csv daygame_stats_approaches_deanon.csv
	$ mv daygame_stats_approaches_anon.csv daygame_stats_approaches.csv

The approaches file can be found [here](./data/daygame_approaches.csv),
the sessions file can be found [here](./data/daygame_sessions.csv).

Others
-------

Other metrics I track don't deserve as much elaboration.

### Masturbation

I track when I masturbate & how good it feels & the type of
pornography in [this file](./data/masturbations.csv) via [this
script](./data/mstrbt). Data quality is pretty high.

### Mood

I track my mood via the excellent [Mood
Patterns](https://play.google.com/store/apps/details?id=info.moodpatterns.moodpatterns&hl=en&gl=US)
which allows swift CSV export of the data. They even turned changed the
*annoying* "hitting a block of wood with a hammer" notification sound to
the OS default. No post-processing needed, the data *is just there*. An
app by programmers, for programmers.

CSV [here](./data/mood.csv), the data quality is mediocre (long stretches
of not responding to questions, giving more conservative (closer to
50) answers over time, starting to use activities around July 2022
(and not using it for what it was intended for: when the activity is
"Nothing" that means I carried on with my day as normal afterwards, if
the activity is "Mindfulness" it means I spend a couple of seconds in
a more mindful state)). Also, I use the "interested — uninterested"
metric to track horniness.

### Substances

I track which substances I take (nootropics/melatonin/drugs) in [this
file](./data/substances.csv) via [this script](./data/cnsm). Data
quality is good but fairly few entries. Intend to use it for self-blinded
randomized future experiments (if I ever stop procrastinating on them).

### Bag Spreading

Data on bag spreading on public transport, in [this
file](./data/bag_spreading.csv). Data quality is horrible: probably prone
to multiple biases from my side, from different locations, no tracking
of location or datetime…maybe I should just delete this one.
