#!/usr/bin/env python3

import random
import numpy as np

extrfact=0.5

dim=3
size=9
minval=0
maxval=256
lognormm=2
lognormvar=5

rounds=4096
growth=1.001

factor=1

def fill_space(size, minval, maxval):
	"""Fill a dim-dimensional discrete space of ℕ^{size} with
	some random hyperplane with values ranging from minval to
	maxval. Returns a ℕ^{size} array. Changes space in-place."""

	offsets=[np.array([0]*dim)]
	n_diam_square_rec(offsets, size, minval, maxval)
	return space

def get_cornerspos():
	cornerspos=[('{0:0'+str(dim)+'b}').format(i) for i in range(2**dim)]
	cornerspos=[list(i) for i in cornerspos]
	cornerspos=list(map((lambda x: list(map(int, x))), cornerspos))
	cornerspos=np.array(cornerspos)

	return cornerspos

def n_diam_square_rec (offsets, size, lminval, lmaxval):
	if size==1:
		return

	nsize=size//2

	for o in offsets:
		center=np.array([nsize]*dim)
		center=o+center

		if size==len(space):
			b=1
		else:
			b=0

		cornerspos=get_cornerspos()
		corners=np.array([(i*(size-b))+o for i in cornerspos])

		cornersum=0
		for corner in corners:
			cornersum=cornersum+space[tuple(corner)]

		val=(cornersum/len(corners))+(random.randint(lminval, lmaxval)-((lmaxval-lminval)//2))

		space[tuple(center)]=val

	for o in offsets:
		center=np.array([nsize]*dim)
		center=o+center
		# Recursive square step here (dim times)
		explored=np.array([False]*dim)

		for i in range(0, dim):
			explored[i]=True
			ncenter1=np.array(center)
			ncenter2=np.array(center)
			ncenter1[i]=ncenter1[i]+nsize
			ncenter2[i]=ncenter2[i]-nsize
			square_rec(dim, ncenter1, nsize, explored, round(lminval*extrfact), round(lmaxval*extrfact))
			square_rec(dim, ncenter2, nsize, explored, round(lminval*extrfact), round(lmaxval*extrfact))
			explored[i]=False

	noffsets=[]

	# Recursive square step
	for pos in get_cornerspos():
		noffsets=noffsets+[(pos*nsize)+offset for offset in offsets]

	n_diam_square_rec(noffsets, nsize, round(lminval*extrfact), round(lmaxval*extrfact))

def square_rec(ldim, center, size, explored, lminval, lmaxval):
	if all(explored) or space[tuple(center)]!=0:
		return

	# Actually assign square-based values
	counter=0
	squaresum=0
	squarepos=np.array(center)

	for i in range(0, ldim):
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

	val=(squaresum/counter)+(random.randint(lminval, lmaxval)-((lmaxval-lminval)//2))

	space[tuple(center)]=val

	# Recurse
	for i in range(0, ldim):
		if not explored[i]:
			explored[i]=True
			ncenter1=np.array(center)
			ncenter2=np.array(center)
			ncv1=ncenter1[i]+size
			ncv2=ncenter2[i]-size
			if ncv1>=0:
				ncenter1[i]=ncv1
				square_rec(ldim-1, ncenter1, size, explored, round(lminval*extrfact), round(lmaxval*extrfact))
			if ncv2>=0:
				ncenter2[i]=ncv2
				square_rec(ldim-1, ncenter2, size, explored, round(lminval*extrfact), round(lmaxval*extrfact))
			explored[i]=False

def climb(space, pos, size, dim):
	"""At position pos in space, do some kind of climbing."""

	return climb_dim(space, pos, size, dim)

def climb_dim(space, pos, size, dim):
	"""Look in direction of each dimension (not two dimensions at
	once), then choose maximum spot."""

	maxpos=np.array(pos)
	for i in range(0, dim):
		pos[i]+=1
		if 0<=pos[i]<size:
			if space[tuple(pos)]>space[tuple(maxpos)]:
				maxpos=np.array(pos)
		pos[i]-=2
		if 0<=pos[i]<size:
                        if space[tuple(pos)]>space[tuple(maxpos)]:
                                maxpos=np.array(pos)
		pos[i]+=1
	return maxpos

def climb_hypcub(space, pos):
	"""Look one unit-hypercube around, choose maximum."""
	return pos

def search_around(space, pos, size, dim, intelligence):
	"""At position pos in space, dependent on current optimization
	power, search around in the neighbouring space to find the
	minimum in the subspace searched. This subspace can be an n-ball
	or an n-cube."""

	step=round(intelligence**(1/dim))
	subpos=[slice(0,0)]*dim
	for i in range(0, dim):
		subpos[i]=slice(max(0,pos[i]-step), min(size-1, pos[i]+step))
	subspace=space[tuple(subpos)]
	mp=np.where(subspace == np.amax(subspace))
	pos=np.array([list(mp[i])[0]+subpos[i].start for i in range(0, dim)])
	return pos

space=np.zeros([size]*dim)

# Initialize corner values

cornerspos=get_cornerspos()
corners=np.array([(i*(size-1)) for i in get_cornerspos()])

for c in corners:
	val=random.randint(minval, maxval)
	space[tuple(c)]=random.randint(minval, maxval)

fill_space(size, minval, maxval)

pos=[random.randint(0, size-1) for i in range(0, dim)]

for i in range(0,rounds):
	factor*=growth
	intelligence=max(1, space[tuple(pos)])*factor
	print(space[tuple(pos)])
	print(intelligence)
	print("------------")

	pos=climb(space, pos, size, dim)
	pos=search_around(space, pos, size, dim, intelligence)
