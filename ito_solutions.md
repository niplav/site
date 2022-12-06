[home](./index.md)
-------------------

*author: niplav, created: 2022-10-19, modified: 2022-11-25, language: english, status: in progress, importance: 2, confidence: likely*

> __Solutions to the textbook “Introduction to Optimization”.__

Solutions to “Introduction to Optimization”
=============================================

### 4.0.1

See [here](./mfis_solutions.html#24).

### 4.11

#### (i)

Some standard numpy code:

	import numpy as np

	def givec(x, c=10):
		n=len(x)
		iexp=np.array(range(0,n))
		cdiag=c**(iexp/((n-1)*np.ones(n)))
		C=np.diag(cdiag)
		return C

	def fsq(x, c=10):
		C=givec(x, c=c)
		return x.T@C@x

	def fhole(x, c=10, a=0.1):
	    retval=fsq(x, c=c)
	    return retval/(a**2+retval)

The derivative of `$f_{\text{sq}}=x^{\top}Cx$` is `$(C+C^{\top})x$`
(as per identity 81 from the Matrix Cookbook (Petersen & Pedersen
2012))<!--TODO: link-->.

Which is excellent, since the identity 2.3 of Maths for Intelligent
Systems (Toussaint 2022) gives
`$\frac{\partial}{\partial x} x^{\top}Cx=x^{\top}C \frac{\partial}{\partial x}x+x^{\top} C^{\top} \frac{\partial}{\partial x} x$`
which would be `$x^{\top}C+x^{\top}C^{\top}=C^{\top}x+Cx=(C^{\top}+C)x$`
and therefore the same as above (and in identity 97 from the Matrix
Cookbook).

So then

	def fsqgrad(x, c=10):
		C=givec(x, c=c)
		return (C.T+C)@x

Since `$f_{\text{sq}}$` and `$f_{\text{hole}}$` return a scalar, one can
use a simple [quotient rule](https://en.wikipedia.org/wiki/Quotient_rule):

<div>
        $$f_{\text{hole}}(x)=\\
        \frac{(C^{\top}+C)x\cdot(a^2+x^{\top}Cx)-x^{\top}Cx\cdot (C^{\top}+C)x)}{(a^2+x^{\top}Cx)^2}= \\
         \frac{(C^{\top}+C)x\cdot(a^2+x^{\top}Cx-x^{\top}Cx)}{(a^2+x^{\top}Cx)^2}= \\
         \frac{a^2 \cdot (C^{\top}+C)x}{(a^2+x^{\top}Cx)^2}$$
</div>

The implementation is straightforwardly

	def fholegrad(x, c=10, a=0.1):
	    retval_fsq=fsq(x, c=c)
	    retval_fsqgrad=fsqgrad(x, c=c, a=a)
	    return (retval_fsqgrad*(a**2+retval_fsq)-retval_fsq*retval_fsqgrad)/((a**2+retval_fsq))**2

#### (ii)

The function can be pretty directly translated from the pseudocode in
the book to Python (no surprise here):

	def graddesc(f, fgrad, alpha=0.001, theta=10e-20, x0=[1,1], c=10, a=0.1):
		x=np.array(x0)
		i=0
		prevcost=-math.inf
		curcost=f(x)
		while abs(prevcost-curcost)>theta:
			print("#iteration: ", i)
			print("current cost: ", curcost)
			prevcost=curcost
			x=x-alpha*fgrad(x)
			curcost=f(x)
			i=i+1
		print("solution: ", x)
		print("iterations: ", i)
		print("cost: ", f(x))
		return x

Executing `graddesc` with `fsq`/`fsqgrad` and `fhole`/`fholegrad` gives
~1000 iterations for finding a local minimum with `fsq`, and takes ~185k
iterations for `fhole`. But it finds the minimum:

	print("fsq:")
	graddesc(fsq, fsqgrad)
	print("fhole:")
	graddesc(fhole, fholegrad)

	fsq:
	solution:  [4.98354923e-09 1.65118900e-84]
	iterations:  9549
	cost:  2.4835762963261225e-17
	fhole:
	solution:  [ 4.13240000e-11 -7.98149419e-19]
	iterations:  184068
	cost:  1.7076729729684466e-19

#### (iii)

	def backtrack_graddesc(f, fgrad, alpha=0.05, theta=10e-15, x0=[1,1], c=10, a=0.1, rho_ls=0.01, rho_plus=1.2, rho_minus=0.5, delta_max=math.inf):
		x=np.array(x0)
		i=0
		prevcost=-math.inf
		curcost=f(x)
		delta=-fgrad(x)/np.linalg.norm(fgrad(x))
		while np.linalg.norm(alpha*delta)>=theta:
			while f(x+alpha*delta)>f(x)+rho_ls*fgrad(x)@(alpha*delta).T:
				alpha=rho_minus*alpha
			prevcost=curcost
			x=x+alpha*delta
			alpha=min(rho_plus*alpha, delta_max)
			curcost=f(x)
			i=i+1
		return x

#### iv)

First we compute the derivative of `$\underset{β}{\text{argmin}}||y-Xβ||^2+λ||β||^2$`:

<div>
	$$\frac{\partial ||y-Xβ||^2+λ||β||^2}{\partial β}= \\
	\frac{\partial ||y-Xβ||^2}{\partial β} + \frac{\partial λ||β||^2}{\partial β}= \\
	\frac{\partial ||-Xβ-(-y)||^2}{\partial β}+λ2β=\\
	2 \cdot \frac{-Xβ-(-y)}{||-Xβ-(-y)||}+λ2β$$
</div>

### 4.3.1

<div>
</div>

### 4.3.3

<div>
	$$f(x)=\frac{1}{2}x^{\top} A x+b^{\top}+c=\\
	\frac{1}{2} x^{\top} A x=\\
	\frac{1}{2} x^{\top} \left [\matrix{2 & 0 \cr 0 & 1}\right ] x$$
</div>

(since `$b=\mathbf{0}$` and `$c=0$`). So the negative gradient is

<div>
	$$-\nabla f(x)= \\
	\frac{1}{2} x^{\top} (A+A^{\top})=\\
	\frac{1}{2} x^{\top} \left [\matrix{4 & 0 \cr 0 & 2}\right ]$$
</div>

#### (i)

`$x_0=\left [ \matrix{1 \cr 1} \right ]$`, so

<div>
	$$δ_0=\\
	-\nabla f(x_0)=\\
	-\frac{1}{2} \left [ \matrix{1 & 1} \right ] \left [\matrix{4 & 0 \cr 0 & 2}\right ]=\\
	-\left [ \matrix{2 & 1} \right ]$$
</div>

Then

<div>
	$$f(x+αδ)=\\
	\frac{1}{2} (\left [ \matrix{1 \cr 1} \right]-α\left [ \matrix{2 \cr 1} \right ])^{\top}\left [\matrix{2 & 0 \cr 0 & 1}\right ](\left [ \matrix{1 \cr 1} \right]-α\left [ \matrix{2 \cr 1} \right ])=\\
	\frac{1}{2} (\left [ \matrix{1 \cr 1} \right]-α\left [ \matrix{2 \cr 1} \right ])^{\top}(\left [ \matrix{2 \cr 1} \right]-α\left [ \matrix{4 \cr 1} \right ])=\\
	\frac{1}{2} (\left [ \matrix{1 & 1} \right]-α\left [ \matrix{2 & 1} \right ])(\left [ \matrix{2 \cr 1} \right]-α\left [ \matrix{4 \cr 1} \right ])=\\
	\frac{1}{2}(3-10\cdot α+9 \cdot α^2)=\\
	1.5-5\cdot α+9 \cdot α^2$$
</div>

The derivative of that is `$5+18 \cdot α$`. Setting it to zero gives
`$α=\frac{5}{18}$`.

The next `$x$` then is (going by the values we computed)
`$\left [ \matrix{0.\overline{4} \cr 0.7\overline{2}} \right ]$`.

The new gradient then is

<div>
	$$g=\\
	-\nabla f(x)=\\
	-\frac{1}{2} \left [ \matrix{0.\overline{4} & 0.7\overline{2}} \right ] \left [\matrix{2 & 0 \cr 0 & 1}\right ]=\\
	\left [ \matrix{-0.\overline{4} & -0.36\overline{1}} \right ]$$
</div>

Now computing `$β$`:

<div>
	$$\frac{g^{\top}(g-g')}{g'^{\top}g'}=\\
	\frac{\left [ \matrix{-0.\overline{4} & -0.36\overline{1}} \right ]^{\top}(\left [ \matrix{-0.\overline{4} & -0.36\overline{1}} \right ]-\left [ \matrix{-2 & -1} \right ])}{\left [ \matrix{-2 & -1} \right ]^{\top}\left [ \matrix{-2 & -1} \right ]}\approx \\
	-0.1844$$
</div>

which is smaller than zero, so our new `$β$` is `$0$`.

Then `$δ$` is `$\left [ \matrix{-0.\overline{4} & -0.36\overline{1}} \right ]$`.

We now go through the whole exercise a second time:

<div>
	$$f(x+αδ)=\\
	\frac{1}{2} (\left [ \matrix{0.\overline{4} \cr 0.7\overline{2}} \right ]-α\left [ \matrix{-1.8765 & -1.4938} \right ])^{\top}\left [\matrix{2 & 0 \cr 0 & 1}\right ](\left [ \matrix{0.\overline{4} \cr 0.7\overline{2}} \right ]-α\left [ \matrix{-1.8765 & -1.4938} \right ])=\\
	(\frac{1}{2} (\left [ \matrix{0.\overline{4} \cr 0.7\overline{2}} \right ]-α\left [ \matrix{-1.8765 & -1.4938} \right ])^{\top}\left [ \matrix{0.\overline{8} \cr 0.7\overline{2}} \right]-α\left [ \matrix{-0.\overline{8} \cr -0.36\overline{1}} \right ]) \approx \\
	0.458\overline{3}-0.6559\cdot α+0.2627 \cdot α^2$$
</div>

Then the derivative is approximately `$-0.6559+0.5255 \cdot α$`, and
the new `$α$` is the solution to that, namely `$\approx 1.248$`.

Then the new `$x$` is `$\approx \left [ \matrix{-0.1103 & 0.2715} \right ]$`.
The new `$g$` is `$\approx \left [ \matrix{0.11029 & -0.1358} \right ]$`, and
`$β\approx 0.0933$`, which is this time greater than zero so we can keep it.

The new `$δ$` therefore is `$\approx \left [ \matrix{0.0688 & -0.1694} \right ]$`.

…And we're done with the second round. I'm not going to do this for
`$x_0=(-1,2)$`, in case you were wondering, I hope I've shown that I *can*
do this, and it's tedious to type out.

<!--TODO: maybe do other ones too?-->

#### (ii)

Intuitively, this makes sense: We walked all the way to the minimum in
the direction of the current gradient, so the next direction should not
go "back" in the direction where we came from, or further than we needed
to go.

<!--TODO: actually prove this-->

### 4.4.1

Not gonna show you the sketch, of course. (I also don't have time right
now to learn [manim](https://manim.community) for that, though it would
be cool).

#### (i)

The solution is `$\frac{-π}{2}$`.

#### (ii)

The solution is
`$\left [ \matrix{-\frac{\sqrt{2}}{2} \cr -\frac{\sqrt{2}}{2}} \right ]$`.

#### (iii)

Since the gradient is "pulling" to the bottom left, the best one can do
is to set `$x_1$` to zero. So
`$x=\left [ \matrix{-\frac{\sqrt{2}}{2} \cr -\frac{\sqrt{2}}{2}} \right ]$`.

#### (iv)

The second constraint can be pictured the following way: On the `$x_2$`
axis there is a parabola forming a paraboloid cylinder which is zero where
`$x_2$` is zero, and grows symmetrically in both other directions. At
`$x_2≥1$` and `$x_2≤-1$` this cylinder is greater than `$x_1$`,
which we want to avoid. So we know that `$x_2=-1$`.

But what is `$x_1$`? It should be as small as possible. Plugging in
`$x_1=0$` tells us that this is the best we can do.
