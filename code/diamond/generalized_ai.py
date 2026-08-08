import math
import numpy as np
import itertools as it

def create_space(dim, size, minval=0, maxval=255):
	space=np.zeros([size]*dim, dtype=float)
	corners=np.array(list(np.ndindex(*[2]*dim)))*(size-1)
	space[tuple(corners.T)]=np.random.uniform(minval, maxval, size=len(corners))
	return space

def get_cornerspos(dim):
	return np.array(list(it.product([0, 1], repeat=dim)), dtype=int)

# The subdim axes of a cell get spanned/centered, the rest are pinned to a face.
# Returns corners [n, 2**subdim, dim] and centers [n, dim], ordered
# (combination, face, offset).
def corners_and_centers(dim, subdim, size, offsets):
	half=size//2
	ncomb, nface, ncorn=math.comb(dim, subdim), 2**(dim-subdim), 2**subdim

	occupied=np.array(list(it.combinations(range(dim), subdim)), dtype=int)
	occmask=np.zeros([ncomb, dim], dtype=bool)
	occmask[np.arange(ncomb)[:, np.newaxis], occupied]=True
	free=np.nonzero(~occmask)[1].reshape(ncomb, dim-subdim)

	faces=np.array(list(it.product([0, size-1], repeat=dim-subdim)), dtype=int)
	local=get_cornerspos(subdim)*(size-1)

	# scatter the spanned and the pinned axes into their slots
	cornerspos=np.zeros([ncomb, nface, ncorn, dim], dtype=int)
	np.put_along_axis(cornerspos, np.broadcast_to(occupied[:, np.newaxis, np.newaxis, :], [ncomb, nface, ncorn, subdim]), local, axis=-1)
	np.put_along_axis(cornerspos, np.broadcast_to(free[:, np.newaxis, np.newaxis, :], [ncomb, nface, ncorn, dim-subdim]), faces[np.newaxis, :, np.newaxis, :], axis=-1)

	centerspos=np.zeros([ncomb, nface, dim], dtype=int)
	np.put_along_axis(centerspos, np.broadcast_to(occupied[:, np.newaxis, :], [ncomb, nface, subdim]), half, axis=-1)
	np.put_along_axis(centerspos, np.broadcast_to(free[:, np.newaxis, :], [ncomb, nface, dim-subdim]), faces, axis=-1)

	corners=cornerspos.reshape(ncomb*nface, 1, ncorn, dim)+offsets[np.newaxis, :, np.newaxis, :]
	centers=centerspos.reshape(ncomb*nface, 1, dim)+offsets[np.newaxis, :, :]

	return corners.reshape(-1, ncorn, dim), centers.reshape(-1, dim)

# Mean over the in-bounds points of a [n, k, dim] index array.
def neighbour_mean(space, points):
	inside=np.all((points>=0)&(points<space.shape[0]), axis=-1).T
	vals=space[tuple(np.clip(points, 0, space.shape[0]-1).T)]
	return (vals*inside).sum(axis=0)/inside.sum(axis=0)

def diamond_rec(space, size, offsets, stitch_dim, noise_lo, noise_hi, rng, subdim=None):
	dim=space.ndim

	if subdim is None:
		subdim=dim
	if subdim<=stitch_dim:
		return

	corners, centers=corners_and_centers(dim, subdim, size, offsets)
	means=space[tuple(corners.T)].mean(axis=0)
	space[tuple(centers.T)]=means+rng.uniform(noise_lo, noise_hi, size=means.size)

	diamond_rec(space, size, offsets, stitch_dim, noise_lo, noise_hi, rng, subdim-1)

def square_rec(space, size, offsets, stitch_dim, noise_lo, noise_hi, rng, curdim=None):
	dim=space.ndim

	if curdim is None:
		curdim=stitch_dim
	if curdim<=0:
		return

	half=size//2
	_, centers=corners_and_centers(dim, curdim, size, offsets)

	axis=np.eye(dim, dtype=int)
	neighpos=np.concatenate([axis, -axis])*half
	means=neighbour_mean(space, centers[:, np.newaxis, :]+neighpos)
	space[tuple(centers.T)]=means+rng.uniform(noise_lo, noise_hi, size=means.size)

	square_rec(space, size, offsets, stitch_dim, noise_lo, noise_hi, rng, curdim-1)

def stitch(space, size, offsets, stitch_dim):
	if stitch_dim==0:
		return

	dim=space.ndim
	half=size//2
	nback=2**stitch_dim

	# The axes a seam point is centred on are the ones its combination spans, so
	# take them from the combinatorics rather than reading them back off the
	# coordinate. corners_and_centers orders by (combination, face, offset).
	occupied=np.array(list(it.combinations(range(dim), stitch_dim)), dtype=int)
	occupied=np.repeat(occupied, 2**(dim-stitch_dim)*len(offsets), axis=0)
	_, seams=corners_and_centers(dim, stitch_dim, size, offsets)

	# Reach back by half along every subset of the centred axes. Everything the
	# stencil touches has fewer centred axes than a seam point, so no seam point
	# reads another and the pass is order-independent (hence vectorizable).
	# Seams repeat where cells meet, but a point's centred axes do not depend on
	# which cell produced it, so the repeats all write the same value.
	back=np.zeros([len(seams), nback, dim], dtype=int)
	np.put_along_axis(back, np.broadcast_to(occupied[:, np.newaxis, :], [len(seams), nback, stitch_dim]), get_cornerspos(stitch_dim)*-half, axis=-1)
	space[tuple(seams.T)]=neighbour_mean(space, seams[:, np.newaxis, :]+back)

def diamond_square_nd(space, size=None, offsets=None, *, stitch_dim=1, factor=0.5, noise_lo=-1.0, noise_hi=1.0, seed=None):
	if size is None:
		size=space.shape[0]
	if offsets is None:
		offsets=np.zeros([1, space.ndim], dtype=int)

	if size<=2:
		return space

	dim=space.ndim
	rng=np.random.default_rng(seed)

	diamond_rec(space, size, offsets, stitch_dim, noise_lo, noise_hi, rng)
	square_rec(space, size, offsets, stitch_dim, noise_lo, noise_hi, rng)
	stitch(space, size, offsets, stitch_dim)

	nsize=size//2
	child_offsets=(offsets[:, np.newaxis, :]+get_cornerspos(dim)[np.newaxis, :, :]*nsize).reshape(-1, dim)

	diamond_square_nd(space,
			size=nsize+1,
			offsets=child_offsets,
			stitch_dim=stitch_dim,
			factor=factor,
			noise_lo=noise_lo*factor,
			noise_hi=noise_hi*factor,
			seed=None if seed is None else rng.integers(10**9))
	return space
