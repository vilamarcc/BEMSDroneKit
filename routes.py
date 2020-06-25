import numpy as np
from haversine import getDistanceBetweenCoordinates, getBearingBetweenCoordinates, fromXYtoLatLong, getLocationAtBearing
import math

class perimeter:
    def __init__ (self, cc1, cc2, cc3, cc4, hma, hmi): # ccn = corners of perimeter [lat,lon]
        self.c1 = cc1
        self.c2 = cc2
        self.c3 = cc3
        self.c4 = cc4
        self.ccn = [cc1,cc2,cc3,cc4]
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
    def getPOIs(self):
        POIs = np.linspace(0,0,len(self.ccn))
        i = 0
        while i < len(self.ccn):
            try:
                POIs[i] = getBearingBetweenCoordinates(self.ccn[i][0],self.ccn[i][1],self.ccn[i+1][0],self.ccn[i+1][1])
            except:
                POIs[i] = getBearingBetweenCoordinates(self.ccn[i][0],self.ccn[i][1],self.ccn[0][0],self.ccn[0][1])
            i = i + 1
        return POIs

class wall:
    def __init__ (self, cc1, cc2, hma, hmi): # ccn = corners of perimeter [lat,lon]
        self.c1 = cc1
        self.c2 = cc2
        self.hmax = hma
        self.hmin = hmi
    def getBearing(self):
        return getBearingBetweenCoordinates(self.c1[0],self.c1[1],self.c2[0],self.c2[1])

class polygon:
    def __init__ (self,cn,hma,hmi):
        self.ccn = cn
        self.hmax = hma
        self.hmin = hmi
        self.C = self.getCenter()
    def getCenter(self):
        i = 0
        latT = 0
        lonT = 0
        while(i < len(self.ccn)):
            latT = latT + self.ccn[i][0]
            lonT = lonT + self.ccn[i][1]
            i = i + 1
        
        cLat = latT/len(self.ccn)
        cLon = lonT/len(self.ccn)

        C = [cLat,cLon]
        return C
    def __lt__(self, other):
        return self.hmax < other.hmax
    
    def getPOIs(self):
        POIs = np.linspace(0,0,len(self.ccn))
        i = 0
        while i < len(self.ccn):
            try:
                POIs[i] = getBearingBetweenCoordinates(self.ccn[i][0],self.ccn[i][1],self.ccn[i+1][0],self.ccn[i+1][1])
            except:
                POIs[i] = getBearingBetweenCoordinates(self.ccn[i][0],self.ccn[i][1],self.ccn[0][0],self.ccn[0][1])
            i = i + 1
        return POIs

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
    n = ((hmax - hmin) / sep)
    c = (hmax - hmin) / (2 * np.pi * n)
    theta = np.linspace(0, np.pi * n * 2 , 150)
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

