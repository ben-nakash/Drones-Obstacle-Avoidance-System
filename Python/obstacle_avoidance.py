import time
import math
import simulator
from stoppable_thread import StoppableThread
from flight_data import FlightData
from flight_commands import FlightCommands
from sensors import Sensors
# from vehicle import Vehicle

class ObstacleAvoidance(StoppableThread):
    # Class constants
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DEVIATION_HORIZONTAL = 20
    DEVIATION_VERTICAL = 500
    NO_OBSTACLES_AHEAD = 1
    CAUTION_DISTANCE = 200    # Should be 4000, Measured in Centimeters
    DANGER_DISTANCE = 125     # Should be 1000, Measured in Centimeters
    CAUTION_ALTITUDE = 375    # Should be 3000, Measured in Centimeters.
    DANGER_ALTITUDE = 4000    # Should be 4000, Measured in Centimeters.
    CONSTANT_HEIGHT = 1000    # Should be 1000, Measured in Centimeters.
    MAX_LEFT_RIGHT = 0.875    # Should be 7.0, Maximum distance the drone would go right/left until trying to pass and obstacle from above. Measured in Meters.
    LEFT_SENSOR = "leftSensor"
    RIGHT_SENSOR = "rightSensor"
    FRONT_SENSOR = "frontSensor"
    BOTTOM_SENSOR = "bottomSensor"

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

        # Calling super class constructor
        StoppableThread.__init__(self)

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
        self.__flight_commands = FlightCommands()   # FlightCommands(vehicle)
        self.__sensors = Sensors()
        self.__flight_data = FlightData()           # FlightData(vehicle)

        # Get the drone's location and height for further calculations.
        self.__last_latitude = self.__flight_data.get_current_latitude()
        self.__last_longitude = self.__flight_data.get_current_longitude()
        self.__last_height = self.__flight_data.get_current_height()

        # Counter and flag for being aware of a sequence of illegal sensor inputs in order to be aware of a
        # malfunction in the system
        self.__illegal_input_counter = 0
        self.__legal_input = True

        self.__num_of_lines = int(self.__get_number_of_line_in_file())  # Delete when moving to a full functioning system.

        # Initializing the sensors
        if self.__sensors.connect() == -1:
            raise ConnectionError('Cannot connect to sensors')

        print("Connected Successfuly to Sensors!")

        # Flag that indicates if the system is activated in order to give the user the knowledge if it should override
        # other flight commands given to the drone. The flag is 'True' only for left/right/up maneuvers and False
        # for all other cases including fixing the drone's altitude, since the altitude is fixed for 10 meters and
        # any other running software within the drone shouldn't change its height.
        self.__is_active = False

    def run(self):
        while not self.stopped():
            simulator.altitude_change()     # Delete when moving to a full functioning system.

            self.__num_of_lines -= 1        # Delete when moving to a full functioning system.
            if self.__num_of_lines == 0:    # Delete when moving to a full functioning system.
                self.stopit()               # Delete when moving to a full functioning system.
                continue                    # Delete when moving to a full functioning system.

            print("-----------------------------------------------------------")
            if self.__safety_protocol is True:
                self.__follow_safety_protocol()

            ahead_distance = self.__get_sensor_reading(self.FRONT_SENSOR)
            print("Distance Ahead: %d" % ahead_distance)

            # In case the path ahead is clear of obstacles, reset counters and fix altitude.
            if ahead_distance == self.NO_OBSTACLES_AHEAD or ahead_distance >= self.CAUTION_DISTANCE:
                print("Way is Clear")
                self.__check_flags()
                self.__fix_altitude()
                self.__last_move = None
                self.__is_active = False
                print("Is Active = " + str(self.__is_active))
                self.__right_distance = self.__left_distance = self.__up_distance = 0.0
                continue

            if ahead_distance <= self.DANGER_DISTANCE:
                # There's an obstacle in less than 10 meters - DANGER!
                # In such case the algorithm would slow down the drone drastically in order to give it more
                # time to manouver and avoid a collision.
                print("CAUTION: Obstacle in less than 1.25 meters!")
                print("Slowing Down to avoid collision")
                self.__flight_commands.slow_down(ahead_distance)
            else:
                print("Obstacle in less than 2 meters")

            self.__is_active = True
            print("Is Active = " + str(self.__is_active))

            # Get a reading from the left side sensor.
            left_side_distance = self.__get_sensor_reading(self.LEFT_SENSOR)
            # Get a reading from the right side sensor.
            right_side_distance = self.__get_sensor_reading(self.RIGHT_SENSOR)
            print("Distance Left: %d, Distance Right: %d" % (left_side_distance, right_side_distance))

            # If already tried going to go to the left/right 7 meters and there's
            # still an obstacle ahead then I want to try from above.
            if self.__need_to_go_up() is True:
                self.__climbing = True
                if self.__flight_data.get_current_height() >= self.DANGER_ALTITUDE:
                    self.__safety_protocol = True
                    self.__follow_safety_protocol()
                else:
                    self.__move_in_direction(self.UP)
                    print("Going up")
                continue

            # Check if right side is clear.
            elif right_side_distance > left_side_distance + self.DEVIATION_HORIZONTAL:
                self.__move_in_direction(self.RIGHT)
                self.__check_flags()
                print("Going right")

            # Check if left side is clear.
            elif left_side_distance > right_side_distance + self.DEVIATION_HORIZONTAL:
                self.__move_in_direction(self.LEFT)
                self.__check_flags()
                print("Going left")

            # If both left and right gives about the same distance.
            elif self.__climbing:
                if self.__flight_data.get_current_height() >= self.DANGER_ALTITUDE:
                    self.__safety_protocol = True
                    self.__follow_safety_protocol()
                    continue
                else:
                    self.__move_in_direction(self.UP)
                    print("Going up")
                    continue

            # If both left and right side looks blocked and still want to try to pass the obstacle from one of its sides
            else:
                if self.__last_move is not None:
                    self.__move_in_direction(self.__last_move)
                    print("Going " + self.__last_move)

                else:
                    if left_side_distance > right_side_distance:
                        self.__move_in_direction(self.LEFT)
                        print("Going left")

                    elif left_side_distance < right_side_distance:
                        self.__move_in_direction(self.RIGHT)
                        print("Going right")

            self.__fix_altitude()

    def __need_to_go_up(self):
        if self.__right_distance >= self.MAX_LEFT_RIGHT or self.__left_distance >= self.MAX_LEFT_RIGHT:
            return True
        else:
            return False

    def __move_in_direction(self, direction):
        if direction == self.RIGHT:
            self.__flight_commands.go_right()

        elif direction == self.LEFT:
            self.__flight_commands.go_left()

        elif direction == self.UP:
            self.__flight_commands.go_up()
            self.__keep_altitude = True
            self.__start_time_measure = round(time.time())

        elif type(direction).__name__ is "str":
            raise ValueError('Expected "' + self.UP + '" / "' + self.LEFT + '" / "' + self.RIGHT + '", instead got ' +
                             str(direction))
        else:
            raise TypeError('Expected variable of type str and got a variable of type ' + type(direction).__name__)

        self.__update_distance(direction)
        self.__last_move = direction

    def __update_distance(self, direction):
        if direction != self.RIGHT \
                and direction != self.LEFT \
                and direction != self.UP \
                and isinstance(direction, str):
            raise ValueError('Expected "' + self.UP + '" / "' + self.LEFT + '" / "' + self.RIGHT + '", instead got ' +
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
        if direction == self.RIGHT:
            self.__right_distance += delta
            self.__left_distance = 0
            print("Distance went right: %f" % self.__right_distance)
        elif direction == self.LEFT:
            self.__left_distance += delta
            self.__right_distance = 0
            print("Distance went left: %f" % self.__left_distance)
        elif direction == self.UP:
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
            if sensor is self.FRONT_SENSOR:
                distance = self.__sensors.check_ahead()

            elif sensor is self.RIGHT_SENSOR:
                distance = self.__sensors.check_right_side()

            elif sensor is self.LEFT_SENSOR:
                distance = self.__sensors.check_left_side()

            elif sensor is self.BOTTOM_SENSOR:
                distance = self.__sensors.check_below()

            else:
                if isinstance(sensor, str):
                    raise ValueError('Expected "' + self.FRONT_SENSOR + '" / "' + self.BOTTOM_SENSOR + '" / "' +
                                     self.LEFT_SENSOR + '" / "' + self.RIGHT_SENSOR + '", instead got ' + sensor)
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
        print("Check if safe to land")
        drone_altitude = self.__flight_data.get_current_height()
        bottom_sensor_distance = self.__get_sensor_reading(self.BOTTOM_SENSOR)
        print("Pixhawk height: " + str(drone_altitude) + ", Sensor height: " + str(bottom_sensor_distance))
        heigh_difference = math.fabs(bottom_sensor_distance - drone_altitude)
        if heigh_difference > self.DEVIATION_HORIZONTAL:
            return False
        else:
            return True

    def __fix_altitude(self):
        bottom_sensor_distance = self.__get_sensor_reading(self.BOTTOM_SENSOR)
        altitude = self.__flight_data.get_current_height()
        print("Sensor Below: " + str(bottom_sensor_distance) + ", Pixhawk: " + str(altitude))

        if bottom_sensor_distance > self.DANGER_ALTITUDE:
            self.__safety_protocol = True
            self.__follow_safety_protocol()
            return

        if self.__keep_altitude:
            # This means the drone passed an obstacle from above. in that case I want to maintain my current altitude
            # for 10 seconds to make sure the drone passed the obstacle, before getting back to regular altitude.
            current_time = int(round(time.time()))
            print("maintaining altitude for " + str((current_time - self.__start_time_measure)) + " seconds")
            if current_time - self.__start_time_measure > 10.0:
                # 10 Seconds have passed, now before the drone start decending I want to make sure
                # there's nothing below and its safe for him to descend.
                self.__keep_altitude = False
            else:
                self.__flight_commands.maintain_altitude()
                return

        # Fix the height of the drone to 10 meters from the ground.
        delta_altitude = self.CONSTANT_HEIGHT - bottom_sensor_distance
        if math.fabs(delta_altitude) < self.DEVIATION_HORIZONTAL:
            return
        elif delta_altitude > 0:
            self.__flight_commands.go_up()
            print("Fixing altitude - Going up")
        elif delta_altitude < 0:
            self.__flight_commands.go_down()
            print("Fixing altitude - Going down")

    def __get_number_of_line_in_file(self):
        i = 0
        with open('Sensors Data\\leftSensorData.txt') as file:
            for i, l in enumerate(file):
                pass
            return i + 1

    def __follow_safety_protocol(self):
        # If the code reached here it means the drone raised 25 meters up and still see an obstacle.
        # so in this case we prefer it would abort the mission in so it won't get too high or damaged.
        if self.__safe_for_landing():
            # while(self.__get_sensor_reading(self.__BOTTOM_SENSOR) > 10):
            self.__flight_commands.land()   # Enter this into the while loop above.
            self.stopit()
        else:
            self.__flight_commands.go_back_to_base()

    def take_control(self):
        return self.__is_active
