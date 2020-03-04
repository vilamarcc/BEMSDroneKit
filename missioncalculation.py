from dronekit import *
import math
from routes import *


def writeSimpleHelixMission(hmax, sep, nWPperCircle, bufferD, cc1, cc2, cc3, cc4, filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    alpha = (2*np.pi)/nWPperCircle #rad
    x,y,z,theta = getHelix(hmax,sep,bufferD,cc1,cc2,cc3,cc4)
    C = getCenterofPerimeter(cc1,cc2,cc3,cc4)
    xf,yf,zf = getHelixinCoords(x,y,z,C)
    file.write("0 1 0 16 0 0 0 0 " + str(xf[0]) + " " + str(yf[0]) + " " + str(round(zf[0],2)) + " " + "1\n")
    i = 0
    j = 0
    rpm = 0
    while (j < len(xf)):
        if(round(alpha*i,1) == round(theta[j],1) or round(alpha*i,1) == round(theta[j] - (2*np.pi*rpm),1) or round(alpha*i,1) + 0.1 == round(theta[j],1) or round(alpha*i,1) - 0.1 == round(theta[j],1)):
            file.write(str(i + 1) +  " 0 10 82 0 0 0 0 " + str(xf[j]) + " " + str(yf[j]) + " " + str(round(zf[j],2)) + " " + "1\n")
            i = i + 1
        if(round(theta[j] - (2*np.pi*(rpm + 1))) == 0):
            rpm = rpm + 1
        j = j + 1

    #Añadimos el perimetro para comprobar (eliminar luego)
    file.write(str(i) +  " 0 10 16 0 0 0 0 " + str(cc1[0]) + " " + str(cc1[1]) + " " + str(0) + " " + "1\n")
    file.write(str(i + 1) +  " 0 10 16 0 0 0 0 " + str(cc2[0]) + " " + str(cc2[1]) + " " + str(0) + " " + "1\n")
    file.write(str(i + 2) +  " 0 10 16 0 0 0 0 " + str(cc3[0]) + " " + str(cc3[1]) + " " + str(0) + " " + "1\n")
    file.write(str(i + 3) +  " 0 10 16 0 0 0 0 " + str(cc4[0]) + " " + str(cc4[1]) + " " + str(0) + " " + "1\n")
    file.close()

def writeSimpleFacadeMission(hmax, sep, n, bufferD, cc1, cc2, filename):
    filename = filename + ".txt"
    file = open(filename, "w")
    file.write("QGC WPL 110\n")