def getMultiHelix(sep, bufferD, ps): #ps = [Vector with the perimeters class] #bufferH = security distance between helixes
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
        zT.append(hmin)
        wall1 = max(getDistanceBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]), getDistanceBetweenCoordinates(cc3[0],cc3[1],cc4[0],cc4[1]))
        wall2 = max(getDistanceBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1]), getDistanceBetweenCoordinates(cc1[0],cc1[1],cc4[0],cc4[1]))
        a = max(wall1,wall2) / 2
        b = min(wall2,wall1) / 2
        n = ((hmax - hmin) / sep)
        c = (hmax - (hmin) ) / (2 * np.pi * n)
        alpha = np.arctan2(b,a)
        rr = (a*b) / np.sqrt((a**2)*(np.sin(alpha)**2) + (b**2)*(np.cos(alpha)**2))
        rmax = np.sqrt(a**2 + b**2)
        rextra = (rmax - rr) + bufferD
        if(max(wall1, wall2) == wall1):
            brng = (np.pi / 2) - (getBearingBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]) + getBearingBetweenCoordinates(cc4[0],cc4[1],cc3[0],cc3[1])) / 2 
            theta = np.linspace(-brng, -brng + np.pi * n * 2 , 100)
            z = (c * theta) + hmin #altitude in m 
            x = (a + rextra) * np.cos(theta) 
            y = (b + rextra) * np.sin(theta) 
            xprime = x*np.cos(brng) - y*np.sin(brng) + ax #longitude
            yprime = x*np.sin(brng) + y*np.cos(brng) + bx #latitude
        else:
            brng =  - (getBearingBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1]) + getBearingBetweenCoordinates(cc1[0],cc1[1],cc4[0],cc4[1])) / 2
            theta = np.linspace(-brng, -brng + np.pi * n * 2 , 100)
            z = (c * theta) + hmin #altitude in m 
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
    n = round((hmax- hmin)/sep)
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
    isnextconvex = False
    while (i < len(walls)):
        cc1 = walls[i].c1
        cc2 = walls[i].c2
        if(i + 1 >= len(walls)):
            wallpost = walls[0]
        else:
            wallpost = walls[i + 1]
            
        hmax = walls[i].hmax
        hmin = walls[i].hmin
        fix = 2
        brngfix = getBearingBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1])
        if(brngfix < 0):
            brngfix = brngfix + np.pi*2
        if((brngfix > np.pi/4 and brngfix < np.pi*0.75) or (brngfix - np.pi > np.pi/4 and brngfix - np.pi < np.pi*0.75)):
            fix = 1
        brng = getBearingBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1])
        [pLat1,pLon1] = getLocationAtBearing(cc1[0],cc1[1],bufferD*fix, brng + ori*(np.pi) / 2)
        [pLat2,pLon2] = getLocationAtBearing(cc2[0],cc2[1],bufferD*fix, brng + ori*(np.pi) / 2)
        if(isnextconvex == True):
            [pLat1,pLon1] = getLocationAtBearing(pLat1,pLon1,bufferD, brng)
            isnextconvex = False
        if(ori == 1):
            if(convex(walls[i],wallpost) == True and wallpost != 0):
                [pLat2,pLon2] = getLocationAtBearing(pLat2,pLon2, bufferD*fix, brng - np.pi)
                isnextconvex = True
        if(ori == -1):
            if(convex(walls[i],wallpost) == False and wallpost != 0):
                if(i != 0):
                    [pLat2,pLon2] = getLocationAtBearing(pLat2,pLon2, bufferD, brng - np.pi)
                    isnextconvex = True
                else:
                    [pLat1,pLon1] = getLocationAtBearing(pLat1,pLon1,bufferD, brng)
                    [pLat2,pLon2] = getLocationAtBearing(pLat2,pLon2, bufferD, brng - np.pi)
                    isnextconvex = True
        
        n = round((hmax - hmin)/sep)
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
    fix1,fix2 = 1,1
    brngfix = brng1
    if(brngfix < 0):
        brngfix = brngfix + np.pi*2
    if(brngfix > np.pi/2 and brngfix < np.pi*1.5):
        fix1 = 2
    else:
        fix2 = 2
    [pLat2,pLon2] = getLocationAtBearing(cc2[0],cc2[1],bufferD*fix2, brng1)
    [pLat3,pLon3] = getLocationAtBearing(cc3[0],cc3[1],bufferD*fix1, brng2)
    [pLat4,pLon4] = getLocationAtBearing(cc4[0],cc4[1],bufferD*fix2, brng3)
    [pLat1,pLon1] = getLocationAtBearing(cc1[0],cc1[1],bufferD*fix1, brng4)
    [pLat22,pLon22] = getLocationAtBearing(cc2[0],cc2[1],bufferD*fix1, brng2 + np.pi)
    [pLat33,pLon33] = getLocationAtBearing(cc3[0],cc3[1],bufferD*fix2, brng3 + np.pi)
    [pLat44,pLon44] = getLocationAtBearing(cc4[0],cc4[1],bufferD*fix1, brng4 + np.pi)
    [pLat11,pLon11] = getLocationAtBearing(cc1[0],cc1[1],bufferD*fix2, brng1 + np.pi)
    n = round((hmax - hmin)/sep) + 1
    x = np.tile([pLat11,pLat1,pLat22,pLat2,pLat33,pLat3,pLat44,pLat4,pLat11],n)
    y = np.tile([pLon11,pLon1,pLon22,pLon2,pLon33,pLon3,pLon44,pLon4,pLon11],n)
    z = np.linspace(0,hmax,len(x))
    i = 0
    h = 0
    while i < len(x):
        z[i] = hmax - sep*h
        z[i + 1] = hmax - sep*h
        z[i + 2] = hmax - sep*h
        z[i + 3] = hmax - sep*h
        z[i + 4] = hmax - sep*h
        z[i + 5] = hmax - sep*h
        z[i + 6] = hmax - sep*h
        z[i + 7] = hmax - sep*h
        z[i + 8] = hmax - sep*h
        if(hmax - sep*h < hmin):
            z[i] = hmin
            z[i + 1] = hmin
            z[i + 2] = hmin
            z[i + 3] = hmin
            z[i + 4] = hmin
            z[i + 5] = hmin
            z[i + 6] = hmin
            z[i + 7] = hmin
            z[i + 8] = hmin
        i = i + 9
        h = h + 1
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

