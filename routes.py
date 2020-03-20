import numpy as np
from haversine import getDistanceBetweenCoordinates, getBearingBetweenCoordinates, fromXYtoLatLong, getLocationAtBearing
import math

class perimeter:
    def __init__ (self, cc1, cc2, cc3, cc4, hma, hmi): # ccn = corners of perimeter [lat,lon]
        self.c1 = cc1
        self.c2 = cc2
        self.c3 = cc3
        self.c4 = cc4
        self.hmax = hma
        self.hmin = hmi
        self.C = self.getCenter()
    def getCenter(self):
        cLat = round((self.c1[0] + self.c2[0] + self.c3[0] + self.c4[0]) / 4 , 7)
        cLon = round((self.c1[1] + self.c2[1] + self.c3[1] + self.c4[1]) / 4 , 7)
        C = [cLat,cLon]
        return C
    def __lt__(self, other):
        return self.hmax < other.hmax

class wall:
    def __init__ (self, cc1, cc2, hma, hmi): # ccn = corners of perimeter [lat,lon]
        self.c1 = cc1
        self.c2 = cc2
        self.hmax = hma
        self.hmin = hmi

def getHelix(sep, bufferD, perimeter, hmin): 

    cc1 = perimeter.c1 
    cc2 = perimeter.c2
    cc3 = perimeter.c3
    cc4 = perimeter.c4
    hmax = perimeter.hmax
    wall1 = max(getDistanceBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]), getDistanceBetweenCoordinates(cc3[0],cc3[1],cc4[0],cc4[1]))
    wall2 = max(getDistanceBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1]), getDistanceBetweenCoordinates(cc1[0],cc1[1],cc4[0],cc4[1]))
    a = max(wall1,wall2) / 2
    b = min(wall2,wall1) / 2
    n = (hmax / sep)
    c = (hmax - hmin) / (2 * np.pi * n)
    theta = np.linspace(0, np.pi * n * 2 , 200)
    z = (c * theta) + hmin #altitude in m 
    alpha = np.arctan2(b,a)
    rr = (a*b) / np.sqrt((a**2)*(np.sin(alpha)**2) + (b**2)*(np.cos(alpha)**2))
    rmax = np.sqrt(a**2 + b**2)
    rextra = (rmax - rr) + bufferD
    if(max(wall1, wall2) == wall1):
        brng = getBearingBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]) - np.pi
        x = (a + rextra) * np.cos(theta) 
        y = (b + rextra) * np.sin(theta) 
        yprime = x*np.cos(brng) - y*np.sin(brng)
        xprime = x*np.sin(brng) + y*np.cos(brng)
    else:
        brng = getBearingBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1]) - np.pi
        y = (a + rextra) * np.cos(theta) 
        x = (b + rextra) * np.sin(theta)
        xprime = x*np.cos(brng) - y*np.sin(brng)
        yprime = x*np.sin(brng) + y*np.cos(brng)

    return xprime,yprime,z,theta

def getMultiHelix(hmin, sep, bufferD, ps): #ps = [Vector with the perimeters class]
    ps.sort()
    xT = []
    yT = []
    zT = [] 
    tT = []
    i = 1
    Center = ps[0].C
    #We calculate the first helix of the lowest perimeter
    xp1,yp1,zp1,tp1 = getHelix(sep,bufferD,ps[0],hmin)
    xT.extend(xp1)
    yT.extend(yp1)
    zT.extend(zp1)
    tT.extend(tp1)
    while(i < len(ps)):
        cc1 = ps[i].c1 
        cc2 = ps[i].c2
        cc3 = ps[i].c3
        cc4 = ps[i].c4
        dc = getDistanceBetweenCoordinates(Center[0],Center[1],ps[i].C[0],ps[i].C[1])
        brngC = np.pi - getBearingBetweenCoordinates(Center[0],Center[1],ps[i].C[0],ps[i].C[1])
        ax = np.sqrt((dc**2)/((np.tan(brngC))+ 1))
        bx = ax * np.tan(brngC)
        hmax = ps[i].hmax
        hmin = ps[i].hmin
        wall1 = max(getDistanceBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]), getDistanceBetweenCoordinates(cc3[0],cc3[1],cc4[0],cc4[1]))
        wall2 = max(getDistanceBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1]), getDistanceBetweenCoordinates(cc1[0],cc1[1],cc4[0],cc4[1]))
        a = max(wall1,wall2) / 2
        b = min(wall2,wall1) / 2
        n = ((hmax - ps[i - 1].hmax) / sep)
        c = (hmax - hmin) / (2 * np.pi * n)
        theta = np.linspace(tT[-1], tT[-1] + np.pi * n * 2 , 200)
        z = (c * theta) #altitude in m 
        alpha = np.arctan2(b,a)
        rr = (a*b) / np.sqrt((a**2)*(np.sin(alpha)**2) + (b**2)*(np.cos(alpha)**2))
        rmax = np.sqrt(a**2 + b**2)
        rextra = (rmax - rr) + bufferD
        if(max(wall1, wall2) == wall1):
            brng = getBearingBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]) - np.pi
            x = (a + rextra) * np.cos(theta) 
            y = (b + rextra) * np.sin(theta) 
            yprime = x*np.cos(brng) - y*np.sin(brng) - bx
            xprime = x*np.sin(brng) + y*np.cos(brng) + ax
        else:
            brng = getBearingBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1]) - np.pi
            y = (a + rextra) * np.cos(theta) 
            x = (b + rextra) * np.sin(theta)
            xprime = x*np.cos(brng) - y*np.sin(brng) - bx
            yprime = x*np.sin(brng) + y*np.cos(brng) + ax
        
        xT.extend(xprime)
        yT.extend(yprime)
        zT.extend(z)
        tT.extend(tp1)
        i = i + 1

    return xT,yT,zT,tT

