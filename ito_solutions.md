[home](./index.md)
-------------------

*author: niplav, created: 2022-10-19, modified: 2022-10-25, language: english, status: in progress, importance: 2, confidence: likely*

> __Solutions to the textbook “Introduction to Optimization”.__

Solutions to “Introduction to Optimization”
=============================================

### 4.0.1

#### a)

<div>
	$$XA+A^{\top}=\mathbf{I} \Leftrightarrow \\
	XA=\mathbf{I}-A^{\top} \Leftrightarrow \\
	X=(\mathbf{I}-A^{\top})A^{-1}$$
</div>

#### b)

<div>
	$$ X^{\top}C=(2A(X+B))^{\top} \Leftrightarrow \\
	X^{\top}C=(2AX)^{\top}+(2AB)^{\top} \Leftrightarrow \\
	X^{\top}C-X^{\top}(2A)^{\top}=(2AB)^{\top} \Leftrightarrow \\
	X^{\top}(C-(2A)^{\top})=(2AB)^{\top} \\
	X^{\top}=(2AB)^{\top} (C^{-1}-((2A)^{\top})^{-1}) \Leftrightarrow \\
	X=((C^{-1})^{\top}-(2A)^{-1}) 2AB \Leftrightarrow \\
	X=(C^{-1})^{\top}2AB-B $$
</div>

#### c)

<div>
	$$(Ax-y)^{\top}A=\mathbf{0}_n^{\top} \Leftrightarrow \\
	A^{\top}(Ax-y)=\mathbf{0}_n^{\top} \Leftrightarrow \\
	A^{\top}Ax -A^{\top}y=\mathbf{0}_n^{\top} \Leftrightarrow \\
	x=(A^{\top}A)^{-1}(\mathbf{0}_n^{\top}+A^{\top}y)$$
</div>

#### d)

<div>
	$$(Ax-y)^{\top}A+x^{\top}B=\mathbf{0}_n^{\top} \Leftrightarrow \\
	A^{\top}(Ax-y)+x^{\top}B=\mathbf{0}_n^{\top} \Leftrightarrow \\
	A^{\top}Ax-A^{\top}y+x^{\top}B=\mathbf{0}_n^{\top} \Leftrightarrow \\
	A^{\top}Ax+x^{\top}B=\mathbf{0}_n^{\top}+A^{\top}y \Leftrightarrow \\
	A^{\top}Ax+B^{\top}x=\mathbf{0}_n^{\top}+A^{\top}y \Leftrightarrow \\
	(A^{\top}A+B^{\top})x=\mathbf{0}_n^{\top}+A^{\top}y \Leftrightarrow \\
	x=(A^{\top}A+B^{\top})^{-1}(\mathbf{0}_n^{\top}+A^{\top}y) $$
</div>

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
	\frac{(C^{\top}+C)x\cdot(a^2+x^{\top}Cx)-x^{\top}Cx\cdot (C^{\top}+C)x)}{(a^2+x^{\top}Cx)^2}$$
</div>

The implementation is straightforwardly

	def fholegrad(x, c=10, a=0.1):
	    retval_fsq=fsq(x, c=c)
	    retval_fsqgrad=fsqgrad(x, c=c, a=a)
	    return (retval_fsqgrad*(a**2+retval_fsq)-retval_fsq*retval_fsqgrad)/((a**2+retval_fsq))**2

#### ii)

The function can be pretty directly translated from the pseudocode in
the book to Python (no surprise here):

	def graddesc(f, fgrad, alpha=0.05, theta=0.000001, x0=[1,1], c=10, a=0.1):
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

Executing `graddesc` with `fsq`/`fsqgrad` and `fhole`/`fholegrad`
gives 60 iterations for finding a local minimum with `fsq`, and only
one iteration with `fhole`, indicating that I've probably made a mistake
writing `fholegrad`.
