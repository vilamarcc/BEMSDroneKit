# GROUP 5 / ROVERADDICT / Eduard & Hector

import math
import time
import serial
import threading

from dronekit import connect, VehicleMode, LocationGlobal
#from PyCRC.CRCCCITT import CRCCCITT

##### FUNCTIONS #####

# Connecting Pixhawk with Raspberry Pi
def ConnectingPixhawkRaspi():
    print('Connecting Pixhawk with Raspberry Pi...')
    vehicle = connect('/dev/ttyAMA0', baud=921600, wait_ready=True)
    print('Connected')
    return vehicle

# Enabling Raspberry Pi serial port function
def EnablingSerialRaspi():
    print('Enabling Raspberry Pi serial port...')
    ser = serial.Serial(
        port = '/dev/ttyUSB0',
        baudrate = 57600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 100
        )
    print('Enabled')
    return ser

# Function for code telemetry
def SendingTelemetry():
    ID = 3 # Change by your ID number
    Lat = int(round(vehicle.location.global_frame.lat, 5)*100000)
    print(Lat)
    Lon = int(round(vehicle.location.global_frame.lon, 5)*100000)
    Vel = int(round(vehicle.groundspeed, 2)*100)
    Track = int(vehicle.heading)
    TurnRate = int(math.degrees(round(vehicle.attitude.yaw, 4)))
    word_int1 = TurnRate + (Track<<16) + (Vel<<(16*2)) + (Lon<<(16*3)) + (Lat<<(16*3+32)) + (ID<<(16*3+32*2))
    word_string1 = str(word_int1)
    CRC = 0
    word_int2 = CRC + (TurnRate<<16) + (Track<<(16*2)) + (Vel<<(16*3)) + (Lon<<(16*4)) + (Lat<<(16*4+32)) + (ID<<(16*4+32*2))
    word_string2 = str(word_int2)
    word_binary = bin(word_int2)[2:].zfill(132)
    print(word_string2)
    print(word_binary)
  #  print(CRC)
    return word_string2

# Function for decode telemetry
def ReceivingTelemetry(word):
    try:
        word = int(word)
        ID = (word & 5104235503814076951950619111476523171840)>>128
        print('ID ' + str(ID))
        Lat = float((word & 340282366841710300949110269838224261120)>>96)/100000
        print('Lat ' + str(Lat))
        Lon = float((word & 79228162495817593519834398720)>>64)/100000
        print('Lon ' + str(Lon))
        Vel = float((word & 18446462598732840960)>>48)/100
        print('Vel ' + str(Vel))
        Track = (word & 281470681743360)>>32
        print('Track ' + str(Track))
        TurnRate = round(((word & 4294901760)>>16), 4)
        print('TurnRate ' + str(TurnRate))
#        ID_CRC = int(ID)
#        Lat_CRC = int(round(Lat, 5)*100000)
#        Lon_CRC = int(round(Lon, 5)*100000)
#        Vel_CRC = int(round(Vel, 2)*100)
#        Track_CRC = int(Track)
#        TurnRate_CRC = int(math.degrees(round(TurnRate, 4)))
        #word_int = TurnRate_CRC + (Track_CRC<<16) + (Vel_CRC<<(16*2)) + (Lon_CRC<<(16*3)) + (Lat_CRC<<(16*3+32)) + (ID_CRC<<(16*3+32*2))
       # word_string = str(word_int)
        #CRC_CRC = CRCCCITT().calculate(word_string)
        #print(CRC_CRC)       
	return ID, Lat, Lon, Vel, Track, TurnRate
    except ValueError:
        print('Value error exception triggered')


# Function for compute the distance between two coordinates
def  DistanceBetweenCoordinates(lat1, lon1, lat2, lon2):
    R = 6378 # Earth radius in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = math.sin(dLat/2)*math.sin(dLat/2) + math.sin(dLon/2)*math.sin(dLon/2)*math.cos(lat1)*math.cos(lat2)
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = round((R*c)*1000, 2)
    print(distance)
    return distance, a # Distance in m 

