from missioncalculation import *
from droneCommands import *
from dronekit import *
from dronekit_sitl import *
from routes import *
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from plotRoutes import *
import threading
from matplotlib.animation import FuncAnimation

#### General Parameters #######
sep = 2
sep_J = 1
D = 4
D_C3 = 6
D_J = 2
ori = 1
cW = 1
filename = "demoTest4"
filenameKML = "demoKML_Test4"

############# BUILDING LIBRARY EETAC CBL #############################

c1 = [41.2757453, 1.9848481]
c2 = [41.2754258, 1.9849782]
c3 = [41.2755750, 1.9856085]
c4 = [41.2758965, 1.9854744]
hmax_CBL = 12
hmin_CBL = 2
cn_CBL = [c1,c2,c3,c4]
p_CBL = perimeter(c1,c2,c3,c4,hmax_CBL,hmin_CBL)
polygonCBL = polygon(cn_CBL,hmax_CBL,hmin_CBL)
wallsCBL = [wall(c2,c3,12,2),wall(c3,c4,12,2),wall(c4,c1,12,2),wall(c1,c2,12,2)]
wallCBL = [wall(c2,c3,12,2)]

############## C3 ################

#Primer piso (base)

c11 = [41.2754178,1.9861114]
c12 = [41.2749914,1.9862992]
c13 = [41.2753472,1.9877368]
c14 = [41.2757766,1.9875652]
p1_C3 = perimeter(c11,c12,c13,c14,8,2)
cn1_C3 = [c11,c12,c13,c14]
poly1_C3 = polygon(cn1_C3,8,2)

#Segundo piso

c21 = [41.2754017,1.9861972]
c22 = [41.2750297,1.9863568]
c23 = [41.275192,1.9870274]
c24 = [41.2755609,1.9868731]
p2_C3 = perimeter(c21,c22,c23,c24,15,9)
cn2_C3 = [c21,c22,c23,c24]
poly2_C3 = polygon(cn2_C3,15,9)

#Tercer piso

c31 = [41.275322,1.9862375]
c32 = [41.2752646,1.9862616]
c33 = [41.2754178,1.9869362]
c34 = [41.2754833,1.9869107]
p3_C3 = perimeter(c31,c32,c33,c34,20,16)
cn3_C3 = [c31,c32,c33,c34]
poly3_C3 = polygon(cn3_C3,20,16)


ps_C3 = [p1_C3,p2_C3,p3_C3]
polys_C3 =[poly1_C3,poly2_C3,poly3_C3]

#################### Colegio ########################
hmax_HS = 8
hmin_HS = 2
cc1 = [41.2785442,1.9814122]
cc2 = [41.2784152,1.9814926]
cc3 = [41.2785563,1.9818842]
cc4 = [41.2780262,1.9822302]
cc5 = [41.2781915,1.9826996]
cc6 = [41.2787277,1.9823670]
cc7 = [41.2789756,1.9830430]
cc8 = [41.2791086,1.9829544]
cn = [cc1,cc2,cc3,cc4,cc5,cc6,cc7,cc8]
wall1 = wall(cc1,cc2,hmax_HS,hmin_HS)
wall2 = wall(cc2,cc3,hmax_HS,hmin_HS)
wall3 = wall(cc3,cc4,hmax_HS,hmin_HS)
wall4 = wall(cc4,cc5,hmax_HS,hmin_HS)
wall5 = wall(cc5,cc6,hmax_HS,hmin_HS)
wall6 = wall(cc6,cc7,hmax_HS,hmin_HS)
wall7 = wall(cc7,cc8,hmax_HS,hmin_HS)
wall8 = wall(cc8,cc1,hmax_HS,hmin_HS)
wallsHS = [wall1,wall2,wall3,wall4,wall5,wall6,wall7,wall8]
polyHS = polygon(cn,hmax_HS,hmin_HS)

######### JAULA C3 ##############
hmax_J = 7
hmin_J = 2
cj1 = [41.2751567,1.9867417]
cj2 = [41.2753724,1.9866492]
cj3 = [41.2754107,1.9867913]
cj4 = [41.2751668,1.9868906]
wall1 = wall(cj1,cj2,hmax_J,hmin_J)
wall2 = wall(cj2,cj3,hmax_J,hmin_J)
wall3 = wall(cj3,cj4,hmax_J,hmin_J)
walls_J = [wall1,wall2,wall3]


x = []
y = []
z = []
wallsF = 0
sqF = 0
hF = 0
eF = 0

print("DEMO FOR TFG MARC VILA VERTICAL EVALUATION BUIDLINGS ALGORITHM                                   (c) UPC EETAC 2020")
print("")
print("Please select type of route to demo:")
print("\t 1. - Facade")
print("\t 2. - Square")
print("\t 3. - Helix")
print("\t 4. - Elipse")

