[home](./index.md)
------------------

*author: niplav, created: 2019-09-09, modified: 2019-12-23, language: english, status: notes, importance: 2, confidence: log*

> __Notes and ideas for texts & programs that will be written decades
> in the future, as well as music.__

TODO
====

Site
-----

* Make more mobile-friendly
* Add tooltips to links (Title of Text)
* Find out how to make the site more inclusive
* (a) link for archives?
* Get rid of "we", use "I" instead.
* Confidence intervals for some values
* Improve citation (both to wikipedia and to papers)

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
* In Favor of Selling Glee
	* Pointing out problems with the ideas in [The Price Of Glee In China](http://slatestarcodex.com/2016/03/23/the-price-of-glee-in-china/)
	*	General idea: When you find out that making people wealthier
		doesn't make them happier, you start thinking about how to make
		them happier instead of trying to find reasons why making them
		wealthier is still a good idea.
	* Read the post carefully
	* Read up on the research
* Missing the Movement
	* "Most Hedonists end up sad!"
	* "Utilitarianism leads to bad results!"
	* "Rationalism leads to believing wrong things!"
	* Related text: [Incremental Progress and the Valley](https://www.lesswrong.com/s/pvim9PZJ6qHRTMqD3/p/oZNXmHcdhb4m7vwsv)
* In Favor of Gish-Gallop
	* https://en.wikipedia.org/wiki/Gish_gallop

### Analyses

* Modelling the Dream-Time (Population will probably start growing again)
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
* Daygame Cost-Benefit
	* Model from ../prog/daygame/daygame.lua
* Actuarial tables for dictators
* Ideology Transition Graphs
	* When people move along ideologies, which paths do they take?
	* How long do they stay at certain ideologies?
	* What are the overall transition probabilities, what are the "sinks" (look up on markov chains)
	* Survey on /r/CapitalismVSocialism
	* One part with selected ideologies:
		* Centrism, Apolitical
		* Social Democracy, Socialism, Communism
		* Liberalism, Left Liberalism, Anarchism
		* Libertarianism, Minarchism, Anarcho-Capitalism
		* Conservativism, Alt-Right, National Socialism, Fascism
	* One part with freely choosable ideologies
* Dice Chains
	*	Throw n dice as long as the sum of their values is higher
		than the previous throw. What is the probability
		distribution on the length of the run?
	* Simulation from ../prog/dicechain/dicechain.lua
* 	Algorithm for distributing production of goods among different
	producers according to comparative advantage
	* producers: {2,n}
	* products: {2,n}
	* transformation curves: {linear, marginal, any}
	* indifference curves: {linear, fixed number, any}
* Building A Big Tower
	* 500 years, ~1 trio. dollars, stable technology, build a tower as big as possible
	* considerations
		* location
			* some mountains nearby for material
			* very stable ground (tower doesn't sink into the ground)
		* energy production
			* nuclear, probably
	* base of the tower probably square
		* length 5-10 km
	* pyramid shaped
		* 100 m for every layer, 20-50m distance to the edge of the last layer
	* big blocks
		* use lava to form them, from pulverized mountains
			* pump up powder/sand/little stones or magma?
			* in the former case, one also needs electricity at the top
* Nuking the Amazon Cost-Benefit Analysis
* What is the most common word I don't use?
* How Strong is the Gender Difference In Sex Drive?
	* /usr/local/doc/unread/blackpill/is_there_a_gender_difference_in_strength_of_sex_drive_baumeister_et_al_2001.pdf
	* /usr/local/doc/unread/blackpill/in_heterosexual_relationships_men_masturbate_more_than_women_waterink_2014.pdf
* Do eegs burst when they're not poked before boiling?
	* Blinded, person needs to poke & write down, but not tell
	* Student's t-test
	* N=200
	* Pre-register

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
	* The Hedonic Treadmill is very good & very bad
* Moral progress as an EA cause area?
* Writing system based on all binary trees with maximal height 2
	* no 's' sounds
* Moving the Lever Closer
	*	Due to an asymmetry in human decision making, making somebody
		causally more responsible for a negative action makes them less
		likely to take that action
	* Related: The bystander effect
* Salty fries
	* Buy something, that creates a need for something else (software <-> support, salty fries <-> drinks)
* Running Away from Your Problems

### Collections

* Simple Unsolved Math Problems
* Differences Between GNU and POSIX `make`
* Better Mathematical Notation
	*	Mathematical notation is not a planned and systematic
		endeavour, but the result of a long process of generation
		and selection of different notations. Here I collect
		contemporary ideas for better notation, and discuss old &
		discarded methods of writing mathematics.
	* Discarded Methods
		* https://en.wikipedia.org/wiki/Begriffsschrift
		* https://en.wikipedia.org/wiki/Newton%27s_notation#Newton's_notation
	* New Notations
		* General
			* https://www.stephenwolfram.com/publications/mathematical-notation-past-future/
			* /usr/local/doc/unread/towards_a_better_notation_for_mathematics_olah_2010.pdf
		* Triangle of Power
			* https://www.youtube.com/watch?v=sULa9Lc4pck
			* https://math.stackexchange.com/questions/30046/alternative-notation-for-exponents-logs-and-roots
			* http://www.solidangl.es/2015/04/a-radical-new-look-for-logarithms.html
	* Read
		* /usr/local/doc/unread/notation/notation_as_a_tool_of_thought_iverson_1986.pdf
* Day Game Log
	*	Keeping track of ones own performance is usually useful for
		improvement<!--TODO: find source!-->. Many people
		who do pick-up, especially daygame<!--TODO: links for
		those two-->, maintain spreadsheets and write field
		reports. This is my personal instance of such a track
		record.
	*	Sessions are usually warm-up (collecting data for other projects, asking
		for directions, compliments, directly asking men for their
		phone number) and then main approaches, with notes on the
		quality of the interaction and the result. At the end,
		I try to extract lessons and ideas for improvement out
		of the session.

### Other

* Coding Standards
	* General Project Setup
	* C
	* Shell Scripting

### Notes

* Be Liberal in what you Accept, but Conservative in what you Emit
* Believing Something Doesn't Mean You to Tell it to Everyone

### Misc

* Mistakes
* Open Questions
* Fundamentals
* Good Ideas

> we should be far more explicit about the assumed background against
> which we intend to communicate.

*– John Nerst, [“30 Fundamentals”](https://everythingstudies.com/2018/07/16/30-fundamentals/), 2018*

### Fiction

* A Religion
	*	A pseudo-mathematical religion combining several
		unrelated ideas is presented and explained.
		Inspired by [Unsong](http://unsongbook.com/)
	* Ingredients
		* Timelessness
			* Plotinus
		* Tegmark's Mathematical Universe
			* /usr/local/doc/unread/physics/our_mathematical_universe_tegmark_2014.epub
		* Symmetry Theory of Valence
			* /usr/local/doc/unread/principia_qualia_johnson_2017.pdf
		* Scott Alexander's Solution to Theodicy
			https://slatestarcodex.com/2015/03/15/answer-to-job/
	* Explanation
		* Creation
		* God
		* Heaven
		* Hell
* Homeless Super-Mathematicians
	* Perhaps in the SCP format?
* Guten Morgen
* A History of Names
* Skalpell Bizeps

> 11-uhr-luft liegt rauh auf dem parkplatzboden.  in den ritzen des
asphalt streitet sich krepierender löwenzahn mit ausgeblichenen
zigarettenstummeln um platz. abblätternde farbe liegt dazwischen,
obwohl die altbauten noch ein paar hundert meter entfernt liegen.

* myzel

> moderne kapitalistische verteilung ist weder zentralisiert noch
dezentralisiert, sie ist myzelisch, verwaberndes, meist unsichtbares
gewebe in einem fruchtbaren umfeld, mit anhäufungen, ballungen und
kumulationen von produktionszentren – zur festigkeit verdichtetes
gewebe dort fassbar, wo es sich am wenigsten äußert. werden als
eine kontingente verschmelzung von fast-sein und konkretheit"

### Translations

* Kodomulo Manifesto (translation of “A Hacker Manifesto”)

Music
-----

### Clarinet

* Clarinet Concerto (Mozart)

### Piano

* The People United Will Never be Defeated (Rzewski)
* Das Wohltemperirte Clavier
* Beethoven Piano Sonatas (Beethoven)
* Impromptus (Schubert)
* Nocturnes (Chopin)
* Gymnopédies/Gnosiemmes (Satie)
* Rhapsodie in Blue (Gershwin)

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
* sif
	* simple text processing filter that takes only one instruction
	* (single instruction filter)
	* instruction form:
		* `[^]/str/[,[^]/str/]((a|i|c)/str/)|d|p`
		* str is a literal string here (no regex)
		* a=>append, i=>insert, c=>change, d=>delete, p=>print
		* '^' means that the following str is excluded from the matched text
	* sif does not do input/output buffering and does treat whitespace as any other character.
	* normally, everything is printed, unless the option '-n' is used.
* pau
	* vis-digraph reads from the terminal input directly and emulates the input of the corresponding character
		* uses table from RFC 1345
			* Seems not extendable, damn
	* if vis-digraph extendable, add:
		* Interrobang	‽	?!
		* Join	⋈	><
		* Expected value	𝔼	|E
		* Real numbers	ℝ	|R
		* Integers        ℤ       |Z
		* Natural numbers	ℕ	|N
		* Triple e	≡	3=
		* Approximately e	≈	~~
		* Subscript a	ₐ	_a / as
		* Subscript e	ₑ	_e / es
		* Subscript h	ₕ	_h / hs
		* Subscript k	ₖ	_k / ks
		* Subscript l	ₗ	_l / ls
		* Subscript m	ₘ	_m / ms
		* Subscript n	ₙ	_n / ns
		* Subscript o	ₒ	_o / os
		* Subscript p	ₚ	_p / ps
		* Subscript s	ₛ	_s / ss
		* Subscript t	ₜ	_t / ts
		* Superscript i	ⁱ	^i
		* Superscript n	ⁿ	^n
	*	daemon that catches such digraphs and emulates them as
		if they were typed, using vis-digraph
* 	mtfs: plan9 file server for a file that returns the current
	metric time on read
* libbruch
	* rational numbers with libzahl
	* some functions:
		* badd(bruch a, bruch b, bruch c): a:=b+c
		* bsub(bruch a, bruch b, bruch c): a:=b-c
		* bdiv(bruch a, bruch b, bruch c): a:=b÷c
		* bmul(bruch a, bruch b, bruch c): a:=a⋅c
		* binv(bruch a, bruch b): a=b^(-1)
	* more functions:
		*	bset, bseti, bsets, bsetu, bstr, bfloor, bceil,
			bmod, bcmp, bcmpu, bsqrt, binit, bfree, bsave,
			bload, bsetup, bunsetup, berror, bperror
* nager
	* sxhkd for the mouse
	* syntax: `[MOUSEEVENT] [, MOUSEEVENT] [ /*possibly nested*/ COMMAND ]`
* erle
	* rlwrap alternative, takes ideas from the fish shell interactive mode
	* normal readline like behavior (but using something simpler, like linenoise/dietline)
	* history file is loaded during startup
	* 	`<text>[UP]` shows the last command containing `<text>`,
		again `[UP]` the one before that, and so on
	*	`<word1> <word2>[TAB]` expands `<word2>` into the last word
		(string separated from the others with a newline/space)
		beginning with `<word2>`
	*	no input for more than half a second/a second shows a suggestion
	        of the last command beginning with the current line.
	* ideas for speeding it up:
	        * use `char**` for storing each history and words
	        * benchmark and optimise, of course
* pandeck
	* convert files from different spaced repetition softwares into another
		* fulgurate .crd
		* mnemosyne
		* anki
* unitspheretransform
	* VR application that visualizes the transformation of the unit sphere in 3-dimensional space
	* also unit circle transform
	* color code the original vectors
	* interpolate them?
* hedonium
	* look up different information-processing centric ideas about consciousness
	* combine them with the symmetry theory of valence
	* implement the best approximation of these
* minspantree
	* implement all algorithms for the minimum spanning tree in a functional programming language
	* like sml/ocaml
	* /usr/local/doc/unread/cs/state_of_the_art_algorithms_for_minimum_spanning_trees_eisner_1997.pdf
* nenio
	* a suckless prolog implementation
	* ISO prolog
* rien
	* suckless sml implementation, sml '97
	* maybe build on mosml

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
	* date/time library for klong: convert different date formats to another
* utf8.kg
	* unicode decoding/encoding library
	* see how myrddin/lua/libutf/plan9 did it
* linalg.kg
	* linear algebra library for klong
	* function for the determinant
	* function for gaussian elimination
	* function for matrix multiplication
	* function for matrix inversion
	* function for the calculation of eigenvalues and eigenbases
	* function for the calculation of polynomial division
* statests.kg
	* library for statistical tests

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
* klong
	* receiving output of shell commands via pipe
	* receiving output of shell commands (maybe via pipe?)
	* self adverb (options are :!, :&, :,, :;, :<, :>, :?)
		* :< and :> should be reserved for something symetric
		* :; is not fit because ; is not really a verb or adverb
		* :!, :&, :? and :, are the best options
	* support for imaginary numbers?
	* nplot
		* Support for multiple bargraphs
		* Bargraphs with negative values
	* nstat
		* n% confidence interval
	* Range is extremely slow for anything but integers, why?
	* error with klong: `#'s58'!40` returns `kg: error: call: type error: [6 :triad %call1 %pop1]`
		* bug, report
* fzf
	* Why doesn't fzf cope well with shuffled or repeated letters?
	* 'niiiiiplav' and 'nlapiv' both take me to the wrong directory, they're obviously meant for my home directory
* dc 9base manpage:
	* typo in the order of operations in the manpage

> \+  - /  *  %  ^
>      Add subtract multiply divide remainder or exponentiate the top
>      two values on the stack.

Archive
-------

* Blogs of which to list the posts chronologically:
	* hbd chick

Structure
---------

* Top-level:
	* Translations
		* English to Esperanto
	* Music
		* Clarinet
		* Piano
	* Programs

General
-------

* Send typos to people, let them correct them
