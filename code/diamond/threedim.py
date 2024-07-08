from matplotlib import cm
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from pandas import DataFrame
from pylab import *
import matplotlib.pyplot as plt
import numpy as np

exec(open("ndim_diamond_square.py").read())

size=9
minval=0
maxval=127

space=create_space(3, size, minval, maxval, 1.0)

def randrange(n, vmin, vmax):
	return (vmax-vmin)*np.random.rand(n) + vmin

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(projection='3d')
ax.view_init(elev=25, azim=60, roll=0)

xs=np.array((size*size)*list(range(0,size)))

ys=[]
for i in range(0, size):
	ys+=size*[i]
ys*=size
ys=np.array(ys)
zs=[]
for i in range(0, size):
	zs+=size*size*[i]
zs=np.array(zs)

fs=np.zeros([size**3])

for i in range(0, size**3):
	fs[i]=space[xs[i],ys[i],zs[i]]

colors = cm.plasma(fs/max(fs))

colmap = cm.ScalarMappable(cmap=cm.plasma)
colmap.set_array(fs)

yg = ax.scatter(xs, ys, zs, c=colors, marker='.')
cb = fig.colorbar(colmap, shrink=0.5)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.savefig("threedim.png")
plt.close()
