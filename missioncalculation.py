from dronekit import *
import math
from routes import *


def writeSimpleHelixMission(hmax, sep, nCircles, nWP, bufferD, cc1, cc2, cc3, cc4):
    file = open("Mission1.txt", "w")
    file.write("QGC WPL 110\n")
    x,y,z = getHelix(hmax,sep,bufferD,cc1,cc2,cc3,cc4)
    C = getCenterofPerimeter(cc1,cc2,cc3,cc4)
    xf,yf,zf = getHelixinCoords(x,y,z,C)
    file.write("0 1 0 16 0 0 0 0 " + str(xf[0]) + " " + str(yf[0]) + " " + str(round(zf[0],2)) + " " + "1\n")
    i = 0
    while (i < len(xf)):
        file.write(str(i + 1) +  " 0 10 82 0 0 0 0 " + str(xf[i]) + " " + str(yf[i]) + " " + str(round(zf[i],2)) + " " + "1\n")
        i = i + 1

    #Añadimos el perimetro para comprobar (eliminar luego)
    file.write(str(i) +  " 0 10 16 0 0 0 0 " + str(cc1[0]) + " " + str(cc1[1]) + " " + str(0) + " " + "1\n")
    file.write(str(i + 1) +  " 0 10 16 0 0 0 0 " + str(cc2[0]) + " " + str(cc2[1]) + " " + str(0) + " " + "1\n")
    file.write(str(i + 2) +  " 0 10 16 0 0 0 0 " + str(cc3[0]) + " " + str(cc3[1]) + " " + str(0) + " " + "1\n")
    file.write(str(i + 3) +  " 0 10 16 0 0 0 0 " + str(cc4[0]) + " " + str(cc4[1]) + " " + str(0) + " " + "1\n")
    file.close()