def getElipse(sep,bufferD,perimeter):
    cc1 = perimeter.c1 
    cc2 = perimeter.c2
    cc3 = perimeter.c3
    cc4 = perimeter.c4
    xT = []
    yT = []
    hmax = perimeter.hmax
    hmin = perimeter.hmin
    wall1 = max(getDistanceBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]), getDistanceBetweenCoordinates(cc3[0],cc3[1],cc4[0],cc4[1]))
    wall2 = max(getDistanceBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1]), getDistanceBetweenCoordinates(cc1[0],cc1[1],cc4[0],cc4[1]))
    a = max(wall1,wall2) / 2
    b = min(wall2,wall1) / 2
    n = round((hmax - hmin) / sep)
    theta = np.linspace(0, np.pi * 2 , 25)
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
        xT.extend(xprime)
        yT.extend(yprime)
    else:
        brng =  - (getBearingBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1]) + getBearingBetweenCoordinates(cc1[0],cc1[1],cc4[0],cc4[1])) / 2
        y = (a + rextra) * np.cos(theta) 
        x = (b + rextra) * np.sin(theta)
        xprime = x*np.cos(brng) - y*np.sin(brng)
        yprime = x*np.sin(brng) + y*np.cos(brng)
        xT.extend(xprime)
        yT.extend(yprime)
    
    z = np.zeros(len(xprime)*(n+ 1))
    i = 0
    h = 0
    while i < len(z):
        if(i == (h+1)*25):
            xT.extend(xprime)
            yT.extend(yprime)
            h = h + 1
        if(hmax - sep*h < hmin):
            z[i] = hmin
        z[i] = hmax - sep*h
        i = i + 1

    return xT,yT,z

def getMultiElipse(sep,bufferD,ps):
    ps.sort()
    xT = []
    yT = []
    zT = [] 
    i = 1
    Center = ps[0].C
    #We calculate the first helix of the lowest perimeter
    xp1,yp1,zp1 = getElipse(sep,bufferD,ps[0])
    xT.extend(xp1)
    yT.extend(yp1)
    zT.extend(zp1[::-1])
    while(i < len(ps)):

        xT.append(xT[-1])
        yT.append(yT[-1])
        xL = []
        yL = []
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
        zT.append(hmin)
        wall1 = max(getDistanceBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]), getDistanceBetweenCoordinates(cc3[0],cc3[1],cc4[0],cc4[1]))
        wall2 = max(getDistanceBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1]), getDistanceBetweenCoordinates(cc1[0],cc1[1],cc4[0],cc4[1]))
        a = max(wall1,wall2) / 2
        b = min(wall2,wall1) / 2
        n = round((hmax - hmin) / sep)
        alpha = np.arctan2(b,a)
        rr = (a*b) / np.sqrt((a**2)*(np.sin(alpha)**2) + (b**2)*(np.cos(alpha)**2))
        rmax = np.sqrt(a**2 + b**2)
        rextra = (rmax - rr) + bufferD
        if(max(wall1, wall2) == wall1):
            brng = (np.pi / 2) - (getBearingBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]) + getBearingBetweenCoordinates(cc4[0],cc4[1],cc3[0],cc3[1])) / 2 
            theta = np.linspace(-brng, -brng + np.pi * 2 , 25)
            x = (a + rextra) * np.cos(theta) 
            y = (b + rextra) * np.sin(theta) 
            xprime = x*np.cos(brng) - y*np.sin(brng) + ax #longitude
            yprime = x*np.sin(brng) + y*np.cos(brng) + bx #latitude
        else:
            brng =  - (getBearingBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1]) + getBearingBetweenCoordinates(cc1[0],cc1[1],cc4[0],cc4[1])) / 2
            theta = np.linspace(-brng, -brng + np.pi * 2 , 25)
            y = (a + rextra) * np.cos(theta) 
            x = (b + rextra) * np.sin(theta)
            xprime = x*np.cos(brng) - y*np.sin(brng) - ax #latitude
            yprime = x*np.sin(brng) + y*np.cos(brng) + bx #longitude
        
        z = np.zeros(len(xprime)*(n + 1))
        j = 0
        h = 0
        xL.extend(xprime)
        yL.extend(yprime)
        while j < len(z):
            if(j == (h+1)*25):
                xL.extend(xprime)
                yL.extend(yprime)
                h = h + 1
            if(hmax - sep*h < hmin):
                z[j] = hmin
            z[j] = hmax - sep*h
            j = j + 1
        
        xT.extend(xL)
        yT.extend(yL)
        zT.extend(z[::-1])

        i = i + 1

    return xT,yT,zT

