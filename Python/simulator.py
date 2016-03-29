import random
import time

start_time = round(time.time())
ahead = [4500, 4100, 5000, 3900, 3700, 3500, 3200, 4300, 3500, 3800]
left = [0, 0, 0, 2000, 2200, 2022, 2103, 2015, 2300, 2312]
right = [0, 0, 0, 1800, 2000, 1982, 1762, 1974, 2000, 2100]
height = 0
latitude = 0
longitude = 0
index = -1

def ahead_reading(scenario):
    global ahead
    global index
    index = index+1
    if scenario == 1:
        time.sleep(1)
        # if round(time.time()) - start_time < 3:
        #     return random.randint(4001,5000)
        # elif round(time.time()) - start_time < 8:
        #     ahead = ahead - 137
        #     return ahead
        # else:
        #     return 5000
        return random.randint(500,5500)
        # return ahead[index]

    # ahead = 0
    # if self.test_num == 1:

    # return ahead


def left_reading(scenario):
    global left
    global index
    # if round(time.time()) - start_time < 3:
    #     return random.randint(2000,3000)
    # else:
    return random.randint(1000,5000)
    # return left[index]

def right_reading(scenario):
    global right
    global index
    # if round(time.time()) - start_time < 3:
    return random.randint(1000,5000)
    # return right[index]

def height_reading(scenario):
    global height
    height = height + random.randint(1,10)* 0.15
    return height


def latitude_reading(scenario):
    global latitude
    latitude = latitude + random.randint(1,3)*0.000001
    return latitude


def longitude_reading(scenario):
    global longitude
    longitude = longitude + random.randint(1,3)*0.000001
    return longitude
