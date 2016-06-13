import random
import time


class Simulator:

    def __init__(self):
        self.__start_time = round(time.time())
        self.__height = 0
        self.__latitude = 0
        self.__longitude = 0
        self.__index = -1
        try:
            self.sensors_data_file = open('Sensors Data\\SensorData.txt', 'r')
        except:
            print("Error: Can't open sensors data file")
        return

    def ahead_reading(self):
        time.sleep(1)
        return float(self.sensors_data_file.readline())

    def left_reading(self):
        return float(self.sensors_data_file.readline())

    def right_reading(self):
        return float(self.sensors_data_file.readline())

    def below_reading(self):
        return 20.0

    def height_reading(self):
        self.__height += random.uniform(1, 10) * 0.15
        return self.__height

    def latitude_reading(self):
        self.__latitude += random.uniform(1, 3) * 0.000001
        return self.__latitude

    def longitude_reading(self):
        self.__longitude += random.uniform(1, 3) * 0.000001
        return self.__longitude
