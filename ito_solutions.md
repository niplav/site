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