def getPolySquare(sep,bufferD,poly):

    i = 0
    Lats = []
    Lons = []
    z = []
    hmax = poly.hmax
    hmin = poly.hmin
    n = round((hmax-hmin)/sep) + 1
    while i < len(poly.ccn):
        cc0 = poly.ccn[i]
        if(i + 1 >= len(poly.ccn)):
            ccpost = poly.ccn[0]
        else:
            ccpost = poly.ccn[i + 1]
        if(i - 1 < 0):
            ccpre = poly.ccn[-1]
        else:
            ccpre = poly.ccn[i - 1]

        brngpre = getBearingBetweenCoordinates(ccpre[0],ccpre[1],cc0[0],cc0[1])
        brngpost = getBearingBetweenCoordinates(ccpost[0],ccpost[1],cc0[0],cc0[1])
        brngav = (brngpre + brngpost)/2
        fix1,fix2 = 1,1
        bfix = brngpost + np.pi
        if(bfix < 0):
            bfix = bfix + np.pi*2
        if((bfix > np.pi/4 and bfix < np.pi*0.75) or (bfix - np.pi > np.pi/4 and bfix - np.pi < np.pi*0.75 )):
            fix1 = 2
        else:
            fix2 = 2

        [pLatn,pLonn] = getLocationAtBearing(cc0[0],cc0[1],bufferD*fix2, brngpre)
        [cLatn,cLonn] = getLocationAtBearing(cc0[0],cc0[1],bufferD*fix1, brngpost)

        w1 = wall(ccpre,cc0,0,0)
        w2 = wall(cc0,ccpost,0,0)

        if(convex(w1,w2) == True):
            [cLatn,cLonn] = getLocationAtBearing(cc0[0],cc0[1],bufferD*2, brngav + np.pi)
            Lats.append(cLatn)
            Lons.append(cLonn)
        else:
            Lats.append(cLatn)
            Lons.append(cLonn)
            Lats.append(pLatn)
            Lons.append(pLonn)

        i = i + 1
    
    Lats.append(Lats[0])
    Lons.append(Lons[0])

    x = np.tile(Lats,n)
    y = np.tile(Lons,n)
    z = np.linspace(0,0,len(x))

    j = 0
    h = 0
    cornercount = len(poly.ccn) + 1
    while (j < len(z)):
        if(hmax - sep*h >= hmin):
            z[j:cornercount*(h + 1)] = hmax - sep*h
        else:
            z[j:cornercount*(h + 1)] = hmin
        h = h + 1
        j = j + cornercount
    
    return x,y,z

def getMultiPolySquare(sep,bufferD,polys):
    polys.sort()
    xT = []
    yT = []
    zT = []
    i = 0
    if(len(polys) > 1):
        hTrans = (-polys[0].hmax + polys[1].hmin)
    else:
        hTrans = 0
    while i < len(polys):
        xp,yp,zp = getPolySquare(sep,bufferD,polys[i])
        xp = xp[::-1]
        yp = yp[::-1]
        zp = zp[::-1]
        xT.extend(xp)
        yT.extend(yp)
        zT.extend(zp)
        if i < len(polys) - 1:
            xT.append(xp[-1])
            yT.append(yp[-1])
            zT.append(zT[-1] + hTrans)
            hTrans = polys[i + 1].hmin - polys[i].hmax
        
        i = i + 1

    return xT,yT,zT    

def checkIfInsidePoly(P,poly):
    lat = P[0]
    lon = P[1]
    n = len(poly.ccn)
    inside = False

    p1x,p1y = poly.ccn[0]
    for i in range(n+1):
        p2x,p2y = poly.ccn[i % n]
        if lon > min(p1y,p2y):
            if lon <= max(p1y,p2y):
                if lat <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (lon-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or lat <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def convex(w1,w2):
    if(w2 == 0):
        return False
    [x1,y1] = w1.c1
    [x2,y2] = w1.c2
    [x3,y3] = w2.c2

    def area(x1,y1,x2,y2,x3,y3):

        areaSum = 0

        areaSum = areaSum + x1 * (y3 - y2)
        areaSum = areaSum + x2 * (y1 - y3)
        areaSum = areaSum + x3 * (y2 - y1)
        return areaSum

    if (area(x1, y1, x2, y2, x3, y3) < 0):
        return True
    else:
        return False