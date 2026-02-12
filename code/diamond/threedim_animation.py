from matplotlib import cm
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.pyplot as plt
import numpy as np
import gc

from generalized_o3_pro import create_space, diamond_square_nd

size = 129
minval = 0
maxval = 127
seed = 42
frame_skip = 1  # Show every Nth slice (1=all, 2=half, 4=quarter)

# Generate animations for all three stitch_dim values
configs = [
	{'stitch_dim': 0, 'title': 'Long Diamond'},
	{'stitch_dim': 1, 'title': 'Balanced'},
	{'stitch_dim': 2, 'title': 'Long Square'},
]

for config in configs:
	stitch_dim = config['stitch_dim']

	space = create_space(3, size, minval, maxval)
	diamond_square_nd(space, stitch_dim=stitch_dim, factor=0.4,
	                  noise_lo=-maxval/2, noise_hi=maxval/2, seed=seed)

	# Set up the figure
	fig = plt.figure(figsize=(12, 10))
	ax = fig.add_subplot(111, projection='3d')

	x = np.arange(size)
	y = np.arange(size)
	X, Y = np.meshgrid(x, y)

	vmin, vmax = space.min(), space.max()
	height_scale = 0.5

	def init():
		ax.clear()
		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Height')
		ax.set_xlim(0, size)
		ax.set_ylim(0, size)
		ax.set_zlim(vmin * height_scale, vmax * height_scale)
		ax.view_init(elev=30, azim=-60)
		return []

	def update(frame):
		ax.clear()
		z_idx = frame

		# Get the 2D slice at this z index
		slice_2d = space[:, :, z_idx]

		# Plot as 3D surface
		surf = ax.plot_surface(X, Y, slice_2d * height_scale,
		                       cmap='plasma', vmin=vmin, vmax=vmax,
		                       alpha=0.9, linewidth=0, antialiased=True)

		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Height')
		ax.set_title(f'3D Terrain Slice at z={z_idx}/{size-1} (stitch_dim={stitch_dim}, {config["title"]})')
		ax.set_xlim(0, size)
		ax.set_ylim(0, size)
		ax.set_zlim(vmin * height_scale, vmax * height_scale)
		ax.view_init(elev=30, azim=-60)

		# Force garbage collection every 10 frames to limit memory usage
		if frame % 10 == 0:
			gc.collect()

		return [surf]

	# Create animation going through z slices
	frames_list = list(range(0, size, frame_skip))
	anim = FuncAnimation(fig, update, init_func=init,
	                     frames=frames_list, interval=200, blit=False)

	# Save as GIF
	filename = f'threedim_animation_{stitch_dim}.gif'
	writer = PillowWriter(fps=5)
	anim.save(filename, writer=writer, dpi=80)
	plt.close(fig)

	# Clean up before next config
	del space, fig, ax, X, Y, anim
	gc.collect()
