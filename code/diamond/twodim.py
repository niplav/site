from matplotlib import cm
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np

from generalized_o3_pro import create_space, diamond_square_nd

size=129
minval=0
maxval=255

space=create_space(2, size, minval, maxval)
diamond_square_nd(space, stitch_dim=1, factor=0.5, noise_lo=-maxval/2, noise_hi=maxval/2)

fig=plt.figure()
ax = fig.add_subplot(projection='3d')

X=np.arange(0, size, 1)
Y=np.arange(0, size, 1)

X,Y=np.meshgrid(X, Y)

surf=ax.plot_surface(X, Y, space, cmap=cm.coolwarm)
ax.set_zlim(minval, maxval)
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.savefig("twodim.png")
plt.close()
