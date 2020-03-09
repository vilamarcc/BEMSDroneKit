from routes import *
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from missioncalculation import *

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()

#Square
cc11 = [41.275321, 1.9843143]
cc22 = [41.27507910, 1.98441620]
cc33 = [41.27515570 ,1.98475960]
cc44 = [41.27540170, 1.98464420]

#Rectangle
cc1 = [41.27545100, 1.98420030]
cc2 = [41.27479290, 1.98449130]
cc3 = [41.27489470, 1.98491650]
cc4 = [41.27554780, 1.98462680]

ax = fig.gca(projection='3d')

# BUILDING WALLS #
hmax = 15
hmin = 2
ax.scatter(cc11[0],cc11[1],hmax, label = "c1")
ax.scatter(cc22[0],cc22[1],hmax, label = "c2")
ax.scatter(cc33[0],cc33[1],hmax, label = "c3")
ax.scatter(cc44[0],cc44[1],hmax, label = "c4")
ax.legend()
ax.scatter(cc11[0],cc11[1],0)
ax.scatter(cc22[0],cc22[1],0)
ax.scatter(cc33[0],cc33[1],0)
ax.scatter(cc44[0],cc44[1],0)
basex = [cc11[0],cc22[0],cc33[0],cc44[0],cc11[0]]
basey = [cc11[1],cc22[1],cc33[1],cc44[1],cc11[1]]
i = 0
ccn = [cc11,cc22,cc33,cc44]
while i < 4:
    cc = ccn[i]
    linex = [cc[0],cc[0]]
    liney = [cc[1],cc[1]]
    linez = [0,hmax]
    ax.plot(linex,liney,linez)
    i = i + 1
ax.plot(basex,basey,hmax)
ax.plot(basex,basey,0)


#p1 = perimeter(cc1,cc2,cc3,cc4,10,0)
#p2 = perimeter(cc11,cc22,cc33,cc44,15,10)
#ps = [p1,p2]
wall1 = wall(cc11,cc22,hmax,hmin)
wall2 = wall(cc22,cc33,hmax,hmin)
wall3 = wall(cc33,cc44,hmax,hmin)
wall4 = wall(cc44,cc11,hmax,hmin)
walls = [wall1,wall2,wall3]
sep = 2
bufferD = 5
x,y,z = getMultiFacade(sep,bufferD,walls,-1)
#x,y,z,theta = getMultiHelix(0,sep,bufferD,ps)
ax.plot(x, y, z)





def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([0, 20 + 20/4])

set_axes_equal(ax)
plt.show()