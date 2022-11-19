[home](./index.md)
-------------------

*author: niplav, created: 2022-10-19, modified: 2022-10-24, language: english, status: in progress, importance: 2, confidence: likely*

> __Solutions to the textbook “Maths for Intelligent Systems”.__

Solutions to “Maths for Intelligent Systems”
=============================================

Chapter 2
----------

### Stray Non-Exercise 1

> Let me start with an example: We have three real-valued quantities `$x,
g$` and `$f$` which depend on each other. Specifically, $f(x,g)=3x+2g$
and `$g(x)=2x$`.  
> Question: What is the “derivative of `$f$` w.r.t. `$x$`”?

Intuitively, I'd say that `$\frac{\partial}{\partial x}f(x,g)=3$`. But then I notice that `$g$`
is allegedly a "real-valued quantity", what is that supposed to mean? Is
it not a function?

Alas, plugging in `$g$` into `$f$` gives `$f(x)=3x+2(2x)$` and
`$\frac{\partial}{\partial x}f(x)=3+4=7$`.

### 2.4

#### (i)

<div>
	$$XA+A^{\top}=\mathbf{I} \Leftrightarrow \\
	XA=\mathbf{I}-A^{\top} \Leftrightarrow \\
	X=(\mathbf{I}-A^{\top})A^{-1}$$
</div>

#### (ii)

<div>
	$$ X^{\top}C=(2A(X+B))^{\top} \Leftrightarrow \\
	X^{\top}C=(2AX)^{\top}+(2AB)^{\top} \Leftrightarrow \\
	X^{\top}C-X^{\top}(2A)^{\top}=(2AB)^{\top} \Leftrightarrow \\
	X^{\top}(C-(2A)^{\top})=(2AB)^{\top} \\
	X^{\top}=(2AB)^{\top} (C^{-1}-((2A)^{\top})^{-1}) \Leftrightarrow \\
	X=((C^{-1})^{\top}-(2A)^{-1}) 2AB \Leftrightarrow \\
	X=(C^{-1})^{\top}2AB-B $$
</div>

#### (iii)

<div>
	$$(Ax-y)^{\top}A=\mathbf{0}_n^{\top} \Leftrightarrow \\
	A^{\top}(Ax-y)=\mathbf{0}_n^{\top} \Leftrightarrow \\
	A^{\top}Ax -A^{\top}y=\mathbf{0}_n^{\top} \Leftrightarrow \\
	x=(A^{\top}A)^{-1}(\mathbf{0}_n^{\top}+A^{\top}y)$$
</div>

#### (iv)

<div>
	$$(Ax-y)^{\top}A+x^{\top}B=\mathbf{0}_n^{\top} \Leftrightarrow \\
	A^{\top}(Ax-y)+x^{\top}B=\mathbf{0}_n^{\top} \Leftrightarrow \\
	A^{\top}Ax-A^{\top}y+x^{\top}B=\mathbf{0}_n^{\top} \Leftrightarrow \\
	A^{\top}Ax+x^{\top}B=\mathbf{0}_n^{\top}+A^{\top}y \Leftrightarrow \\
	A^{\top}Ax+B^{\top}x=\mathbf{0}_n^{\top}+A^{\top}y \Leftrightarrow \\
	(A^{\top}A+B^{\top})x=\mathbf{0}_n^{\top}+A^{\top}y \Leftrightarrow \\
	x=(A^{\top}A+B^{\top})^{-1}(\mathbf{0}_n^{\top}+A^{\top}y) $$
</div>

#### (v)

<!--TODO-->

#### (vi)

<!--TODO-->

### 2.6.1

I… I don't know what the skew is :-/

### 2.6.2

<!--TODO: do this later when I understand tensors, or am maybe just a
bit more comfortable in general-->

### 2.6.3

Writing code: This I can do.

#### i)

	using Random, LinearAlgebra

	function gradient_check(x, f, df):
		n=length(x)
		d=length(f(x))
		ε=10^-6
		J=zero(Matrix{Float64}(undef, d, n))
		for i in 1:n
			unit=zero(rand(n))
			unit[i]=1
			J[:,i]=(f(x+ε*unit)-f(x-ε*unit))/(2*ε)
		end
		if norm(J-df(x), Inf)<10^-4
			return true
		else
			return false
		end
	end

#### ii)

	julia> A=rand(Float64, (10, 15))
	julia> f(x)=A*x
	julia> df(x)=A
	julia> x=randn(15)
	15-element Vector{Float64}:
	  1.536516645971545
	  1.0136394994998532
	 -0.09863977762813898
	  1.3510191388362935
	  0.84503226122143
	  0.09296670831415606
	 -1.5390337565597376
	  1.4679194319980104
	 -0.7085023577127753
	 -0.10676335224166593
	 -0.8686753109089055
	  1.2912744597257453
	  0.7364123079861109
	  0.5736005534388826
	  0.5332386427039576
	julia> gradient_check(x, f, df)
	true

And now the cooler `$f$`:

	julia> f(x)=transpose(x)*x
	f (generic function with 1 method)
	julia> df(x)=2*transpose(x)
	df (generic function with 1 method)
