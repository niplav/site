from matplotlib import cm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
import gc

from generalized_o3_pro import create_space, diamond_square_nd

try:
	from skimage import measure
except ImportError:
	print("Error: scikit-image not installed. Install with: pip install scikit-image")
	exit(1)

size = 65
minval = 0
maxval = 127
seed = 42

# Generate 3D landscapes with different stitch_dim values
configs = [
	{'stitch_dim': 0, 'title': 'stitch_dim=0 (Long Diamond)'},
	{'stitch_dim': 1, 'title': 'stitch_dim=1 (Balanced)'},
	{'stitch_dim': 2, 'title': 'stitch_dim=2 (Long Square)'},
]

# Generate versions with 2, 3, and 4 shells
for num_shells in [2, 3, 4]:
	fig = plt.figure(figsize=(18, 6))
	axes = []

	for config_idx, config in enumerate(configs):
		# Generate terrain for this config only
		space = create_space(3, size, minval, maxval)
		diamond_square_nd(space, stitch_dim=config['stitch_dim'],
		                  factor=0.3, noise_lo=-maxval/2, noise_hi=maxval/2,
		                  seed=seed)

		ax = fig.add_subplot(1, 3, config_idx + 1, projection='3d')
		axes.append(ax)

		vmin, vmax = space.min(), space.max()

		# Create isosurfaces at different threshold levels
		# Use logistic-scaled percentiles to push toward extremes
		# This creates tighter, more separated shells
		linear_percentiles = np.linspace(100 / (num_shells + 1), 100 * num_shells / (num_shells + 1), num_shells)
		# Normalize to [0, 1]
		normalized = linear_percentiles / 100.0
		# Apply logit transformation (inverse sigmoid) to spread values
		# Clip to avoid infinity at 0 and 1
		epsilon = 0.01
		normalized = np.clip(normalized, epsilon, 1 - epsilon)
		logit = np.log(normalized / (1 - normalized))
		# Scale the logit values (higher scale = more extreme percentiles)
		scale = 2.0
		scaled_logit = logit * scale
		# Apply sigmoid to bring back to [0, 1]
		sigmoid = 1 / (1 + np.exp(-scaled_logit))
		# Convert back to percentiles
		percentiles = sigmoid * 100
		levels = np.percentile(space, percentiles)

		# Generate colors from cool to warm
		cmap = plt.colormaps.get_cmap('coolwarm')
		colors = [cmap(i / (num_shells - 1)) if num_shells > 1 else cmap(0.5) for i in range(num_shells)]

		# Alpha increases from outer to inner shells
		alphas = np.linspace(0.4, 0.9, num_shells)

		for level, color, alpha in zip(levels, colors, alphas):
			try:
				# Use marching cubes to find isosurface
				verts, faces, normals, values = measure.marching_cubes(space, level=level)

				# Create mesh
				mesh = Poly3DCollection(verts[faces], alpha=alpha, edgecolor='none')
				mesh.set_facecolor(color)
				ax.add_collection3d(mesh)

				# Clean up mesh data immediately
				del verts, faces, normals, values, mesh
			except (ValueError, RuntimeError) as e:
				# If isosurface can't be found at this level, skip it
				pass

		# Set the limits
		ax.set_xlim(0, size)
		ax.set_ylim(0, size)
		ax.set_zlim(0, size)
		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')
		ax.set_title(config['title'])
		ax.view_init(elev=20, azim=-60)

		# Clean up space array before next config
		del space
		gc.collect()

	fig.suptitle(f'Isosurfaces of 3D Terrain ({num_shells} shells, {size}×{size}×{size})',
	             fontsize=14, y=0.98)
	plt.tight_layout(rect=[0, 0, 1, 0.96])
	filename = f"threedim_isosurface_{num_shells}.png"

	# Use lower DPI for large sizes to reduce rendering memory
	dpi = 80 if size > 100 else 120
	plt.savefig(filename, dpi=dpi, bbox_inches='tight')

	# Explicitly close and cleanup
	plt.close(fig)
	del fig, axes
	gc.collect()
