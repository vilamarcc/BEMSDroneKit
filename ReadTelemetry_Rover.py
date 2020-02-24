from dronekit import connect, VehicleMode, LocationGlobalRelative,Command, LocationGlobal
import time
import argparse
from pymavlink import mavutil

###################################
###########Functions###############
###################################

def connectRover():

    connection_string = '/dev/ttyAMA0'
    baud_rate = 921600
    print('Connection to the vehicle on %s'%connection_string)
    vehicle = connect(connection_string, baud=baud_rate,wait_ready=True)
    return vehicle


################   MAIN    #################

print('Connecting...')
vehicle = connectRover()


vehicle.wait_ready('autopilot_version')
print('Autopilot version: %s'%vehicle.version)

#- Read the actual position
print('Position: %s'% vehicle.location.global_relative_frame)

#- Read the actual attitude roll, pitch, yaw
print('Attitude: %s'% vehicle.attitude)

#- Read the actual velocity (m/s)
print('Velocity: %s'%vehicle.velocity) #- North, east, down

#- When did we receive the last heartbeat
print('Last Heartbeat: %s'%vehicle.last_heartbeat)

#- Is the vehicle good to Arm?
print('Is the vehicle armable: %s'%vehicle.is_armable)

#- Which is the total ground speed?   Note: this is settable
print('Groundspeed: %s'% vehicle.groundspeed) #(%)

#- What is the actual flight mode?    Note: this is settable
print('Mode: %s'% vehicle.mode.name)

#- Is the vehicle armed               Note: this is settable
print('Armed: %s'%vehicle.armed)