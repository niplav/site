import matplotlib.pyplot as plt
import numpy as np

from generalized_o3_pro import create_space, diamond_square_nd

size = 513
minval = 0
maxval = 255

# Generate multiple 1D landscapes with different parameters
configs = [
	{'seed': 42, 'factor': 0.5, 'title': 'seed=42, factor=0.5', 'color': 'purple'},
	{'seed': 123, 'factor': 0.7, 'title': 'seed=123, factor=0.7', 'color': 'blue'},
	{'seed': 999, 'factor': 0.3, 'title': 'seed=999, factor=0.3', 'color': 'green'},
	{'seed': 256, 'factor': 0.6, 'title': 'seed=256, factor=0.6', 'color': 'orange'},
]

fig, axes = plt.subplots(4, 1, figsize=(12, 10))

for idx, config in enumerate(configs):
	ax = axes[idx]
	space = create_space(1, size, minval, maxval)
	diamond_square_nd(space, stitch_dim=0, factor=config['factor'],
	                  noise_lo=-maxval/2, noise_hi=maxval/2, seed=config['seed'])

	x = np.arange(size)
	ax.plot(x, space, linewidth=1.5, color=config['color'])
	ax.fill_between(x, 0, space, alpha=0.3, color=config['color'])
	ax.set_ylabel('Height')
	ax.set_title(config['title'])
	ax.grid(True, alpha=0.3)
	# Set ylim based on actual data range
	data_min, data_max = space.min(), space.max()
	margin = (data_max - data_min) * 0.1
	ax.set_ylim(min(0, data_min - margin), data_max + margin)

	if idx == len(configs) - 1:
		ax.set_xlabel('Position')

fig.suptitle('1D Terrains with Different Parameters', fontsize=14, y=0.995)
plt.tight_layout()
plt.savefig("onedim_multi.png", dpi=120, bbox_inches='tight')
plt.close()
