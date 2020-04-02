from missioncalculation import writeSimpleHelixMission
from droneCommands import *
from dronekit import * 
from routes import perimeter

#BUILDING SAMPLE LIBRARY EETAC CBL#

c1 = [41.2757453, 1.9848481]
c2 = [41.2754258, 1.9849782]
c3 = [41.2755750, 1.9856085]
c4 = [41.2758965, 1.9854744]


p = 0
sep = 0
hmin = 0
bufferD = 0
hmax = 0
filename = ""
print("Simple Helix Mission Script")
print("Please indicate perimeter input:")
print("\t 1 - Default (CBL Library)")
print("\t 2 - Input own coordinates")
select = str(input())
if(select == str(1)):
    print("Using default perimeter")
    print("Please input mission definition parameters:")
    paramT = False
    while(paramT == False):
        print("Separation between laps:")
        sep = float(input())            
        print("Minimum height: [m]")
        hmin = float(input())
        print("Maximum height: [m]")
        hmax = float(input())
        print("Security Distance: [m]")
        bufferD = float(input())
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
        print("COORDINATES OF DEFAULT PERIMETER: [Latitude, Longitude] \n")
        print("\t Corner 1: " + str(c1))
        print("\t Corner 2: " + str(c2))            
        print("\t Corner 3: " + str(c3))
        print("\t Corner 4: " + str(c4) + "\n")
        print("Verify parameters. [Y/N]")
        ans = str(input())
        if(ans == "Y" or ans == "y"):
            paramT = True
            p = perimeter(c1,c2,c3,c4,hmax,hmin)
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
    if(sitl == str(2)):
        print("Yikes")

writeSimpleHelixMission(sep,bufferD,p,filename)
print("Mission Calculated")
upload_mission(filename + ".txt",vehicle)
n_WP, missionList = get_current_mission(vehicle)
printStatus(vehicle)
        
            

