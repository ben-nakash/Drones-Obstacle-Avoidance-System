# from lidar_lite import LidarLite
from simulator import Simulator


class Sensors:

    def __init__(self):
        self.simulator = Simulator()
        # When not simulating the data, we will use this class object to get the data from the sensors.
        # self.lidar = LidarLite()
        return

    def connect(self):
        # Since I simulate the data within the software there's no need to connect to the sensors,
        # and for this reason this code is under comment, and this method returns a constant value just
        # to be simbolic and to show that this step is needed.
        # for i in range(0, 5):
        #     if self.lidar.connect(1) < -1:
        #         continue
        #     else:
        #         return 0
        # return -1
        return 0

    def check_ahead(self):
        # Get data from file since I use a simulator.
        ahead_read = self.simulator.ahead_reading()

        # When not simulating the data - next line will be instead in order to get real data from sensor
        # ahead_read = self.lidar.get_distance()
        return ahead_read

    def check_left_side(self):
        # Get data from file since I use a simulator.
        left_side_read = self.simulator.left_reading()
        return left_side_read

    def check_right_side(self):
        # Get data from file since I use a simulator.
        right_side_read = self.simulator.right_reading()
        return right_side_read

    def check_below(self):
        # Get data from file since I use a simulator.
        below_read = self.simulator.below_reading()
        return below_read