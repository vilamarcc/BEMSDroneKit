import numpy as np
from haversine import getDistanceBetweenCoordinates, getBearingBetweenCoordinates, fromXYtoLatLong


def getHelix(hmax, sep, bufferD, cc1, cc2, cc3, cc4): ##ccn = corners of perimeter [lat,lon]

    wall1 = max(getDistanceBetweenCoordinates(cc1[0],cc1[1],cc2[0],cc2[1]), getDistanceBetweenCoordinates(cc3[0],cc3[1],cc4[0],cc4[1]))
    wall2 = max(getDistanceBetweenCoordinates(cc2[0],cc2[1],cc3[0],cc3[1]), getDistanceBetweenCoordinates(cc1[0],cc1[1],cc4[0],cc4[1]))
    a = max(wall1,wall2) / 2
    b = min(wall2,wall1) / 2
    n = (hmax / sep)
    c = hmax / (2 * np.pi * n) 
    theta = np.linspace(0, np.pi * n * 2 , 300)
    z = c * theta #altitude in m
    alpha = np.arctan2(b,a)
    brng = (((getBearingBetweenCoordinates(cc2[0],cc2[1],cc1[0],cc1[1])) + getBearingBetweenCoordinates(cc3[0],cc3[1],cc4[0],cc4[1])) / 2) - np.pi
    rr = (a*b) / np.sqrt((a**2)*(np.sin(alpha)**2) + (b**2)*(np.cos(alpha)**2))
    rmax = np.sqrt(a**2 + b**2)
    rextra = (rmax - rr) + bufferD
    if(max(wall1, wall2) == wall1):
        x = (a + rextra) * np.cos(theta) 
        y = (b + rextra) * np.sin(theta) 
        yprime = x*np.cos(brng) - y*np.sin(brng)
        xprime = x*np.sin(brng) + y*np.cos(brng)
    else:
        y = (a + rextra) * np.cos(theta) 
        x = (b + rextra) * np.sin(theta)
        xprime = x*np.cos(brng) - y*np.sin(brng)
        yprime = x*np.sin(brng) + y*np.cos(brng)

    return xprime,yprime,z

def getCenterofPerimeter(cc1, cc2, cc3, cc4): 
    cLat = round((cc1[0] + cc2[0] + cc3[0] + cc4[0]) / 4 , 7)
    cLon = round((cc1[1] + cc2[1] + cc3[1] + cc4[1]) / 4 , 7)
    C = [cLat,cLon]

    return C

def getHelixinCoords(x,y,z,C):
    i = 0
    while i < len(x):
        [Lat,Lon] = fromXYtoLatLong(x[i],y[i],C[0],C[1])
        x[i] = round(Lat,7)
        y[i] = round(Lon,7)
        i = i + 1

    return x,y,z
        
