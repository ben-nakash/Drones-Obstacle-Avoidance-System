import random
import time


class Simulator:

    start_time = round(time.time())
    height = 0
    latitude = 0
    longitude = 0
    index = -1

    def __init__(self):
        try:
            self.sensors_data_file = open('Sensors Data\\SensorData.txt', 'r')
        except:
            print("Error: Can't open sensors data file")
        return

    def ahead_reading(self):
        time.sleep(1)
        return int(self.sensors_data_file.readline())

    def left_reading(self):
        return int(self.sensors_data_file.readline())

    def right_reading(self):
        return int(self.sensors_data_file.readline())

    def below_reading(self):
        # Returns a constant value since
        return 20.0

    def height_reading(self):
        self.height += random.randint(1, 10) * 0.15
        return self.height

    def latitude_reading(self):
        self.latitude += random.randint(1, 3) * 0.000001
        return self.latitude

    def longitude_reading(self):
        self.longitude += random.randint(1, 3) * 0.000001
        return self.longitude
