import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from routes import perimeter

def set_axes_equal(ax, hmax):

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
    ax.set_zlim3d([0, hmax + hmax/4])

def plotPreviewSimpleHelix(x,y,z,perimeter,n,home):
    fig = plt.figure(n)
    ax = fig.gca(projection='3d')
    #mpl.rcParams['legend.fontsize'] = 10
    cc1 = perimeter.c1
    cc2 = perimeter.c2
    cc3 = perimeter.c3
    cc4 = perimeter.c4
    hmax = perimeter.hmax
    hmin = perimeter.hmin

    ax.scatter(cc1[0],cc1[1],hmax, color = "b")
    ax.scatter(cc2[0],cc2[1],hmax, color = "b")
    ax.scatter(cc3[0],cc3[1],hmax, color = "b")
    ax.scatter(cc4[0],cc4[1],hmax, color = "b")
    ax.scatter(cc1[0],cc1[1],0, color = "b")
    ax.scatter(cc2[0],cc2[1],0, color = "b")
    ax.scatter(cc3[0],cc3[1],0, color = "b")
    ax.scatter(cc4[0],cc4[1],0, color = "b")
    ax.scatter(home.lat,home.lon,color = "r", label = "Home")
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
    xs = np.linspace(min(cc1[0],cc2[0],cc3[0],cc4[0]),max(cc1[0],cc2[0],cc3[0],cc4[0]),5)
    ys = np.linspace(min(cc1[1],cc2[1],cc3[1],cc4[1]),max(cc1[1],cc2[1],cc3[1],cc4[1]),5)
    Xs, Ys = np.meshgrid(xs,ys)
    Zsmax = Xs*0 + hmax
    Zsmin = Xs*0 + hmin
    ax.plot_surface(Xs,Ys,Zsmax, color = "r", label = "Hmax")
    ax.plot_surface(Xs,Ys,Zsmin, color = "g", label = "Hmin")
    ax.plot(basex,basey,0)
    np.insert(x,0,home.lat)
    np.insert(y,0,home.lon)
    np.insert(z,0,hmax)
    np.insert(x,0,home.lat)
    np.insert(y,0,home.lon)
    np.insert(z,0,0)
    np.append(x,x[-1])
    np.append(y,y[-1])
    np.append(z,hmax)
    np.append(x,home.lat)
    np.append(y,home.lon)
    np.append(z,hmax)
    np.append(x,home.lat)
    np.append(y,home.lon)
    np.append(z,0)
    ax.set(xlabel = "Latitude", ylabel = "Longitude", zlabel = "Height")
    ax.plot(x, y, z)
    #ax.legend()
    set_axes_equal(ax,hmax)
    plt.show()