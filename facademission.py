from missioncalculation import writeSimpleFacadeMission
from droneCommands import *
from dronekit import *
from routes import wall
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from plotRoutes import plotPreviewSimpleFacade

#WALL SAMPLE  SOUTH WALL LIBRARY EETAC CBL#

c1 = [41.2754309, 1.9849822]
c2 = [41.2755821, 1.9856085]

x = []
y = []
z = []
w = 0
sep = 0
hmin = 0
bufferD = 0
hmax = 0
ori = 0
filename = ""
print("Simple Facade Mission Script")
print("Please indicate wall input:")
print("\t 1 - Default (CBL Library)")
print("\t 2 - Input own coordinates")
select = str(input())
if(select == str(1)):
    print("Using default wall")
    print("Please input mission definition parameters:")
    paramT = False
    while(paramT == False):
        print("Separation between sweeps:")
        sep = float(input())            
        print("Minimum height: [m]")
        hmin = float(input())
        print("Maximum height: [m]")
        hmax = float(input())
        print("Security Distance: [m]")
        bufferD = float(input())
        print("Orientation [1/-1]: ")
        ori = int(input())
        print("Filename to write: ")
        filename = str(input())
        print("\n")
        print("PARAMETERS: \n")
        print("\t Separation: " + str(sep))
        print("\t Minumum Height: " + str(hmin) + " m")
        print("\t Maximum Height: " + str(hmax) + " m")
        print("\t Security Distance: " + str(bufferD) + " m")
        print("\t Orientation: " + str(ori))
        print("\t Filename: " + str(filename) + ".txt")
        print("-------------------------------------------------------------------------")
        print("COORDINATES OF DEFAULT WALL: [Latitude, Longitude] \n")
        print("\t Corner 1: " + str(c1))
        print("\t Corner 2: " + str(c2) + "\n")            
        print("Verify parameters. [Y/N]")
        ans = str(input())
        if(ans == "Y" or ans == "y"):
            paramT = True
            w = wall(c1,c2,hmax,hmin)
        else:
            paramT = False
if(select == str(2)):
    print("Please input coordinates of perimeter:")
    paramT = False
    while(paramT == False):
        print("\t Corner 1, Latitude:")
        Lat1 = float(input())
        print("\t Corner 1, Longitude:")
        Lon2 = float(input())
        c1 = [Lat1, Lon2]
        print("\t Corner 2, Latitude:")
        Lat1 = float(input())
        print("\t Corner 2, Longitude:")
        Lon2 = float(input())
        c2 = [Lat1, Lon2]
        print("Separation between laps:")
        sep = float(input())            
        print("Minimum height: [m]")
        hmin = float(input())
        print("Maximum height: [m]")
        hmax = float(input())
        print("Security Distance: [m]")
        bufferD = float(input())
        print("Orientation [1/-1]: ")
        ori = int(input())
        print("Filename to write: ")
        filename = str(input())
        print("\n")
        print("PARAMETERS: \n")
        print("\t Separation: " + str(sep))
        print("\t Minumum Height: " + str(hmin) + " m")
        print("\t Maximum Height: " + str(hmax) + " m")
        print("\t Security Distance: " + str(bufferD) + " m")
        print("\t Filename: " + str(filename) + ".txt")
        print("-------------------------------------------------------------------------")
        print("COORDINATES OF INPUT WALL: [Latitude, Longitude] \n")
        print("\t Corner 1: " + str(c1))
        print("\t Corner 2: " + str(c2) + "\n")            
        print("Verify parameters. [Y/N]")
        ans = str(input())
        if(ans == "Y" or ans == "y"):
            paramT = True
            w = wall(c1,c2,hmax,hmin)
        else:
            paramT = False


print("Please indicate the type of mission you want to execute: ")
print("\t 1 - Normal connection with drone at ttyAM0")
print("\t 2 - SITL Sofware")
selectmode = str(input())
if(selectmode == str(1)):
    print("Mode Selected: Connection via ttyAMA0")
if(selectmode == str(2)):
    print("Mode Selected: SITL Software")
    print("Please, indicate if you want to connect to external simulation or let this script create a simulation:")
    print("\t 1 - External SITL")
    print("\t 2 - Execute SITL")
    sitl = input()
    if(sitl == str(1)):
        vehicle = connectSITL()
        clear_mission(vehicle)
        x,y,z = writeSimpleFacadeMission(sep,bufferD,w,ori,filename)
        print("Mission Calculated")
        upload_mission(filename + ".txt",vehicle)
        n_WP, missionList = get_current_mission(vehicle)
        vehicle.mode = VehicleMode("STABILIZE")
        printStatus(vehicle)
        print("Mission ready to start.")
        print("Do you wish to see a preview of the route? [Y/N]")
        plot = input()
        if(plot == "y" or plot == "Y"):
            plotPreviewSimpleFacade(x,y,z,w,1,vehicle.home_location)

        print("\t 1 - Arm and Start Mission")
        se = input()
        if(se == str(1)):
            time.sleep(3)
            arm_and_takeoff(vehicle,hmax)
            print("Changing to AUTO")
            ChangeMode(vehicle, "AUTO")
            vehicle.airspeed = 5.0
            time.sleep(2)
            if(vehicle.mode == "AUTO" and vehicle.armed == True):
                time.sleep(2)
                print("Mission Started")
                t = True
                while t == True:
                    time.sleep(5)
                    print("Current WP: %d of %d " % (vehicle.commands.next, vehicle.commands.count))
                    printStatus(vehicle)
                    if vehicle.commands.next == (vehicle.commands.count - 1):
                        print("Final waypoint reached")
                        t = False
                        time.sleep(5)
                        break
            else:
                print("ERROR CLOSING VEHICLE")

            clear_mission(vehicle)
            print("Mission deleted")
            print ('Mision Ended...............................')
            print("Disarming.........................")
            vehicle.armed = False
            print("Disarmed")

    if(sitl == str(2)):
        print("FALTA")