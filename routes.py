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
    def getBearing(self):
        return getBearingBetweenCoordinates(self.c1[0],self.c1[1],self.c2[0],self.c2[1])

def getHelix(sep, bufferD, perimeter): 

    cc1 = perimeter.c1 
    cc2 = perimeter.c2
    cc3 = perimeter.c3
    cc4 = perimeter.c4
    hmax = perimeter.hmax
    hmin = perimeter.hmin
    wall1 = max(getDistanceBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]), getDistanceBetweenCoordinates(cc3[0],cc3[1],cc4[0],cc4[1]))
    wall2 = max(getDistanceBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1]), getDistanceBetweenCoordinates(cc1[0],cc1[1],cc4[0],cc4[1]))
    a = max(wall1,wall2) / 2
    b = min(wall2,wall1) / 2
    n = (hmax / sep)
    c = (hmax - hmin) / (2 * np.pi * n)
    theta = np.linspace(0, np.pi * n * 2 , 100)
    z = (c * theta) + hmin #altitude in m 
    alpha = np.arctan2(b,a)
    rr = (a*b) / np.sqrt((a**2)*(np.sin(alpha)**2) + (b**2)*(np.cos(alpha)**2))
    rmax = np.sqrt(a**2 + b**2)
    rextra = (rmax - rr) + bufferD
    if(max(wall1, wall2) == wall1):
        brng = (np.pi / 2) - (getBearingBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]) + getBearingBetweenCoordinates(cc4[0],cc4[1],cc3[0],cc3[1])) / 2 
        x = (a + rextra) * np.cos(theta) 
        y = (b + rextra) * np.sin(theta) 
        xprime = x*np.cos(brng) - y*np.sin(brng)
        yprime = x*np.sin(brng) + y*np.cos(brng)
    else:
        brng =  - (getBearingBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1]) + getBearingBetweenCoordinates(cc1[0],cc1[1],cc4[0],cc4[1])) / 2
        y = (a + rextra) * np.cos(theta) 
        x = (b + rextra) * np.sin(theta)
        xprime = x*np.cos(brng) - y*np.sin(brng)
        yprime = x*np.sin(brng) + y*np.cos(brng)

    return xprime,yprime,z,theta

def getMultiHelix(sep, bufferD, bufferH, ps): #ps = [Vector with the perimeters class] #bufferH = security distance between helixes
    ps.sort()
    xT = []
    yT = []
    zT = [] 
    tT = []
    i = 1
    Center = ps[0].C
    #We calculate the first helix of the lowest perimeter
    xp1,yp1,zp1,tp1 = getHelix(sep,bufferD,ps[0])
    xT.extend(xp1)
    yT.extend(yp1)
    zT.extend(zp1)
    tT.extend(tp1)
    while(i < len(ps)):
        xT.append(xT[-1])
        yT.append(yT[-1])
        zT.append(zT[-1] + bufferH)
        tT.append(tT[-1])
        cc1 = ps[i].c1 
        cc2 = ps[i].c2
        cc3 = ps[i].c3
        cc4 = ps[i].c4
        dc = getDistanceBetweenCoordinates(Center[0],Center[1],ps[i].C[0],ps[i].C[1])
        brngC = getBearingBetweenCoordinates(Center[0],Center[1],ps[i].C[0],ps[i].C[1]) + np.pi / 2
        ax = np.sqrt((dc**2)/((np.tan(brngC))**2 + 1))
        bx = ax * np.tan(brngC)
        hmax = ps[i].hmax
        hmin = ps[i].hmin
        wall1 = max(getDistanceBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]), getDistanceBetweenCoordinates(cc3[0],cc3[1],cc4[0],cc4[1]))
        wall2 = max(getDistanceBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1]), getDistanceBetweenCoordinates(cc1[0],cc1[1],cc4[0],cc4[1]))
        a = max(wall1,wall2) / 2
        b = min(wall2,wall1) / 2
        n = ((hmax - ps[i - 1].hmax) / sep)
        c = (hmax - (hmin) ) / (2 * np.pi * n)
        alpha = np.arctan2(b,a)
        rr = (a*b) / np.sqrt((a**2)*(np.sin(alpha)**2) + (b**2)*(np.cos(alpha)**2))
        rmax = np.sqrt(a**2 + b**2)
        rextra = (rmax - rr) + bufferD
        if(max(wall1, wall2) == wall1):
            brng = (np.pi / 2) - (getBearingBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]) + getBearingBetweenCoordinates(cc4[0],cc4[1],cc3[0],cc3[1])) / 2 
            theta = np.linspace(-brng, -brng + np.pi * n * 2 , 100)
            z = (c * theta) + hmin + bufferH #altitude in m 
            x = (a + rextra) * np.cos(theta) 
            y = (b + rextra) * np.sin(theta) 
            xprime = x*np.cos(brng) - y*np.sin(brng) + ax #longitude
            yprime = x*np.sin(brng) + y*np.cos(brng) + bx #latitude
        else:
            brng =  - (getBearingBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1]) + getBearingBetweenCoordinates(cc1[0],cc1[1],cc4[0],cc4[1])) / 2
            theta = np.linspace(-brng, -brng + np.pi * n * 2 , 100)
            z = (c * theta) + hmin + bufferH #altitude in m 
            y = (a + rextra) * np.cos(theta) 
            x = (b + rextra) * np.sin(theta)
            xprime = x*np.cos(brng) - y*np.sin(brng) - ax #latitude
            yprime = x*np.sin(brng) + y*np.cos(brng) + bx #longitude
        
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
    hmin = wall.hmin
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
        if(hmax - sep*h < hmin):
            z[i] = hmin
            z[i + 1] = hmin
        i = i + 2
        h = h + 1
    return x,y,z

