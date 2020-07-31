from matplotlib import cm
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from pandas import DataFrame
from pylab import *
import matplotlib.pyplot as plt
import numpy as np

exec(open("takeoff.py").read())

def randrange(n, vmin, vmax):
	return (vmax-vmin)*np.random.rand(n) + vmin

fig = plt.figure()

ax = fig.gca(projection='3d')

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

colors = cm.hsv(fs/max(fs))

colmap = cm.ScalarMappable(cmap=cm.hsv)
colmap.set_array(fs)

yg = ax.scatter(xs, ys, zs, c=colors, marker='.')
cb = fig.colorbar(colmap)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.savefig("threedim.png")
plt.close()
