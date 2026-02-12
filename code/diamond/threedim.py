from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

from generalized_o3_pro import create_space, diamond_square_nd

size = 129
minval = 0
maxval = 127

space = create_space(3, size, minval, maxval)
diamond_square_nd(space, stitch_dim=1, factor=0.6, noise_lo=-maxval/2, noise_hi=maxval/2, seed=42)

# Create 3D plot with stacked 2D terrain surfaces
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

x = np.arange(size)
y = np.arange(size)
X, Y = np.meshgrid(x, y)

# Show every few slices to avoid visual clutter
step = max(1, size // 4)
z_slices = range(0, size, step)

# Normalize colors across all slices
vmin, vmax = space.min(), space.max()

# Scale factor for terrain height to make it visible but not overwhelming
height_scale = 0.3

for idx, z in enumerate(z_slices):
	slice_2d = space[:, :, z]
	# Plot the actual terrain height, offset vertically by z-slice index
	Z = slice_2d * height_scale + idx * (maxval * height_scale * 1.2)
	surf = ax.plot_surface(X, Y, Z, cmap='plasma',
	                       vmin=vmin, vmax=vmax,
	                       alpha=0.8, linewidth=0, antialiased=True)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Height (stacked by depth)')
ax.set_title(f'3D Terrain as Stacked 2D Landscapes ({size}×{size}×{size})')
ax.view_init(elev=25, azim=-60)

# Add colorbar
m = cm.ScalarMappable(cmap=cm.plasma)
m.set_array([vmin, vmax])
m.set_clim(vmin, vmax)
fig.colorbar(m, ax=ax, shrink=0.5, aspect=10, label='Terrain Height')

plt.savefig("threedim.png", dpi=120, bbox_inches='tight')
plt.close()
