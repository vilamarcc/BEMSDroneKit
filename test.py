from routes import getHelix
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


mpl.rcParams['legend.fontsize'] = 10


# Helix Single Squared
fig = plt.figure()

ax = fig.gca(projection='3d')
wall1 = 2.5
wall2 = 5
hmax = 15
yy, zz = np.meshgrid(np.linspace(-wall2,wall2,2), np.linspace(0,hmax,2))
xx = np.linspace(-wall1,wall1,2)
surf = ax.plot_surface(wall1, yy, zz)
surf_2 = ax.plot_surface(-wall1, yy, zz)
surf_3 = ax.plot_surface(xx, wall2, zz)
surf_3 = ax.plot_surface(xx, -wall2, zz)


sep = 2
bufferD = 0.5
x,y,z = getHelix(hmax, sep, wall1, wall2, bufferD)
ax.plot(x, y, z)
plt.show()