import numpy as np
from collections import deque
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_space(dim, size, minval=0, maxval=255):
    """Initialize n-dimensional space with random corners"""
    space = np.zeros([size]*dim)
    # Initialize corners with random values
    indices = np.array(list(np.ndindex(*[2]*dim))) * (size-1)
    space[tuple(indices.T)] = np.random.randint(minval, maxval, size=len(indices))
    return space

def get_corners_for_cell(base_pos, cell_size, current_dim, max_size):
    """
    Get corners for a cell of specific dimension.
    For a d-dimensional cell, returns 2^d corners.
    """
    # Generate all corner offsets for the current dimension
    corner_offsets = np.array(list(np.ndindex(*[2]*(current_dim + 1)))) * cell_size
    
    # Add base position to get actual corner coordinates
    corners = []
    for offset in corner_offsets:
        pos = list(base_pos)
        for i in range(current_dim + 1):
            pos[i] += offset[i]
        if all(0 <= p < max_size for p in pos):
            corners.append(tuple(pos))
    return corners

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

def diamond_rec(space, stitch_dim=1, minval=0, maxval=255, factor=1.0):
	return space

def square_rec(space, stitch_dim=1, minval=0, maxval=255, factor=1.0):
	return space

# Needs to be recursive! When given space go big first then into smaller & smaller cells
def diamond_square_nd(space, stitch_dim=1, minval=0, maxval=255, factor=1.0):
	return diamond_square_nd_rec(space, dim, size, offsets, minval, maxval, factor)

# Needs to be recursive! When given space go big first then into smaller & smaller cells
def diamond_square_nd_rec(space, stitch_dim=1, minval=0, maxval=255, factor=1.0):
	dim=len(space.shape)

	if not (0<=stitch_dim<dim):
		raise ValueError(f"stitch_dim must be between 0 and {dim-1}")

	space=diamond_rec(space, stitch_dim=stitch_dim, minval=minval, maxval=maxval, factor=factor)
	space=square_rec(space, stitch_dim=stitch_dim, minval=minval, maxval=maxval, factor=factor)
	space=stitch(space, stitch_dim=stitch_dim, minval=minval, maxval=maxval, factor=factor)

	return space

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
