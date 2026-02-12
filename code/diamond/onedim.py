import matplotlib.pyplot as plt
import numpy as np

from generalized_o3_pro import create_space, diamond_square_nd

size = 129
minval = 0
maxval = 255

space = create_space(1, size, minval, maxval)
diamond_square_nd(space, stitch_dim=0, factor=0.5, noise_lo=-maxval/2, noise_hi=maxval/2, seed=42)

fig, ax = plt.subplots(figsize=(12, 4))
x = np.arange(size)
ax.plot(x, space, linewidth=1.5, color='purple')
ax.fill_between(x, 0, space, alpha=0.3, color='purple')
ax.set_xlabel('Position')
ax.set_ylabel('Height')
ax.set_title('1D Terrain (Diamond-Square)')
ax.grid(True, alpha=0.3)
# Set ylim to show full range of data
data_min, data_max = space.min(), space.max()
margin = (data_max - data_min) * 0.1
ax.set_ylim(min(0, data_min - margin), data_max + margin)
plt.tight_layout()
plt.savefig("onedim.png", dpi=120, bbox_inches='tight')
plt.close()
