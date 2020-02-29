import math
import numpy as np

def  getDistanceBetweenCoordinates(lat1, lon1, lat2, lon2):
    R = 6378 # Earth radius in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = math.sin(dLat/2)*math.sin(dLat/2) + math.sin(dLon/2)*math.sin(dLon/2)*math.cos(lat1)*math.cos(lat2)
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = round((R*c)*1000,3)
    return distance # Distance in m 

def getLocationAtBearing(lat1, lon1, distance, angle):
    R = 6378 # Earth radius in km
    distance = distance/1000 # Distance in km
    lat1 = math.radians(lat1) # Current lat point converted to radians
    lon1 = math.radians(lon1) # Current long point converted to radians
    lat2 = math.degrees(math.asin(math.sin(lat1)*math.cos(distance/R) + math.cos(lat1)*math.sin(distance/R)*math.cos(angle)))
    lat2 = round(lat2, 8)
    lon2 = math.degrees(lon1 + math.atan2(math.sin(angle)*math.sin(distance/R)*math.cos(lat1), math.cos(distance/R) - math.sin(lat1)*math.sin(lat2)))
    lon2 = round(lon2, 8)
    return lat2, lon2

def getBearingBetweenCoordinates(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lon1 = math.radians(lon1)
    lon2 = math.radians(lon2)
    y = math.sin(lon2-lon1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1)*math.cos(lon2)*math.cos(lon2-lon1)
    brng = math.atan2(y, x)
    return brng #Bearing in radians

def getIntersectionBetweenCoordinates(lat1,lon1,brng1,lat2,lon2,brng2): #bearings in radians coords in degrees
    φ1 = math.radians(lat1)
    φ2 = math.radians(lat2)
    λ1 = math.radians(lon1)
    λ2 = math.radians(lon2)
    θ13 = brng1
    θ23 = brng2
    Δφ = φ2 - φ1
    Δλ = λ2 - λ1
    δ12 = 2 * math.asin(math.sqrt(math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2)))
    cosθa = (math.sin(φ2) - math.sin(φ1)*math.cos(δ12)) / (math.sin(δ12)*math.cos(φ1))
    cosθb = (math.sin(φ1) - math.sin(φ2)*math.cos(δ12)) / (math.sin(δ12)*math.cos(φ2))
    θa = math.acos(min(max(cosθa, -1), 1))
    θb = math.acos(min(max(cosθb, -1), 1))
    θ12 = math.sin(λ2 - λ1)
    if (math.sin(λ2 - λ1) > 0):
        θ12 = θa
        θ21 = 2*np.pi - θb
    else:
        θ12 = 2*np.pi - θa
        θ21 = θb  

    α1 = θ13 - θ12 #angle 2-1-3
    α2 = θ21 - θ23 #angle 1-2-3

    if (math.sin(α1) == 0 and math.sin(α2) == 0):
        return 0,0  #infinite intersections
    if (math.sin(α1) * math.sin(α2) < 0): 
        return 0,0  #ambiguous intersection
    
    cosα3 = -math.cos(α1)*math.cos(α2) + math.sin(α1)*math.sin(α2)*math.cos(δ12)
    δ13 = math.atan2(math.sin(δ12)*math.sin(α1)*math.sin(α2), math.cos(α2) + math.cos(α1)*cosα3)

    φ3 = math.asin(math.sin(φ1)*math.cos(δ13) + math.cos(φ1)*math.sin(δ13)*math.cos(θ13))
    Δλ13 = math.atan2(math.sin(θ13)*math.sin(δ13)*math.cos(φ1), math.cos(δ13) - math.sin(φ1)*math.sin(φ3))
    λ3 = λ1 + Δλ13
    return math.degrees(φ3), math.degrees(λ3) #[lat,lon] in degrees

def fromXYtoLatLong(X,Y,lat1,lon1):
    R = 6371 * 1000
    d = np.sqrt((X * X) + (Y * Y))
    brng = math.atan2(Y, - X) - (np.pi / 2)
    φ1 = lat1 * (np.pi / 180)
    λ1 = lon1 * (np.pi / 180)
    φ2 = math.asin(math.sin(φ1) * math.cos(d / R) + math.cos(φ1) * math.sin(d / R) * math.cos(brng))
    λ2 = λ1 + math.atan2(math.sin(brng) * math.sin(d / R) * math.cos(φ1), math.cos(d / R) - math.sin(φ1) * math.sin(φ2))

    return math.degrees(φ2),math.degrees(λ2)