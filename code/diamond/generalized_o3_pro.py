import math
import numpy as np
import itertools as it

def create_space(dim, size, minval=0, maxval=255):
	space=np.zeros([size]*dim, dtype=float)
	corners=np.array(list(np.ndindex(*[2]*dim)))*(size - 1)
	space[tuple(corners.T)]=np.random.uniform(minval, maxval, size=len(corners))
	return space

def get_cornerspos(dim):
	return np.array(list(it.product([0, 1], repeat=dim)), dtype=int)

def corners_and_centers(dim, subdim, size, offsets):
	half=size // 2
	offsets=np.asarray(offsets, dtype=int)

	corner_catalog=[]
	centre_catalog=[]

	for occupied in it.combinations(range(dim), subdim):
		occupied=np.array(occupied, dtype=int)
		fixed_axes=np.setdiff1d(np.arange(dim), occupied, assume_unique=True)

		for fixed_values in it.product([0, size - 1], repeat=len(fixed_axes)):
			fixed_values=np.array(fixed_values, dtype=int)

			for off in offsets:
				local_corners=get_cornerspos(subdim)*(size - 1)
				full_corners=np.empty((2 ** subdim, dim), dtype=int)
				full_corners[:, occupied]=local_corners
				full_corners[:, fixed_axes]=fixed_values
				full_corners += off
				corner_catalog.append(full_corners)

				centre=np.array(off)
				centre[occupied] += half
				centre[fixed_axes] += fixed_values
				centre_catalog.append(centre)

	corners=np.stack(corner_catalog, axis=0)
	centers=np.stack(centre_catalog, axis=0)
	return corners, centers

def _average(space, corners):
	dim=space.ndim
	flat_idx=tuple(corners[..., d].ravel() for d in range(dim))
	values=space[flat_idx].reshape(corners.shape[0], corners.shape[1])
	return values.mean(axis=1)

def diamond_rec(space, size, offsets, stitch_dim, noise_lo, noise_hi, rng,
				subdim=None):
	dim=space.ndim

	if subdim is None:
		subdim=dim
	if subdim <= stitch_dim:
		return

	corners, centers=corners_and_centers(dim, subdim, size, offsets)
	means=_average(space, corners)
	space[tuple(centers.T)]=means+rng.uniform(noise_lo, noise_hi, size=means.size)

	diamond_rec(space, size, offsets, stitch_dim,
				noise_lo, noise_hi, rng, subdim - 1)

def square_rec(space, size, offsets, stitch_dim, noise_lo, noise_hi, rng,
			   curdim=None):
	dim=space.ndim
	if curdim is None:
		curdim=stitch_dim
	if curdim <= 0:
		return

	half=size // 2
	_, centers=corners_and_centers(dim, curdim, size, offsets)

	neigh_offsets=np.eye(dim, dtype=int)
	neigh_offsets=np.concatenate([neigh_offsets, -neigh_offsets])*half

	for centre in centers:
		neighbours=centre+neigh_offsets
		valid=np.all(neighbours >= 0, axis=1) & np.all(neighbours < space.shape[0], axis=1)
		vals=space[tuple(neighbours[valid].T)]
		space[tuple(centre)]=vals.mean()+rng.uniform(noise_lo, noise_hi)

	square_rec(space, size, offsets, stitch_dim,
			   noise_lo, noise_hi, rng, curdim - 1)

def stitch(space, size, offsets, stitch_dim):
	if stitch_dim == 0:
		return

	dim=space.ndim
	half=size // 2
	dims=range(dim)

	seam_centers=[]
	for centred in it.combinations(dims, stitch_dim):
		fixed_axes=[d for d in dims if d not in centred]
		for fixed_vals in it.product([0, size - 1], repeat=len(fixed_axes)):
			for off in offsets:
				pt=np.array(off)
				pt[list(centred)]+=half
				pt[fixed_axes]+=fixed_vals
				seam_centers.append(pt)

	if not seam_centers:
		return

	seam_centers=np.unique(np.stack(seam_centers), axis=0)
	for pt in seam_centers:
		centred_dims=[d for d in range(dim) if pt[d] not in [0, size - 1]]

		vals=[]
		for v in it.product([0, -half], repeat=len(centred_dims)):
			neighbour=pt.copy()
			for i, dim_idx in enumerate(centred_dims):
				neighbour[dim_idx] += v[i]
			if ((neighbour >= 0) & (neighbour < space.shape[0])).all():
				vals.append(space[tuple(neighbour)])
		if vals:
			space[tuple(pt)]=np.mean(vals)

def diamond_square_nd(space, size=None, offsets=None, *, stitch_dim=1, factor=0.5, noise_lo=-1.0, noise_hi=1.0, seed=None):
	if size is None:
		size=space.shape[0]
	if offsets is None:
		offsets=np.zeros((1, space.ndim), dtype=int)

	if size <= 2:
		return space

	rng=np.random.default_rng(seed)

	diamond_rec(space, size, offsets, stitch_dim, noise_lo, noise_hi, rng)
	square_rec(space, size, offsets, stitch_dim, noise_lo, noise_hi, rng)
	stitch(space, size, offsets, stitch_dim)

	half=size//2
	dim=space.ndim
	child_offsets=(offsets[:, None, :]+get_cornerspos(dim)[None, :, :]*half).reshape(-1, dim)

	diamond_square_nd(space,
			  size=half+1,
			  offsets=child_offsets,
			  stitch_dim=stitch_dim,
			  factor=factor,
			  noise_lo=noise_lo*factor,
			  noise_hi=noise_hi*factor,
			  seed=None if seed is None else rng.integers(10**9))
	return space
