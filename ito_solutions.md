[home](./index.md)
-------------------

*author: niplav, created: 2022-10-19, modified: 2022-11-08, language: english, status: in progress, importance: 2, confidence: likely*

> __Solutions to the textbook “Introduction to Optimization”.__

Solutions to “Introduction to Optimization”
=============================================

### 4.0.1

See [here](./mfis_solutions.html#24).

### 4.11

#### i)

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

#### ii)

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

#### iii)

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
