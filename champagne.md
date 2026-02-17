
The Champagne Toasting Problem
--------------------------------

Here's a puzzle: A few two-dimensional telekinetics are sitting around
a circular table. They want to toast each other with their champagne
glasses so that each person's glass touches each other person's glass
at least once, but they want to move their glasses as little as possible
(telekinesis is kind of stressful), and return the glass to their seat.

What's the optimal path for their glasses to take?

Or, formulating it slightly more mathematically: Take a 2-d
plane (`$ℝ^2$`), and create `$n$` disks of radius `$r$` on
that plane, arranged so that they're at the corners of a regular
`$n$`-[gon](https://en.wikipedia.org/wiki/Regular_polygon) and the
distance `$d$` of two adjacent disks is greater than `$2r$`. We want to
find a path for each (center of a) disk so that:

1. Every disk has a tangent with/touches every other disk.
2. Disks don't intersect, ever, neither while moving nor while stationary.
3. Every disk returns to its original location.
3. The sum of all path-lengths is minimized.

Disks are allowed to graze while moving, paths taken by disks can overlap
but disks may not intersect.

The problem is trivial for zero to three disks:

Zero disks: Don't do anything. You win.  
One disk: Also don't do anything. You win.  
Two disks: The disks move in a straight line to meet, then move back.

<video src="./vid/champagne/2.webm" type='video/webm' controls>
</video>

Three disks: All three disks move to the center of the [equilateral triangle](https://en.wikipedia.org/wiki/Equilateral_triangle) their initial positions formed, form a triplet, and then return to their original position.

<video src="./vid/champagne/3.webm" type='video/webm' controls>
</video>

I have an idea for four disks that I suspect is probably correct (for
disks A, B, C, D, we move A & B & C into the middle so they form a
triplet, then move in D so that D first touches B & C, then D "pushes"
B & C away to briefly touch A and then all return to their corners)
but I'm not certain this is the optimal solution.

<video src="./vid/champagne/4.webm" type='video/webm' controls>
</video>

I have some intuitions around how to approach `$n=5$` but nothing
really reliable, I got Claude 4.5 Sonnet to implement a search for a
best solution for `$n=5$`, here's the resulting solution:

<video src="./vid/champagne/5_ea.webm" type='video/webm' controls>
</video>

(Claude 4.5 Sonnet also wrote the [manim](https://www.manim.community/)
code for the animations, thanks Claude :-)

### Is This Problem Known?

I asked Claude 4.5 Sonnet & Opus to research whether this problem has
been formulated, they both returned the answer "no". This surprises me,
since it feels pretty intuitive? Maybe this means that anyone who notices
this problem is also smart enough to see the trick to immediately solve
it (at least conceptually), *or* this means that it's kind of an ugly
problem that nobody wants to deal with?

### Concepts That Could Be Relevant

1. [Circle packing](https://en.wikipedia.org/wiki/Circle_packing), [kissing number](https://en.wikipedia.org/wiki/Kissing_number)
2. Combinatorial geometry, [rendezvous problems](https://en.wikipedia.org/wiki/Rendezvous_problem)
3. [Constrained optimization](https://en.wikipedia.org/wiki/Constrained_optimization), collision-free path planning, [Lagrangian relaxation](https://en.wikipedia.org/wiki/Lagrangian_relaxation)
4. [Variational principle](https://en.wikipedia.org/wiki/Variational_Principle)???

### How To Solve It?

Vague intuitions: One probably wants a bunch of triplets to meet early
on. Maybe divide all disks into triplets (triplets of neighbors along
the polygon?) which meet early on, split up again?

### Speculation

__Conjecture__: In optimal solutions all disks take piecewise linear
paths.

This could be wrong if it's sometimes optimal to slide a disk around
some other disk because moving many disks to disentangle them is not
worth the distance incurred.

__Speculative question 1__: What happens in higher dimensions
where we want all pairs of spheres to kiss at least once? Initial
placement through equal spacing on a sphere via [Thompson's
problem](https://en.wikipedia.org/wiki/Thomson_problem).

__Speculative question 2__: Could a generalized version be
[Turing-complete](https://en.wikipedia.org/wiki/Turing-Complete)? Where
you drop the constraint of keeping all disks on the corners of a
polygon and instead position them arbitrarily relative to each
other in space? In that case the initial position of the disks
is the "program", the trajectory taken is the output of the
program. Perhaps one needs to restrict the underlying space to
something more discrete than `$ℝ^2$` to avoid accidental [real
computation](https://en.wikipedia.org/wiki/Real_computation).

### Visualizations of Best Approximations

<video src="./vid/champagne/6_ea.webm" type='video/webm' controls>
</video>

<video src="./vid/champagne/7_ea.webm" type='video/webm' controls>
</video>
