from dronekit import *
import time
import argparse
from pymavlink import mavutil

def connectDrone(connection_string):
    
    #connection_string = '/dev/ttyAMA0'
    baud_rate = 921600
    print('Connection to the vehicle on %s'%connection_string)
    vehicle = connect(connection_string, baud=baud_rate,wait_ready=True)
    return vehicle