# Function for get coordinates given current position, distance and bearing
def FinalCoordinates(lat1, lon1, distance, angle):
    R = 6378 # Earth radius in km
    angle = math.radians(angle) # Angle in radians
    distance = distance/1000 # Distance in km
    lat1 = math.radians(lat1) # Current lat point converted to radians
    lon1 = math.radians(lon1) # Current long point converted to radians
    lat2 = math.degrees(math.asin(math.sin(lat1)*math.cos(distance/R) + math.cos(lat1)*math.sin(distance/R)*math.cos(angle)))
    lat2 = round(lat2, 5)
    lon2 = math.degrees(lon1 + math.atan2(math.sin(angle)*math.sin(distance/R)*math.cos(lat1), math.cos(distance/R) - math.sin(lat1)*math.sin(lat2)))
    lon2 = round(lon2, 5)
    print(lat2)
    print(lon2)
    return lat2, lon2

def CalculateTau2(dist, v1, v2, track1, track2, angle):
	print ('CALCULATING TAU...')
	print ('dist ' + str(dist) )
	print ('track1 ' + str(track1))
	print ('track2 ' + str(track2))
	print ('v1 ' + str(v1))
	print ('v2 ' + str(v2))
	r2 = dist**2
	DMOD = 4
	x1 = 0
	y1 = 0
	x2 = dist*math.sin(angle)
	y2 = dist*math.cos(angle)
	track1 = math.radians(track1)
	track2 = math.radians(track2)
	v1x = v1*math.sin(track1)
	v1y = v1*math.cos(track1)
	v2x = v2*math.sin(track2)
	v2y = v2*math.cos(track2)
	rx = x2-x1
	ry = y2-y1
	rdotx =  v2x-v1x
	rdoty = v2y-v1y
	denom = rx*rdotx+ry*rdoty
	numer = r2-DMOD**2
	if denom == 0:
		tau = 1000
	else:
		tau = numer/denom
	print('tau ' + str(-tau))
	return -tau
	 
	

def WRITE():
    while 1:
        print('Sending telemetry...')
        word_sended = SendingTelemetry()
        ser.write('0' +word_sended + '\n')
        time.sleep(0.5)

def READ():
    count = 0
    while 1:
        print('Receiving telemetry...')
#	try:
        word_received = ser.readline()
	print('word: '+ word_received) 
        [ID, Lat, Lon, Vel, Track, TurnRate] = ReceivingTelemetry(word_received)
	if (ID > 5 or ID < 1) or (Lat < 41.27393 or Lat >41.27702) or (Lon > 1.98960 or Lon < 1.98352) or (Vel < 0):
		print ('Corrupted Message, next')
	else:
        	[distance, angle] = DistanceBetweenCoordinates(vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, Lat, Lon)
        	print('distance ' + str(distance) + '\n')
		tau = CalculateTau2(distance, vehicle.groundspeed, Vel, vehicle.heading, Track, angle)
              	[final_Lat, final_Lon] = FinalCoordinates(vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, 5, 90)
		if(distance < 4):
			vehicle.mode = VehicleMode("HOLD")
			print("CONFLICT DISTANCE DETECTED, VEHICLE HOLDING")
			print(vehicle.mode)
			count = 0
		elif(tau > 0 and tau < 15):
#			vehicle.mode = VehicleMode("HOLD")
			vehicle.mode = VehicleMode('GUIDED')
			location = LocationGlobal(final_Lat, final_Lon, 3)
			vehicle.simple_goto(location,groundspeed=2)
			print("CONFLICT TAU DETECTED, VEHICLE HOLDING")
			print(vehicle.mode)
			count = 0
		else:
			count = count + 1
			if (count >= 50):
				vehicle.mode = VehicleMode("AUTO")
				print("NO MORE CONFLICT DETECTED CONTINUING MISSION")
				print("---------------------------------------------------------------------------------")
	print(vehicle.mode)
#	                vehicle.mode = VehicleMode('GUIDED')
#	                location = LocationGlobal(final_Lat, final_Lon, 3)
#	                vehicle.simple_goto(location, groundspeed = 2)
#	except:
#		print('Exception triggered in function READ')


##### MAIN #####

# Connecting Pixhawk with Raspberry Pi
vehicle = ConnectingPixhawkRaspi()

# Enabling Raspberry Pi serial port
ser = EnablingSerialRaspi()

t = threading.Thread(target=WRITE, name='WRITE')
w = threading.Thread(target=READ, name='READ')

t.start()
time.sleep(5)
w.start()
