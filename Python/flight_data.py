import math
from simulator import Simulator


class FlightData:

    __EARTH_RADIUS_IN_METERS = 6371000

    # This module should have this constructor which gets a vehicle object in order to send the proper orders
    # to the drone. Since I can't initialize this object, This section and all vehicle-related commands
    # are under comment.
    
    # def __init__(self, vehicle):
    #     # Check for correct input
    #     if isinstance(vehicle, Vehicle) is False:
    #         raise TypeError('Expected object of type Vehicle, got '+type(vehicle).__name__)
    #
    #     self.__simulator = Simulator()
    #     self.__vehicle = vehicle
    #     return

    def __init__(self):
        self.__simulator = Simulator()
        return

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        phi1 = self.__degree_to_radian(lat1)
        phi2 = self.__degree_to_radian(lat2)
        dPhi = self.__degree_to_radian((lat2-lat1))
        dLambda = self.__degree_to_radian(lon2-lon1)

        a = math.sin(dPhi/2)*math.sin(dPhi/2) + math.cos(phi1)*math.cos(phi2)*math.sin(dLambda/2)*math.sin(dLambda/2)
        c = 2* math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance_in_meters = self.__EARTH_RADIUS_IN_METERS*c
        return distance_in_meters

    def __degree_to_radian(self, deg):
        return deg * (math.pi/180)

    def get_current_latitude(self):
        latitude = float(self.__simulator.latitude_reading())
        # latitude = self.__vehicle.get_location_latitude()
        return latitude

    def get_current_longitude(self):
        longitude = float(self.__simulator.longitude_reading())
        # longitude = self.__vehicle.get_location_longitude()
        return longitude

    def get_current_height(self):
        height = float(self.__simulator.height_reading())
        # height = self.__vehicle.get_location_altitude()
        return height
