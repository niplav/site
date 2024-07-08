import random
import itertools
import numpy as np

def create_space(dim, size, minval, maxval, factor):
	"""Creates a size^{dim} space and initializes it with the
	n-dimensional diamond square algorithm."""

	space=np.zeros([size]*dim)
	corners=(size-1)*get_cornerspos(dim)
	space[*(corners.T)]=np.random.randint(minval, maxval, size=len(corners))

	offsets=[np.array([0]*dim)]

	"""Fill a dim-dimensional discrete space of ℕ^{size} with
	some random landscape with values ranging from minval to
	maxval. Returns a ℕ^{size} array."""
	return ndim_diamond_square_rec(space, dim, size, offsets, minval, maxval, factor)

def ndim_diamond_square_rec (space, dim, size, offsets, minval, maxval, factor):
	if size==1:
		return

	nsize=size//2

	for o in offsets:
		center=o+np.array([nsize]*dim)
		b=int(size==len(space))

		corners=get_cornerspos(dim)*(size-b)+o
		cornersum=0

		cornersum=np.sum(space[*(corners.T)])
		val=(cornersum/len(corners))+(random.randint(minval, maxval)-((maxval-minval)//2))

		space[tuple(center)]=val

	for o in offsets:
		center=o+np.array([nsize]*dim)
		# Recursive square step here (dim times)
		explored=np.array([False]*dim)

		for i in range(0, dim):
			explored[i]=True
			ncenter1=np.array(center)
			ncenter2=np.array(center)
			ncenter1[i]=ncenter1[i]+nsize
			ncenter2[i]=ncenter2[i]-nsize
			square_rec(space, dim, nsize, ncenter1, explored, round(minval*factor), round(maxval*factor), factor)
			square_rec(space, dim, nsize, ncenter2, explored, round(minval*factor), round(maxval*factor), factor)
			explored[i]=False

	noffsets=[]

	for pos in get_cornerspos(dim):
		noffsets=noffsets+[(pos*nsize)+offset for offset in offsets]

	ndim_diamond_square_rec(space, dim, nsize, noffsets, round(minval*factor), round(maxval*factor), factor)

	return space

def square_rec(space, dim, size, center, explored, minval, maxval, factor):
	if all(explored) or space[tuple(center)]!=0:
		return

	# Actually assign square-based values
	counter=0
	squaresum=0
	squarepos=np.array(center)

	for i in range(0, dim):
		tmp=squarepos[i]
		ndp1=squarepos[i]+size
		ndp2=squarepos[i]-size
		if 0<=ndp1<len(space):
			squarepos[i]=ndp1
			squaresum+=space[tuple(squarepos)]
			counter+=1
		if 0<=ndp2<len(space):
			squarepos[i]=ndp2
			squaresum+=space[tuple(squarepos)]
			counter+=1
		squarepos[i]=tmp

	val=(squaresum/counter)+(random.randint(minval, maxval)-((maxval-minval)//2))

	space[tuple(center)]=val

	# Recurse
	for i in range(0, dim):
		if not explored[i]:
			explored[i]=True
			ncenter1=np.array(center)
			ncenter2=np.array(center)
			ncv1=ncenter1[i]+size
			ncv2=ncenter2[i]-size
			if ncv1>=0:
				ncenter1[i]=ncv1
				square_rec(space, dim-1, size, ncenter1, explored, round(minval*factor), round(maxval*factor), factor)
			if ncv2>=0:
				ncenter2[i]=ncv2
				square_rec(space, dim-1, size, ncenter2, explored, round(minval*factor), round(maxval*factor), factor)
			explored[i]=False

def get_cornerspos(dim):
	return np.array(list(itertools.product([0, 1], repeat=dim)))
