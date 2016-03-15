import smbus
import time


class LidarLite:
    def __init__(self):
        self.address = 0x62
        self.distWriteReg = 0x00
        self.distWriteVal = 0x04
        self.distReadReg1 = 0x8f
        self.distReadReg2 = 0x10
        self.velWriteReg = 0x04
        self.velWriteVal = 0x08
        self.velReadReg = 0x09

    def connect(self, bus):
        try:
            self.bus = smbus.SMBus(bus)
            time.sleep(0.5)
            return 0
        except:
            return -1

    def write_and_wait(self, register, value):
        self.bus.write_byte_data(self.address, register, value)
        time.sleep(0.02)

    def read_and_wait(self, register):
        res = self.bus.read_byte_data(self.address, register)
        time.sleep(0.02)
        return res

    def get_distance(self):
        self.write_and_wait(self.distWriteReg, self.distWriteVal)
        dist1 = self.read_and_wait(self.distReadReg1)
        dist2 = self.read_and_wait(self.distReadReg2)
        return (dist1 << 8) + dist2

    def get_velocity(self):
        self.write_and_wait(self.distWriteReg, self.distWriteVal)
        self.write_and_wait(self.velWriteReg, self.velWriteVal)
        vel = self.read_and_wait(self.velReadReg)
        return self.signed_int(vel)

    def signed_int(self, value):
        if value > 127:
            return (256-value) * (-1)
        else:
            return value
