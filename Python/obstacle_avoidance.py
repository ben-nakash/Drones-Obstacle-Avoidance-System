import time
import distance_calculator
from flight_commands import FlightCommands
from sensors import Sensors
from threading import Thread


LEFT = "left"
RIGHT = "right"
UP = "up"
DEVIATION = 20.0
WARNING_DISTANCE = 4000.0
DANGER_DISTANCE = 1000.0
DANGER_ALTITUDE = 20.0
MAX_LEFT_RIGHT = 10.0


class ObstacleAvoidance:

    def __init__(self):
        self.right_distance = 0.0
        self.left_distance = 0.0
        self.up_distance = 0.0
        self.last_latitude = distance_calculator.get_current_latitude()
        self.last_longitude = distance_calculator.get_current_longitude()
        self.last_height = distance_calculator.get_current_height()
        self.last_move = None
        self.keep_altitude = False
        self.start_time_measure = 0.0
        self.deviation = 20.0
        self.safety_protocol = False
        self.flight_commands = FlightCommands()
        self.sensors = Sensors()

    def init_sensors(self):
        if self.sensors.connect() == -1:
            return -1

    # This function create a new thread that runs a function with an endless loop
    # that calls the search_and_avoid function each time.
    def start_avoiding_obstacles(self):
        if self.init_sensors() == -1:
            print("Error connecting to lidar, terminating program")
            return

        new_thread = Thread(target=self.run(), args=[])
        new_thread.start()

    def run(self):
        for i in range(0, 15):  # This should be an endless loop
            self.search_and_avoid()

    def search_and_avoid(self):
        print("-----------------------------------------------------------")

        if self.safety_protocol is True:
            self.flight_commands.land()
            return

        ahead_distance = self.sensors.check_ahead()
        print("Ahead: %d" % ahead_distance)

        # Taking care of false readings duo to no obstacle ahead
        if ahead_distance <= 0 or ahead_distance > WARNING_DISTANCE:
            self.last_move = None
            self.reset_distances()
            print("Clear")
            return

        elif ahead_distance < WARNING_DISTANCE:
            if ahead_distance < DANGER_DISTANCE:
                # There's an obstacle in less than 10 meters - DANGER!
                # In such case we prefer that the drone would stop moving forward
                # to prevent serious damage to the drone.
                print("Obstacle in less than 10 meters!")
                self.flight_commands.dont_move_forward()  # Another option is to slow down drastically
            else:
                print("Obstacle in less than 40 meters")

            # Get a reading when sensor is 20 degrees to the left.
            left_side_distance = self.sensors.check_left_side()
            # Get a reading when sensor is 20 degrees to the right.
            right_side_distance = self.sensors.check_right_side()
            print("Left: %d, Right: %d" % (left_side_distance, right_side_distance))

            # If already tried going to go to the left/right 10 meters and there's
            # still an obstacle ahead then I want to try from above.
            if self.need_to_go_up() is True:
                if self.up_distance >= DANGER_ALTITUDE:
                    # If the code reached here it means the drone raised 20 meters up and still see an obstacle.
                    # so in this case we prefer it would abort the mission in so it won't get too high or damaged.
                    self.flight_commands.land()
                    self.safety_protocol = True
                else:
                    self.move_in_direction(UP)

            # If left side looks clear.
            elif left_side_distance > right_side_distance + DEVIATION:
                self.move_in_direction(LEFT)

            # If right side looks clear.
            elif right_side_distance > left_side_distance + DEVIATION:
                self.move_in_direction(RIGHT)

            # If both left and right gives about the same distance.
            else:
                if self.last_move is not None:
                    self.move_in_direction(self.last_move)

                else:
                    if left_side_distance > right_side_distance:
                        self.move_in_direction(LEFT)

                    elif left_side_distance < right_side_distance:
                        self.move_in_direction(RIGHT)

        if self.keep_altitude is True:
            # This means the drone tried to pass an obstacle from above.
            # in that case I want to maintain my current altitude for 10 seconds to make sure
            # the drone passed the obstacle, before getting back to regular altitude.
            current_time = int(round(time.time()))
            print("keep altitude elapsed time: %d" % (current_time - self.start_time_measure))
            if current_time - self.start_time_measure > 10.0:
                self.keep_altitude = False

            if self.keep_altitude is True:
                self.flight_commands.maintain_altitude()

    def need_to_go_up(self):
        print("right_distance: %d, left_distance: %d, up_distance: %d"
              % (self.right_distance, self.left_distance, self.up_distance))
        if self.right_distance >= MAX_LEFT_RIGHT or self.left_distance >= MAX_LEFT_RIGHT:
            return True
        else:
            return False

    def move_in_direction(self, direction):
        if direction == RIGHT:
            self.flight_commands.go_right()

        elif direction == LEFT:
            self.flight_commands.go_left()

        elif direction == UP:
            self.flight_commands.go_up()
            self.keep_altitude = True
            self.start_time_measure = round(time.time())

        self.update_distance(direction)
        self.last_move = direction

    def reset_distances(self):
        self.right_distance = self.left_distance = self.up_distance = 0

    def update_distance(self, direction):
        current_latitude = distance_calculator.get_current_latitude()
        current_longitude = distance_calculator.get_current_longitude()
        current_height = distance_calculator.get_current_height()

        delta = distance_calculator.calculate_distance(
            self.last_latitude, self.last_longitude, current_latitude, current_longitude)

        if direction == RIGHT:
            self.right_distance += delta
            self.left_distance = 0
        elif direction == LEFT:
            self.left_distance += delta
            self.right_distance = 0
        elif direction == UP:
            self.up_distance += current_height - self.last_height
            self.left_distance = self.right_distance = 0

        self.last_latitude = current_latitude
        self.last_longitude = current_longitude
        self.last_height = current_height
