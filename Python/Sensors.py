from lidar_lite import LidarLite


class Sensors:

    def __init__(self):
        self.ahead_read = None
        self.left_side_read = None
        self.right_side_read = None
        self.lidar = LidarLite()
        self.serial_port_reading = 0

    def connect(self):
        for i in range(0, 5):
            if self.lidar.connect(4) is not 0:
                continue
            else:
                return 0
        return -1

    def check_ahead(self):
        # return int(input("Enter Ahead Distance: "))
        # return random.randint(800,6000)
        return self.ahead_read

    def check_left_side(self):
        # return int(input("Enter left Distance: "))
        # return random.randint(2000,2100)
        return self.left_side_read

    def check_right_side(self):
        # return int(input("Enter right Distance: "))
        # return random.randint(2000,2100)
        return self.right_side_read
