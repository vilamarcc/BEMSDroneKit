import math

def  DistanceBetweenCoordinates(lat1, lon1, lat2, lon2):
    R = 6378 # Earth radius in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = math.sin(dLat/2)*math.sin(dLat/2) + math.sin(dLon/2)*math.sin(dLon/2)*math.cos(lat1)*math.cos(lat2)
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = (R*c)*1000
    return distance, a # Distance in m 

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
    return lat2, lon2