route_answer = str(input())
if(route_answer == "1"):
    print("")
    print("Facade Route Selected, please select pre-established test building: ")
    print("\t 1. - Library BCBL")
    print("\t 2. - Josep Lluis Sert High School")
    print("\t 3. - Cage C3")
    building_answer = str(input())
    if(building_answer == "1"):
        print("Library Selected:")
        print("Write Facade mission for full BCBL or just South Wall?")
        print("\t 1.- Single Facade (South Wall)")
        print("\t 2.- Multi Facade (Whole BCBL)")
        fanswer = str(input())
        print("The following parameters will be used:")
        print("\n")
        print("PARAMETERS: \n")
        print("\t Separation: " + str(sep))
        print("\t Minumum Height: " + str(hmin_CBL) + " m")
        print("\t Maximum Height: " + str(hmax_CBL) + " m")
        print("\t Security Distance: " + str(D) + " m")
        print("\t Orientation: " + str(ori))
        print("\t Filename: " + str(filename) + ".txt")
        if(fanswer == "1"):
            print("-------------------------------------------------------------------------")
            print("COORDINATES OF DEFAULT WALL BCBL: [Latitude, Longitude] \n")
            print("\t Corner 1: " + str(c2))
            print("\t Corner 2: " + str(c3) + "\n")
            wallsF = wallCBL    
        if(fanswer == "2"):
            print("-------------------------------------------------------------------------")
            print("COORDINATES OF DEFAULT WALLS BCBL: [Latitude, Longitude] \n")
            print("\t Corner 1: " + str(c2))
            print("\t Corner 2: " + str(c3))
            print("\t Corner 3: " + str(c4))
            print("\t Corner 4: " + str(c1) + "\n")
            wallsF = wallsCBL
           
    if(building_answer == "2"):
        print("Josep Lluis Sert High School selected")
        print("The following parameters will be used:")
        print("\n")
        print("PARAMETERS: \n")
        print("\t Separation: " + str(sep))
        print("\t Minumum Height: " + str(hmin_HS) + " m")
        print("\t Maximum Height: " + str(hmax_HS) + " m")
        print("\t Security Distance: " + str(D) + " m")
        print("\t Orientation: " + str(ori))
        print("\t Direction (cW): " + str(cW))
        print("\t Filename: " + str(filename) + ".txt")
        print("COORDINATES OF DEFAULT WALLS JLS HS: [Latitude, Longitude] \n")
        print("\t Corner 1: " + str(cc1))
        print("\t Corner 2: " + str(cc2))
        print("\t Corner 3: " + str(cc3))
        print("\t Corner 4: " + str(cc4))
        print("\t Corner 5: " + str(cc5))
        print("\t Corner 6: " + str(cc6))
        print("\t Corner 7: " + str(cc7))
        print("\t Corner 8: " + str(cc8) + "\n")
        wallsF = wallsHS

    if(building_answer == "3"):
        sep = sep_J
        D = D_J
        print("The following parameters will be used:")
        print("\n")
        print("PARAMETERS: \n")
        print("\t Separation: " + str(sep))
        print("\t Minumum Height: " + str(hmin_J) + " m")
        print("\t Maximum Height: " + str(hmax_J) + " m")
        print("\t Security Distance: " + str(D) + " m")
        print("\t Orientation: " + str(-1))
        print("\t Filename: " + str(filename) + ".txt")
        print("-------------------------------------------------------------------------")
        print("COORDINATES OF DEFAULT WALLS Cage: [Latitude, Longitude] \n")
        print("\t Corner 1: " + str(cj2))
        print("\t Corner 2: " + str(cj3))
        print("\t Corner 3: " + str(cj4))
        print("\t Corner 4: " + str(cj1) + "\n")
        wallsF = walls_J

    x,y,z = getMultiFacade(sep,D,wallsF,ori)
    writeFacade(x,y,z,cW,wallsF,filename)

