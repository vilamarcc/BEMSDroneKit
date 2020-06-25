from dronekit import *
import math
from routes import getMultiHelix, getMultiFacade, getHelix, getFacade, getHelixinCoords,getSquare,getElipse,getMultiElipse,getMultiSquare
import numpy as np


def writeSimpleHelixMission(sep, bufferD, perimeter, filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    x,y,z,theta = getHelix(sep, bufferD, perimeter)
    C = perimeter.C
    xf,yf,zf = getHelixinCoords(x,y,z,C)
    xf = xf[::-1]
    yf = yf[::-1]
    zf = zf[::-1]
    file.write("1 0 3 22 0 0 0 0 0 0 " + str(round(zf[0],2)) + " " + "1\n")
    file.write("2 0 3 201 0 0 0 0 " + str(perimeter.C[0]) + " " + str(perimeter.C[1]) + " " + str(perimeter.hmax) + " 1\n")
    i = 0
    j = 0
    while (j < len(xf)):
        file.write(str(i + 3) +  " 0 3 82 0 0 0 0 " + str(xf[j]) + " " + str(yf[j]) + " " + str(round(zf[j],2)) + " " + "1\n")
        file.write(str(i + 4) +  " 0 3 201 0 0 0 0 " + str(perimeter.C[0]) + " " + str(perimeter.C[1]) + " " + str(round(zf[j],2)) + " " + "1\n")
        i = i + 2
        j = j + 1
    
    file.write(str(i + 3) +" 0 3 201 0 0 0 0 0 0 0 1\n")
    file.write(str(i + 4) + " 0 3 16 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(zf[0],2)) + " " + "1\n")
    file.write(str(i + 5) + " 0 3 20 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(zf[0],2)) + " " + "1\n")
    file.write(str(i + 6) + " 0 3 21 0 0 0 0 0 0 0 1\n")
    file.close()
    return xf,yf,zf

def writeSimpleFacadeMission(sep, bufferD, wall, ori, filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    x,y,z = getFacade(sep,bufferD,wall,ori)
    brng = wall.getBearing()
    j = 0
    i = 1
    poi = round((brng  - (np.pi/2)*ori)*(180/np.pi),3)
    if(poi < 0):
        poi = poi + 360
    file.write("0 1 0 22 0 0 0 0 0 0 " + str(round(z[0],2)) + " " + "1\n")
    file.write("1 0 10 16 0 0 0 0 " + str(x[0]) + " " + str(y[0]) + " " + str(round(z[j],2)) + " " + "1\n")
    file.write("2 0 0 115 " + str(poi) + " 0 " + str(1) + " 0 0 0 0 1\n")
    while (i < len(x)):
        file.write(str(j + 3) + " 0 10 16 0 0 0 0 " + str(x[i]) + " " + str(y[i]) + " " + str(round(z[i],2)) + " " + "1\n")
        file.write(str(j + 4) + " 0 0 115 " + str(poi) + " 0 " + str(1) + " 0 0 0 0 1\n")
        j = j + 2
        i = i + 1

    file.write(str(len(x) + 2) + " 0 10 16 0 0 0 0 " + str(x[-1]) + " " + str(y[-1]) + " " + str(round(z[0],2)) + " " + "1\n")
    file.write(str(len(x) + 3) + " 0 10 20 0 0 0 0 " + str(x[-1]) + " " + str(y[-1]) + " " + str(round(z[0],2)) + " " + "1\n")
    file.write(str(len(x) + 4) + " 0 10 21 0 0 0 0 0 0 0 1\n")  
    file.close()
    return x,y,z

def writeMultiFacadeMission(sep,bufferD,walls,ori,cW,filename): #cW = Counterclock  or clock wise [-1/1]
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    x,y,z = getMultiFacade(sep,bufferD,walls,ori)
    brng = walls[0].getBearing()
    poi = round((brng  - (np.pi/2)*cW)*(180/np.pi),3)
    if(poi < 0):
        poi = poi + 360
    j = 0
    file.write("0 1 0 22 0 0 0 0 0 0 " + str(round(z[0] + 2,2)) + " " + "1\n")
    file.write("1 0 10 16 0 0 0 0 " + str(x[0]) + " " + str(y[0]) + " " + str(round(z[0],2)) + " " + "1\n")
    file.write("2 0 0 115 " + str(poi) + " 0 " + str(1) + " 0 0 0 0 1\n")
    nW = round(len(x)/len(walls))
    qW = 1
    i = 0
    while (i < len(x)):
        file.write(str(j + 3) + " 0 10 16 0 0 0 0 " + str(x[i]) + " " + str(y[i]) + " " + str(round(z[i],2)) + " " + "1\n")
        file.write(str(j + 4) + " 0 0 115 " + str(poi) + " 0 " + str(1) + " 0 0 0 0 1\n")
        j = j + 2
        i = i + 1
        if(i > nW*qW):
            brng = walls[qW].getBearing()
            poi = round((brng  - (np.pi/2)*cW)*(180/np.pi),3)
            if(poi < 0):
                poi = poi + 360
            qW = qW + 1
    
    file.write(str(len(x) + 2) + " 0 10 16 0 0 0 0 " + str(x[-1]) + " " + str(y[-1]) + " " + str(round(z[0],2)) + " " + "1\n")
    file.write(str(len(x) + 3) + " 0 10 20 0 0 0 0 " + str(x[-1]) + " " + str(y[-1]) + " " + str(round(z[0],2)) + " " + "1\n")
    file.write(str(len(x) + 4) + " 0 10 21 0 0 0 0 0 0 0 1\n")
    file.close()
    return x,y,z

def writeMultiHelixMission(sep,bufferD,perimeters,filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    x,y,z,theta = getMultiHelix(sep, bufferD, perimeters)
    perimeters.sort()
    C = perimeters[0].C
    xf,yf,zf = getHelixinCoords(x,y,z,C)
    xf = xf[::-1]
    yf = yf[::-1]
    zf = zf[::-1]
    perimeter = perimeters[0]
    file.write("0 1 0 22 0 0 0 0 0 0 " + str(round(zf[0],2)) + " " + "1\n")
    file.write("1 0 10 22 0 0 0 0 0 0 " + str(round(zf[0],2)) + " " + "1\n")
    file.write("2 0 10 201 0 0 0 0 " + str(perimeter.C[0]) + " " + str(perimeter.C[1]) + " " + str(perimeter.hmax) + " 1\n")
    i = 0
    j = 0
    h = 1
    while (j < len(xf)):
        file.write(str(i + 3) +  " 0 10 82 0 0 0 0 " + str(xf[j]) + " " + str(yf[j]) + " " + str(round(zf[j],2)) + " " + "1\n")
        file.write(str(i + 4) +  " 0 10 201 0 0 0 0 " + str(perimeter.C[0]) + " " + str(perimeter.C[1]) + " " + str(round(zf[j],2)) + " " + "1\n")
        i = i + 2
        if(j == 99*h):
            file.write(str(i + 2) +  " 0 10 16 0 0 0 0 " + str(xf[j + 1]) + " " + str(yf[j + 1]) + " " + str(round(zf[j + 1],2)) + " " + "1\n")
            file.write(str(i + 3) +  " 0 10 16 0 0 0 0 " + str(xf[j + 2]) + " " + str(yf[j + 2]) + " " + str(round(zf[j + 2],2)) + " " + "1\n")
            perimeter = perimeters[h]
            h = h + 1
            i = i + 2
            j = j + 1

        j = j + 1

    file.write(str(i + 2) + " 0 10 16 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(zf[0] + 2,2)) + " " + "1\n")
    file.write(str(i + 3) + " 0 10 20 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(zf[0] + 2,2)) + " " + "1\n")
    file.write(str(i + 4) + " 0 10 21 0 0 0 0 0 0 0 1\n")
    file.close()

def writeSimpleSquare(sep,bufferD,perimeter,filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    xf,yf,zf = getSquare(sep, bufferD, perimeter)
    file.write("1 0 3 22 0 0 0 0 0 0 " + str(round(zf[0],2)) + " " + "1\n")
    file.write("2 0 3 201 0 0 0 0 " + str(perimeter.C[0]) + " " + str(perimeter.C[1]) + " " + str(perimeter.hmax) + " 1\n")
    i = 0
    j = 0
    while (j < len(xf)):
        file.write(str(i + 3) +  " 0 3 16 0 0 0 0 " + str(xf[j]) + " " + str(yf[j]) + " " + str(round(zf[j],2)) + " " + "1\n")
        file.write(str(i + 4) +  " 0 3 201 0 0 0 0 " + str(perimeter.C[0]) + " " + str(perimeter.C[1]) + " " + str(round(zf[j],2)) + " " + "1\n")
        i = i + 2
        j = j + 1
    
    file.write(str(i + 3) +" 0 3 201 0 0 0 0 0 0 0 1\n")
    file.write(str(i + 4) + " 0 3 16 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(zf[0],2)) + " " + "1\n")
    file.write(str(i + 5) + " 0 3 20 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(zf[0],2)) + " " + "1\n")
    file.write(str(i + 6) + " 0 3 21 0 0 0 0 0 0 0 1\n")
    file.close()
    return xf,yf,zf

def writeMultiElipse(sep,bufferD,perimeters,filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    x,y,z = getMultiElipse(sep, bufferD, perimeters)
    perimeters.sort()
    C = perimeters[0].C
    xf,yf,zf = getHelixinCoords(x,y,z,C)
    xf = xf[::-1]
    yf = yf[::-1]
    zf = zf[::-1]
    perimeter = perimeters[-1]
    file.write("0 1 0 22 0 0 0 0 0 0 " + str(round(zf[0],2)) + " " + "1\n")
    file.write("1 0 10 22 0 0 0 0 0 0 " + str(round(zf[0],2)) + " " + "1\n")
    file.write("2 0 10 201 0 0 0 0 " + str(perimeter.C[0]) + " " + str(perimeter.C[1]) + " " + str(perimeter.hmax) + " 1\n")
    n = round((perimeters[0].hmax - perimeters[0].hmin)/sep)
    i = 0
    j = 0
    h = len(perimeters)
    while (j < len(xf)):
        file.write(str(i + 3) +  " 0 10 82 0 0 0 0 " + str(xf[j]) + " " + str(yf[j]) + " " + str(round(zf[j],2)) + " " + "1\n")
        file.write(str(i + 4) +  " 0 10 201 0 0 0 0 " + str(perimeter.C[0]) + " " + str(perimeter.C[1]) + " " + str(round(zf[j],2)) + " " + "1\n")
        i = i + 2
        if(j == 25*h*(n + 1) + 1):
            file.write(str(i + 2) +  " 0 10 16 0 0 0 0 " + str(xf[j + 1]) + " " + str(yf[j + 1]) + " " + str(round(zf[j + 1],2)) + " " + "1\n")
            file.write(str(i + 3) +  " 0 10 16 0 0 0 0 " + str(xf[j + 2]) + " " + str(yf[j + 2]) + " " + str(round(zf[j + 2],2)) + " " + "1\n")
            perimeter = perimeters[h]
            n = round((perimeters[h].hmax - perimeters[h].hmin)/sep)
            h = h - 1
            i = i + 2
            j = j + 1

        j = j + 1

    file.write(str(i + 2) + " 0 10 16 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(zf[0],2)) + " " + "1\n")
    file.write(str(i + 3) + " 0 10 20 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(zf[0],2)) + " " + "1\n")
    file.write(str(i + 4) + " 0 10 21 0 0 0 0 0 0 0 1\n")
    file.close()

def writeForKML(x,y,z,filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    file.write("1 0 3 22 0 0 0 0 0 0 " + str(round(z[0],2)) + " " + "1\n")
    j = 0
    while (j < len(x)):
        file.write(str(j + 2) +  " 0 3 16 0 0 0 0 " + str(x[j]) + " " + str(y[j]) + " " + str(round(z[j],2)) + " " + "1\n")
        j = j + 1
    file.close()

def writeFacade(x,y,z,cW,walls,filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    file.write("0 1 0 22 0 0 0 0 0 0 " + str(round(z[0],2)) + " " + "1\n")
    file.write("1 0 10 16 0 0 0 0 " + str(x[0]) + " " + str(y[0]) + " " + str(round(z[0],2)) + " " + "1\n")
    brng = walls[0].getBearing()
    poi = round((brng  - (np.pi/2)*cW)*(180/np.pi),3)
    if(poi < 0):
        poi = poi + 360
    file.write("2 0 0 115 " + str(poi) + " 0 " + str(1) + " 1 0 0 0 1\n")
    nW = round(len(x)/len(walls))
    qW = 1
    i = 0
    j = 0
    while (i < len(x)):
        file.write(str(j + 3) + " 0 10 16 0 0 0 0 " + str(x[i]) + " " + str(y[i]) + " " + str(round(z[i],2)) + " " + "1\n")
        file.write(str(j + 4) + " 0 0 115 " + str(poi) + " 0 " + str(1) + " 0 0 0 0 1\n")
        j = j + 2
        i = i + 1
        if(i > nW*qW):
            brng = walls[qW].getBearing()
            poi = round((brng  - (np.pi/2)*cW)*(180/np.pi),3)
            if(poi < 0):
                poi = poi + 360
            
            file.write(str(j + 3) + " 0 0 115 " + str(poi) + " 0 " + str(1) + " 0 0 0 0 1\n")
            j = j + 1
            qW = qW + 1
    
    file.write(str(len(x) + 2) + " 0 10 16 0 0 0 0 " + str(x[-1]) + " " + str(y[-1]) + " " + str(round(z[0],2)) + " " + "1\n")
    file.write(str(len(x) + 3) + " 0 10 20 0 0 0 0 " + str(x[-1]) + " " + str(y[-1]) + " " + str(round(z[0],2)) + " " + "1\n")
    file.write(str(len(x) + 4) + " 0 10 21 0 0 0 0 0 0 0 1\n")
    file.close()

def writeSquarePoly(x,y,z,cW,poly,filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    file.write("0 1 0 22 0 0 0 0 0 0 " + str(round(z[0],2)) + " " + "1\n")
    file.write("1 0 10 16 0 0 0 0 " + str(x[0]) + " " + str(y[0]) + " " + str(round(z[0],2)) + " " + "1\n")
    POIs = poly[0].getPOIs()
    l = 0
    while(l < len(POIs)):
        POIs[l] = round((POIs[l] - (np.pi/2)*cW)*(180/np.pi),3)
        if(POIs[l] < 0):
            POIs[l] = POIs[l] + 360
        l = l + 1
    i = 0
    j = 0
    poi = 0
    while(i < len(x)):
        file.write(str(j + 2) + " 0 10 16 0 0 0 0 " + str(x[i]) + " " + str(y[i]) + " " + str(round(z[i],2)) + " " + "1\n")
        file.write(str(j + 3) + " 0 0 115 " + str(90) + " 0 " + str(1) + " 0 0 0 0 1\n")
        i = i + 1
        j = j + 2
        poi = poi + 1
        if(poi >= len(poly[0].ccn)):
            poi = 0
    
    file.write(str(len(x) + 2) + " 0 10 16 0 0 0 0 " + str(x[-1]) + " " + str(y[-1]) + " " + str(round(z[0],2)) + " " + "1\n")
    file.write(str(len(x) + 3) + " 0 10 20 0 0 0 0 " + str(x[-1]) + " " + str(y[-1]) + " " + str(round(z[0],2)) + " " + "1\n")
    file.write(str(len(x) + 4) + " 0 10 21 0 0 0 0 0 0 0 1\n")
    file.close()

def writeHelix(x,y,z,ps,filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    xf = x[::-1]
    yf = y[::-1]
    zf = z[::-1]
    ps.sort()
    perimeter = ps[0]
    file.write("0 1 0 22 0 0 0 0 0 0 " + str(round(zf[0],2)) + " " + "1\n")
    file.write("1 0 10 22 0 0 0 0 0 0 " + str(round(zf[0],2)) + " " + "1\n")
    file.write("2 0 10 201 0 0 0 0 " + str(perimeter.C[0]) + " " + str(perimeter.C[1]) + " " + str(perimeter.hmax) + " 1\n")
    i = 0
    j = 0
    h = 1
    while (j < len(xf)):
        file.write(str(i + 3) +  " 0 10 82 0 0 0 0 " + str(xf[j]) + " " + str(yf[j]) + " " + str(round(zf[j],2)) + " " + "1\n")
        file.write(str(i + 4) +  " 0 10 201 0 0 0 0 " + str(perimeter.C[0]) + " " + str(perimeter.C[1]) + " " + str(round(zf[j],2)) + " " + "1\n")
        i = i + 2
        if(j == 99*h and len(ps) > h):
            file.write(str(i + 2) +  " 0 10 16 0 0 0 0 " + str(xf[j + 1]) + " " + str(yf[j + 1]) + " " + str(round(zf[j + 1],2)) + " " + "1\n")
            file.write(str(i + 3) +  " 0 10 16 0 0 0 0 " + str(xf[j + 2]) + " " + str(yf[j + 2]) + " " + str(round(zf[j + 2],2)) + " " + "1\n")
            perimeter = ps[h]
            h = h + 1
            i = i + 2
            j = j + 1

        j = j + 1

    file.write(str(i + 2) + " 0 10 16 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(ps[-1].hmax + ps[-1].hmax*0.25,2)) + " " + "1\n")
    file.write(str(i + 3) + " 0 10 20 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(ps[-1].hmax + ps[-1].hmax*0.25,2)) + " " + "1\n")
    file.write(str(i + 4) + " 0 10 21 0 0 0 0 0 0 0 1\n")
    file.close()

def writeElipse(x,y,z,sep,ps,filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    ps.sort()
    xf = x[::-1]
    yf = y[::-1]
    zf = z[::-1]
    perimeter = ps[-1]
    file.write("0 1 0 22 0 0 0 0 0 0 " + str(round(zf[0],2)) + " " + "1\n")
    file.write("1 0 10 22 0 0 0 0 0 0 " + str(round(zf[0],2)) + " " + "1\n")
    file.write("2 0 10 201 0 0 0 0 " + str(perimeter.C[0]) + " " + str(perimeter.C[1]) + " " + str(perimeter.hmax) + " 1\n")
    n = round((ps[0].hmax - ps[0].hmin)/sep)
    i = 0
    j = 0
    h = len(ps)
    while (j < len(xf)):
        file.write(str(i + 3) +  " 0 10 82 0 0 0 0 " + str(xf[j]) + " " + str(yf[j]) + " " + str(round(zf[j],2)) + " " + "1\n")
        file.write(str(i + 4) +  " 0 10 201 0 0 0 0 " + str(perimeter.C[0]) + " " + str(perimeter.C[1]) + " " + str(round(zf[j],2)) + " " + "1\n")
        i = i + 2
        if(j == 25*h*(n + 1) + 1):
            file.write(str(i + 2) +  " 0 10 16 0 0 0 0 " + str(xf[j + 1]) + " " + str(yf[j + 1]) + " " + str(round(zf[j + 1],2)) + " " + "1\n")
            file.write(str(i + 3) +  " 0 10 16 0 0 0 0 " + str(xf[j + 2]) + " " + str(yf[j + 2]) + " " + str(round(zf[j + 2],2)) + " " + "1\n")
            perimeter = ps[h]
            n = round((ps[h].hmax - ps[h].hmin) / sep)
            h = h - 1
            i = i + 2
            j = j + 1

        j = j + 1

    file.write(str(i + 2) + " 0 10 16 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(ps[-1].hmax + ps[-1].hmax*0.25,2)) + " " + "1\n")
    file.write(str(i + 3) + " 0 10 20 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(ps[-1].hmax + ps[-1].hmax*0.25,2)) + " " + "1\n")
    file.write(str(i + 4) + " 0 10 21 0 0 0 0 0 0 0 1\n")
    file.close()