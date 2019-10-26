[home](./index.md)
------------------

*author: niplav, created: 2019-09-09, modified: 2019-10-22, language: english, status: notes, importance: 5, confidence: log*

> __Notes and ideas for texts that will be written decades in the future.__

TODO
====

Site
-----

* Make more mobile-friendly
* Add tooltips to links (Title of Text)
* Find out how to make the site more inclusive
* (a) link for archives?

Texts
-----

### Arguments

* Why Still Choose C?
	* Long-term reliability/stability
	* Performance
	* Portability
	* → Caveat: Only portable if very reliably/portably written
* Unix is Not About Reimplementing Unix
	* Examples for claim:
		* [Node JS](http://blog.izs.me/post/48281998870/unix-philosophy-and-nodejs)
		* [The Internet](https://victorops.com/blog/internet-age-unix-philosophy/)
		* [Vim](https://www.reddit.com/r/vim/comments/22w1li/a_fair_comparison_between_vim_and_emacs/cgqyqst/)
		* https://gist.github.com/rjsteinert/f3823f3cdc9971779c17
	* ["Do one thing, and do it well. Use text streams, since that is the universal interface"](http://www.catb.org/esr/writings/taoup/html/ch01s06.html)
	* Most systems reimplement unix ("Those who don't understand unix are doomed to reimplement it, poorly.")
* Libertarianism is too Simple
	*	Libertarianism is a very simple method of organising society,
		so it must have been tried in the history of societies. However,
		none of those societies have survived, which makes it an
		unsuccessful way of structuring societies
	* Counter-argument: Humans are consistently biased against liberty
	*	Counter-argument: Libertarianism is very well suited for
		*modern* (capitalist, technological) societies, which haven't
		existed for very long
* Antinatalism and Consent
* Limit “Philosophy” and “Art”
* Against Advertising
	* Strong claim: Advertising is always bad
	* Weak claim: Advertising in public spaces is bad
	* Does this hold up to a good consequentialist calculation?
* Against News
	* Priming → News+Wikipedia≤Wikipedia
* On the Importance of
	* Qualia Engineering
	* Track Records, Forecasting and Prediction Markets
	* The Difference in Sexual Behavior Between Men and Women
	* Pick Up

### Analyses

* Modelling the Dream-Time (Population will probably start growing again)
* Considerations on Cryonics
	* Model of when to sign up for Alcor neurocryopreservation
	* Sign up as early as possible
	* Value of a year of life in the future
		* Freedom to die again?
		* How probable is malevolent AI?
		* What about "meh" futures?
		* What about work, friends, language, culture and other circumstances?
		* Prior: The quality of future human life is normally distributed around the neutral case
	* Which methods of revival?
		* Personal identity?
		* If only neuropreservation, where do I get my body from?
* Dumpster Diving
* Hitch Hiking
* Keyboards
	* Hardware
		* Hands too near each other
		*	Staggered keys maybe increase learning time, possibly
			increase typing time (sqr(2) instead of 1 movement distance)
	* Software
		* Layouts are a problem
		* Two modes: key position on keyboard & character presented by key
* Table Diving
* Walking Barefoot
* Pick Up
	* Direct Number on Street
	* Direct Date on Street
	* Direct Date off Street
* Actuarial tables for dictators

### Ideas

* Ends of Discussions
	* Dissolving the question
		* Discussion about the meaning of a word
		* Disagreement about an arbitrary category (morality/aethetics)
	* Bet
	* Agreement
* The End of History Fallacy
* The “If Everyone Just” Argument
	* The argument just assumes one of the biggest problems away: coordination and cooperation
	* Related: [Malthusianisms](https://www.scottaaronson.com/blog/?p=418)
* Missing the Movement
	* "Most Hedonists end up sad!"
	* "Utilitarianism leads to bad results!"
	* "Rationalism leads to believing wrong things!"
	* Related text: [Incremental Progress and the Valley](https://www.lesswrong.com/s/pvim9PZJ6qHRTMqD3/p/oZNXmHcdhb4m7vwsv)
* Information and Markets:
	* Explanation
		* Information as a non-scarce good
	* Existing solution
		* Copyright
		* Patents
	* Problems with patents/copyright
		* creates a temporary monopoly
		* → all regular problems with monopolies as result
			* no competition
			* therefore, less/no innovation
			* higher prices
			* prevention of further work based on the innovation
			*	copying is inherent to (all but quantum) information,
				preventing it is theoretically (and for the most part also
				practically) impossible
			*	possible overcompensation: some people get a lot more money
				than appropriate for the work they put in, some get nothing
			* it's ontologically confused
	* Possible solutions:
		* Pay for production
			* Patreon
			* Kickstarter
		* Premium models
		* Advertising
			* Problem: getting harder the more products come into the information domain
		* Open-source model: free work
* Infinite Fractal Meta Recursion
* Preference Frustration Auctions
* The Tyranny of the Mill
* Moral progress as an EA cause area?

### Collections

* Simple Unsolved Math Problems
* Differences Between GNU and POSIX `make`

### Other

* Coding Standards
	* General Project Setup
	* C
	* Shell Scripting

### Notes

* Use Things Up
* Be Liberal in what you Accept, but Conservative in what you Emit

### Misc

* Project Ideas
* Mistakes
* Open Questions
* Fundamentals

> we should be far more explicit about the assumed background against
> which we intend to communicate.

*– John Nerst, [“30 Fundamentals”](https://everythingstudies.com/2018/07/16/30-fundamentals/), 2018*

### Fiction

* Homeless Super-Mathematicians
	* Perhaps in the SCP format?

### Translations

* Kodomulo Manifesto (translation of “A Hacker Manifesto”)

Music
-----

### Clarinet

* Clarinet Concerto (Mozart)

### Piano

* The People United Will Never be Defeated (Rzewski)
* Das Wohltemperirte Clavier
* Beethoven Piano Sonatas
* Schubert Impromptus
* Chopin Nocturnes
* Satie Gymnopédies/Gnosiemmes

Programming
-----------

* cap
	*	simple language for assembling different files into one. syntax very
		sed/ed like, mostly like this: `[line,]line@file[<|^|>][line,]line[|comm]`
		where line is a regex enclosed in '/' with an optional number suffix
		or a line number, file is a filename and comm is a shell command in
		single quotes. the text from each file is inserted into a buffer and
		printed at the end of the cap script.
* toc
	*	time out cat, which prints its input unless there was no
		input for more than argv[1] seconds (try different
		versions, settle for the most exact version that is
		not unbearably slow).
* lvst
	* print levensthein distances of strings
	* option '-f' for the field separator
	* can be used for fuzzy search
	* usage:

			$ lvst "test"
			foo
			3:test:foo
			bar
			4:test:bar

* cy
	* A very simple version control system, written in rc. inspiration from put and get, from "the unix programming environment".
	* supports 3 operations
		* init (initialize a repository)
		* put (make a commit)
		* get (go back to a certain commit)
	* tracks changes within files and deletion/creation of files
	* reason: git/hg are good, but way too huge for private, simple, linear, personal repositories.
	* inspiration: svn/rvn/eie<!--TODO: links for these-->
* fle
	* suckless pager
	* commands
		* [f]orwards
		* [b]ackwards
		* [u]p
		* [d]own
		* [j] (line up)
		* [k] (line down)
		* [g] (first line)
		* [G] (last line)
		* [/] for searching
		* [n]ext and [p]revious match
	* support for arbitrary length files, loading lazily, unicode is displayed properly, big lines are dealt with properly.
* recog
	* program that accepts one backus-naur form grammar and checks if it's input or other files match that grammar.
	* BNF -(Convert to Chomsky Normal Form)> CNF -(Cocke-Younger-Kasami algorithm)> Boolean
	* Relevant material:
		* RFC 2234
		* RFC 4234
		* RFC 5234
		* RFC 7405
	* Possible BNF forms:
		* ABNF (RFCs)
		* EBNF
		* naive & simple form (similar to the one used on Wikipedia)
			* <symbol\>
			* optionality: '?'
			* repetition: '+'
			* repetition with optionality: '*'
			* alternative symbols: '|'
			* assignment: '::='
			* "string"

### Klong Libraries

* combin.kg
	* combinatorics library for klong
	* exponentiation
	* tetration
	* n-tation
	* factorial
	* binomial coefficient
	* stirling numbers (1st/2nd kind)
	* eulerian numbers (1st order, 2nd order)
	* catalan numbers
	* counting partitions
* date.kg
	* date/time library for Klong: convert different date formats to another
* utf8.kg
	* unicode decoding/encoding library
	* see how myrddin/lua/libutf/plan9 did it
* linalg.kg
	* linear algebra library for klong
	* function for the determinant
	* function for matrix inversion
	* function for the calculation of eigenvalues and eigenbases
	* function for the calculation of polynomial division

### Contributions

* mupdf
	* implement unicode search
	* improve search overall, lacking
	* why don't ← and → work for next/prev page?
* myrddin
	* documentation: "and modern features with a high cost-benefit ratio"
	* cost/benefit is high? Clarify
* vis
	* add C-a and C-e for beginning of line and end of line in insert mode
	* add C-← and C-→ for jumping words in insert mode (equivalent of b and e)
	* fix syntax highlighting for ocaml with single quotes: 'a takes the whole line
	* Syntax highlighting of inline code in markdown is annoying (dark blue background!)
* sad
	* implement features that weren't finished
	* care for it
* toxcore
	* maybe
	* single/group
	* chat/audio/video
	* not much more, really
* neo2
	* port neo2 to plan9/9front/Haiku OS

Archive
-------

* Blogs of which to list the posts chronologically:
	* hbd chick

Structure
---------

* Top-level:
	* Writing
		* Nonfiction
			* Analyses
	* Translations
		* English to Esperanto
	* Music
		* Clarinet
		* Piano
	* Programs

General
-------

Get rid of "we", use "I" instead.
