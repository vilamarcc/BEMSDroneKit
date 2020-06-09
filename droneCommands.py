from dronekit import *
import time
import argparse
from pymavlink import mavutil
from plotRoutes import plotLiveSimpleFacade
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np

def connectDrone():
    print('Connecting.............................')
    connection_string = '/dev/ttyAMA0'
    baud_rate = 115200
    print('Connection to the vehicle on %s'%connection_string)
    vehicle = connect(connection_string, baud=baud_rate,wait_ready=True)
    return vehicle

def connectSITL():
    print('Connecting.............................')
    connection_string = 'tcp:127.0.0.1:5672'
    baud_rate = 921600
    vehicle = connect(connection_string, baud=baud_rate,wait_ready=True)
    print('Connection to the vehicle on %s'%connection_string)
    return vehicle

def arm_and_wait(vehicle):
    print('Arming')
    vehicle.armed = True
    print('........................')
    print('Armed')

def clear_mission(vehicle):
    cmds = vehicle.commands
    vehicle.commands.clear()
    vehicle.flush()

    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()
    print("Mission Cleared")

def download_mission(vehicle):

    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()  # wait until download is complete.

def get_current_mission(vehicle):

    print("Downloading mission")
    download_mission(vehicle)
    missionList = []
    n_WP = 0
    for wp in vehicle.commands:
        missionList.append(wp)
        n_WP += 1

    return n_WP, missionList

def ChangeMode(vehicle, mode):
    while vehicle.mode != VehicleMode(mode):
        vehicle.mode = VehicleMode(mode)
        time.sleep(0.5)
        print("Mode changed to: " + mode)
    return True

def readmission(aFileName, vehicle):
    print("\nReading mission from file: %s" % aFileName)
    cmds = vehicle.commands
    missionlist=[]
    with open(aFileName) as f:
        for i, line in enumerate(f):
            if i==0:
                if not line.startswith('QGC WPL 110'):
                    raise Exception('File is not supported WP version')
            else:
                linearray=line.split(' ')
                ln_index=int(linearray[0])
                ln_currentwp=int(linearray[1])
                ln_frame=int(linearray[2])
                ln_command=int(linearray[3])
                ln_param1=float(linearray[4])
                ln_param2=float(linearray[5])
                ln_param3=float(linearray[6])
                ln_param4=float(linearray[7])
                ln_param5=float(linearray[8])
                ln_param6=float(linearray[9])
                ln_param7=float(linearray[10])
                ln_autocontinue=int(linearray[11].strip())
                cmd = Command( 0, 0, 0, ln_frame, ln_command, ln_currentwp, ln_autocontinue, ln_param1, ln_param2, ln_param3, ln_param4, ln_param5, ln_param6, ln_param7)
                missionlist.append(cmd)
    return missionlist

def upload_mission(aFileName, vehicle):
    # Read mission from file
    missionlist = readmission(aFileName,vehicle)

    print("\nUpload mission from a file: %s" % aFileName)
    # Clear existing mission from vehicle
    print(' Clear mission')
    cmds = vehicle.commands
    cmds.clear()
    # Add new mission to vehicle
    for command in missionlist:
        cmds.add(command)
    print(' Upload mission')
    vehicle.commands.upload()

def printStatus(vehicle):
    print("-------------------------------------------------------------------------------")
    print("STAUTS:")
    vehicle.wait_ready('autopilot_version')
    print('Autopilot version: %s'%vehicle.version)
    print('%s'% vehicle.location.global_relative_frame)
    print('%s'% vehicle.attitude)
    print('Velocity [North, East, Down]: %s'%vehicle.velocity + " m/s")
    print('Last Heartbeat: %s'%vehicle.last_heartbeat)
    print('Is the vehicle armable: %s'%vehicle.is_armable)
    print('Airspeed: %s'% vehicle.airspeed)
    print('Mode: %s'% vehicle.mode.name)
    print('Armed: %s'%vehicle.armed)
    print("-------------------------------------------------------------------------------")

def arm_and_takeoff(vehicle,hmax):

    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(5)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off")
    vehicle.simple_takeoff(hmax)

    while True:
        print(" Altitude: " + str(vehicle.location.global_relative_frame.alt))
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=hmax*0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def MissionStart(vehicle,hmax):
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