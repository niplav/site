import numpy as np
import itertools as it
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_space(dim, size, minval=0, maxval=255):
	"""Initialize n-dimensional space with random corners"""
	space = np.zeros([size]*dim)
	# Initialize corners with random values
	indices = np.array(list(np.ndindex(*[2]*dim))) * (size-1)
	space[tuple(indices.T)] = np.random.randint(minval, maxval, size=len(indices))
	return space

def get_cornerspos(dim):
	return np.array(list(it.product([0, 1], repeat=dim)))

def cartsum(a1, a2):
	return np.array(list(it.product(a1, a2))).sum(axis=1)

def diamond_rec(space, size, offsets, stitch_dim, minval, maxval, factor, curdim=None):
	if curdim is None:
		curdim = len(space.shape)

	if curdim == 0 or size <= 1:
		return space

	dim = len(space.shape)
	cornerspos = get_cornerspos(dim)

	# Calculate corners for all offsets
	corners = offsets[:, np.newaxis, :] + cornerspos[np.newaxis, :, :] * (size-1)
	centers = offsets + size//2

	# Convert to list of indices for each dimension
	corner_indices = [corners[:,:,d].flatten() for d in range(dim)]
	center_indices = [centers[:,d] for d in range(dim)]

	# Update center values based on corner averages
	space[tuple(center_indices)] = np.mean(space[tuple(corner_indices)].reshape(-1, corners.shape[1]), axis=1)

	return diamond_rec(space, size, offsets, stitch_dim, minval, maxval, factor, curdim-1)

def square_rec(space, size, offsets, stitch_dim, minval, maxval, factor, curdim=None):
	if curdim is None:
		curdim = 0

	if curdim >= len(space.shape) or size <= 1:
		return space

	dim = len(space.shape)

	# Process current dimension
	basis = np.eye(dim, dtype=int)[curdim]
	edge_centers = offsets + (size//2) * basis
	corner_offsets = np.array([-size//2, size//2])[:, np.newaxis] * basis
	neighbors = edge_centers[:, np.newaxis, :] + corner_offsets[np.newaxis, :, :]

	# Convert to list of indices for each dimension
	edge_indices = [edge_centers[:,d] for d in range(dim)]
	neighbor_indices = [neighbors[:,:,d].flatten() for d in range(dim)]

	# Update edge values
	space[tuple(edge_indices)] = np.mean(space[tuple(neighbor_indices)].reshape(-1, neighbors.shape[1]), axis=1)

	return square_rec(space, size, offsets, stitch_dim, minval, maxval, factor, curdim+1)

def stitch(space, size, offsets, stitch_dim, minval, maxval, factor):
	if size <= 1:
		return space

	dim = len(space.shape)
	stitch_basis = np.eye(dim, dtype=int)[stitch_dim]

	# Simpler approach: just get adjacent points along stitch dimension
	stitch_points = offsets + (size//2) * stitch_basis
	stitch_offsets = np.array([-size//2, size//2])[:, np.newaxis] * stitch_basis
	neighbors = stitch_points[:, np.newaxis, :] + stitch_offsets[np.newaxis, :, :]

	# Convert to list of indices
	stitch_indices = [stitch_points[:,d] for d in range(dim)]
	neighbor_indices = [neighbors[:,:,d].flatten() for d in range(dim)]

	# Update values
	space[tuple(stitch_indices)] = np.mean(space[tuple(neighbor_indices)].reshape(-1, 2), axis=1)

	return space

def diamond_square_nd(space, size=None, offsets=None, stitch_dim=1, minval=0, maxval=255, factor=0.5):
	if size is None:
		size = space.shape[0]
	if offsets is None:
		offsets = np.zeros([1, len(space.shape)], dtype=int)

	if size <= 2:
		return space

	dim = len(space.shape)

	# Add random displacement scaled by size
	scale = (maxval - minval) * (size / space.shape[0]) * factor

	# Diamond step with random displacement
	space = diamond_rec(space, size, offsets, stitch_dim, minval, maxval, scale)

	# Square step with reduced random displacement
	space = square_rec(space, size, offsets, stitch_dim, minval, maxval, scale * 0.5)

	# Stitch subgrids
	space = stitch(space, size, offsets, stitch_dim, minval, maxval, scale * 0.25)

	# Recursive call for smaller grids
	nsize = size//2
	noffsets = np.array(list(it.product(
		*[range(0, space.shape[0]-1, nsize) for _ in range(dim)]
	)))

	return diamond_square_nd(space, nsize+1, noffsets, stitch_dim, minval, maxval, factor)

def visualize_landscape(filled, title="Terrain Visualization", elevation_scale=1.0, azim=-60, elev=30):
	"""
	Visualize a 2D numpy array as a 3D landscape/terrain.

	Args:
		filled (np.ndarray): 2D numpy array representing height values
		title (str): Title for the plot
		elevation_scale (float): Scale factor for height values
		azim (float): Azimuthal viewing angle in degrees
		elev (float): Elevation viewing angle in degrees
	"""
	# Create figure and 3D axis
	fig = plt.figure(figsize=(12, 8))
	ax = fig.add_subplot(111, projection='3d')

	# Create coordinate grids
	x = np.arange(0, filled.shape[1], 1)
	y = np.arange(0, filled.shape[0], 1)
	X, Y = np.meshgrid(x, y)

	# Create the surface plot
	surf = ax.plot_surface(X, Y, filled * elevation_scale,
						  cmap='plasma',
						  linewidth=0,
						  antialiased=True,
						  alpha=0.8)

	# Add a color bar
	fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Height')

	# Customize the view
	ax.view_init(elev=elev, azim=azim)

	# Add wireframe for better depth perception
	ax.plot_wireframe(X, Y, filled * elevation_scale,
					 color='black',
					 linewidth=0.1,
					 alpha=0.3)

	# Add title and labels
	ax.set_title(title)
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Height')

	# Set aspect ratio to be equal
	ax.set_box_aspect([1, 1, 0.5])

	plt.show()
