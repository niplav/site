[home](./index.md)
-------------------

*author: niplav, created: 2019-04-24, modified: 2019-05-14, language: english, status: draft, importance: 4, confidence: possible*

> __Pipes (TODO: link to Wikipedia here) are an integral part of the unix
> operating system. They come in different variants (TODO: FIFOs and unnamed
> pipes here) and have many applications. Here I show how to abuse simple
> text files and unnamed pipes to create cycles of data flow.__

Pipe Rings
==========

The Basic Idea
--------------

A pipe ring has the following structure:

	$ echo init >a
	$ tail -f a | [filters] >>a

Usually, `fil` contains some initialization values. These initialization
values are then written into the pipeline, transformed by the filters,
and concatenated to the file. `tail -f` then reads those new lines from
the file in the order that they were generated, and new data is produced
by the filters.

Examples
--------

### Fill Disk

The simplest pipe ring uses no filters at all:

	$ echo test >a
	$ tail -f a >>a

It simply fills the disk with a file containing the line "test".

### Stop Ring

To stop the unconstrained use of hard disk memory, one can use sed:

	$ echo test >a
	$ tail -f a | stdbuf -oL sed '100q' >>a
	$ wc -l a
	101

`stdbuf` is needed because on most system, the bytestreams flowing through
pipes are buffered. This means that if the command is `tail -f a | sed
'100q' >>a` instead, sed consumes all input, writes to the buffered
output (which has usually a size greater than the length of the line,
on my system it is `#define BUFSIZ 1024`). `bufsiz` sets the output to line
mode, which allows the `sed` output to be propagated without delay.
Fortunately, `stdbuf` only needs to be used once, the effect propagates in the
pipe:

### mu

TODO: Quote the relevant passage from the book, formulate it as a formal
grammar and describe what kind of grammar it is.

In his book “Gödel, Escher, Bach: An Eternal Golden Braid” Douglas
Hofstadter describes a logical system called mu. It contains the alphabet
`${m, u, i}$`, a starting word, and four rules to modify words to create
new ones.

The rules are:

* An 'i' at the end of a word can be changed to 'ui'
* A 'm' at the beginning of a word, followed by the rest of the word 'X', can be changed to 'mXX'
* 'iii' can be substituted with 'uu'
* 'uu' can be deleted

One can now implement a system that generates valid derivations of words
in mu.  For this, one can use a pipe ring: The first word is written at
the beginning of a file, and one generates new words and appends them
to the file to again be used for derivation.

A gawk script implements the four rules (TODO: find out whether gensub()
is gawk specific, and if yes, whether it can be replaced):

	/i$/ { print(gensub("i$", "iu", 1)) }
	/^m/ { print(gensub("^m(.+)$", "m\\1\\1", 1)) }
	/iii/ { i=split($0, a, "iii")-1; for(c=1; c<=i; c++) print(gensub("iii", "uu", c)) }
	/uu/ { i=split($0, a, "uu")-1; for(c=1; c<=i; c++) print(gensub("uu", "", c)) }

One can now write an rc script (TODO: link here) to implement a pipe
ring that generates mu expressions.

	#!/usr/bin/env rc
	
	fn apr{
		awk '/i$/ { print(gensub("i$", "iu", 1)) }
			/^m/ { print(gensub("^m(.+)$", "m\\1\\1", 1)) }
			/iii/ { i=split($0, a, "iii")-1; for(c=1; c<=i; c++) print(gensub("iii", "uu", c)) }
			/uu/ { i=split($0, a, "uu")-1; for(c=1; c<=i; c++) print(gensub("uu", "", c)) }'
	}
	
	# function for unsorted uniq
	fn usuniq{
		awk '{ if(a[$0]==0) { print($0); a[$0]=1; } }'
	}
	
	tail -f mu | stdbuf -i0 -oL apr | usuniq >>mu

### Crawl a Website

External Links
--------------

dgsh (directed graph shell)
