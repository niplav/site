from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

from generalized_o3_pro import create_space, diamond_square_nd

size = 257
minval = 0
maxval = 255

# Generate multiple 2D landscapes with different seeds and parameters
configs = [
	{'seed': 999, 'factor': 0.3, 'stitch_dim': 1, 'title': 'seed=999, factor=0.3'},
	{'seed': 42, 'factor': 0.4, 'stitch_dim': 1, 'title': 'seed=42, factor=0.4'},
	{'seed': 123, 'factor': 0.5, 'stitch_dim': 1, 'title': 'seed=123, factor=0.5'},
	{'seed': 256, 'factor': 0.5, 'stitch_dim': 0, 'title': 'seed=256, factor=0.5, stitch_dim=0'},
]

fig, axes = plt.subplots(2, 2, figsize=(14, 12), subplot_kw={'projection': '3d'})
axes = axes.flatten()

for idx, config in enumerate(configs):
	ax = axes[idx]
	space = create_space(2, size, minval, maxval)
	diamond_square_nd(space, stitch_dim=config['stitch_dim'],
	                  factor=config['factor'],
	                  noise_lo=-maxval/2, noise_hi=maxval/2,
	                  seed=config['seed'])

	x = np.arange(0, size, 1)
	y = np.arange(0, size, 1)
	X, Y = np.meshgrid(x, y)

	surf = ax.plot_surface(X, Y, space, cmap='plasma',
	                       linewidth=0, antialiased=True, alpha=0.9)
	ax.set_title(config['title'])
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Height')
	ax.view_init(elev=30, azim=-60)

plt.tight_layout()
plt.savefig("twodim_multi.png", dpi=120, bbox_inches='tight')
plt.close()
