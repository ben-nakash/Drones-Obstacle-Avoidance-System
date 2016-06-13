import time
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
    __DEVIATION = 20.0
    __WARNING_DISTANCE = 4000.0     # Measured in Centimeters since the sensors data is received in this unit
    __DANGER_DISTANCE = 1000.0      # Measured in Centimeters since the sensors data is received in this unit
    __DANGER_ALTITUDE = 20.0        # Measured in Meters since the 'vehicle' library returns height value in this unit.
    __MAX_LEFT_RIGHT = 5.0         # Measured in Meters

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

        # In case the drone went higher to pass an obstacle from above - Keeping a flag to know I
        # should maintain altitude until fulfilling a condition.
        self.__keep_altitude = False

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

        # Initializing the sensors
        if self.__sensors.connect() == -1:
            raise ConnectionError('Cannot connect to sensors')

        print("Connected Successfuly to lidar!")

        # Creating a new thread to run the software parallel to other applications running in the drone's computer.
        new_thread = Thread(target=self.__start_avoiding_obstacles(), args=[])
        new_thread.start()

    def __start_avoiding_obstacles(self):
        num_of_lines = int(self.__get_number_of_line_in_file())
        # This loop suppose to run forever (while(true)), but since I use a file to simulate the data from the
        # sensors, it cannot run forever. Therefore I limit the runtime according to the length of the file.
        for i in range(0, num_of_lines):
            self.__main()

    def __main(self):
        print("-----------------------------------------------------------")

        if self.__safety_protocol is True:
            self.__flight_commands.land()
            return

        ahead_distance = self.__sensors.check_ahead()
        print("Distance Ahead: %d" % ahead_distance)

        # Taking care of false readings duo to no obstacle ahead
        if ahead_distance <= 0 or ahead_distance > self.__WARNING_DISTANCE:
            self.__last_move = None
            self.__right_distance = self.__left_distance = self.__up_distance = 0
            print("Way is Clear")

        elif ahead_distance < self.__WARNING_DISTANCE:
            if ahead_distance < self.__DANGER_DISTANCE:
                # There's an obstacle in less than 10 meters - DANGER!
                # In such case the algorithm would slow down the drone drastically in order to give it more
                # time to manouver and avoid a collision.
                print("Obstacle in less than 10 meters!")
                self.__flight_commands.slow_down(ahead_distance)
            else:
                print("Obstacle in less than 40 meters")

            # Get a reading from the left side sensor.
            left_side_distance = self.__sensors.check_left_side()
            # Get a reading from the right side sensor.
            right_side_distance = self.__sensors.check_right_side()
            print("Distance Left: %d, Distance Right: %d" % (left_side_distance, right_side_distance))

            # If already tried going to go to the left/right 10 meters and there's
            # still an obstacle ahead then I want to try from above.
            if self.__need_to_go_up() is True:
                if self.__up_distance >= self.__DANGER_ALTITUDE:
                    # If the code reached here it means the drone raised 20 meters up and still see an obstacle.
                    # so in this case we prefer it would abort the mission in so it won't get too high or damaged.
                    self.__flight_commands.land()
                    self.__safety_protocol = True
                    return
                else:
                    self.__move_in_direction(self.__UP)
                    return

            # Check if left side is clear.
            elif left_side_distance > right_side_distance + self.__DEVIATION:
                self.__move_in_direction(self.__LEFT)

            # Check if right side is clear.
            elif right_side_distance > left_side_distance + self.__DEVIATION:
                self.__move_in_direction(self.__RIGHT)

            # If both left and right gives about the same distance.
            else:
                if self.__last_move is not None:
                    self.__move_in_direction(self.__last_move)

                else:
                    if left_side_distance > right_side_distance:
                        self.__move_in_direction(self.__LEFT)

                    elif left_side_distance < right_side_distance:
                        self.__move_in_direction(self.__RIGHT)

        if self.__keep_altitude is True:
            # This means the drone tried to pass an obstacle from above.
            # in that case I want to maintain my current altitude for 10 seconds to make sure
            # the drone passed the obstacle, before getting back to regular altitude.
            current_time = int(round(time.time()))
            print("keep altitude elapsed time: %d" % (current_time - self.__start_time_measure))
            if current_time - self.__start_time_measure > 10.0:
                # 10 Seconds have passed, now before the drone start decending I want to make sure
                # there's nothing below and its safe for him to descend.
                below_distance = self.__sensors.check_below()
                if below_distance >= 10.0:
                    self.__keep_altitude = False

            if self.__keep_altitude is True:
                self.__flight_commands.maintain_altitude()

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
            raise ValueError('Expected "'+self.__UP+'" / "'+self.__LEFT+'" / "'+self.__RIGHT+'", instead got '+str(direction))

        else:
            raise TypeError('Expected variable of type str and got a variable of type ' + type(direction).__name__)

        self.__update_distance(direction)
        self.__last_move = direction

    def __update_distance(self, direction):
        if direction != self.__RIGHT \
                and direction != self.__LEFT \
                and direction != self.__UP\
                and type(direction).__name__ is "str":
            raise ValueError('Expected "'+self.__UP+'" / "'+self.__LEFT+'" / "'+self.__RIGHT+'", instead got '+str(direction))

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

    def __get_number_of_line_in_file(self):
        i = 0
        with open('Sensors Data\\SensorData.txt') as file:
            for i, l in enumerate(file):
                pass
            # The number of lines is devided by 3 since every 3 lines represents one point in time
            return (i + 1) / 3
