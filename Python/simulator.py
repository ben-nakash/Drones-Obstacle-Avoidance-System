import random
import time

start_time = round(time.time())
__below_reading = 1000
__height = 1000
__latitude = 0
__longitude = 0

try:
    __leftSensorData = open('Sensors Data\\leftSensorData.txt', 'r')
    __middleSensorData = open('Sensors Data\\middleSensorData.txt', 'r')
    __rightSensorData = open('Sensors Data\\rightSensorData.txt', 'r')
except:
    print("Error: Can't open sensors data file")


def ahead_reading():
    time.sleep(0.1)
    return int(__middleSensorData.readline())


def left_reading():
    return int(__leftSensorData.readline())


def right_reading():
    return int(__rightSensorData.readline())


def below_reading():
    global __below_reading
    return __below_reading


def height_reading():
    global __height
    return __height


def latitude_reading():
    global __latitude
    return __latitude


def longitude_reading():
    global __longitude
    return __longitude


def change_longitude_latitude():
    global __latitude
    global __longitude
    __longitude += random.uniform(1, 3) * 0.00000001
    __latitude += random.uniform(1, 3) * 0.00000004


def skip():
    __leftSensorData.readline()
    __rightSensorData.readline()
    return


def go_up():
    global __below_reading
    global __height
    __height += int(random.uniform(10, 25))
    __below_reading += int(random.uniform(10, 25))
    return __below_reading


def go_down():
    global __below_reading
    global __height
    __height -= int(random.uniform(10, 25))
    __below_reading -= int(random.uniform(10, 25))
    return __below_reading


def altitude_change():
    global __below_reading
    global __height
    __below_reading += int(random.uniform(-15, 15))
    __height = __below_reading + int(random.uniform(0, 23))
