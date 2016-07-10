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


# Returns front sensor simulated measurament
def ahead_reading():
    time.sleep(0.1)
    return int(__middleSensorData.readline())


# Returns left sensor simulated measurament
def left_reading():
    return int(__leftSensorData.readline())


# Returns right sensor simulated measurament
def right_reading():
    return int(__rightSensorData.readline())


# Returns below sensor simulated measurament
def below_reading():
    global __below_reading
    return __below_reading


# Returns the simulated height of the drone given by the Pixhawk flight controller.
def height_reading():
    global __height
    return __height


# Returns the simulated latitude position of the drone given by the Pixhawk flight controller.
def latitude_reading():
    global __latitude
    return __latitude


# Returns the simulated longitude position of the drone given by the Pixhawk flight controller
def longitude_reading():
    global __longitude
    return __longitude


# When the drone is ordered to move to the left/right, this method changes the simulated longitude/latitude values
# of the drone to simulate a change in its position.
def change_longitude_latitude():
    global __latitude
    global __longitude
    __longitude += random.uniform(1, 3) * 0.00000001
    __latitude += random.uniform(1, 3) * 0.00000004


# When the front sensor's data indicates there's no obstacle, the simulator need to skip the matching lines in the
# other files that represents the other sensors
def skip():
    __leftSensorData.readline()
    __rightSensorData.readline()
    return


# When the drone is ordered to ascend, this method increases the simulated values of the height of the drone given by
# the Pixhawk flight controller and the below sensor height measurament.
def go_up():
    global __below_reading
    global __height
    __height += int(random.uniform(10, 25))
    __below_reading += int(random.uniform(10, 25))
    return __below_reading


# When the drone is ordered to descend, this method decreases the simulated values of the height of the drone given by
# the Pixhawk flight controller and the below sensor height measurament.
def go_down():
    global __below_reading
    global __height
    __height -= int(random.uniform(10, 25))
    __below_reading -= int(random.uniform(10, 25))
    return __below_reading


# This method changes the simulated values of the height of the drone given by the Pixhawk flight controller
# and the below sensor height measurament. It's been called after every reading from the front sensor to simulate
# a height difference for more realistic simulation.
def altitude_change():
    global __below_reading
    global __height
    __below_reading += int(random.uniform(-15, 15))
    __height = __below_reading + int(random.uniform(0, 23))
