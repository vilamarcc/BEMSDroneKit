from routes import *
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from missioncalculation import *


mpl.rcParams['legend.fontsize'] = 10


# Helix Single Squared
fig = plt.figure()

#Square
#cc1 = [41.275321, 1.9843143]
#cc2 = [41.27507910, 1.98441620]
#cc3 = [41.27515570 ,1.98475960]
#cc4 = [41.27540170, 1.98464420]

#Rectangle
cc1 = [41.27545100, 1.98420030]
cc2 = [41.27479290, 1.98449130]
cc3 = [41.27489470, 1.98491650]
cc4 = [41.27554780, 1.98462680]

ax = fig.gca(projection='3d')

# BUILDING WALLS #
hmax = 15
ax.scatter(cc1[0],cc1[1],hmax)
ax.scatter(cc2[0],cc2[1],hmax)
ax.scatter(cc3[0],cc3[1],hmax)
ax.scatter(cc4[0],cc4[1],hmax)
ax.scatter(cc1[0],cc1[1],0)
ax.scatter(cc2[0],cc2[1],0)
ax.scatter(cc3[0],cc3[1],0)
ax.scatter(cc4[0],cc4[1],0)
basex = [cc1[0],cc2[0],cc3[0],cc4[0],cc1[0]]
basey = [cc1[1],cc2[1],cc3[1],cc4[1],cc1[1]]
i = 0
ccn = [cc1,cc2,cc3,cc4]
while i < 4:
    cc = ccn[i]
    linex = [cc[0],cc[0]]
    liney = [cc[1],cc[1]]
    linez = [0,hmax]
    ax.plot(linex,liney,linez)
    i = i + 1
ax.plot(basex,basey,hmax)
ax.plot(basex,basey,0)



sep = 3
bufferD = 2
x,y,z = getHelix(hmax, sep, bufferD,cc1, cc2, cc3, cc4)
cLat,cLon = getCenterofPerimeter(cc1, cc2, cc3, cc4)
C = [cLat,cLon]
x,y,z = getHelixinCoords(x,y,z,C)
#ax.plot(x, y, z)
#writeSimpleHelixMission(hmax,sep,n,8,bufferD,cc1,cc2,cc3,cc4)
x,y,z = getFacade(hmax,sep,bufferD,cc2,cc3)
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