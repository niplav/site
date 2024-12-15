[home](./index.md)
------------------

*author: niplav, created: 2020-11-20, modified: 2024-12-15, language: english, status: in progress, importance: 4, confidence: highly likely*

> __The [Diamond-Square
algorithm](https://en.wikipedia.org/wiki/Diamond-square_algorithm)
is a terrain-generation algorithm for two dimensions (producing a
three-dimensional terrain). I generalize the algorithm to any positive
number of dimensions, and analyze the resulting algorithm.__

Generalizing the Diamond-Square Algorithm to n Dimensions
=========================================================

> Libre de la metáfora y del mito  
labra un arduo cristal: el infinito  
mapa de Aquel que es todas Sus estrellas.

*— [Jorge Luis Borges](https://en.wikipedia.org/wiki/Jorge_Luis_Borges), [“Spinoza”](https://thefunambulist.net/literature/litterature-spinoza-by-borges), 1964*

I learned of the diamond-square algorithm by reading through the archives
of [Chris Wellon's blog](https://nullprogram.com/), specifically his post
on [noise fractals](https://nullprogram.com/blog/2007/11/20) and terrain
generation. The algorithm is a fairly simple and old one (dating back
to the 80s), but not being interested in graphics or game programming,
I shelved it as a curiosity.

However, a while later I needed a way to generate high-dimensional
landscapes for [a simulation](./toy_ai_takeoff_model.html), and
remembered the algorithm, I felt like I could contribute something here
by generalizing the algorithm to produce landscapes in an arbitrary number
of dimensions, and that this would be a fun challenge to sharpen my (then
fairly weak) Python and [numpy](https://en.wikipedia.org/wiki/NumPy)
skills.

Description
------------

The original (2-dimensional) diamond-square algorithm, in its simplest
form, starts with a `$2^n+1 \times 2^n+1$` grid of numbers.

It is easiest explained visually:

![](./img/diamond/diamond_square.png)

1. Either a user or the algorithm itself assigns the four corners some values, which can be random.
2. In the __diamond step__ after that, the value in the middle of the grid is determined as the average of the four values in the corners, plus a random value.
3. Next, the middle value every "face" of the grid is determined by the average of the three values in orthogonal directions plus a random value—the __square step__.
4. The grid is broken down into four sub-grids, and each sub-grid undergoes the __diamond step__ and the __square step__. The only difference is in the square step: If a point on the grid lies at the face of two sub-grids, it receives the average of all four orthogonal points.
5. The algorithm terminates if each sub-grid is of size `$1 \times 1$`.

For `$n$` dimensions, do that, just higher-dimensional.

----------

We start by initializing an n-dimensional space with zeros, and the
corners with random values:

	def create_space(dim, size, minval, maxval, factor):
		space=np.zeros([size]*dim)
		corners=(size-1)*get_cornerspos(dim)
		space[*(corners.T)]=np.random.randint(minval, maxval, size=len(corners))

Here, `get_cornerspos` is just the one-liner
`return np.array(list(itertools.product([0, 1], repeat=dim)))`.

We then intialize the variable `offsets`, and call the recursive
diamond-square algorithm:

		offsets=[np.array([0]*dim)]
		return ndim_diamond_square_rec(space, dim, size, offsets, minval, maxval, factor)

Now there are two possible variants of the generalized diamond-square
algorithm: the Long Diamond variation and the Long Square variation.

The Long Diamond ⇔ Long Cube Spectrum
--------------------------------------

Let's take a cube and think about how we can run the diamond-square
algorithm on it.

__One way__ of doing so would be to calculate the center of the cube as
the mean of all the corners, and then the center of each face as the mean
of its corners. The value for the midpoint of each edge is calculated
from the midpoints of the edges and the centers adjacent faces.

<video src="./vid/diamond/long_diamond_white.mp4" type="video/mp4" controls>
</video>

I call this variant the __Long Diamond__ variant. It performs *two*
diamond steps and only one square step along the three dimensions.

But there's __another way__: Calculate the center of the cube as the
mean of its corners, just as before. But now go directly to the edges
and calculate their midpoints as the mean of the endpoints of each edge.
Then, calculate the value of each face as the mean of the value in the
center of the cube *and* the centers of the adjacent edges.

<video src="./vid/diamond/long_square_white.mp4" type="video/mp4" controls>
</video>

That is the __Long Square__ variant: It performs one diamond step
(computing the value for the center) and two square steps (for edges
and for faces).

Consecutive diamond steps go from *higher* dimensions to *lower*
ones, consecutive square steps go from *lower* dimensions to *higher*
ones. There is one dimension where the values are "stitched together"—in
the long diamond case it's the first dimension (on edges), in the long
square step it's the second dimension (on faces). I guess one could
also leave out the diamond steps together and calculate the center of
the cube as the mean of the faces—zero diamond, very long square.

### Long Diamond

The diamond step of the algorithm starts out with the base case: If the
space is only one element big, we return and do nothing (assuming the
value has been filled in):

	def ndim_diamond_square_rec(space, dim, size, offsets, minval, maxval, factor):
		if size<=1:
			return

We also have to update the size of any axis in the space (*not* the size
of the space itself), we are halving this every recursive call.

		nsize=size//2

Now we come to `offsets`. Remember above when after the first square
step, we moved into a diamond step on the smaller squares? `offsets`
describes where the "left lower corner" of those smaller squares is. We
initialized it with zeros, that way we start in a definite corner.

#### Diamond

#### Square

Code [here](code/diamond/ndim_diamond_square.py). I think this is probably
the 2nd-most beautiful code I've ever written, just after [this absolute
smokeshow](./99_problems_klong_solution.html#P25__Generate_a_random_permutation_of_the_elements_of_a_list).

Analysis
--------

Results
-------

### One Dimension

![Space generated by the algorithm in one dimension](./img/diamond/onedim.png "Space generated by the algorithm in one dimension")

### Two Dimensions

![Space generated by the algorithm in two dimensions](./img/diamond/twodim.png "Space generated by the algorithm in two dimensions")

### Three Dimensions

<!--TODO: slice plot perhaps-->

![Space generated by the algorithm in three dimensions](./img/diamond/threedim.png "Space generated by the algorithm in three dimensions")
