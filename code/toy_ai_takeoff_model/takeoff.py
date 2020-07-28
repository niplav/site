# https://en.wikipedia.org/wiki/Brownian_surface
# https://en.wikipedia.org/wiki/Fractal_landscape
# https://en.wikipedia.org/wiki/Fractional_Brownian_motion
# https://en.wikipedia.org/wiki/Gradient_descent
# https://en.wikipedia.org/wiki/Hill_climbing
# https://en.wikipedia.org/wiki/Newton%27s_method
# https://en.wikipedia.org/wiki/OpenSimplex_noise
# https://en.wikipedia.org/wiki/Perlin_noise
# https://en.wikipedia.org/wiki/Simplex_noise
# https://github.com/buckinha/DiamondSquare
# https://nullprogram.com/blog/2007/11/20/

import random
import numpy as np

def fill_space(space, dim, size, minval, maxval):
	"""Fill a dim-dimensional discrete space of ℕ^{size} with
	some random hyperplane with values ranging from minval to
	maxval. Returns a ℕ^{size} array. Changes space in-place."""
	offset=np.array([0]*dim)
	n_diam_square_rec(space, dim, offset, size, minval, maxval)
	return space

def n_diam_square_rec (space, dim, offset, size, minval, maxval):
	if size==1:
		return

	center=np.array([size//2]*dim)
	center=offset+center

	cornerspos=[('{0:0'+str(dim)+'b}').format(i) for i in range(2**dim)]
	cornerspos=[list(i) for i in cornerspos]
	cornerspos=list(map((lambda x: list(map(int, x))), cornerspos))
	cornerspos=np.array(cornerspos)
	corners=np.array([(i*(size-1))+offset for i in cornerspos])

	cornersum=0
	for corner in corners:
		cornersum=cornersum+space[tuple(corner)]

	space[tuple(center)]=(cornersum/len(corners))+random.randint(minval, maxval)

	nsize=size//2

	# Recursive diamond step here (dim-1 times)
	explored=np.array([False]*dim)

	for i in range(0,dim):
		explored[i]=True
		ncenter1=np.array(center)
		ncenter2=np.array(center)
		ncenter1[i]=ncenter1[i]+nsize
		ncenter2[i]=ncenter2[i]-nsize
		diamond_rec(space, ncenter1, dim-1, nsize, explored, minval, maxval)
		diamond_rec(space, ncenter2, dim-1, nsize, explored, minval, maxval)
		explored[i]=False

	# Recursive square step
	for pos in cornerspos:
		noffset=(pos*nsize)+offset
		n_diam_square_rec(space, dim, noffset, nsize, minval, round(maxval*extrfact))

def diamond_rec(space, center, dim, size, explored, minval, maxval):
	# Field already assigned or dimension is 0
	# Only a heuristic, use {True, False}^dim instead?
	if dim==0 or space[tuple(center)]!=0:
		return

	# TODO: using len(explored) to mean the dimension is questionable

	# Actually assign diamond-based values

	counter=0
	diamondsum=0
	diamondpos=np.array(center)

	for i in range(0, len(explored)):
		tmp=diamondpos[i]
		ndp1=diamondpos[i]+size
		ndp2=diamondpos[i]-size
		if 0<=ndp1<len(space):
			diamondpos[i]=ndp1
			diamondsum+=space[tuple(diamondpos)]
			counter+=1
		if 0<=ndp2<len(space):
			diamondpos[i]=ndp2
			diamondsum+=space[tuple(diamondpos)]
			counter+=1
		diamondpos[i]=tmp

	space[tuple(center)]=(diamondsum/counter)+random.randint(minval, maxval)

	# Recurse
	for i in range(0, len(explored)):
		if not explored[i]:
			explored[i]=True

			# Possibly beware by-reference passing here!

			ncenter1=np.array(center)
			ncenter2=np.array(center)
			ncv1=ncenter1[i]+size
			ncv2=ncenter2[i]-size
			if ncv1>=0:
				ncenter1[i]=ncv1
				diamond_rec(space, ncenter1, dim-1, size, explored, minval, round(maxval*extrfact))
			if ncv2>=0:
				ncenter2[i]=ncv2
				diamond_rec(space, ncenter2, dim-1, size, explored, minval, round(maxval*extrfact))
			explored[i]=False

def descent(space, pos):
	"""At position pos in space, do some kind of descent."""
	return pos

def search_around(space, pos):
	"""At position pos in space, dependent on current optimization
	power, search around in the neighbouring space to find the
	minimum in the subspace searched. This subspace can be an n-ball
	or an n-cube."""
	return pos

extrfact=0.75
dim=2
size=33
minval=0
maxval=255
space=np.zeros([size]*dim)
fill_space(space, dim, size, minval, maxval)

pos=[random.randint(0, size-1) for i in range(0, dim)]

#while True:
#	pos=descent(space, pos)
#	pos=search_around(space, pos)
