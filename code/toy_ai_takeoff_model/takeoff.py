# https://en.wikipedia.org/wiki/Brownian_surface
# https://en.wikipedia.org/wiki/Fractal_landscape
# https://en.wikipedia.org/wiki/Fractional_Brownian_motion
# https://en.wikipedia.org/wiki/Gradient_descent
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
	center=np.array([size//2]*dim)
	center=offset+center

	corners=[('{0:0'+str(dim)+'b}').format(i) for i in range(2**dim)]
	corners=[list(i) for i in corners]
	corners=list(map((lambda x: list(map(int, x))), corners))
	corners=np.array(corners)
	corners=np.array([(i*(size-1))+offset for i in corners])

	cornersum=0
	for corner in corners:
		cornersum=cornersum+space[tuple(corner)]

	space[tuple(center)]=(cornersum/len(corners))+random.randint(minval, maxval)

	print(center)
	print(corners)
	print(space)
	print(space[tuple(center)])
	return

def generate_space(dim, size, maxval, minval):
	space=np.zeros(size)
	return space

def descent(space, pos):
	"""At position pos in space, do some kind of descent."""
	return pos

def search_around(space, pos):
	"""At position pos in space, dependent on current optimization
	power, search around in the neighbouring space to find the
	minimum in the subspace searched. This subspace can be an n-ball
	or an n-cube."""
	return pos

dim=1
size=17
minval=0
maxval=255
space=np.zeros([size]*dim)
fill_space(space, dim, size, minval, maxval)

exit()

pos=random.sample(range(0,size),dim)

while True:
	print(np.take(space, pos))
	pos=descent(space, pos)
	print(np.take(space, pos))
	pos=search_around(space, pos)