def getHelixinCoords(x,y,z,C): #C = Center of perimeter
    i = 0
    while i < len(x):
        [Lat,Lon] = fromXYtoLatLong(x[i],y[i],C[0],C[1])
        x[i] = round(Lat,7)
        y[i] = round(Lon,7)
        i = i + 1

    return x,y,z

def getFacade(sep, bufferD, wall, ori): #ori = Orientation of the wall towards outside
    cc1 = wall.c1
    cc2 = wall.c2
    hmax = wall.hmax
    brng = getBearingBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]) + ori*np.pi / 2
    [pLat1,pLon1] = getLocationAtBearing(cc1[0],cc1[1],bufferD, brng)
    [pLat2,pLon2] = getLocationAtBearing(cc2[0],cc2[1],bufferD, brng)
    n = round(hmax/sep)
    x = np.tile([pLat1,pLat2,pLat2,pLat1],math.ceil(n/2))
    y = np.tile([pLon1,pLon2,pLon2,pLon1],math.ceil(n/2))
    z = np.linspace(0,hmax,len(x))
    i = 0
    h = 0
    while i < len(x):
        z[i] = hmax - sep*h
        z[i + 1] = hmax - sep*h
        i = i + 2
        h = h + 1
    return x,y,z

def getMultiFacade(sep, bufferD, walls, ori): #ori = [-1, 1], 1 = Outside facade, -1 Inside facade
    i = 0
    xT = []
    yT = []
    zT = []
    while (i < len(walls)):
        cc1 = walls[i].c1
        cc2 = walls[i].c2
        hmax = walls[i].hmax
        hmin = walls[i].hmin
        brng = getBearingBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]) + (ori*np.pi) / 2
        [pLat1,pLon1] = getLocationAtBearing(cc1[0],cc1[1],bufferD, brng)
        [pLat2,pLon2] = getLocationAtBearing(cc2[0],cc2[1],bufferD, brng)
        n = round(hmax/sep)
        if (i + 1) % 2 == 0:
            x = np.tile([pLat1,pLat2,pLat2,pLat1],math.ceil(n/2))
            y = np.tile([pLon1,pLon2,pLon2,pLon1],math.ceil(n/2))
            z = np.linspace(0,hmax,len(x))
            j = len(x) - 1
            h = 0
            while j > 0:
                z[j] = hmin + sep*h
                z[j - 1] = hmin + sep*h
                if(hmin + sep*h > hmax):
                    z[j] = hmax
                    z[j - 1] = hmax
                j = j - 2
                h = h + 1
            z = z[::-1]
            x = np.append(x,x[-2])
            y = np.append(y,y[-2])
            z = np.append(z,hmax)
        else:
            x = np.tile([pLat1,pLat2,pLat2,pLat1],math.ceil(n/2))
            y = np.tile([pLon1,pLon2,pLon2,pLon1],math.ceil(n/2))
            z = np.linspace(0,hmax,len(x))
            j = 0
            h = 0
            while j < len(x):
                z[j] = hmax - sep*h
                z[j + 1] = hmax - sep*h
                if(hmax - sep*h < hmin):
                    z[j] = hmin
                    z[j + 1] = hmin
                j = j + 2
                h = h + 1
            
            x = np.append(x,x[-2])
            y = np.append(y,y[-2])
            z = np.append(z,hmin)

        xT.extend(x)
        yT.extend(y)
        zT.extend(z)
            
        i = i + 1

    return xT,yT,zT