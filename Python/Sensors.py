from lidar_lite import LidarLite
import simulator


class Sensors:

    def __init__(self, test_num):
        self.scenario = test_num
        self.lidar = LidarLite()

    def connect(self):
        for i in range(0, 5):
            if self.lidar.connect(1) < -1:
                continue
            else:
                return 0
        return -1

    def check_ahead(self):
        ahead_read = self.lidar.get_distance()
        # return int(input("Enter Ahead Distance: "))
        # return random.randint(800,6000)
        # ahead_read = simulator.ahead_reading(self.scenario)
        return ahead_read

    def check_left_side(self):
        # return int(input("Enter left Distance: "))
        # return random.randint(2000,2100)
        left_side_read = simulator.left_reading(self.scenario)
        return left_side_read

    def check_right_side(self):
        # return int(input("Enter right Distance: "))
        # return random.randint(2000,2100)
        right_side_read = simulator.right_reading(self.scenario)
        return right_side_read
