[home](./index.md)
-------------------

*author: niplav, created: 2022-07-07, modified: 2024-07-08, language: english, status: maintenance, importance: 2, confidence: log*

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

*—[Gwern](https://gwern.net), [“Zeo sleep self-experiments”](https://www.gwern.net/Zeo), 2018*

At least I now know that I'm falling into this trap, "Selbsterkenntnis
ist der erste Schritt zur Besserung". And the second step is to bring
all of your data in a usable format.

Anki
-----

I use spaced repetition, and plan to take it as a proxy for cognitive
performance in QS experiments.

The data can be found in the helpfully named `collection.anki2`, which
is actually an [sqlite](https://en.wikipedia.org/wiki/SQLITE) database
in disguise.

The [Anki manual](https://docs.ankiweb.net/stats.html#manual-analysis)
helpfully informs that the most important table is `revlog`, one can
then export the data to CSV with the following command:

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

Similarly, one can export meditation data from Medativo (if one has
coughed up 5€ for the premium version, which I decided was worth it
for the data, after having locked myself in :-|):

	echo -e '.headers on \n select * from History;' |
	sqlite3 meditation_2022-07-02T20:00:00.db |
	tr '|' ',' >meditations.csv

The names for the columns are exceedingly obvious and need no further
explanation.

I didn't rate my sessions in the beginning (and manually inserted
data from meditation retreats with unrated sessions), leading to
a very optimistic default of 4.0 mindfulness and "concentration"
(better called absorption, I claim). So we remove those, using
the [sam](https://plan9.io/sys/doc/sam/sam.html) language in
[vis](https://github.com/martanne/vis):

	,/^1,/;/^860,/
	x/4\.0,4\.0,/c/,/
	,/^1210,/;/^1308,/
	x/4\.0,4\.0,/c/,/
	,/^1594,/;/^1615,/
	x/4\.0,4\.0,/c/,/

The CSV of the meditation data can be found [here](./data/meditations.csv).

`mindfulness_ranking` and `concentration_ranking` are both subjective
impressions directly after meditation, where "mindfulness" describes the
degree of sensory clarity, and "concentration" (better called "absorption"
or "rest") describes my ability to rest on a specific sensory object.

Daygame
--------

<!--TODO: Clean up as per https://claude.ai/chat/f2735ad5-dfd6-4d0c-aaaa-6e1a43f96498-->

Sanitizing the sessions file by converting the datetime to
[ISO-8601](https://en.wikipedia.org/wiki/ISO-8601) using [structural
regular
expressions](./doc/cs/structural_regular_expressions_pike_1990.pdf "Structural Regular Expressions"),
and some other minor fixes:

	,x/([0-9]+)\/([0-9]+)\/([0-9]+) /c/\3-\1-\2T/
	,x/; /c/;/
	,x/(T[0-9]+:[0-9]+),/c/\1:00,/
	,x/-([0-9])-/c/-0\1-/

Formatting the approaches file:

	,x/ ,/c/,/

Find incorrectly written locations:

	$ awk -F, '{ print($2) }' <daygame_approaches.csv | sort | uniq

and manually correct them (this is useful for the other fields as well,
just to check consistency).

Anonymizing locations and the names of the women:

	$ awk -F, 'BEGIN {
		FS = OFS = ","
		while (getline < "admn/daygame/locations") {
			loc[$2] = $1
		}
		close("locations")
	}
	{
		if (name[$8] == "" && $8 != "Name") {
			name[$8] = int(100000 * rand())
			gsub(/\./, "", name[$8])
		}
		if ($2 != "Location") {
			original_location = $2
			gsub(/"/, "", original_location)
			if (loc[original_location] == "") {
				print "Warning: Location '" $2 "' not found in locations file" > "/dev/stderr"
				loc[original_location] = 100000 * rand()
				printf "%d,\"%s\"\n", id, location >> "admn/daygame/locations"
			}
			$2 = loc[original_location]
		}
		if ($8 != "Name") {
			$8 = name[$8]
		}
		print $0
	}' <daygame_approaches.csv >daygame_approaches_anon.csv
	$ mv daygame_approaches.csv daygame_approaches_deanon.csv
	$ mv daygame_approaches_anon.csv daygame_approaches.csv

The approaches file can be found [here](./data/daygame_approaches.csv),
the sessions file can be found [here](./data/daygame_sessions.csv).

Approaches file datapoints (in CSV):

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

Sessions file:

* Datetime start
* Datetime end
* Approaches index number range
* Number of approaches

Fitbit Biometrics
------------------

I use the [Fitbit Inspire
3](https://en.wikipedia.org/wiki/List_of_Fitbit_products#Fitbit_Inspire_3)
because Fitbit is one of the few (the only?) companies whose products
allow for data exporting, mostly to track my sleep, but maybe I'll also
get mileage out of the heart rate, step, glucose and temperature tracking.

Sleep data [here](./data/sleep.json).

Others
-------

<!--TODO: light.csv, islight.csv, ispomodoro.csv, pomodoros.csv-->

Other metrics I track don't deserve as much elaboration.

### Masturbation

I track when I masturbate & how good it feels & the type of
pornography in [this file](./data/masturbations.csv) via [this
script](./data/mstrbt). Data quality is pretty high.

* `t` stands for text
* `a` stands for audio
* `i` stands for image
* `v` stands for video

### Mood

I track my mood via the excellent [Mood
Patterns](https://play.google.com/store/apps/details?id=info.moodpatterns.moodpatterns&hl=en&gl=US)
which performs [experience
sampling](https://en.wikipedia.org/wiki/Experience_sampling_method) allows
swift CSV export of the data. They even turned changed the *annoying*
"hitting a block of wood with a hammer" notification sound to the OS
default. No post-processing needed, the data *is just there*. An app by
programmers, for programmers.

But there is still *some* data cleanup to do:

	sort -n mood.csv >>~/proj/site/data/mood.csv

Finally I rename the mood columns simply to "happy", "content", "relaxed",
and "horny".

CSV [here](./data/mood.csv), the data quality is mediocre (long stretches
of not responding to questions, giving more conservative (closer to
50) answers over time, starting to use activities around July 2022
(and not using it for what it was intended for: when the activity is
"Nothing" that means I carried on with my day as normal afterwards, if
the activity is "Mindfulness" it means I spend a couple of seconds in
a more mindful state)). Also, I use the "interested — uninterested"
metric to track horniness (higher means hornier).

### Substances

I track which substances I take
([nootropics](./nootropics.html)/melatonin/drugs) in [this
file](./data/substances.csv) via [this script](./data/cnsm). Data quality
is good but fairly few entries. At the moment I am mostly using it to
perform self-blinded RCTs.

### Weight

Tracking weight, mostly for exercise purposes. Data
[here](./data/weights.csv), collected with [this script](./data/weight).

### Daily Performance Metrics

Productivity, creativity and the subjective length of the
day. Collected with [this script](./data/mental) into [this
file](./data/mental.csv). Started collecting subjective length of the
day on 2023-08-21.

### Bag Spreading

Data on bag spreading on public transport, in [this
file](./data/bag_spreading.csv). Data quality is horrible: probably prone
to multiple biases from my side, from different locations, no tracking
of location or datetime…maybe I should just delete this one.

### Phone Data

Via [Sensor
Logger](https://play.google.com/store/apps/details?id=com.kelvin.sensorapp&hl=en_US),
I use my phone as an easy way to collect large amounts of data. I don't want to
make the files public, as they contain information that could de-pseudonymise me.

### Forecasting Performance

In principle it should be possible for me to track my forecasting
performance on Manifold, Fatebook/PredictionBook and Metaculus,
given that all of them have APIs over which data can be exported and
analyzed. In practice I haven't done so yet, but it might be a good
(albeit slow-to-evaluate) proxy for cognitive performance.
