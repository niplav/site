import math
import numpy as np
import itertools as it

def create_space(dim, size, minval=0, maxval=255):
	space=np.zeros([size]*dim, dtype=float)
	indices=np.array(list(np.ndindex(*[2]*dim)))*(size-1)
	space[tuple(indices.T)]=np.random.randint(minval, maxval, size=len(indices))
	return space

def get_cornerspos(dim):
	return np.array(list(it.product([0, 1], repeat=dim)))

def cartsum(a1, a2):
	return np.array(list(it.product(a1, a2))).sum(axis=1)

def corners_and_centers(dim, subdim, size, offsets):
	cornerspos=np.broadcast_to(np.zeros(dim, dtype=np.int64), [math.comb(dim, subdim), 2**(dim-subdim), 2**subdim, dim])
	cornerspos=np.array(cornerspos)
	centerspos=np.broadcast_to(np.zeros(dim, dtype=np.int64), [math.comb(dim, subdim), 2**(dim-subdim), dim])
	centerspos=np.array(cornerspos)

	occupied_counter=0
	for occupied in it.combinations(range(dim), subdim):
		unfixed_counter=0
		for unfixed in it.product([0, size-1], repeat=dim-subdim):
			cornerspos[occupied_counter, unfixed_counter, :][:, occupied]=get_cornerspos(subdim)*(size-1)
			free=tuple(set(range(dim))-set(occupied))
			cornerspos[occupied_counter, unfixed_counter, :][:, free]=unfixed
			unfixed_counter+=1
		occupied_counter+=1

	cornerspos=np.reshape(cornerspos, [math.comb(dim, subdim)*2**(dim-subdim),2**subdim, dim])
	corners=offsets[:, np.newaxis, np.newaxis]+cornerspos
	corners=np.reshape(corners, [offsets.shape[0]*cornerspos.shape[0], *cornerspos.shape[1:]])

	return corners

def diamond_rec(space, size, offsets, stitch_dim, minval, maxval, factor, subdim=None):
	dim=space.ndim

	if subdim==None:
		subdim=dim
	if subdim<=stitch_dim:
		return space

	#cornerspos=get_cornerspos(dim)
	#corners=offsets[:, np.newaxis]+cornerspos[np.newaxis, :]*(size-1)

	corners, centers=corners_and_centers(dim, subdim, size, offsets)

	space[tuple(centers.T)]=space[tuple(corners.T)].mean(axis=0)
	return diamond_rec(space, size, offsets, stitch_dim, minval, maxval, factor, subdim-1)

def square_rec(space, size, offsets, stitch_dim, minval, maxval, factor, curdim=None):
	return space

def stitch(space, offsets, stitch_dim, minval, maxval, factor):
	return space

# Needs to be recursive! When given space go big first then into smaller & smaller cells
def diamond_square_nd(space, size=None, offsets=None, stitch_dim=1, minval=0, maxval=255, factor=1.0):
	if size is None:
		size=space.shape[0]
	if offsets is None:
		offsets=np.zeros([1, space.ndim], dtype=int)

	if size<=2:
		return

	dim=len(space.shape)
	# Indexing: space[tuple(offsets.T)]

	if not (0<=stitch_dim<dim):
		raise ValueError(f"stitch_dim must be between 0 and {dim-1}")

	space=diamond_rec(space, size, offsets, stitch_dim, minval, maxval, factor)
	space=square_rec(space, size, offsets, stitch_dim, minval, maxval, factor)
	space=stitch(space, size, offsets, stitch_dim, minval, maxval, factor)

	nsize=size//2
	cornerspos=get_cornerspos(dim)
	# For some reasons, the code below produces one axis *too much* in the beginning!, when offsets has the shape (1, …)
	# child_offsets=offsets[:, np.newaxis]+cornerspos[np.newaxis, :]*nsize
	# This line works, but is ugly
	# child_offsets=(offsets[:, np.newaxis]+cornerspos[np.newaxis, :]*nsize).reshape([offsets.shape[0]*cornerspos.shape[0], dim])
	child_offsets=cartsum(offsets, get_cornerspos(dim)*nsize)

	return diamond_square_nd(space,
				size=nsize+1,
				offsets=child_offsets,
				minval=round(minval*factor),
				maxval=round(maxval*factor),
				factor=factor)
