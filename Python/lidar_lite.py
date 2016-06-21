import smbus
import time


class LidarLite:

    __ADDRESS = 0x62
    __DIST_WRITE_REG = 0x00
    __DIST_WRITE_VAL = 0x04
    __DIST_READ_REG1 = 0x8f
    __DIST_READ_REG2 = 0x10

    def __init__(self, bus):
        self.__bus = bus

    def connect(self):
        try:
            self.__bus = smbus.SMBus(self.__bus)
            time.sleep(0.5)
            return 0
        except:
            return -1

    def __write_and_wait(self, register, value):
        self.__bus.write_byte_data(self.__ADDRESS, register, value)
        time.sleep(0.02)

    def __read_and_wait(self, register):
        res = self.__bus.read_byte_data(self.__ADDRESS, register)
        time.sleep(0.02)
        return res

    def get_distance(self):
        self.__write_and_wait(self.__DIST_WRITE_REG, self.__DIST_WRITE_VAL)
        dist1 = self.__read_and_wait(self.__DIST_READ_REG1)
        dist2 = self.__read_and_wait(self.__DIST_READ_REG2)
        return int((dist1 << 8) + dist2)