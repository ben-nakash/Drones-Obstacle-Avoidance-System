import random
import time


class Simulator:

    def __init__(self):
        self.__start_time = round(time.time())
        self.__below_reading = 1000
        self.__height = 800
        self.__latitude = 0
        self.__longitude = 0
        self.__index = -1
        try:
            self.__leftSensorData = open('Sensors Data\\leftSensorData.txt', 'r')
            self.__middleSensorData = open('Sensors Data\\middleSensorData.txt', 'r')
            self.__rightSensorData = open('Sensors Data\\rightSensorData.txt', 'r')
        except:
            print("Error: Can't open sensors data file")
        return

    def ahead_reading(self):
        time.sleep(0.01)
        return int(self.__middleSensorData.readline())

    def left_reading(self):
        return int(self.__leftSensorData.readline())

    def right_reading(self):
        return int(self.__rightSensorData.readline())

    def below_reading(self):
        self.__below_reading += int(random.uniform(-20,20))
        return self.__below_reading

    def height_reading(self):
        self.__height += random.uniform(1, 10) * 0.15
        return self.__height

    def latitude_reading(self):
        self.__latitude += random.uniform(1, 3) * 0.00000004
        return self.__latitude

    def longitude_reading(self):
        self.__longitude += random.uniform(1, 3) * 0.00000001
        return self.__longitude

    def skip(self):
        self.__leftSensorData.readline()
        self.__rightSensorData.readline()
        return
