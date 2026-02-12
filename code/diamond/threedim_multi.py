from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

from generalized_o3_pro import create_space, diamond_square_nd

size = 65
minval = 0
maxval = 127
seed = 42

# Generate 3D landscapes with different stitch_dim values
# stitch_dim=0: Long Diamond (diamond steps from dim down to 1, then squares from 0)
# stitch_dim=1: Balanced (diamond from dim to 2, square from 1 to 0)
# stitch_dim=2: Long Square (diamond from dim to 3, square from 2 to 0)

configs = [
	{'stitch_dim': 0, 'title': 'stitch_dim=0 (Long Diamond)'},
	{'stitch_dim': 1, 'title': 'stitch_dim=1 (Balanced)'},
	{'stitch_dim': 2, 'title': 'stitch_dim=2 (Long Square)'},
]

fig = plt.figure(figsize=(18, 6))

x = np.arange(size)
y = np.arange(size)
X, Y = np.meshgrid(x, y)

# Scale factor for terrain height
height_scale = 0.3

for config_idx, config in enumerate(configs):
	space = create_space(3, size, minval, maxval)
	diamond_square_nd(space, stitch_dim=config['stitch_dim'],
	                  factor=0.6, noise_lo=-maxval/2, noise_hi=maxval/2,
	                  seed=seed)

	ax = fig.add_subplot(1, 3, config_idx + 1, projection='3d')

	# Show every few slices to avoid clutter
	step = max(1, size // 4)
	z_slices = range(0, size, step)

	vmin, vmax = space.min(), space.max()

	for idx, z in enumerate(z_slices):
		slice_2d = space[:, :, z]
		# Plot the actual terrain height, offset vertically by z-slice index
		Z = slice_2d * height_scale + idx * (maxval * height_scale * 1.2)
		surf = ax.plot_surface(X, Y, Z, cmap='plasma',
		                       vmin=vmin, vmax=vmax,
		                       alpha=0.8, linewidth=0, antialiased=True)

	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Height (stacked)')
	ax.set_title(config['title'])
	ax.view_init(elev=25, azim=-60)

fig.suptitle(f'3D Terrain with Different stitch_dim Values ({size}×{size}×{size})', fontsize=14, y=0.98)
plt.tight_layout(rect=[0, 0, 0.95, 0.96])

# Add a shared colorbar after tight_layout
m = cm.ScalarMappable(cmap=cm.plasma)
m.set_array([minval, maxval])
m.set_clim(minval, maxval)
cbar_ax = fig.add_axes([0.96, 0.15, 0.02, 0.7])  # [left, bottom, width, height]
fig.colorbar(m, cax=cbar_ax, label='Terrain Height')

plt.savefig("threedim_multi.png", dpi=120, bbox_inches='tight')
plt.close()
