from matplotlib import cm
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np

exec(open("takeoff.py").read())

fig=plt.figure()
ax=fig.gca(projection='3d')

X=np.arange(0,size,1)
Y=np.arange(0,size,1)

X,Y=np.meshgrid(X,Y)

surf=ax.plot_surface(X,Y,space, cmap=cm.coolwarm)
ax.set_zlim(0,maxval)
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.savefig("twodim.png")
plt.close()
