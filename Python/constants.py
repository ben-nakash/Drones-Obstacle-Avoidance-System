class Constants:

    def LEFT(self):
        return "left"

    def RIGHT(self):
        return "right"

    def UP(self):
        return "up"

    def DEVIATION(self):
        return 20

    def WARNING_DISTANCE(self):
        return 4000.0

    def DANGER_DISTANCE(self):
        return 1000.0

    def DANGER_ALTITUDE(self):
        return 20.0

    def MAX_LEFT_RIGHT(self):
        return 10.0

    def EARTH_RADIUS_IN_METERS(self):
        return 6371000.0

    def ADDRESS(self):
        return 0x62

    def DIST_WRITE_REG(self):
        return 0x00

    def DIST_WRITE_VAL(self):
        return 0x04

    def DIST_READ_REG1(self):
        return 0x8f

    def DIST_READ_REG2(self):
        return 0x10

    def RIGHT_SENSOR_BUSS(self):
        return 1

    def LEFT_SENSOR_BUSS(self):
        return 2

    def FRONT_SENSOR_BUSS(self):
        return 3

    def BOTTOM_SENSOR_BUSS(self):
        return 4

    def LATITUDE_LONGITUDE_CONST(self):
        return 0.000001

    def HEIGHT_CONST(self):
        return 0.15

    def DISTANCE_FROM_GROUND_CONST(self):
        return 20