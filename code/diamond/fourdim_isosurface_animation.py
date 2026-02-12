from matplotlib import cm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.pyplot as plt
import numpy as np
import gc

from generalized_o3_pro import create_space, diamond_square_nd

try:
	from skimage import measure
except ImportError:
	print("Error: scikit-image not installed. Install with: pip install scikit-image")
	exit(1)

size = 33
minval = 0
maxval = 127
seed = 42

# Generate variants for different stitch_dim and shell counts
configs = [
	{'stitch_dim': 0, 'num_shells': 2, 'title': 'Long Diamond, 2 shells'},
	{'stitch_dim': 1, 'num_shells': 2, 'title': 'Balanced (1), 2 shells'},
	{'stitch_dim': 2, 'num_shells': 2, 'title': 'Balanced (2), 2 shells'},
	{'stitch_dim': 3, 'num_shells': 2, 'title': 'Long Square, 2 shells'},
	{'stitch_dim': 0, 'num_shells': 3, 'title': 'Long Diamond, 3 shells'},
	{'stitch_dim': 1, 'num_shells': 3, 'title': 'Balanced (1), 3 shells'},
	{'stitch_dim': 2, 'num_shells': 3, 'title': 'Balanced (2), 3 shells'},
	{'stitch_dim': 3, 'num_shells': 3, 'title': 'Long Square, 3 shells'},
]

for config in configs:
	stitch_dim = config['stitch_dim']
	num_shells = config['num_shells']

	space_4d = create_space(4, size, minval, maxval)
	diamond_square_nd(space_4d, stitch_dim=stitch_dim, factor=0.4,
	                  noise_lo=-maxval/2, noise_hi=maxval/2, seed=seed)

	vmin_global, vmax_global = space_4d.min(), space_4d.max()

	# Set up the figure
	fig = plt.figure(figsize=(12, 10))
	ax = fig.add_subplot(111, projection='3d')

	# Precompute logistic-scaled percentiles for shells
	linear_percentiles = np.linspace(100 / (num_shells + 1), 100 * num_shells / (num_shells + 1), num_shells)
	normalized = linear_percentiles / 100.0
	epsilon = 0.01
	normalized = np.clip(normalized, epsilon, 1 - epsilon)
	logit = np.log(normalized / (1 - normalized))
	scale = 2.0
	scaled_logit = logit * scale
	sigmoid = 1 / (1 + np.exp(-scaled_logit))
	percentiles = sigmoid * 100

	# Colors and alphas for shells
	cmap_shells = plt.colormaps.get_cmap('coolwarm')
	colors = [cmap_shells(i / (num_shells - 1)) if num_shells > 1 else cmap_shells(0.5) for i in range(num_shells)]
	alphas = np.linspace(0.3, 0.9, num_shells)

	def init():
		ax.clear()
		ax.set_xlim(0, size)
		ax.set_ylim(0, size)
		ax.set_zlim(0, size)
		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')
		ax.view_init(elev=20, azim=-60)
		return []

	def update(w_idx):
		ax.clear()

		# Extract 3D slice at this w coordinate
		slice_3d = space_4d[w_idx, :, :, :]

		# Compute percentile levels for this slice
		levels = np.percentile(slice_3d, percentiles)

		meshes_this_frame = []

		# Create isosurfaces for this 3D slice
		for level, color, alpha in zip(levels, colors, alphas):
			try:
				verts, faces, normals, values = measure.marching_cubes(slice_3d, level=level)
				mesh = Poly3DCollection(verts[faces], alpha=alpha, edgecolor='none')
				mesh.set_facecolor(color)
				ax.add_collection3d(mesh)
				meshes_this_frame.append(mesh)

				# Clean up immediately
				del verts, faces, normals, values
			except (ValueError, RuntimeError):
				pass

		ax.set_xlim(0, size)
		ax.set_ylim(0, size)
		ax.set_zlim(0, size)
		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')
		ax.set_title(f'4D Terrain at w={w_idx}/{size-1}\n(stitch_dim={stitch_dim}, {num_shells} shells)')
		ax.view_init(elev=20, azim=-60)

		# Garbage collect every few frames
		if w_idx % 5 == 0:
			gc.collect()

		return meshes_this_frame

	# Create animation through w dimension
	frames_list = list(range(size))
	anim = FuncAnimation(fig, update, init_func=init,
	                     frames=frames_list, interval=300, blit=False)

	# Save as GIF
	filename = f'fourdim_isosurface_animation_{size}_stitch{stitch_dim}_{num_shells}shells.gif'
	writer = PillowWriter(fps=3)
	anim.save(filename, writer=writer, dpi=80)
	plt.close()

	# Clean up before next config
	del space_4d, fig, ax, anim
	gc.collect()
