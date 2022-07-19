[home](./index.md)
-------------------

*author: niplav, created: 2022-07-07, modified: 2022-07-19, language: english, status: notes, importance: 2, confidence: log*

> __.__

Types & Methods of Data Collection I Use
=========================================

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
