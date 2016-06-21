import time
import math
from flight_data import FlightData
from flight_commands import FlightCommands
from sensors import Sensors
from threading import Thread
# from vehicle import Vehicle


class ObstacleAvoidance:

    # Software constants
    __LEFT = "left"
    __RIGHT = "right"
    __UP = "up"
    __DEVIATION = 20
    __NO_OBSTACLES_AHEAD = 1
    __WARNING_DISTANCE = 200    # 4000, Measured in Centimeters
    __DANGER_DISTANCE = 125     # 1000, Measured in Centimeters
    __DANGER_ALTITUDE = 312     # 2500, Measured in Centimeters.
    __CONSTANT_HEIGHT = 1000     # 1000, Measured in Centimeters.
    __MAX_LEFT_RIGHT = 0.875      # 7.0, Maximum distance the drone would go right/left until trying to pass and obstacle from above. Measured in Meters.
    __LEFT_SENSOR = "leftSensor"
    __RIGHT_SENSOR = "rightSensor"
    __FRONT_SENSOR = "frontSensor"
    __BOTTOM_SENSOR = "bottomSensor"

    # In the final software, the __init__ function signature should look like:
    # def __init__(self, vehicle):
    # vehicle object is an object from external module that has been developed by a different person within
    # the company. Since this module use other modules which is not related
    # to this project, I put all the relevant code line for proper functioning in comment.

    # def __init__(self, vehicle):
    def __init__(self):
        # # Check for correct input
        # if isinstance(vehicle, Vehicle) is False:
        #     raise TypeError('Expected object of type Vehicle, got '+type(vehicle).__name__)

        # These are the distances the drone passed in a certain direction.
        # They are used to know if I need to try to pass the obstacle from another direction.
        self.__right_distance = 0.0
        self.__left_distance = 0.0
        self.__up_distance = 0.0

        # Always keep track of my last move in order to know better what to do in certain situations.
        self.__last_move = None

        # In case the drone need to pass an obstacle from above - keeping 2 flags. One for indicating its in the
        # process of climbing, and another one to indicate it finished climbing and should now keep its altitude
        # until passing the obstacle.
        self.__keep_altitude = False
        self.__climbing = False

        # I want to maintain the drone's altitude for a short period of time before descending back to the
        # original constant altitude, so for that I keep tracking of the time since it ascended.
        self.__start_time_measure = 0.0

        # In case of emergency, keeping a flag to order the drone to land.
        self.__safety_protocol = False

        # Other classes within the software for giving flight orders, get sensors data and
        # calculate distances by geographic positioning system data.
        # the __flight_commands & __location objects should get as a parameter the vehicle object
        self.__flight_commands = FlightCommands()  # FlightCommands(vehicle)
        self.__sensors = Sensors()
        self.__flight_data = FlightData()  # Location(vehicle)

        # Get the drone's location and height for further calculations.
        self.__last_latitude = self.__flight_data.get_current_latitude()
        self.__last_longitude = self.__flight_data.get_current_longitude()
        self.__last_height = self.__flight_data.get_current_height()

        # Counter and flag for being aware of a sequence of illegal sensor inputs in order to be aware of a
        # malfunction in the system
        self.__illegal_input_counter = 0
        self.__legal_input = True

        # Initializing the sensors
        if self.__sensors.connect() == -1:
            raise ConnectionError('Cannot connect to sensors')

        print("Connected Successfuly to Sensors!")

        # Creating a new thread to run the software parallel to other applications running in the drone's computer.
        self.new_thread = Thread(target=self.__start_avoiding_obstacles(), args=[])
        self.new_thread.start()

    def __start_avoiding_obstacles(self):
        num_of_lines = 190  # int(self.__get_number_of_line_in_file())
        # This loop suppose to run forever (while(true)), but since I use a file to simulate the data from the
        # sensors, it cannot run forever. Therefore I limit the runtime according to the length of the file.
        for i in range(0, num_of_lines):
            self.__main()

    def __main(self):
        print("-----------------------------------------------------------")

        if self.__safety_protocol is True:
            self.__follow_safety_protocol()

        ahead_distance = self.__get_sensor_reading(self.__FRONT_SENSOR)
        print("Distance Ahead: %d" % ahead_distance)

        # In case the path ahead is clear of obstacles
        if ahead_distance == self.__NO_OBSTACLES_AHEAD or ahead_distance >= self.__WARNING_DISTANCE:
            self.__check_flags()
            self.__fix_altitude()
            self.__last_move = None
            self.__right_distance = self.__left_distance = self.__up_distance = 0
            print("Way is Clear")
            return

        if ahead_distance <= self.__DANGER_DISTANCE:
            # There's an obstacle in less than 10 meters - DANGER!
            # In such case the algorithm would slow down the drone drastically in order to give it more
            # time to manouver and avoid a collision.
            print("Obstacle in less than 10 meters!")
            self.__flight_commands.slow_down(ahead_distance)
        else:
            print("Obstacle in less than 40 meters")

        # Get a reading from the left side sensor.
        left_side_distance = self.__get_sensor_reading(self.__LEFT_SENSOR)
        # Get a reading from the right side sensor.
        right_side_distance = self.__get_sensor_reading(self.__RIGHT_SENSOR)
        print("Distance Left: %d, Distance Right: %d" % (left_side_distance, right_side_distance))

        # If already tried going to go to the left/right 7 meters and there's
        # still an obstacle ahead then I want to try from above.
        if self.__need_to_go_up() is True:
            self.__climbing = True
            if self.__flight_data.get_current_height() >= self.__DANGER_ALTITUDE:
                self.__safety_protocol = True
                self.__follow_safety_protocol()
                return
            else:
                self.__move_in_direction(self.__UP)
                return

        # Check if right side is clear.
        elif right_side_distance > left_side_distance + self.__DEVIATION:
            self.__move_in_direction(self.__RIGHT)
            self.__check_flags()

        # Check if left side is clear.
        elif left_side_distance > right_side_distance + self.__DEVIATION:
            self.__move_in_direction(self.__LEFT)
            self.__check_flags()

        # If both left and right gives about the same distance.
        elif self.__climbing:
            if self.__flight_data.get_current_height() >= self.__DANGER_ALTITUDE:
                self.__safety_protocol = True
                self.__follow_safety_protocol()
                return
            else:
                self.__move_in_direction(self.__UP)
                return

        # If both left and right side looks blocked and I still want to try to pass the obstacle from on of its sides
        else:
            if self.__last_move is not None:
                self.__move_in_direction(self.__last_move)

            else:
                if left_side_distance > right_side_distance:
                    self.__move_in_direction(self.__LEFT)

                elif left_side_distance < right_side_distance:
                    self.__move_in_direction(self.__RIGHT)

        self.__fix_altitude()

    def __need_to_go_up(self):
        if self.__right_distance >= self.__MAX_LEFT_RIGHT or self.__left_distance >= self.__MAX_LEFT_RIGHT:
            return True
        else:
            return False

    def __move_in_direction(self, direction):
        if direction == self.__RIGHT:
            self.__flight_commands.go_right()

        elif direction == self.__LEFT:
            self.__flight_commands.go_left()

        elif direction == self.__UP:
            self.__flight_commands.go_up()
            self.__keep_altitude = True
            self.__start_time_measure = round(time.time())

        elif type(direction).__name__ is "str":
            raise ValueError('Expected "'+self.__UP+'" / "'+self.__LEFT+'" / "'+self.__RIGHT+'", instead got ' +
                             str(direction))
        else:
            raise TypeError('Expected variable of type str and got a variable of type ' + type(direction).__name__)

        self.__update_distance(direction)
        self.__last_move = direction

    def __update_distance(self, direction):
        if direction != self.__RIGHT \
                and direction != self.__LEFT \
                and direction != self.__UP\
                and type(direction).__name__ is "str":
            raise ValueError('Expected "'+self.__UP+'" / "'+self.__LEFT+'" / "'+self.__RIGHT+'", instead got ' +
                             str(direction))

        elif type(direction).__name__ != "str":
            raise TypeError('Expected variable of type str and got a variable of type ' + type(direction).__name__)

        # Get current location data.
        current_latitude = self.__flight_data.get_current_latitude()
        current_longitude = self.__flight_data.get_current_longitude()
        current_height = self.__flight_data.get_current_height()

        delta = self.__flight_data.calculate_distance(
            self.__last_latitude, self.__last_longitude, current_latitude, current_longitude)

        # Update the distance travelled in certain direction
        if direction == self.__RIGHT:
            self.__right_distance += delta
            self.__left_distance = 0
            print("Distance went right: %f" % self.__right_distance)
        elif direction == self.__LEFT:
            self.__left_distance += delta
            self.__right_distance = 0
            print("Distance went left: %f" % self.__left_distance)
        elif direction == self.__UP:
            self.__up_distance += current_height - self.__last_height
            self.__left_distance = self.__right_distance = 0
            print("Distance went up: %f" % self.__up_distance)

        # Update last known location attributes
        self.__last_latitude = current_latitude
        self.__last_longitude = current_longitude
        self.__last_height = current_height

    def __get_sensor_reading(self, sensor):
        legal_input = False
        while legal_input is False:
            distance = -1
            if sensor is self.__FRONT_SENSOR:
                distance = self.__sensors.check_ahead()

            elif sensor is self.__RIGHT_SENSOR:
                distance = self.__sensors.check_right_side()

            elif sensor is self.__LEFT_SENSOR:
                distance = self.__sensors.check_left_side()

            elif sensor is self.__BOTTOM_SENSOR:
                distance = self.__sensors.check_below()

            else:
                if type(sensor).__name__ is "str":
                    raise ValueError('Expected "'+self.__FRONT_SENSOR+'" / "'+self.__BOTTOM_SENSOR+'" / "' +
                                     self.__LEFT_SENSOR+'" / "'+self.__RIGHT_SENSOR+'", instead got '+str(sensor))
                else:
                    raise TypeError('Expected variable of type str and got a variable of type ' + type(sensor).__name__)

            legal_input = self.__check_measurement(distance)
            if legal_input:
                return distance

    def __check_measurement(self, measurement):
        if isinstance(measurement, int):
            if measurement > 0:
                self.__legal_input = True
                return True

        if self.__legal_input is True:
            self.__illegal_input_counter = 1
        else:
            self.__illegal_input_counter += 1
            if self.__illegal_input_counter >= 10:
                raise SystemError('Malfunction in sensors, check physical connections')

        self.__legal_input = False
        return False

    def __check_flags(self):
        if self.__climbing is True:
            self.__climbing = False
            self.__keep_altitude = True

    def __safe_for_landing(self):
        drone_altitude = self.__flight_data.get_current_height()
        bottom_sensor_distance = self.__get_sensor_reading(self.__BOTTOM_SENSOR)
        heigh_difference = math.fabs(bottom_sensor_distance - drone_altitude)
        if heigh_difference > self.__DEVIATION:
            return False
        else:
            return True

    def __fix_altitude(self):
        bottom_sensor_distance = self.__get_sensor_reading(self.__BOTTOM_SENSOR)
        if self.__keep_altitude:
            # This means the drone passed an obstacle from above. in that case I want to maintain my current altitude
            # for 10 seconds to make sure the drone passed the obstacle, before getting back to regular altitude.
            current_time = int(round(time.time()))
            print("keep altitude elapsed time: %d" % (current_time - self.__start_time_measure))
            if current_time - self.__start_time_measure > 10.0:
                # 10 Seconds have passed, now before the drone start decending I want to make sure
                # there's nothing below and its safe for him to descend.
                self.__keep_altitude = False
            else:
                self.__flight_commands.maintain_altitude()
                return

        # Fix the height of the drone to 10 meters from the ground
        delta_altitude = self.__CONSTANT_HEIGHT - bottom_sensor_distance
        if delta_altitude > 0:
            self.__flight_commands.go_up()
        elif delta_altitude < 0:
            self.__flight_commands.go_down()

    def __get_number_of_line_in_file(self):
        i = 0
        with open('Sensors Data\\leftSensorData.txt') as file:
            for i, l in enumerate(file):
                pass
            # The number of lines is devided by 3 since every 3 lines represents one point in time
            return (i + 1) / 3

    def __follow_safety_protocol(self):
        # If the code reached here it means the drone raised 25 meters up and still see an obstacle.
        # so in this case we prefer it would abort the mission in so it won't get too high or damaged.
        if self.__safe_for_landing():
            self.__flight_commands.land()
            # NEED TO KILL THE THREAD.
        else:
            self.__flight_commands.go_back_to_base()
