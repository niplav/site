from matplotlib import cm
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from pandas import DataFrame
from pylab import *
import matplotlib.pyplot as plt
import numpy as np

# TODO: finish this sometime else

exec(open("takeoff.py").read())

def randrange(n, vmin, vmax):
	return (vmax-vmin)*np.random.rand(n) + vmin

fig = plt.figure()

ax = fig.gca(projection='3d')
n = 100

xs = randrange(n, 0, 100)
ys = randrange(n, 0, 100)
zs = randrange(n, 0, 100)
the_fourth_dimension = randrange(n,0,100)

colors = cm.hsv(the_fourth_dimension/max(the_fourth_dimension))

colmap = cm.ScalarMappable(cmap=cm.hsv)
colmap.set_array(the_fourth_dimension)

yg = ax.scatter(xs, ys, zs, c=colors, marker='o')
cb = fig.colorbar(colmap)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.savefig("threedim.png")
plt.close()

exit()

fig=plt.figure()
ax=fig.gca(projection='3d')
X=np.arange(0,size,1)
Y=np.arange(0,size,1)
X,Y=np.meshgrid(X,Y)
surf=ax.plot_surface(X,Y,space, cmap=cm.coolwarm)
ax.set_zlim(0,2*maxval)
fig.colorbar(surf, shrink=0.5, aspect=5)