if(route_answer == "2"):
    print("")
    print("Square Route Selected, please select pre-established test building: ")
    print("\t 1. - Library CBL")
    print("\t 2. - EETAC C3 Building")
    print("\t 3. - Josep Lluis Sert High School")
    building_answer = str(input())
    if(building_answer == "1"):
        print("The following parameters will be used:")
        print("\n")
        print("PARAMETERS: \n")
        print("\t Separation: " + str(sep))
        print("\t Minumum Height: " + str(hmin_CBL) + " m")
        print("\t Maximum Height: " + str(hmax_CBL) + " m")
        print("\t Security Distance: " + str(D) + " m")
        print("\t Direction (cW): " + str(cW))
        print("\t Filename: " + str(filename) + ".txt")

        print("-------------------------------------------------------------------------")
        print("COORDINATES OF DEFAULT PERIMETER BCBL: [Latitude, Longitude] \n")
        print("\t Corner 1: " + str(c2))
        print("\t Corner 2: " + str(c3))
        print("\t Corner 3: " + str(c4))
        print("\t Corner 4: " + str(c1) + "\n")

        sqF = [polygonCBL]

    if(building_answer == "2"):
        D = D_C3
        print("The following parameters will be used:")
        print("\n")
        i = 0
        print("PARAMETERS: \n")
        while(i < len(ps_C3)):
            ps = ps_C3[i]
            print("PERIMETER %d" % (i + 1))
            print("")
            print("\t Minumum Height: " + str(ps.hmin) + " m")
            print("\t Maximum Height: " + str(ps.hmax) + " m")
            print("-------------------------------------------------------------------------")
            print("COORDINATES OF DEFAULT PERIMETER C3: [Latitude, Longitude] \n")
            j = 0
            while(j < len(ps.ccn)):
                print("\t Corner "+ str(j + 1) +": "  + str(ps.ccn[j]))
                j = j + 1
            print("\n")

            i = i + 1

        print("COMMON REMAINDER PARAMETERS: \n")
        print("\t Separation: " + str(sep) + " m")
        print("\t Security Distance: " + str(D) + " m")
        print("\t Direction (cW): " + str(cW))
        print("\t Filename: " + str(filename) + ".txt")
        sqF = polys_C3

    if(building_answer == "3"):
        print("The following parameters will be used:")
        print("\n")
        print("PARAMETERS: \n")
        print("\t Separation: " + str(sep))
        print("\t Minumum Height: " + str(hmin_CBL) + " m")
        print("\t Maximum Height: " + str(hmax_CBL) + " m")
        print("\t Security Distance: " + str(D) + " m")
        print("\t Direction (cW): " + str(cW))
        print("\t Filename: " + str(filename) + ".txt")

        print("COORDINATES OF DEFAULT WALLS JLS HS: [Latitude, Longitude] \n")
        print("\t Corner 1: " + str(cc1))
        print("\t Corner 2: " + str(cc2))
        print("\t Corner 3: " + str(cc3))
        print("\t Corner 4: " + str(cc4))
        print("\t Corner 5: " + str(cc5))
        print("\t Corner 6: " + str(cc6))
        print("\t Corner 7: " + str(cc7))
        print("\t Corner 8: " + str(cc8) + "\n")

        sqF = [polyHS]

    x,y,z = getMultiPolySquare(sep,D,sqF)
    writeSquarePoly(x,y,z,cW,sqF,filename)

if(route_answer == "3"):
    print("")
    print("Helix Route Selected, please select pre-established test building: ")
    print("\t 1. - Library CBL")
    print("\t 2. - EETAC C3 Building")
    building_answer = str(input())
    if(building_answer == "1"):

        print("The following parameters will be used:")
        print("\n")
        print("PARAMETERS: \n")
        print("\t Separation: " + str(sep))
        print("\t Minumum Height: " + str(hmin_CBL) + " m")
        print("\t Maximum Height: " + str(hmax_CBL) + " m")
        print("\t Security Distance: " + str(D) + " m")
        print("\t Filename: " + str(filename) + ".txt")

        print("-------------------------------------------------------------------------")
        print("COORDINATES OF DEFAULT PERIMETER BCBL: [Latitude, Longitude] \n")
        print("\t Corner 1: " + str(c2))
        print("\t Corner 2: " + str(c3))
        print("\t Corner 3: " + str(c4))
        print("\t Corner 4: " + str(c1) + "\n")
        hf = [p_CBL]


    if(building_answer == "2"):
        D = D_C3
        print("The following parameters will be used:")
        print("\n")
        i = 0
        print("PARAMETERS: \n")
        while(i < len(ps_C3)):
            ps = ps_C3[i]
            print("PERIMETER %d" % (i + 1))
            print("")
            print("\t Minumum Height: " + str(ps.hmin) + " m")
            print("\t Maximum Height: " + str(ps.hmax) + " m")
            print("-------------------------------------------------------------------------")
            print("COORDINATES OF DEFAULT PERIMETER C3: [Latitude, Longitude] \n")
            j = 0
            while(j < len(ps.ccn)):
                print("\t Corner "+ str(j + 1) +": "  + str(ps.ccn[j]))
                j = j + 1
            print("\n")

            i = i + 1

        print("COMMON REMAINDER PARAMETERS: \n")
        print("\t Separation: " + str(sep) + " m")
        print("\t Security Distance: " + str(D) + " m")
        print("\t Filename: " + str(filename) + ".txt")
        hf = ps_C3

    x,y,z,theta = getMultiHelix(sep,D,hf)
    x,y,z = getHelixinCoords(x,y,z,hf[0].getCenter())
    writeHelix(x,y,z,hf,filename)

