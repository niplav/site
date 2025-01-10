import math
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
	dim=len(space.shape)

	if subdim==None:
		subdim=dim
	if subdim<=stitch_dim:
		return space

	# Test with:
	# * offsets zeroes, subdim 0
	# * offsets zeroes, subdim 1
	# * offsets zeroes, subdim 2
	# * offsets nonzeroes, subdim 0
	# * offsets nonzeroes, subdim 1

	#cornerspos=get_cornerspos(dim)
	#corners=offsets[:, np.newaxis] + cornerspos[np.newaxis, :]*(size-1)

	#TODO: compute centers!
	centers=offsets+size//2
	space[tuple(centers.T)]=space[tuple(corners.T)].mean(axis=0)
	return diamond_rec(space, size, offsets, stitch_dim, minval, maxval, factor, subdim-1)

def square_rec(space, size, offsets, stitch_dim, minval, maxval, factor, curdim=None):
	return space

def stitch(space, offsets, stitch_dim, minval, maxval, factor):
	return space

# Needs to be recursive! When given space go big first then into smaller & smaller cells
def diamond_square_nd(space, size=None, offsets=None, stitch_dim=1, minval=0, maxval=255, factor=1.0):
	if size==None:
		size=space.shape[0]

	if size<=2:
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
	# For some reasons, the code below produces one axis *too much* in the beginning!, when offsets has the shape (1, …)
	# noffsets=offsets[:, np.newaxis] + cornerspos[np.newaxis, :] * nsize
	# This line works, but is ugly
	# noffsets=(offsets[:, np.newaxis] + cornerspos[np.newaxis, :] * nsize).reshape([offsets.shape[0]*cornerspos.shape[0], dim])
	noffsets=cartsum(offsets, get_cornerspos(dim)*nsize)

	return diamond_square_nd(space,
				size=nsize+1,
				offsets=noffsets,
				minval=round(minval*factor),
				maxval=round(maxval*factor),
				factor=factor)

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
