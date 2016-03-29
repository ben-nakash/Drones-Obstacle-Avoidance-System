import math
# from tester import Test
import simulator


class DistanceCalculator:

    def __init__(self, test_num):
        self.scenario = test_num
    #     self.tester = Test(test_num)

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        earth_radius = 6371
        dis_lat = self.degree_to_radian(lat2-lat1)
        dis_lon = self.degree_to_radian(lon2-lon1)
        a = math.sin(dis_lat/2) * math.sin(dis_lat/2) + \
            math.cos(self.degree_to_radian(lat1)) * math.cos(self.degree_to_radian(lat2))\
            * math.sin(dis_lon/2) * math.sin(dis_lon/2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance_in_meters = earth_radius * c * 1000
        return distance_in_meters

    def degree_to_radian(self, deg):
        return deg * (math.pi/180)

    # This method goes to Location library shai would provide in order
    # to get the current latitude of the drone
    def get_current_latitude(self):
        latitude = simulator.latitude_reading(self.scenario)
        return latitude

    # This method goes to Location library shai would provide in order
    # to get the current longitude of the drone
    def get_current_longitude(self):
        longitude = simulator.longitude_reading(self.scenario)
        return longitude

    # This method goes to Location library shai would provide in order
    # to get the current height of the drone
    def get_current_height(self):
        height = simulator.height_reading(self.scenario)
        return height
