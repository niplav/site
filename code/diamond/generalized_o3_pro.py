import math
import itertools as it
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D              # noqa – needed by mpl

def create_space(dim, size, minval=0, maxval=255):
    """Initialise an n-dimensional grid with random-valued corner points."""
    space = np.zeros([size] * dim, dtype=float)
    corners = np.array(list(np.ndindex(*[2] * dim))) * (size - 1)
    space[tuple(corners.T)] = np.random.uniform(minval, maxval, size=len(corners))
    return space

def get_cornerspos(dim):
    return np.array(list(it.product([0, 1], repeat=dim)), dtype=int)

def corners_and_centers(dim, subdim, size, offsets):
    """
    Generate the *global* coordinates of

    • all `2**subdim` corner points of every sub-cube of dimension `subdim`
    • the corresponding centre points.

    That is exactly the structure required for a diamond (or square) step
    on the given hyper-faces.

    Returned shapes
    ---------------
    corners : (N, 2**subdim, dim)
    centres : (N, dim)
    with  N =  comb(dim, subdim) * 2**(dim-subdim) * len(offsets)
    """
    half = size // 2
    offsets = np.asarray(offsets, dtype=int)

    corner_catalog = []
    centre_catalog = []

    # choose which axes are “free” (= vary inside the sub-cube)
    for occupied in it.combinations(range(dim), subdim):
        occupied = np.array(occupied, dtype=int)
        fixed_axes = np.setdiff1d(np.arange(dim), occupied, assume_unique=True)

        # for every combination of 0 / size-1 on the fixed axes …
        for fixed_values in it.product([0, size - 1], repeat=len(fixed_axes)):
            fixed_values = np.array(fixed_values, dtype=int)

            # now iterate over all *real* sub-cubes, i.e. over every offset
            for off in offsets:
                local_corners = get_cornerspos(subdim) * (size - 1)          # 0|max on free axes
                full_corners = np.empty((2 ** subdim, dim), dtype=int)
                full_corners[:, occupied] = local_corners
                full_corners[:, fixed_axes] = fixed_values
                full_corners += off
                corner_catalog.append(full_corners)

                centre = np.array(off)                     # start with offset
                centre[occupied] += half                  # middle along free axes
                centre[fixed_axes] += fixed_values        # fixed axes stay fixed
                centre_catalog.append(centre)

    corners = np.stack(corner_catalog, axis=0)
    centres = np.stack(centre_catalog, axis=0)
    return corners, centres

def _average(space, corners):
    """
    Fast vectorised averaging for a batch of corner sets:
    `corners` has the shape (N, C, dim) where C = 2**k.
    """
    dim = space.ndim
    flat_idx = tuple(corners[..., d].ravel() for d in range(dim))
    values = space[flat_idx].reshape(corners.shape[0], corners.shape[1])
    return values.mean(axis=1)


def diamond_rec(space, size, offsets, stitch_dim, noise_lo, noise_hi, rng,
                subdim=None):
    """
    Perform *all* diamond steps from `dim` down to `stitch_dim + 1`
    inside the cube described by `size` and `offsets`.
    """
    dim = space.ndim
    if subdim is None:
        subdim = dim

    if subdim <= stitch_dim:
        return

    corners, centres = corners_and_centers(dim, subdim, size, offsets)
    means = _average(space, corners)
    space[tuple(centres.T)] = means + rng.uniform(noise_lo, noise_hi, size=means.size)

    # recurse to next lower sub-dimension
    diamond_rec(space, size, offsets, stitch_dim,
                noise_lo, noise_hi, rng, subdim - 1)

def square_rec(space, size, offsets, stitch_dim, noise_lo, noise_hi, rng,
               curdim=None):
    """
    Perform all square steps from `stitch_dim` down to 1.
    For a sub-cube with `curdim` free axes we still re-use
    `corners_and_centers` to find *where* to write.  The *value*,
    however, is now the mean of the 2·dim orthogonally adjacent
    neighbours (classic square step).
    """
    dim = space.ndim
    if curdim is None:
        curdim = stitch_dim
    if curdim <= 0:
        return

    half = size // 2
    _, centres = corners_and_centers(dim, curdim, size, offsets)

    # neighbourhood offsets: ±half along every axis – one at a time
    neigh_offsets = np.eye(dim, dtype=int)
    neigh_offsets = np.concatenate([neigh_offsets, -neigh_offsets]) * half

    for centre in centres:
        neighbours = centre + neigh_offsets
        # stay inside current macro-cube
        valid = np.all(neighbours >= 0, axis=1) & np.all(neighbours < space.shape[0], axis=1)
        vals = space[tuple(neighbours[valid].T)]
        space[tuple(centre)] = vals.mean() + rng.uniform(noise_lo, noise_hi)

    square_rec(space, size, offsets, stitch_dim,
               noise_lo, noise_hi, rng, curdim - 1)

