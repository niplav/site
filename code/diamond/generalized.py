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

def get_centers_from_higher_dim(center_pos, cell_size, dim_index, max_size):
	"""
	Get centers from the higher dimensional cell that influence this position.
	These are the points computed in the previous step.
	"""
	centers = []
	# For each dimension up to current
	for d in range(dim_index + 1):
		# Try both positive and negative offsets
		for offset in [-cell_size, cell_size]:
			pos = list(center_pos)
			pos[d] += offset
			if all(0 <= p < max_size for p in pos):
				centers.append(tuple(pos))
	return centers

#def cartsum(a1, a2):
#	return np.array(list(it.product(a1, a2))).sum(axis=1)

def get_face_corners(dim, curdim):
	"""Get corners for all faces of dimension curdim in a dim-dimensional space"""
	fixed_dims = np.array(list(it.combinations(range(dim), curdim)))
	moving_dims = np.array([np.setdiff1d(range(dim), f) for f in fixed_dims])
	template = np.array(list(it.product([0, 1], repeat=dim-curdim+1)))[:, None, :] * np.eye(dim)[fixed_dims]
	return (template[:, None, :, :] + np.array(list(it.product([0, 1], repeat=curdim)))[None, :, None, :] * np.eye(dim)[moving_dims][:, None, :, :]).reshape(-1, 2**curdim, dim)

def get_face_corners(dim, curdim):
	"""Get corners for all faces of dimension curdim in a dim-dimensional space"""
	if curdim == dim:
		return get_cornerspos(dim)[None, :, :]
	fixed_dims = np.array(list(it.combinations(range(dim), dim - curdim)))
	moving_dims = np.array([np.setdiff1d(range(dim), f) for f in fixed_dims])
	template = np.array(list(it.product([0, 1], repeat=dim - curdim)))[:, None, :] * np.eye(dim)[fixed_dims]
	return (template[:, None, :, :] + np.array(list(it.product([0, 1], repeat=curdim)))[None, :, None, :] * np.eye(dim)[moving_dims][:, None, :, :]).reshape(-1, 2**curdim, dim)

def diamond_rec(space, size, offsets, stitch_dim, minval, maxval, factor, curdim=None):
	"""
	Corners first iteration (center) [Shape not quite correct bc only one element]:
		array([[[0, 0, 0],
	        [0, 0, 4],
	        [0, 4, 0],
	        [0, 4, 4],
	        [4, 0, 0],
	        [4, 0, 4],
	        [4, 4, 0],
	        [4, 4, 4]]])
	Corners second iteration (faces):
		array([[
		[
			[0, 0, 0],
			[0, 0, 4],
			[0, 4, 0],
			[0, 4, 4]
		],
		[
			[0, 0, 0],
			[0, 4, 0],
			[4, 0, 0],
			[4, 4, 0]
		],
	]])
	"""

	if curdim==None:
		curdim=len(space.shape)
	if curdim<=stitch_dim:
		return space

	dim=len(space.shape)
	cornerspos=get_cornerspos(dim)
	# TODO: zero out unneeded dimensions!
	corners=offsets[:, np.newaxis, :] + cornerspos[np.newaxis, :, :] * (size-1)
	centers=offsets+size//2
	space[tuple(centers.T)]=space[tuple(corners.T)].mean(axis=0)
	return diamond_rec(space, size, offsets, stitch_dim, minval, maxval, factor, curdim-1)

def square_rec(space, size, offsets, stitch_dim, minval, maxval, factor, curdim=None):
	return space

def stitch(space, offsets, stitch_dim, minval, maxval, factor):
	return space

# Needs to be recursive! When given space go big first then into smaller & smaller cells
def diamond_square_nd(space, size=None, offsets=None, stitch_dim=1, minval=0, maxval=255, factor=1.0):
	print("size: ", size)
	print("offsets: ", offsets)

	if size==None:
		size=space.shape[0]

	if size<=2:
		print("returning")
		return

	dim=len(space.shape)

	if type(offsets)==type(None):
		offsets=np.zeros([1, dim], dtype=int)
	# Indexing: space[tuple(offsets.T)]

	if not (0<=stitch_dim<dim):
		raise ValueError(f"stitch_dim must be between 0 and {dim-1}")

	space=diamond_rec(space, size, offsets, stitch_dim, minval, maxval, factor)
	space=square_rec(space, size, offsets, stitch_dim, minval, maxval, factor)
	space=stitch(space, size, offsets, stitch_dim, minval, maxval, factor)

	nsize=size//2
	cornerspos=get_cornerspos(dim)
	noffsets=offsets[:, np.newaxis, :] + cornerspos[np.newaxis, :, :] * (nsize)
	#noffsets=cartsum(offsets, get_cornerspos(dim)*nsize)

	return diamond_square_nd(space, size=nsize+1, offsets=noffsets, minval=round(minval*factor), maxval=round(maxval*factor), factor=factor)

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