if(route_answer == "4"):
    print("")
    print("Elliptic Route Selected, please select pre-established test building: ")
    print("\t 1. - Library CBL")
    print("\t 2. - EETAC C3 Building")
    building_answer = str(input())
    if(building_answer == "1"):
        print("The following parameters will be used:")
        print("\n")
        print("PARAMETERS: \n")
        print("\t Separation: " + str(sep))
        print("\t Minumum Height: " + str(hmin_CBL) + " m")
        print("\t Maximum Height: " + str(hmax_CBL) + " m")
        print("\t Security Distance: " + str(D) + " m")
        print("\t Filename: " + str(filename) + ".txt")

        print("-------------------------------------------------------------------------")
        print("COORDINATES OF DEFAULT PERIMETER BCBL: [Latitude, Longitude] \n")
        print("\t Corner 1: " + str(c2))
        print("\t Corner 2: " + str(c3))
        print("\t Corner 3: " + str(c4))
        print("\t Corner 4: " + str(c1) + "\n")
        ef = [p_CBL]

    if(building_answer == "2"):
        D = D_C3
        print("The following parameters will be used:")
        print("\n")
        i = 0
        print("PARAMETERS: \n")
        while(i < len(ps_C3)):
            ps = ps_C3[i]
            print("PERIMETER %d" % (i + 1))
            print("")
            print("\t Minumum Height: " + str(ps.hmin) + " m")
            print("\t Maximum Height: " + str(ps.hmax) + " m")
            print("-------------------------------------------------------------------------")
            print("COORDINATES OF DEFAULT PERIMETER C3: [Latitude, Longitude] \n")
            j = 0
            while(j < len(ps.ccn)):
                print("\t Corner "+ str(j + 1) +": "  + str(ps.ccn[j]))
                j = j + 1
            print("\n")

            i = i + 1

        print("COMMON REMAINDER PARAMETERS: \n")
        print("\t Separation: " + str(sep) + " m")
        print("\t Security Distance: " + str(D) + " m")
        print("\t Filename: " + str(filename) + ".txt")
        ef = ps_C3
    
    x,y,z = getMultiElipse(sep,D,ef)
    x,y,z = getHelixinCoords(x,y,z, ef[0].getCenter())
    writeElipse(x,y,z,sep,ef,filename)

fig = None
writeForKML(x,y,z,filenameKML)
print("Do you wish to see a preview of the route?")
print("[Y/N]")
if(str(input()) == "y" or str(input()) == "Y"):
    if(route_answer == "1"):
        plotPreviewMultiFacade(x,y,z,wallsF,1)
        fig = plotPreviewMultiFacade(0,0,0,wallsF,2,live =True)
    if(route_answer == "2"):
        plotPreviewMutlyPolygon(x,y,z,sqF,1)
        fig = plotPreviewMutlyPolygon(0,0,0,sqF,2,live = True)
    if(route_answer == "3" or route_answer == "4"):
        try:
            plotPreviewMultiPerimeter(x,y,z,eF,1)
            fig = plotPreviewMultiPerimeter(0,0,0,eF,2,live = True)
        except:
            plotPreviewMultiPerimeter(x,y,z,hF,1)
            fig = plotPreviewMultiPerimeter(0,0,0,hF,2,live = True)

## ONLY SITL MISSIONS ON THIS DEMO ##
vehicle = None
print("Select SITL Simulation")
print("\t 1. - External SITL")
print("\t 2. - Execute SITL from this script")
sitl = input()
if(str(sitl) == "1"):
    vehicle = connectSITL()

elif(str(sitl) == "2"):
    sitl = SITL()
    #sitl.download('copter','3.3', verbose = True)
    args = ['-S','--model','quad','--home=41.2754077,1.9845396,6,90']
    sitl.launch(args,await_ready=False,restart=False,verbose = False)
    cs = sitl.connection_string()
    sitl.block_until_ready()
    vehicle = connect(cs,wait_ready=True,baud = 921600)

printStatus(vehicle)
clear_mission(vehicle)
upload_mission(filename + ".txt",vehicle)
n_WP, missionList = get_current_mission(vehicle)
vehicle.mode = VehicleMode("STABILIZE")
printStatus(vehicle)
print("Mission ready to start.")
print("\t 1 - Arm and Start Mission")
se = input()
if(se == str(1)):
    #p = threading.Thread(target=updatePlotLive(fig,vehicle) , name = "PLOT")
    m = threading.Thread(target=MissionStart(vehicle,max(z)) , name = "MISSION")
    m.start()
    #p.start()