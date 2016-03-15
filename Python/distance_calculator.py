import math

def calculate_distance(lat1,lon1,lat2,lon2):
    earthRadius = 6371
    dLat = degree_to_radian(lat2-lat1)
    dLon = degree_to_radian(lon2-lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(degree_to_radian(lat1)) * math.cos(degree_to_radian(lat2))\
        * math.sin(dLon/2) * math.sin(dLon/2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distanceInMeters = (earthRadius * c) * 1000
    return distanceInMeters


def degree_to_radian(deg):
    return deg * (math.pi/180)


# This method goes to Location library shai would provide in order
# to get the current latitude of the drone
def get_current_latitude():
    return

# This method goes to Location library shai would provide in order
# to get the current longitude of the drone
def get_current_longitude():
    return

# This method goes to Location library shai would provide in order
# to get the current height of the drone
def get_current_height():
    return