def getMultiFacade(sep, bufferD, walls, ori): #ori = [-1, 1], 1 = Outside facade, -1 Inside facade
    i = 0
    xT = []
    yT = []
    zT = []
    if(ori == 1):
        while (i < len(walls)):
            cc1 = walls[i].c1
            cc2 = walls[i].c2
            hmax = walls[i].hmax
            hmin = walls[i].hmin
            brng = getBearingBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]) + (np.pi) / 2
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
    if(ori == -1):
         while (i < len(walls)):
            cc1 = walls[i].c1
            cc2 = walls[i].c2
            hmax = walls[i].hmax
            hmin = walls[i].hmin
            brngprime1 = getBearingBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1])
            brngprime2 = getBearingBetweenCoordinates(cc2[0],cc2[1],cc1[0],cc1[1])
            Lat1p,Lon1p = getLocationAtBearing(cc1[0],cc1[1],bufferD/2,brngprime1)
            Lat2p,Lon2p = getLocationAtBearing(cc2[0],cc2[1],bufferD/2,brngprime2)
            brng = getBearingBetweenCoordinates(Lat1p,Lon1p,Lat2p,Lon2p) - (np.pi) / 2
            [pLat1,pLon1] = getLocationAtBearing(Lat1p,Lon1p,bufferD, brng)
            [pLat2,pLon2] = getLocationAtBearing(Lat2p,Lon2p,bufferD, brng)
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
    if(ori != 1 and ori != -1):
        return 0,0,0

    return xT,yT,zT

def getSquare(sep, bufferD, perimeter):
    cc1 = perimeter.c1 
    cc2 = perimeter.c2
    cc3 = perimeter.c3
    cc4 = perimeter.c4
    hmax = perimeter.hmax
    hmin = perimeter.hmin
    brng1 = getBearingBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1])
    brng2 = getBearingBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1])
    brng3 = getBearingBetweenCoordinates(cc3[0],cc3[1],cc4[0],cc4[1])
    brng4 = getBearingBetweenCoordinates(cc4[0],cc4[1],cc1[0],cc1[1])
    [pLat2,pLon2] = getLocationAtBearing(cc2[0],cc2[1],bufferD, brng1)
    [pLat3,pLon3] = getLocationAtBearing(cc3[0],cc3[1],bufferD*2, brng2)
    [pLat4,pLon4] = getLocationAtBearing(cc4[0],cc4[1],bufferD, brng3)
    [pLat1,pLon1] = getLocationAtBearing(cc1[0],cc1[1],bufferD*2, brng4)
    [pLat22,pLon22] = getLocationAtBearing(cc2[0],cc2[1],bufferD*2, brng2 + np.pi)
    [pLat33,pLon33] = getLocationAtBearing(cc3[0],cc3[1],bufferD, brng3 + np.pi)
    [pLat44,pLon44] = getLocationAtBearing(cc4[0],cc4[1],bufferD*2, brng4 + np.pi)
    [pLat11,pLon11] = getLocationAtBearing(cc1[0],cc1[1],bufferD, brng1 + np.pi)
    [lat2,lon2] = getLocationAtBearing(pLat2,pLon2,bufferD,getBearingBetweenCoordinates(pLat2,pLon2,cc2[0],cc2[1]) - np.pi/2)
    [lat3,lon3] = getLocationAtBearing(pLat3,pLon3,bufferD,getBearingBetweenCoordinates(pLat3,pLon3,cc3[0],cc3[1]) - np.pi/2)
    [lat4,lon4] = getLocationAtBearing(pLat4,pLon4,bufferD,getBearingBetweenCoordinates(pLat4,pLon4,cc4[0],cc4[1]) - np.pi/2)
    [lat1,lon1] = getLocationAtBearing(pLat1,pLon1,bufferD,getBearingBetweenCoordinates(pLat1,pLon1,cc1[0],cc1[1]) - np.pi/2)
    n = round(hmax/sep)
    x = np.tile([lat1,lat2,lat3,lat4,lat1],n)
    y = np.tile([lon1,lon2,lon3,lon4,lon1],n)
    z = np.linspace(0,hmax,len(x))
    i = 0
    h = 0
    while i < len(x):
        z[i] = hmax - sep*h
        z[i + 1] = hmax - sep*h
        z[i + 2] = hmax - sep*h
        z[i + 3] = hmax - sep*h
        z[i + 4] = hmax - sep*h
        if(hmax - sep*h < hmin):
            z[i] = hmin
            z[i + 1] = hmin
            z[i + 2] = hmin
            z[i + 3] = hmin
            z[i + 4] = hmin
        i = i + 5
        h = h + 1
    x = [pLat11,pLat1,pLat22,pLat2,pLat33,pLat3,pLat44,pLat4]
    y = [pLon11,pLon1,pLon22,pLon2,pLon33,pLon3,pLon44,pLon4]
    z = [hmax,hmax,hmax,hmax,hmax,hmax,hmax,hmax]
    return x,y,z

def getMultiSquare(sep, bufferD, ps):
    ps.sort()
    xT = []
    yT = []
    zT = []
    i = 0
    hTrans = (-ps[0].hmax + ps[1].hmin)
    while i < len(ps):
        xp,yp,zp = getSquare(sep,bufferD,ps[i])
        xp = xp[::-1]
        yp = yp[::-1]
        zp = zp[::-1]
        xT.extend(xp)
        yT.extend(yp)
        zT.extend(zp)
        if i < len(ps) - 1:
            xT.append(xp[-1])
            yT.append(yp[-1])
            zT.append(zT[-1] + hTrans)
            hTrans = ps[i + 1].hmin - ps[i].hmax
        i = i + 1
    return xT,yT,zT