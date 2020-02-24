from dronekit import connect, VehicleMode, LocationGlobalRelative,Command, LocationGlobal
import time
import argparse
from pymavlink import mavutil


def connectRover():
    parser = argparse.ArgumentParser(description = 'commands')
    parser.add_argument('--connect')
    args = parser.parse_args()

    connection_string = args.connect
    print('Connection to the vehicle on %s'%connection_string)
    vehicle = connect(connection_string,wait_ready=True)
    return vehicle

def arm_and_wait():
    print('Arming')
    while not vehicle.is_armable:
        time.sleep(1)
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    print('........................')
    print('Armed')

def clear_mission(vehicle):
    """
    Clear the current mission.
    """
    cmds = vehicle.commands
    vehicle.commands.clear()
    vehicle.flush()

    # After clearing the mission you MUST re-download the mission from the vehicle
    # before vehicle.commands can be used again
    # (see https://github.com/dronekit/dronekit-python/issues/230)
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()

def download_mission(vehicle):
    """
    Download the current mission from the vehicle.
    """
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()  # wait until download is complete.

def get_current_mission(vehicle):
    """
    Downloads the mission and returns the wp list and number of WP

    Input:
        vehicle

    Return:
        n_wp, wpList
    """

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
    return True

def readmission(aFileName):
    """
    This function is used by upload_mission().
    """
    print("\nReading mission from file: %s" % aFileName)
    cmds = vehicle.commands
    missionlist=[]
    with open(aFileName) as f:
        for i, line in enumerate(f):
            if i==0:
                if not line.startswith('QGC WPL 110'):
                    raise Exception('File is not supported WP version')
            else:
                linearray=line.split('\t')
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

def upload_mission(aFileName):
    """
    Upload a mission from a file.
    """
    # Read mission from file
    missionlist = readmission(aFileName)

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


############################################
################   MAIN    #################
############################################

print('Connecting...')
vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True)
clear_mission(vehicle)
import_mission_filename = 'SuperRover.txt'
upload_mission(import_mission_filename)

n_WP, missionList = get_current_mission(vehicle)
time.sleep(2)
arm_and_wait()
vehicle.groudspeed = 5

if n_WP > 0:
    print ("A valid mission has been uploaded!")
    visto_bueno = True
    print("Changing to AUTO")
    ChangeMode(vehicle, "AUTO")
    time.sleep(2)
else:
    print ('Error, closing vehicle')

if visto_bueno == True:
    t = True
    while t == True:
        print("Mission started")
        print("Current WP: %d of %d " % (vehicle.commands.next, vehicle.commands.count))
        if vehicle.commands.next == vehicle.commands.count:
            print("Final waypoint reached")
            #borramos mision y cerramos vehiculo
            clear_mission(vehicle)
            print("Mission deleted")
            t = False
        time.sleep(5)

print ('Mision Finalizada...............................')
print ('Closing vehicle')
vehicle.close()