[home](./index.md)
-------------------

*author: niplav, created: 2019-02-10, modified: 2019-06-17, language: english, status: in progress, importance: 3, confidence: possible*

> __Solutions to the [99 problems](./99_klong_problems.md)
> in [Klong](http://t3x.org/klong/index.html) in a [literate
> programming](https://en.wikipedia.org/wiki/Literate_programming)
> style. Attempts to produce the shortest complete solution to these
> problems up to date.__

99 Problems Klong Solutions
===========================

Acknowledgements
----------------

s7 is by [nmh](http://t3x.org/nmh/index.html), who wrote it
[in the Klong documentation](http://t3x.org/klong/klong-ref.txt.html).
[/u/John_Earnest](https://old.reddit.com/user/John_Earnest) provided a
[more elegant](https://old.reddit.com/r/apljk/comments/59asq0/pack_duplicate_consecutive_elements_into_sublists/)
s9 on [/r/apljk](https://old.reddit.com/r/apljk/). Dave Long provided
a much more elegant s8, s26, c1, s49 and s55 over email.

Conventions
-----------

Since this collection of solutions attempts to maximize for terseness,
several considerations concerning completeness have to be made. There
is nearly no checking for correct arguments, except for empty lists.
Variables are declared locally. The solution for problem N is called
`sN`, helper functions are numbered `aN` for the Nth helper function
in __Working with lists__, `bN` in __Arithmetic__, `cN` in __Logic and
Codes__ and so on.

Prerequisites
-------------

The solutions use `flr` from the util library and `sqr` from the math
library in the standard library.

	.l("util")
	.l("math")

These would be, of course, trivial to implement on your own: `flr::{[f];f::x;y@(f'y)?1}`
and `sqr::{[a];a::x;:[0=x;0;{(x+a%x)%2}:~a]}` (taken directly from the library).

Working with Lists
------------------

### P01 (\*) Find the last element of a list.

The function reverses the first argument and then returns the first element.

	s1::{*|x}
	mylast::s1

Testing with the example obtains the correct result:

		mylast([:a :b :c :d])
	:d

Another possible version would be `s1::{x@((#x)-1)}`, but much to my
surprise it takes about twice as long on 3 mio. elements (1.47 seconds
as opposed to 0.65 seconds on my machine):

	$ time -p kg -e 's1::{*|x};s1(!3000000)'
	2999999
	real 0.65
	user 0.57
	sys 0.06
	$ time -p kg -e 's1::{x@((#x)-1)};s1(!3000000)'
	2999999
	real 1.47
	user 1.41
	sys 0.06

Klong apparently has a very efficient reversing operation for lists.

### P02 (\*) Find the last but one sublist of a list.

This implementation uses a property of the Take verb that allows
indexing from the end of the list with negative numbers. A longer and
less elegant solution, re-using `s1`, would be `s2::{((|x)@2),s1(x)}`.
Alternatively, one could also use direct indexing while reversing the
list: `s2::{(|x)@[1 0]}`.

	s2::{(-2)#x}
	mybutlast::s2

We again take the test from the problems list:

		mybutlast([:a :b :c :d])
	[:c :d]

### P03 (\*) Find the K'th element of a list.

This one is very straightforward in Klong: indexing is zero-based,
so one subtracts one of the second element and then extracts the value.

	s3::{x@y-1}
	elementat::s3

Testing:

		elementat([:a :b :c :d :e];3)
	:c

### P04 (\*) Find the number of elements of a list.

Since `#` is a Klong primitive for the length of a list, this
problem is trivial.

	s4::{#x}

### P05 (\*) Reverse a list.

Similar to problem 5, there is a primitive for this.

	s5::{|x}

### P06 (\*) Find out whether a list is a palindrome.

Since `=` compares a list element-wise (and returns a list with boolean
values corresponding to the equality of the two lists), we have to use
the `~` primitive, which compares lists by structure and content. So we
compare `x` and its reversion that way.

	s6::{x~|x}

### P07 (\*\*) Flatten a nested list structure.

This particularly elegant solution is taken from the Klong
documentation. It applies the concatenation operator to the sublists of
a list as long as the list changes with each operation, and then returns
the list.

	s7::{,/:~x}
	myflatten::s7

Tests:

		myflatten([:a [:b [:c :d] :e]])
	[:a :b :c :d :e]

This is also the result in the problems statement.
Testing it with nested empty lists also works:

		myflatten([[] [[]] [[][]]])
	[]

Unfortunately, this solution fails with lists containing only one element:

		myflatten([0])
	0

TODO: Find a solution that doesn't do this.

### P08 (\*\*) Eliminate consecutive duplicates of list elements.

This solution first creates a list of `1` and `0` that has `1` at at
positions where in `x` the element is followed by an value different
from itself. Because one has one element too much in the list (`[]` has
the positions `[1]`), we only take as many elements as we need off the
beginning of the resulting positions list (in these cases, it's `#x`,
the length of the argument list).
We then use Expand/Where to find the positions of 1 in the list of
positions, and extract them with At/Index.

	s8::{x@&(#x)#~0,~:'x}
	compress::s8

Compressing the example list returns the desired result:

		compress([:a :a :a :a :b :c :c :a :a :d :e :e :e :e])
	[:a :b :c :a :d :e]

And compressing the empty list (and a 1-element list) works as well:

		compress([])
	[]
		compress([1])
	[1]

### P09 (\*\*) Pack consecutive duplicates of list elements into sublists.

Here, we first do the same matching between the elements as in P08,
but then we reverse the results and append 0 at the start. In that
way, we can use Expand/Where to obtain the positions of `1` in the list
(that's where the element in the list changes). We then can use Cut to
cut out sublists ending before the given positions. Because `~~:'[]`
returns not `[]`, but the number `1` (for whatever reason), we have
to build in a special case for the empty list at the beginning.

	s9::{:[x~[];[];(&0,~~:'x):_x]}
	pack::s9

Since the problems don't specify how we should deal with empty
lists (whether one should return `[]` or `[[]]`), we could consider
`s9::{(&0,~'~:'x):_x}`, which returns the latter. But this clashes with
`s10`, where `s10([])` returns `[[0]]`, which doesn't seem to be correct
at all.

Testing it:

		pack([:a :a :a :a :b :c :c :a :a :d :e :e :e :e])
	[[:a :a :a :a] [:b] [:c :c] [:a :a] [:d] [:e :e :e :e]]

### P10 (\*) Run-length encoding of a list.

As the problem statement suggests, this solution is pretty
straightforward. For every sublist of the result of `s9`, we append
its length to its first element.

	s10::{{(#x),*x}'s9(x)}
	encode::s10

Tests:

		encode([:a :a :a :a :b :c :c :a :a :d :e :e :e :e])
	[[4 :a] [1 :b] [2 :c] [2 :a] [1 :d] [4 :e]]

### P11 (\*) Modified run-length encoding.

Again, this is quite easy. For the result of `s10`, we test whether the
length of the sublist is 1, and if it is, then we return just the value,
otherwise we return the list.

	s11::{{:[1=*x;*|x;x]}'s10(x)}
	encodemodified::s11

Testing:

		encodemodified([:a :a :a :a :b :c :c :a :a :d :e :e :e :e])
	[[4 :a] :b [2 :c] [2 :a] :d [4 :e]]

This works fine. However, `encodemodified` shows weird behavior with lists with one element:

		encodemodified([0])
	[0 [0]]
		encodemodified([1])
	[1]

TODO: Fix this.

It works fine with `[]`, though:

		encodemodified([])
	[]

### P12 (\*\*) Decode a run-length encoded list.

Here, we simply execute a function over the list: If the list element
is an atom (it is itself not a list), we simply return it, otherwise
we use Reshape to repeat the last element of `x` (`x` has the form
`[freq val]`) `freq` times. The result is then flattened by appending
the list elements to each other.

	s12::{,/{:[@x;x;(*x):^x@1]}'x}

### P13 (\*\*) Run-length encoding of a list (direct solution).

The difference between 'creating sublists' and 'indexing them' is
not very big in Klong, but a reasonable attempt is presented here.
We start like in P09: First, we check whether our function argument
is the empty list, in case of which we return immediately with the
empty list. Otherwise we store the outer function argument `x` in
the local variable `a`. Then we proceed by again executing Match
between the elements of the list, and append `1` at the beginning
to indicate that we want to include the first sublist. This results
in a list containing the starting positions of the sublists with different
elements. We pass this list pairwise to a function, where we first
check whether the difference is `1`. In this case, the sublist has
length `1` as well and can be returned as an atom, otherwise we
return the length of the sequence concatenated with its first element.

	s13::{[a];a::x;:[x~[];[];{:[1=y-x;a@x;(y-x),a@x]}:'&1,~~:'x]}
	encodedirect::s13

Testing this function should return the same result as `s11`:

		encodedirect([:a :a :a :a :b :c :c :a :a :d :e :e :e :e])
	[[4 :a] :b [2 :c] [2 :a] :d]

Which it does.

One can now compare the speed of the direct solution with the speed of
the indirect solution:

	$ time -p kg -e 's9::{:[x~[];[];(&0,~~:\'x):_x]};s10::{{(#x),*x}\'s9(x)};s11::{{:[1=*x;*|x;x]}\'s10(x)};s11(!1000000)'
	[...]
	real 1.99
	user 1.82
	sys 0.10
	$ time -p kg -e 's13::{[a];a::x;:[x~[];[];{:[1=y-x;a@x;(y-x),a@x]}:\'&1,~~:\'x]};s13(!1000000)'
	[...]
	^C
	real 8582.60
	user 8196.00
	sys 0.11

`s13` ran too long, so it had to be aborted, but it is at least 2
orders of magnitude slower than `s11`.

TODO: Explore why `s13` is so much slower.

### P14 (\*) Duplicate the elements of a list.

This solution is a specialization of the solution to P15. We take the function
`2:^x` (repeat x 2 times, abusing Reshape) and call Each-Left on the first
function argument with it. Because the result is a list of lists, we then have
to flatten the list using the well known `,/` pattern.

	s14::{,/2:^:\x}
	dupli::s14

There are two alternative, but longer solutions: `s14::{,/{x,x}'x}`
is more naïve, and `s14::{x@_0.5*!2*#x}` is perhaps slightly more
amusing.

The test runs through, as expected:

		dupli([:a :b :c :c :d])
	[:a :a :b :b :c :c :c :c :d :d]

We're now interested in the performance of these functions, so we time
calling the different versions with `10000` elements:

	$ time -p kg -e 's14::{,/2:^:\\x};s14(!10000)'
	[...]
	real 1.39
	user 1.37
	sys 0.00
	$ time -p kg -e 's14::{,/{x,x}\'x};s14(!10000)'
	[...]
	real 1.38
	user 1.36
	sys 0.00
	$ time -p kg -e 's14::{x@_0.5*!2*#x};s14(!10000)'
	[...]
	real 0.11
	user 0.09
	sys 0.01

As one can see, the indexing-based solution is by far the fastest,
with little difference between the other two.

### P15 (\*\*) Replicate the elements of a list a given number of times.

Here we have the more general case of P14. We simply have to replace `2`
by the second argument `y` here: Repeat `x` `y` times for every `x` in
the first argument, then concatenate the result.

	s15::{,/y:^:\x}
	repli::s15

Test:

		repli([:a :b :c];3)
	[:a :a :a :b :b :b :c :c :c]

### P16 (\*\*) Drop every N'th element from a list.

The example given indicates that the indexing is 1-based. The Drop verb
doesn't work with two lists (although that would make a nice addition
to the language), so we have to find a simpler solution. `s16` works
by creating a list with all indices to `x` (`!#x`) and then executing
the modulo of `y` on it. The result is a list in the form of `[0 1 2 3 … (y-1) 0 1 2 3 …]`.
The elements we want to avoid are at the positions where the list
contains `y-1`, so we create a list where `1` is at the positions
where the original list had elements smaller than `y-1`. We then use
`&` to obtain the positions of the value `1` and then simply index `x`
by those positions.

	s16::{x@&(y-1)>(!#x)!y}
	drop::s16

We test the implementation:

		drop([:a :b :c :d :e :f :g :h :i :k];3)
	[:a :b :d :e :g :h :k]
		drop([:a :b :c];1)
	[]
		drop([];1)
	kg: error: rem: type error: [[] 1]

So our solution fails for empty lists. We could modify it to
include a simple conditional statement to return the empty list
if `x` is `[]`: `s16::{:[x~[];[];x@&(y-1)>(!#x)!y]}`.

TODO: Think about including this into the full text.

### P17: (\*) Split a list into two parts, the length of the first part is given.

For this problem, Split is the fitting verb. It can receive a list of
lengths, and is quite lenient with lists that don't fit exactly. So we
concatenate `y` with the total length of `x` and then just split `x`
by that.

	s17::{(y,#x):#x}
	split::s17

An alternative solution could be `s17::{(,y#x),,y_x}`, in which one
concatenates taking `y` elements of `x` with dropping `y` elements of `x`.

Executing the test returns the correct result:

		split([:a :b :c :d :e :f :g :h :i :k]; 3)
	[[:a :b :c] [:d :e :f :g :h :i :k]]


The Split verb doesn't work with a range of `0`:

		split([1 2 3];0)
	kg: error: split: range error: 0

### P18: (\*\*) Extract a slice from a list.

Here, we can simply take the first `z` elements from the start of
the list, and then drop `y-1` elements of that list (we have to subtract
`1` because indexing in lists is `0`-based).

	s18::{(y-1)_z#x}
	slice::s18

The test runs through, as expected:

		slice([:a :b :c :d :e :f :g :h :i :k];3;7)
	[:c :d :e :f :g]

However, passing arguments that are not long enough gives some
interesting results:

		slice([:a];3;7)
	[:a :a :a :a :a]

This happens because if Take doesn't find enough elements, it simply
repeats the elements it finds.

An alternative solution, using Index over a range, is
`s18::{x@(y-1)+!1+z-y}`.

### P19: (\*\*) Rotate a list N places to the left.

Klong has a verb for that™. By default, `:+` rotates to the right with
positive, and to the left with negative integers, so we have to reverse
the sign of `y`.

	s19::{(-y):+x}
	rotate::s19

Tests:

		rotate([:a :b :c :d :e :f :g :h];3)
	[:d :e :f :g :h :a :b :c]
		rotate([:a :b :c :d :e :f :g :h];-2)
	[:g :h :a :b :c :d :e :f]

### P20: (\*) Remove the K'th element from a list.

It's quite possible that there is a short and elegant solution with 3
combined adverbs, but this solution does the obvious: it concatenates
the first `y-1` elements of `x` with the last elements of `x` that don't
contain the `y`th element.

	s20::{((y-1)#x),y_x}
	removeat::s20

Tests:

		removeat([:a :b :c :d];2)
	[:a :c :d]
		removeat([];1)
	[]

Alternative solutions could use Expand over a list of booleans
`s20::{x@&~(y-1)=!#x}` or double rotation `s20::{(-y-2):+1_(y-1):+x}`

### P21: (\*) Insert an element at a given position into a list.

Here, one can use a naïve solution takes the first `z-1` elements from
the list, concatenates them with `x`, and then concatenates the result
with the rest of `y`.

	s21::{((z-1)#y),x,(z-1)_y}
	insertat::s21

The given test passes successfully:

		s21(:alfa;[:a :b :c :d];2)
	[:a :alfa :b :c :d]

Other solutions are possible, for example a hack using the Amend verb with
lists and then flattening the result `s21::{,/y:=(,x,y@z-1),z-1}` or re-using
solution 17 to obtain the sublists `s21::{[r];r::s17(y;z-1);(*r),x,r@1}`.

Timing the different solutions returns unsurprising results:

	$ time -p kg -e 's21::{((z-1)#y),x,(z-1)_y};s21(1;!1000000;500000)'
	[...]
	real 0.55
	user 0.34
	sys 0.08
	$ time -p kg -e 's21::{,/y:=(,x,y@z-1),z-1};s21(1;!1000000;500000)'
	^C
	real 6819.67
	user 6437.26
	sys 0.30
	[...]
	$ time -p kg -e 's17::{(y,#x):#x};s21::{[r];r::s17(y;z-1);(*r),x,r@1};s21(1;!1000000;500000)'
	[...]
	real 0.66
	user 0.47
	sys 0.09

The Amend solution is much slower, mainly because of the flattening at
the end. The solution re-using `s17` is a bit slower, maybe because
of storing the result in a local variable or because Cut is a more
expensive operation.

### P22: (\*) Create a list containing all integers within a given range.

This one is quite simple, although a bit clunky. We simply create a
list of integers from 0 to `y-(x-1)` (in Klong, because of right-to-left
operator evaluation, simply `y-x-1`), and add x to that.

	s22::{x+!y-x-1}
	range::s22

Tests run through like a breeze:

		range(4;9)
	[4 5 6 7 8 9]

### P23 (\*\*) Extract a given number of randomly selected elements from a list.

We don't use solution 20 because we don't have to. Instead, we wrap the
function into an Iterate verb that gets executed `(#x)-y` times, and
each of these iterations we drop one element of the list that has been
rotated a random number of positions in the range `0`..`#x`. That way
we remove the right number of elements and return a list of the size `y`.

	s23::{((#x)-y){1_(_.rn()*#x):+x}:*x}
	rndselect::s23

Tests are a bit different here, because we obtain a random result. But
we can check if it does the approximately right thing:

		rndselect([:a :b :c :d :e :f :g :h];3)
	[:b :d :f]
		rndselect([:a :b :c :d :e :f :g :h];1)
	[:h]
		rndselect([:a :b :c :d :e :f :g :h];0)
	[]

### P24 (\*) Lotto: Draw N different random numbers from the set 1..M.

The solution to this is pretty simple. With `s23`, we already have a
function to draw N elements from a list, so we only have to create the
set 1..M, or, in Klong-speak, `1+!M` (where M is the second argument
`y` to the function).

	s24::{s23(1+!y;x)}
	lottoselect::s24

Testing:

		lottoselect(6;49)
	[6 11 12 13 35 37]
		lottoselect(1;49)
	[13]
		lottoselect(0;49)
	[]
		lottoselect(10;10)
	[1 2 3 4 5 6 7 8 9 10]

Using `s22` here would be wasteful, since that would use up more bytes
than simply typing `1+!y`: `s24::{s23(s22(1;1+y);x)}`. We don't need
the given hint.

### P25 (\*) Generate a random permutation of the elements of a list.

A quite nice solution is the following: First, one creates a list of
random numbers that has the same length as the first argument using the
Iterate adverb. Then, one uses Grade-Down (or Grade-Up, in this case
synonymous) to create a list of random indices, and uses Index/At to
pick the elements in this random order from `x`.

	s25::{x@<(#x){x,.rn()}:*[]}
	rndpermu::s25

Tests:

		rndpermu([:a :b :c :d :e :f])
	[:d :c :b :a :e :f]
		rndpermu([])
	[]
		rndpermu([:a])
	[:a]

It is probably slower than a more naïve
[Fischer-Yates shuffle](https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle)
like equivalent `s25::{(#x){p::_.rn()*#x;(x@p),s20(x;p+1)}:*x}`, since
Grade-Up `<` sorts the list, which results in a `$O(n*log(n))$` time
complexity, while Fischer-Yates is just `$O(n)$`.

We can compare the two:

	$ time -p kg -e 's25::{x@<(#x){x,.rn()}:*[]};s25(!10000)'
	[...]
	real 0.94
	user 0.93
	sys 0.00
	$ time -p kg -e 's20::{((y-1)#x),y_x};s25::{(#x){p::_.rn()*#x;(x@p),s20(x;p+1)}:*x};s25(!10000)'
	[...]
	real 4.48
	user 4.45
	sys 0.00
	$ time -p kg -e 's25::{x@<(#x){x,.rn()}:*[]};s25(!20000)'
	[...]
	real 3.62
	user 3.59
	sys 0.00
	$ time -p kg -e 's20::{((y-1)#x),y_x};s25::{(#x){p::_.rn()*#x;(x@p),s20(x;p+1)}:*x};s25(!20000)'
	[...]
	real 14.68
	user 14.54
	sys 0.01

Further doubling of the array size returns following runtimes in seconds:

* Grading: `0.94,3.62,14.93,64.56`
* Fisher-Yates: `4.48,14.68,76.71,298.38`

Both seem to grow with roughly `$O(n^2)$`. There is probably a Klong verb that
runs in `$O(n^2)$` and was used in `s20` or `s25`.

### P26 (\*\*) Generate the combinations of K distinct objects chosen from the N elements of a list.

This solution is a _bit_ more complicated than the previous ones. It
takes a recursive approach, with the base case being `1`, returning a
list that contains all elements in the original list as sublists: `,'y`.
Each recursive step first creates all suffixes of the list, then calls
`s26` with the tail of that suffix and appends the first element to each
of the results.

If the suffixes were not created, calling the function would result in
duplicates: `s26([:a :b];2)` would return `[[:a :b][:b :a]]`.

The suffixes are created with the expression `{x}{1_x}\``y`, using the
While adverb and exploiting the fact that `[]` is equivalent to `0`
(false) in Klong. This expression can be expressed as "While x is not
the empty list, drop one element of the front of list, and return all
intermediary results".

The appending uses the Append verb with the Each-Left adverb, appending
the first element of the list to all sublists.

In the end, the result needs to be flattened with `,/`, because the
elements are themselves put in sublists and empty lists are left in
the result.

	s26::{[k];k::x;:[1=k;,'y;,/{(1#x),:\s26(k-1;1_x)}'{x}{1_x}\~y]}
	combination::s26

Testing:

		combination(3;[:a :b :c :d :e :f])
	[[:a :b :c] [:a :b :d] [:a :b :e] ...]
		combination(3;[])
	[]
		combination(0;[:a :b])
	[]
		combination(3;[:a :b])
	[]

### P27 (\*\*) Group the elements of a set into disjoint subsets.

Fortunately, given `s26`, both `group3` and `s27` are quite easy to
implement. `group3` First generates all subsets of `x` containing 2
members, and then passes them on to another function. This function
creates the set difference `a1` of the argument and the set passed
(for example, when `x` is for the local function is `[:a :b]`, and `a`
is `[:a :b :c :d]`, then `a1(a;x)` is of course `[:c :d]`). Of this,
all subsets with length 3 are generated with `s26`, and the result is
concatenated with the sets from the first call of `s26`. The results
are then passed, and the same procedure is repeated for subsets of size 4.

`a1` is not a very efficient implementation of set difference (it seems
to have a quadratic run-time of `$O(n*m)$`). But it is short and easy to
implement: it filters out all elements out of `x` that can be found in
`y`. The quadratic run-time can thus be explained easily: For each
element in x; that element has to be searched in `y`, resulting in
[a runtime](https://en.wikipedia.org/wiki/Big_O_notation#Product) of
`$O(n)*O(m)=O(n*m)$`, where `$n$` is the size of `x` and `$m$` is the
size of `y`.

`s27` is basically a recursive version of `group3`, producing just the
result of `s26` for the base case and applying the same set-difference
call of `s26` as in `group3`.
It does not check whether the length of `x` corresponds to the size specified
by `+/y`, although that would be trivial to implement.

	a1::{[b];b::y;flr({[]~b?x};x)}
	group3::{[a];a::x;*'{x,:\,'s26(4;a1(a;,/x))}',/{(,x),:\,'s26(3;a1(a;x))}'s26(2;x)}
	s27::{[a b];a::x;b::y;:[1=#y;,'s26(*y;x);,/{x,:\,'s26(*b;a1(a;,/x))}'.f(x;1_y)]}
	group::s27

The tests given in the specification have gigantic results, but small samples confirm
the correct behavior of `group3`:

		group3([:aldo :beat :carla :david :evi :flip :gary :hugo :ida])@[0 1 2 3]
	[[[:aldo :beat] [:carla :david :evi] [:flip :gary :hugo :ida]]
	[[:aldo :beat] [:carla :david :flip] [:evi :gary :hugo :ida]]
	[[:aldo :beat] [:carla :david :gary] [:evi :flip :hugo :ida]]
	[[:aldo :beat] [:carla :david :hugo] [:evi :flip :gary :ida]]]

Similarly, this also works for `s27`:

		s27([:aldo :beat :carla :david :evi :flip :gary :hugo :ida];[2 3 4])@[0 1 2 3]
	[[[:aldo :beat :carla :david] [:evi :flip :gary] [:hugo :ida]]
	[[:aldo :beat :carla :david] [:evi :flip :hugo] [:gary :ida]]
	[[:aldo :beat :carla :david] [:evi :flip :ida] [:gary :hugo]]
	[[:aldo :beat :carla :david] [:evi :gary :hugo] [:flip :ida]]]
		s27([:a :b :c];[1 2])
	[[[:a :b] [:c]] [[:a :c] [:b]] [[:b :c] [:a]]]
		s27([:a :b :c :d];[2 2])
	[[[:a :b] [:c :d]] [[:a :c] [:b :d]] [[:a :d] [:b :c]]
	[[:b :c] [:a :d]] [[:b :d] [:a :c]] [[:c :d] [:a :b]]]
		s27([:a];[1])
	[[[:a]]]

Empty lists don't work

		s27([:];[])
	kg: error: interrupted

But set sizes that don't sum to the length of the original list still work:

		s27([:a :b :c :d];[1 2])
	[[[:a :b] [:c]] [[:a :b] [:d]] [[:a :c] [:b]]
	[[:a :c] [:d]] [[:a :d] [:b]] [[:a :d] [:c]]
	[[:b :c] [:a]] [[:b :c] [:d]] [[:b :d] [:a]]
	[[:b :d] [:c]] [[:c :d] [:a]] [[:c :d] [:b]]]

### P28 (\*\*) Sorting a list of lists according to length of sublists

a) Sorting a list after the length of its sublists is nearly trivial in
Klong. Create a list with the lengths of the sublists, then grade that
list and select the indexes from the original argument.

	s28a::{x@<#'x}
	lsort::s28a

Tests:

		lsort([[:a :b :c] [:d :e] [:f :g :h] [:d :e] [:i :j :k :l] [:m :n] [:o]])
	[[:o] [:d :e] [:m :n] [:d :e] [:a :b :c] [:f :g :h] [:i :j :k :l]
		lsort([])
	[]
		lsort([:a])
	kg: error: size: type error: [:a]

It is not stable, though:

		lsort([[:a][:b]])
	[[:b] [:a]]

b) In this exercise, the solution is supposed to sort the sublists of a
list according to the frequency of length of the list. So if there are
5 lists with length 2, and one list with length 7, the five lists with
length 2 come first, and then the list with length 7.

I haven't found a very elegant and beautiful solution for this, but the
obvious answer is quite straightforward and direct: First, one obtains the
lengths of the sublists and groups (so that the indices of lists with the
same length are put into sublists. This is assigned to the variable `f`.
We then sort this list after the length of its sublists so that we simply
repeat the implementation of s28a (which takes more bytes to be called
than to be implemented in-line). Finally, `x` is indexed with the flattened
version of these indices.

	s28b::{[f];f::=#'x;x@,/f@<#'f}
	lfsort::s28b

Tests:

		lfsort([[:a :b :c] [:d :e] [:f :g :h] [:d :e] [:i :j :k :l] [:m :n] [:o]])
	[[:o] [:i :j :k :l] [:a :b :c] [:f :g :h] [:d :e] [:d :e] [:m :n]]
		lfsort([])
	[]
		lfsort([[:a]])
	[[:a]]

One can see that `lfsort` returns the correct result, but is not stable:
`[:o]` occurred after `[:i :j :k :l]` in the original list, but is before
it in the returned value.

Arithmetic
----------

	s31::{:[[0 1]?x;0:|[2 3 5]?x;1;&/(x!2,3+2*!_sqr(x)%2)]}
	s32::{:[0=y;x;.f(y;x!y)]}
	s33::{1=s32(x;y)}
	s34::{[t];t::x;#&{s33(x;t)}'!x}
	b1::{[a];a::y;{:[0=x!a;_x%a;x]}\~x}
	b2::{[p a];p::&s31'!1+_x%2;a::x;p@&(#'{b1(a;x)}'p)-1}
	s35::{:[s31(x);,x;b2(x)]}
	s36::{{(x@1),x@0}'s10(s35(x))}
	s37::{*/{((x@0)-1)*(x@0)^((x@1)-1)}'s36(x)}
	s38::{"s34 is faster than s37"}
	s39::{[p];p::&s31'!y;p@(x<p)?1}
	b3::{[n];n::x;flr({s31(x@1)};{x,,n-x}'s39(1;x))}
	s40::{*b3(x)}
	b4::{2*1+_x%2}
	b5::{[l u];l::b4(x);u::b4(y);b3'l+2*!_(u-l)%2}
	s41a::{*'b5(x;y)}
	s41b::{[m];m::z;flr({m<*x};s41a(x;y))}

Logic and Codes
---------------

	and::{x&y}
	or::{x|y}
	nand::{~x&y}
	nor::{~x|y}
	xor::{(x|y)&~x&y}
	impl::{~x&~y}
	equ::{~xor(x;y)}
	c1::{(-x)#(&x),{:[x;.f(x:%2),x!2;0]}:(y)}
	c2::{[n];n::x;{c1(n;x)}'!2^n}
	c3::{[f];f::x;{(,x),,,f(x)}'c2(y)}
	s46::{c3(x;2)}
	s47::{s46(x)}
	s48::{c3(x;y)}
	s49::{:[x;{(0,:\x),1,:\|x}:(.f(x-1));,[]]}
	c4::{(,((**x)+*x@1),(,*x),,(x@1)),2_x}
	c5::{:[2=#x;,(,y),x@1;.f(x@1;y,0),.f(x@2;y,1)]}
	s50::{c5(*{~1=#x}{c4(x@<*'x)}:~x;[])}
	frq::{[t];t::x;{(#x),t@*x}'=x@<x}

Binary Trees
------------

	d1::{:[3=#x;d1(x@2),d1(x@1),,@x@0:|(2>#x)&@*x;1;0]}
	s54::{&/d1(x)}
	d2::{,/x{y,:/x}:\y}
	s55::{:[x<2;
		,x#,:x;
		{:x,'x}'{{:[x~y;d2(x;x);d2(x;y),d2(y;x)]}:(,'s55(x:%2);,'s55(x-x:%2))}:(x-1)]}
	s56::{:[*3=^x;
		&/{:[(~3=*^y)|~3=*^x;
		(^x)=^y;1,.f(x@1;y@2),.f(x@2;y@1)]}:(x@1;x@2):|2>*^x;1;0]}
	d3::{[m];m::(#x):%2;:[2>#x;x;(x@m),(,.f(x@!m)),,.f((1+m)_x)]}
	s57::{d3(x@>x)}
	s58::{flr({s56(x)};s55(x))}
	s59::{:[x<2;,x#,:x;{:x,'x}'{d2(x;x),d2(y;x),d2(x;y)}:(,'s59(x-1);,'s59(x-2))]}

	minnodes::{:[x<1;0:|x=1;1;1+.f(x-1)+.f(x-2)]}

Seems to be the sum of the first `x` fibonacci numbers.

	minnodes::{+/(x-1){(+/2#x),x}:*[1 0]}

Attempt, using the fibonacci number approach:
TODO: currently incorrect.

	maxheight::{[k];k::x;#1_{k>+/x}{(+/2#x),x}:~[1 0]}

	d4::{:[x=0;0;1+_ln(x)%ln(2)]}
	d5::{[n];n::x;({~d4(x)>n}{x+1}:~0)-1}
	d6::{,/x{(,y){x,,y}:\x}:\y}
	d7::{d6(x;y),d6(y;x)}
	d8::{[h];h::(**x),**|x;:[2>#(*h)-*|h;(1+|/h),,[:x],(,(*|*x)),,(*|*|x);[]]}
	s60::{[n];n::x-1;:[x=0;,[0 []]:|x=1;,[1[:x]];
			   {x@((~:'x),0)?0}:({x@<x}:(d8',/{d7(s60(*x);s60(*|x))}'
			   flr({d4(*|x)<2+d5(*x)};{x,,n-x}'!1+n:%2)))]}
	s61::{:[*3=^x;.f(x@1)+.f(x@2);#x]}
	s61a::{:[*3=^x;.f(x@1),.f(x@2);x]}
	s62::{:[*3=^x;(*x),.f(x@1),.f(x@2);[]]}
	s62b::{:[y=1;*x:|3>#x;[];.f(x@1;y-1),.f(x@2;y-1)]}
	d9::{y:=(,x,y@z),z}
	s62c::{{[n];:[(1+z)>#y;n::y,,[];n::y];
		:[*3=^x;.f(x@1;.f(x@2;d9(*x;n;z);z+1);z+1);d9(*x;n;z)]}
		:(x;[];0)}
	s63::{:[0=x;[];
		{(:x,:[y<2*x;[];,.f(x*2;y)]),:[y=2*x;,[]:|y<1+2*x;[];,.f(1+2*x;y)]}:(1;x)]}

Multiway Trees
--------------

Graphs
------

Miscellaneous Problems
----------------------
