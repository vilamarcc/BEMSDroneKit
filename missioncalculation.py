from dronekit import *
import math
from routes import getMultiHelix, getMultiFacade, getHelix, getFacade, getHelixinCoords
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
    j = 0
    if(ori == 1):
        poi = 270
    if(ori == -1):
        poi = 90

    file.write("0 1 0 22 0 0 0 0 0 0 " + str(round(z[0],2)) + " " + "1\n")
    file.write("1 0 10 16 0 0 0 0 " + str(x[0]) + " " + str(y[0]) + " " + str(round(z[0],2)) + " " + "1\n")
    file.write("2 0 3 201 0 " + str(poi) + " 0 1 1 0 0 0")
    while (j < len(x)):
        file.write(str(j + 3) + " 0 10 16 0 0 0 0 " + str(x[j]) + " " + str(y[j]) + " " + str(round(z[j],2)) + " " + "1\n")
        j = j + 1
    
    file.write(str(j) + " 0 10 16 0 0 0 0 " + str(x[-1]) + " " + str(y[-1]) + " " + str(round(z[0],2)) + " " + "1\n")
    file.write(str(j + 1) + " 0 10 20 0 0 0 0 " + str(x[-1]) + " " + str(y[-1]) + " " + str(round(z[0],2)) + " " + "1\n")
    file.write(str(j + 2) + " 0 10 21 0 0 0 0 0 0 0 1\n")
    file.close()
    return x,y,z

def writeMultiFacadeMission(sep,bufferD,walls,ori,filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    x,y,z = getMultiFacade(sep,bufferD,walls,ori)
    j = 0
    file.write("0 1 0 22 0 0 0 0 0 0 " + str(round(z[0] + 2,2)) + " " + "1\n")
    file.write("1 0 10 16 0 0 0 0 " + str(x[0]) + " " + str(y[0]) + " " + str(round(z[0] + 2,2)) + " " + "1\n")

    while (j < len(x)):
        file.write(str(j + 1) +  " 0 10 16 0 0 0 0 " + str(x[j]) + " " + str(y[j]) + " " + str(round(z[j],2)) + " " + "1\n")
        j = j + 1
    
    file.write(str(j) + " 0 10 16 0 0 0 0 " + str(x[-1]) + " " + str(y[-1]) + " " + str(round(z[0] + 2,2)) + " " + "1\n")
    file.write(str(j + 1) + " 0 10 20 0 0 0 0 " + str(x[-1]) + " " + str(y[-1]) + " " + str(round(z[0] + 2,2)) + " " + "1\n")
    file.write(str(j + 2) + " 0 10 21 0 0 0 0 0 0 0 1\n")
    file.close()

def writeMultiHelixMission(sep,bufferD,bufferH,perimeters,filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    x,y,z,theta = getMultiHelix(sep, bufferD,bufferH, perimeters)
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
        i = i + 1
        if(j == 99*h):
            file.write(str(i + 2) +  " 0 10 16 0 0 0 0 " + str(xf[j + 1]) + " " + str(yf[j + 1]) + " " + str(round(zf[j + 1],2)) + " " + "1\n")
            file.write(str(i + 3) +  " 0 10 16 0 0 0 0 " + str(xf[j + 2]) + " " + str(yf[j + 2]) + " " + str(round(zf[j + 2],2)) + " " + "1\n")
            perimeter = perimeters[h]
            h = h + 1
            i = i + 1
            j = j + 1

        j = j + 1

    file.write(str(i + 2) + " 0 10 16 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(zf[0] + 2,2)) + " " + "1\n")
    file.write(str(i + 3) + " 0 10 20 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(zf[0] + 2,2)) + " " + "1\n")
    file.write(str(i + 4) + " 0 10 21 0 0 0 0 0 0 0 1\n")
    file.close()