def stitch(space, size, offsets, stitch_dim):
    """
    Stitch together the “seams” that appear in the long-square regime
    (`stitch_dim` < dim-1): for every seam point simply take the mean
    of the values written from the touching sub-cubes.
    """
    if stitch_dim == 0:
        return                                             # nothing to do

    dim   = space.ndim
    half  = size // 2
    dims  = range(dim)

    # the seam lives on the hyper-faces where *exactly* `stitch_dim`
    # coordinates are centred (…==half) and the others are either 0 or max.
    seam_centres = []
    for centred in it.combinations(dims, stitch_dim):
        fixed_axes = [d for d in dims if d not in centred]
        for fixed_vals in it.product([0, size - 1], repeat=len(fixed_axes)):
            for off in offsets:
                pt = np.array(off)
                pt[list(centred)] += half
                pt[fixed_axes]   += fixed_vals
                seam_centres.append(pt)

    if not seam_centres:
        return

    seam_centres = np.unique(np.stack(seam_centres), axis=0)
    for pt in seam_centres:
        # neighbouring sub-cubes that wrote this point
        vals = []
        for v in it.product([0, -half], repeat=stitch_dim):
            neighbour = pt.copy()
            neighbour[[*it.islice((i for i in range(dim)), stitch_dim)]] += v
            if ((neighbour >= 0) & (neighbour < space.shape[0])).all():
                vals.append(space[tuple(neighbour)])
        if vals:
            space[tuple(pt)] = np.mean(vals)

def diamond_square_nd(space, size=None, offsets=None, *,
                      stitch_dim=1, factor=0.5,
                      noise_lo=-1.0, noise_hi=1.0, seed=None):
    """
    In-place n-dimensional Diamond-Square.

    Parameters
    ----------
    space       ndarray – quadratic (2**k + 1) grid with corner values preset.
    size        int|None – current sub-cube size  (internally managed).
    offsets     ndarray|None – left-lower corners of current sub-cubes.
    stitch_dim  int – 0 … dim-1  (Long-Diamond … Long-Square).
    factor      float – reduction of noise amplitude per recursion level.
    noise_lo / noise_hi
                floats – initial noise interval.
    seed        int|None – RNG seed for reproducibility.
    """
    if size is None:
        size = space.shape[0]
    if offsets is None:
        offsets = np.zeros((1, space.ndim), dtype=int)

    if size <= 2:                         # 1-cell sub-cube – recursion end
        return space

    rng = np.random.default_rng(seed)

    diamond_rec(space, size, offsets, stitch_dim,
                noise_lo, noise_hi, rng)
    square_rec(space, size, offsets, stitch_dim,
               noise_lo, noise_hi, rng)
    stitch(space, size, offsets, stitch_dim)

    half = size // 2
    dim  = space.ndim
    child_offsets = (offsets[:, None, :] + get_cornerspos(dim)[None, :, :] * half)\
        .reshape(-1, dim)

    diamond_square_nd(space,
                      size=half + 1,
                      offsets=child_offsets,
                      stitch_dim=stitch_dim,
                      factor=factor,
                      noise_lo=noise_lo * factor,
                      noise_hi=noise_hi * factor,
                      seed=None if seed is None else rng.integers(10**9))
    return space

def visualize_landscape(filled, title="Terrain Visualization",
                        elevation_scale=1.0, azim=-60, elev=30):
    """3-D matplotlib helper – identical to the previous version."""
    fig = plt.figure(figsize=(12, 8))
    ax  = fig.add_subplot(111, projection='3d')

    y, x = np.indices(filled.shape)
    ax.plot_surface(x, y, filled * elevation_scale,
                    cmap='plasma', linewidth=0, antialiased=True, alpha=.8)
    ax.plot_wireframe(x, y, filled * elevation_scale,
                      color='k', linewidth=.1, alpha=.3)

    ax.view_init(elev=elev, azim=azim)
    ax.set(title=title, xlabel='X', ylabel='Y', zlabel='Height')
    ax.set_box_aspect([1, 1, .5])
    plt.colorbar(plt.cm.ScalarMappable(cmap='plasma'),
                 ax=ax, shrink=.5, aspect=5, label='Height')
    plt.show()
