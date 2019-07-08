[home](./index.md)
------------------

*author: niplav, created: 2019-04-02, modified: 2019-06-24, language: english, status: in progress, importance: 3, confidence: highly likely*

> __A description of this website and its author.__

About
=====

The site
--------

### Content

This website contains essays on different topics, ranging
from programming over philosophy to discussions of odd social
behavior, as well as translations, transcriptions, music
recordings and programming projects.  It follows the idea of [Long
Content](https://www.gwern.net/About#long-content): pages that are
continually getting refined and updated, never quite completely finished,
but approaching stability. This allows for "perpetual drafts", along
with continuous improvement (similar to a wiki, but mainly edited by one
person). Because of this, TODOs are left in the text, making it easier
for me to find them and edit them out, though they may leave the reader
with an unsatisfying feeling of incompleteness.

This is inspired by the idea of Long Content, produced under the motto

> Think Less Wrong, act Long Now and Suck Less.

*– paraphrasing [Gwern Branwen](https://www.gwern.net/), [“About This Website”](https://www.gwern.net/About), 2019*

For this reason, articles are not published by date,
but rather by category, both to make it easier to read
the content of the site in order (i. e. to ["Start at the
Beginning"](https://entirelyuseless.com/2018/06/12/start-at-the-beginning/))
and to structure it by topic and form, rather than to strive for quick
attention grabbing.

The content on this website is licensed under [Creative Commons
4.0](https://creativecommons.org/licenses/by/4.0/).

#### Essays

The essays contain mainly new material, both short arguments and
collections of links, but also longer descriptions of new ideas or
analyses of concepts where existing descriptions (e.g. on Wikipedia or
other blogs) were deemed incomplete. It is of course not possible to
avoid replicating existing ideas (it is not possible for me to read
anything beyond a slim part of existing texts on a topic before writing
my own ideas down), but it seems likely that the idea will at least
be new to most readers.

Generally I use the rule: Let t be the time it would take to write a
text about the idea I was thinking about. Then the time spent researching
whether the idea exists already should stop take at most `$\frac{t}{2}$`.

#### Translations, Transcriptions & Archives

It [seems
possible](https://reducing-suffering.org/ways-writing-valuable/#Old_content_vs_new_content)
that archiving content has a much bigger impact than creating new
content. Given that I write mostly for self-expression, it is a small
factor in most of what I do, but occasionally I transcribe or translate
texts in order to make them more easily accessible.

The translations are often intertwined with the effort of learning other
languages or exercising language skills that would otherwise be forgotten.
For that reason, they can be of quite low quality, so I'm always grateful
for corrections sent my way.

#### Music Recordings

#### Programming Projects

This site also acts as a central place of organisation for different
programming related projects and contributions. That includes pages
representing programming projects, but also literate programs (TODO:
Wikipedia link here) containing code, comments, tests and performance
measurements. Most programs will be written in [a small number of
programming languages](./uses_this.html#List-of-Programs).

### Style

The style of writing is mostly formal US english.

* Titles and headers use the (TODO: information about the exact style) style of capitalization
* MathJax is used only when necessary
* The Oxford comma is not used (find out what exactly that would entail, and check whether this is true or not)
* Code is not syntax-highlighted
* A passive voice is preferred, but I have to get into the flow of writing, so texts may contain that as well. TODO: get rid of "we"?
* No footnotes/endnotes (see https://entirelyuseless.com/2015/07/11/are-hyperlinks-a-bad-idea/)
* Quotes have the following style: `*– [Author Name](https://en.wikipedia.org/wiki/Author_Name), [“Chapter” in “Work Name”, p. 1](https://work-name.com), Year*`. If the work is not online, link the Wikipedia page.
* For pages, optimal is to give the page number of the quotation in the linked PDF. If it is not available, the page number written at the bottom of the page is used.
* Link to document: typical style
	* for one author: `[Author Year](./title_author_year.pdf)`
	* for two authors: `[Author&Coauthor Year](./title_author_coauthor_year.pdf)`
	* for more than two authors: `[Author et al. Year](./title_author_et_al_year.pdf)`
* The year for a text is usually the best date of the last significant change to the text.
* Link individual chapters from books, not whole books, whole papers are okay.
* Sections every article contains:
	* link back to the index page `[home](./index.md)`
	* metadata on the article, bold&quoted abstract
	* title of the article
	* "External Links"/"See Also" for links to other websites discussing the same (or very similar) ideas
	* "Discussions" for external discussions on the article
* Long numbers written with SI-postfixes (K for thousand, M for million etc.) (TODO: Wikipedia link here!)

### Writing Checklist

* Spell checking using [aspell](http://aspell.net/)
* check broken markdown
* broken citations
* "labour" instead of "labor", "behaviour" instead of "behavior"
* links for authors to Wikipedia
* capitalization (capitalisation?) of headings
* proselint?
* fixing 404'ed links?

### Organisation

Tags for texts (mainly taken from http://www.gwern.net/About):

* author "author"
* creation date "created"
* [translator "translator"]
* [translation date "translated"]
* [transcriptor "transcriptor"]
* [transcription date "transcribed"]
* modification date "modified"
* language: {english, german, french, serbocroatian, esperanto, lojban, ithkuil, toki pona}
* confidence {certain, highly likely, likely, possible, unlikely, highly unlikely, remote, impossible, log, fiction, theory, translation, transcription, emotional, other}
* status {notes, draft, in progress, finished, abandoned}
* importance [1;10]

### Implementation

The website is built writing the articles in Markdown (TODO: link here)
and them compiling them to standard HTML using `markdown_py` (TODO:
link). Mathematical formulae are typeset using MathJax. It only uses
only minimal CSS (highlighting code and quotes, centering the text and
limiting line length) and no JavaScript.

### Influences

* [gwern.net](https://www.gwern.net)
* [reducing-suffering.org](https://reducing-suffering.org/)
* [suckless.org](https://suckless.org)
* [lesswrong.com](https://lesswrong.com)

### Inspiration

https://guzey.com/personal/why-have-a-blog/

The author
----------

### Contact

Contact address is `niplav@posteo.net`.

PGP public key:

	-----BEGIN PGP PUBLIC KEY BLOCK-----
	mQENBFxjMzUBCAD1GrTHAZ+K50WTzvZJBoUiXhnqIDO7mHpdsD9bpNDGFLudeQKE
	5BjTV4F4Sfp8BxQU3uo9WUGqPWpYsWZ5VHyYbFoQUZaXulDslwNOfLY4vlT6SLHN
	5aoLHVDnZQ7wP44nsubIu4iDVUWpKCSQBaxSLku9u1eINlGshXVPlQbxwWoHpxS1
	Wkpo3wVI8RKDVNuCnSJhUPdYz9L/yIIm833UJ/sSuv6DM3VVKZxNqCB7XJq8qXdg
	JwaOIMzPiJAnJSvIedOAo5JKDdQNpQ1e7thufPRZVG0vOxt8c+zO8eajMiiG6yMk
	PMPNaRuKfv/2wZVX/37sIwaHIgj7NxknHix1ABEBAAG0Gm5pcGxhdiA8bmlwbGF2
	QHBvc3Rlby5uZXQ+iQFUBBMBCAA+FiEEuOHrdbohn8dtrXQGKf5C00UfR10FAlxj
	MzUCGwMFCQPCZwAFCwkIBwIGFQoJCAsCBBYCAwECHgECF4AACgkQKf5C00UfR12Q
	bwf+LpmGTGKThsOx0yycplid03ws4sbdXYlEnfzWMgemiJqa4jmwmcExHGhbNbnq
	wdz7bnXY2qa8oG3mJW/vqWbFIkv8k96bPTshaHg9JzoelooSkmG3rrtSPuKYebrC
	cJN3eyRERGU39oFJGqPLytVlv9XshLBHvZKA4WRZe6iBco++YRRPk8OLfY4GFXrC
	68DQZof/MLYjYqHxsm9y4eGLhT3MjbgKnFeia0J3XvGnKfAsbQpKGdRkJaOG3ht4
	04jb0QHja/3+Px1+iVL0k405IZ1rxiYmstQ1pa3OTQ4HhoB37BMb6R4sKIF8AyMP
	WGw2ZtikL7HiQZdc3o2I1HLCXrkBDQRcYzM1AQgAucsvQoAi/bYfEKcTtUPt4EqM
	z2NUkwPCOFJxTu5sSIgTioZbXAlHeCCIXAUVi8sUK496Ymmf5cLjqw8rUeSVorL6
	Eh9bB6S+gDn8/RlWgqU377pK4f6SIuOCHo1vHcLJ9YeIpwv660KgHci3J40lcTpz
	7oTlJNu3NxU+F53o+YO5IGOmuNsokXpeCERnnpJpEjaqE+IdyYaAxVHfxcwbUODu
	ZhA9hkmdYMn9pNiSiSFSNpCSS/D9ZS4+UWV3602IfKegGt6V1W89W78QA1mzALze
	I1GmpgqlQM5Z/BmKL/zH3NC4rwBTqU62oaf0XZlgIWaM6SbdCZaK4IxDgTDcBwAR
	AQABiQE8BBgBCAAmFiEEuOHrdbohn8dtrXQGKf5C00UfR10FAlxjMzUCGwwFCQPC
	ZwAACgkQKf5C00UfR12icwgAlIpsa66lxUEQrMk27V9fXH89h540Y7W3n2rssDKb
	bY1D8gtfbnQ3Uhs+Sy+XtKSSfpLlI8qVmYfW1UFmyViYkh3bWmT3lQo4ap/JTACm
	bkA6Gxj91lMqwJMUxSTEgAPaZwkvPB2I2PMWuLBjjsXdA3Y/i64kPPRDO+Exxewi
	DxfYMGTQf89lrPifvT5y78NL6S8FqHcGeWrwEXsuumg0RDC7uBm9PC5DFEtZQmxP
	AxRVmda5oa7eNp72JTYpkbna9n6v6QLpWsbr702tKgJmj8NS1QMx+YKFw5U9eP4x
	INanMfBMaiGYGd1BKfd6xJfapLLRimDp6nUbaVMimNo99w==
	=9nws
	-----END PGP PUBLIC KEY BLOCK-----

### Elsewhere on the Internet

### Personality Tests

### Anonymity
