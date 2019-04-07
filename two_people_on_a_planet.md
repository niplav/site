[home](./index.md)
-----------------

*author: niplav, created: 2019-04-02, modified: 2019-04-07, language: english, status: in progress, importance: 2, confidence: likely*

> __Two people are abducted and placed on the opposite poles of a
> habitable planet. They want to find each other, but they have no
> way to communicate. The only things they know is their their own
> respective position on the planet and the position of the equator and
> the poles. Here, different methods for finding each other under similar
> conditions are explained and discussed.__

Two People on a Planet
======================

The Problem
------------

The original problem is taken from *[What If?, Munroe 2014, p. 183](./doc/lost_immortals_munroe_2014.pdf)*:

> If two immortal people were placed on opposite sides of an uninhabited
> Earthlike planet, how long would it take them to find each other?

Here, several clarifications are added to the problem.

For the following ideas, it is not necessary that the planet is
earth-like, but it is assumed that the planet has a relatively flat
surface, lacking oceans, where the two people can leave footprints.

Each of the two people has the following abilities:

* Know their own position on the planet
* Walk at approximately the same speed
* Reason about the other person

Both lack all other abilities, including (but not limited to) creating
new technology, communicating when they are out of sight (no fireworks,
launching spaceships etc.).

Both people don't know each other, so they can't infer anything about
each others' specific behavior, they also didn't have the ability to
communicate before.

These two people want to find each other.

Different Existing Solutions
----------------------------

### Munroes' Solutions

Munroe proposes different solutions:

* Walk around at random: He states that they would find each other within 3000 years (though no explicit calculation is provided).
* Agree beforehand to meet at a specific point on the planet (such as the highest mountain, one of the poles etc.).
* Follow the coastlines of the continents. This is not applicable here, because it is assumed that there are no oceans.
* Follow the coastlines of the continents, but after each circling, decide randomly whether to switch direction or resume the known path.
* Walk at random, while leaving a trail of signs with increasing counter along the way, increasing ones speed when finding an unknown trail.

### Randomly Switching Positions

Another solution is possible due to the fact that both people start out
at the opposite sides of the planet. Each person determines randomly
whether they should travel to the opposite side of the planet or stay
at ones own side for the duration of such a travel. This drastically
decreases the time until meeting, since the chance of not having met after
n such iterations the chance of having met is `$1-\frac{1}{2^n}$`. Munroe
proposes coin flips to determine whether one changes position, but one
can imagine other such methods if coins are not available: One could
assign the choice of staying to the left body half and the choice of
going to the other side of the planet to the right body half, and then
choosing the strategy based on which part of the body itches first.
This would be useful since humans are notoriously bad at generating
random bits (TODO: put a citation here).

TODO: Think of other possible ways the body can generate random bits.

https://math.stackexchange.com/questions/1214022/fastest-way-to-meet-without-communication-on-a-sphere  
https://mathoverflow.net/questions/184404/randall-munroes-lost-immortals  

[Rendezvous problem](https://en.wikipedia.org/wiki/Rendezvous_problem)  
[Deterministic rendezvous problem](https://en.wikipedia.org/wiki/Deterministic_rendezvous_problem)  

A Better Solution
-----------------

A better solution is possible because both people start out at the
opposite sides of the planet, and know their own respective position on
the planet.

Taking their own position as one pole, they could infer an equator as
the set of points on the planet that is equally far away from each of
their positions. They would then both proceed to go to this equator
and start walking along it. Then each person could follow the following
algorithm: If they had walked less than half of the circumference
of the planet, and encountered footsteps, they would reverse direction.
If they had walked more than half of the circumference of the planet,
they would continue walking no matter whether they would see other
footsteps on the ground.

This would ensure that they would meet in constant time.

Why it Works
------------

Here, it is assumed that they both reach the equator at the same time.

TODO: Add illustrations?

If both start walking towards each other, the algorithm succeeds:
Both can walk at most half of the length of the equator upon meeting
each other in the extreme case, namely, starting back to back and not
realizing it. In this case, the last part of the method is not applied,
because both will walk less than half of the length of the equator in
any case. In this case, finding each other takes at most `$\frac{3}{4}$`
of the time it takes to walk across the whole equator (including the
walk from the starting point to the equator).

If they both start walking in the same direction, the method still
succeeds: one of the two people has a distance of less than half of the
length of the equator to the starting point of the other person. This
person `$p_1$` walks that distance, and then can use that fact as a
distinguishing strategy for acting, namely, turning around and starting
to walk towards the other person. The other person `$p_2$` can use the
fact that their distance to the starting point of the other person is
more than half of the length of the equator to distinguish themselves,
and continue walking. Because `$p_1$` is now walking towards `$p_2$`,
they will definitely meet. Interestingly, because they are both walking
the whole time, it will take them less than one walk across the whole
equator for this algorithm (again including the journey from the pole
to the equator).

Complications
-------------

There are, of course, several problems with this approach.

### The Strategy is not Obvious

This objection of course applies to all possible strategies, including
Randomly Switching Positions and nearly all of Munroes propositions.
Ideally, one would try to generate all possible strategies of a typical
agent and then generate a probability distribution over them, using
methods such as Minimum Message Length and Solomonoff Induction from
algorithmic complexity theory to penalize very complex solutions.

TODO: Add links to Wikipedia for them.

A good approximation to this is to assume that the other person is moving
around randomly, accounting slightly the possibility that they have
stayed where started, and then taking into account the other strategies
proposed here.

### Arriving at Opposite Points on the Equator Fails

If both of them arrive at opposite sides of the equator, following the
algorithm will result in them both switching their direction or both
of them continuing with their course.

See Also
--------
