[home](./index.md)
------------------

*author: niplav, created: 2019-09-02, modified: 2019-09-26, language: english, status: in progress, importance: 2, confidence: other*

> __awitt is a simple window title logger/time tracker. It is linked,
> described and compared to other similar projects. Then, its releases
> and outstanding bugs are listed.__

awitt – Another Window Title Tracker
====================================

The project's sourced code is available on
[github](https://github.com/niplav/awitt), along with its
[README](https://github.com/niplav/awitt/blob/master/README.md) and
[man-page](https://github.com/niplav/awitt/blob/master/awitt.1) for
more documentation.

Description
-----------

awitt is a small unix utility that keeps track of the window title and
class and prints the time, duration spent in the last window, class
and title of the previous window if the focus is changed. The output is
printed to stdout.

This makes it useful for time tracking: window titles usually reflect
the current activity, and with them one can determine how much time was
spent on an activity, and when.

The usual use case is as following:

	awitt >activities.log &

activities.log can then be later analysed using standard unix tools.

Why not Choose `$x$` instead?
------------------------------

There are several time trackers available for unix, but most of them
suffer from the fact that they need manual input of current activities,
which makes them cumbersome and awkward to use. awitt prevents that by
needing only one interaction per restart.

### arbtt

The only other similar time tracker I know is
[arbtt](https://arbtt.nomeata.de/), which is a much more complete and
polished project.

So why not simply choose arbtt and be done with it?

My main problem is with the fact that arbtt is implemented in Haskell.
It's not that Haskell is a bad language, but I heavily dislike having to
install several hundred megabytes of libraries to just run a simple time
tracker. On the other hand, awitt is implemented in C, which makes it
possible to compile and run it on every platform that also provides X11.

awitt also provides little features beyond printing window information
if the focussed window changes, while arbtt seems to integrate a lot of
functionality into a core program. While both approaches have their advantages
and disadvantages, awitt is closer to the unix philosophy of "do one thing,
and do it well".

The disadvantage is that awitt is a duplication of work in arbtt,
and therefore technically a waste of time and energy. I still did it,
because reinventing the wheel is fun.

Releases
--------

* 0.0.1: Core functionality provided

Bugs
----

### Definitely Bugs

* Encoding problems: 'ä' is printed as the two bytes 0xe4 0x2e. `file windows.log` says 'Non-ISO extended-ASCII text, with escape sequences'
* `awitt` crashes when the currently focussed window is closed before obtaining the title (a race condition).

### Possibly Bugs

* Window title changes are only logged if they last longer than 1 second.
* [Unix time](https://en.wikipedia.org/wiki/Unix_time) is not optimal, use [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) instead
