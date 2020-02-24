import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


mpl.rcParams['legend.fontsize'] = 10


# Helix Single Squared
fig = plt.figure()
turnsperlevel = 10
ax = fig.gca(projection='3d')

# BUILDING PERIMETER WALLS #
hmax = 20
yy, zz = np.meshgrid(np.linspace(-2.5,2.5,2), np.linspace(0,hmax,2))
xx = 2.5
surf = ax.plot_surface(xx, yy, zz)
surf_2 = ax.plot_surface(-xx, yy, zz)
surf_3 = ax.plot_surface(yy, xx, zz)
surf_3 = ax.plot_surface(yy, -xx, zz)

# HELIX CALCULATION

pitch = 2
n = (hmax / pitch)
theta = np.linspace(0, 2 * np.pi * n , 300)
r = np.sqrt(2.5**2 + 2.5**2) + 0.5
x = r * np.sin(theta)
y = r * np.cos(theta)
z =  theta 
ax.plot(x, y, z)

plt.show()