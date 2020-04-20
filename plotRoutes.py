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
    xT = []
    yT = []
    zT = []
    xT.extend(x)
    yT.extend(y)
    zT.extend(z)
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
    ax.plot(basex,basey,hmax,color = "b", label = "Hmax")
    xs = np.linspace(min(cc1[0],cc2[0],cc3[0],cc4[0]),max(cc1[0],cc2[0],cc3[0],cc4[0]),2)
    ys = np.linspace(min(cc1[1],cc2[1],cc3[1],cc4[1]),max(cc1[1],cc2[1],cc3[1],cc4[1]),2)
    Xs, Ys = np.meshgrid(xs,ys)
    Zsmin = Xs*0 + hmin
    surf = ax.plot_surface(Xs,Ys,Zsmin, color = "g", label = "Hmin", linewidth = 0, rstride = 10, cstride = 10)
    surf._facecolors2d = surf._facecolors3d
    surf._edgecolors2d = surf._edgecolors3d
    ax.plot(basex,basey,0)
    xT.insert(0,home.lat)
    yT.insert(0,home.lon)
    zT.insert(0,hmax)
    xT.insert(0,home.lat)
    yT.insert(0,home.lon)
    zT.insert(0,0)
    xT.append(x[-1])
    yT.append(y[-1])
    zT.append(hmax)
    xT.append(home.lat)
    yT.append(home.lon)
    zT.append(hmax)
    xT.append(home.lat)
    yT.append(home.lon)
    zT.append(0)
    ax.set(xlabel = "Latitude", ylabel = "Longitude", zlabel = "Height")
    ax.plot(xT, yT, zT)
    ax.legend()
    set_axes_equal(ax,hmax)
    plt.show()

def plotPreviewSimpleFacade(x,y,z,wall,n,home):
    fig = plt.figure(n)
    ax = fig.gca(projection='3d')
    #mpl.rcParams['legend.fontsize'] = 10
    cc1 = wall.c1
    cc2 = wall.c2
    hmax = wall.hmax
    hmin = wall.hmin
    xT = []
    yT = []
    zT = []
    xT.extend(x)
    yT.extend(y)
    zT.extend(z)
    ax.scatter(cc1[0],cc1[1],hmax, color = "b")
    ax.scatter(cc2[0],cc2[1],hmax, color = "b")
    ax.scatter(cc1[0],cc1[1],0, color = "b")
    ax.scatter(cc2[0],cc2[1],0, color = "b")
    ax.scatter(home.lat,home.lon,color = "r", label = "Home")
    i = 0
    ccs = [cc1,cc2]
    while i < 2:
        cc = ccs[i]
        linex = [cc[0],cc[0]]
        liney = [cc[1],cc[1]]
        linez = [0,hmax]
        ax.plot(linex,liney,linez)
        i = i + 1
    basex = [cc1[0],cc2[0]]
    basey = [cc1[1],cc2[1]]
    ax.plot(basex,basey,hmax,color = "b",label = "Hmax")
    ax.plot(basex,basey,0,color = "c")
    ax.plot(basex,basey,hmin,color = "g",label = "Hmin")
    xT.insert(0,home.lat)
    yT.insert(0,home.lon)
    zT.insert(0,hmax)
    xT.insert(0,home.lat)
    yT.insert(0,home.lon)
    zT.insert(0,0)
    xT.append(x[-1])
    yT.append(y[-1])
    zT.append(hmax)
    xT.append(home.lat)
    yT.append(home.lon)
    zT.append(hmax)
    xT.append(home.lat)
    yT.append(home.lon)
    zT.append(0)
    ax.set(xlabel = "Latitude", ylabel = "Longitude", zlabel = "Height")
    ax.plot(xT, yT, zT)
    ax.legend()
    set_axes_equal(ax,hmax)
    plt.show()

def plotPreviewMultiFacade(x,y,z,walls,n,home):
    fig = plt.figure(n)
    ax = fig.gca(projection='3d')
    #mpl.rcParams['legend.fontsize'] = 10
    xT = []
    yT = []
    zT = []
    xT.extend(x)
    yT.extend(y)
    zT.extend(z)
    i = 0
    basex = []
    basey = []
    hmax = walls[0].hmax
    hmin = walls[0].hmin
    while i < len(walls):
        cc1 = walls[i].c1
        cc2 = walls[i].c2
        ax.scatter(cc1[0],cc1[1],hmax, color = "b")
        ax.scatter(cc2[0],cc2[1],hmax, color = "b")
        ax.scatter(cc1[0],cc1[1],0, color = "b")
        ax.scatter(cc2[0],cc2[1],0, color = "b")
        basex.append(cc1[0])
        basey.append(cc1[1])
        i = i + 1
        if (i == len(walls)):
            basex.append(cc2[0])
            basey.append(cc2[1])
    
    ax.plot(basex,basey,hmax, color = "b")
    ax.plot(basex,basey,hmin, color = "b")

    ax.scatter(home.lat,home.lon,color = "r", label = "Home")
    i = 0
    while i < len(walls):
        cc = walls[i].c1
        linex = [cc[0],cc[0]]
        liney = [cc[1],cc[1]]
        linez = [0,hmax]
        ax.plot(linex,liney,linez)
        i = i + 1

    xT.insert(0,home.lat)
    yT.insert(0,home.lon)
    zT.insert(0,hmax)
    xT.insert(0,home.lat)
    yT.insert(0,home.lon)
    zT.insert(0,0)
    xT.append(x[-1])
    yT.append(y[-1])
    zT.append(hmax)
    xT.append(home.lat)
    yT.append(home.lon)
    zT.append(hmax)
    xT.append(home.lat)
    yT.append(home.lon)
    zT.append(0)
    ax.set(xlabel = "Latitude", ylabel = "Longitude", zlabel = "Height")
    ax.plot(xT, yT, zT)
    ax.legend()
    set_axes_equal(ax,hmax)
    plt.show()