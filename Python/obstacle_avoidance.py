import time
from location import Location
from flight_commands import FlightCommands
from sensors import Sensors
from threading import Thread


class ObstacleAvoidance:

    # Software constants
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DEVIATION = 20.0
    WARNING_DISTANCE = 4000.0
    DANGER_DISTANCE = 1000.0
    DANGER_ALTITUDE = 20.0
    MAX_LEFT_RIGHT = 10.0

    def __init__(self):
        # These are the distances the drone passed in a certain direction.
        # They are used to know if I need to try to pass the obstacle from another direction.
        self.right_distance = 0.0
        self.left_distance = 0.0
        self.up_distance = 0.0

        # Always keep track of my last move in order to know better what to do in certain situations.
        self.last_move = None

        # In case the drone went higher to pass an obstacle from above - Keeping a flag to know I
        # should maintain altitude until fulfilling a condition.
        self.keep_altitude = False

        # I want to maintain the drone's altitude for a short period of time before descending back to the
        # original constant altitude, so for that I keep tracking of the time since it ascended.
        self.start_time_measure = 0.0

        # In case of emergency, keeping a flag to order the drone to land.
        self.safety_protocol = False

        # Other classes within the software for giving flight orders, get sensors data and
        # calculate distances by geographic positioning system data.
        self.flight_commands = FlightCommands()
        self.sensors = Sensors()
        self.location = Location()

        # Keeping track of the drone's location for required calculation.
        self.last_latitude = self.location.get_current_latitude()
        self.last_longitude = self.location.get_current_longitude()
        self.last_height = self.location.get_current_height()

    # This method initializing the sensors and create a new thread that runs a function that calls the
    # search_and_avoid method.
    def start_avoiding_obstacles(self):
        if self.sensors.connect() == -1:
            print("Error connecting to sensors, terminating program")
            return
        print("Connected Successfuly to lidar!")

        new_thread = Thread(target=self.run(), args=[])
        new_thread.start()

    def run(self):
        num_of_lines = int(get_number_of_line_in_file())
        # This loop suppose to run forever, but since I use a file to simulate the data from the sensors, it cannot
        # run forever. Therefore I limit the runtime according to the length of the file.
        for i in range(0, num_of_lines):
            self.main()

    def main(self):
        print("-----------------------------------------------------------")

        if self.safety_protocol is True:
            self.flight_commands.land()
            return

        ahead_distance = self.sensors.check_ahead()
        print("Ahead: %d" % ahead_distance)

        # Taking care of false readings duo to no obstacle ahead
        if ahead_distance <= 0 or ahead_distance > self.WARNING_DISTANCE:
            self.last_move = None
            self.right_distance = self.left_distance = self.up_distance = 0
            print("Way is Clear")
            return

        elif ahead_distance < self.WARNING_DISTANCE:
            if ahead_distance < self.DANGER_DISTANCE:
                # There's an obstacle in less than 10 meters - DANGER!
                # In such case we prefer that the drone would stop moving forward
                # to prevent serious damage to the drone.
                print("Obstacle in less than 10 meters!")
                self.flight_commands.dont_move_forward()  # Another option is to slow down drastically
            else:
                print("Obstacle in less than 40 meters")

            # Get a reading from the left side sensor.
            left_side_distance = self.sensors.check_left_side()
            # Get a reading from the right side sensor.
            right_side_distance = self.sensors.check_right_side()
            print("Left: %d, Right: %d" % (left_side_distance, right_side_distance))

            # If already tried going to go to the left/right 10 meters and there's
            # still an obstacle ahead then I want to try from above.
            if self.need_to_go_up() is True:
                if self.up_distance >= self.DANGER_ALTITUDE:
                    # If the code reached here it means the drone raised 20 meters up and still see an obstacle.
                    # so in this case we prefer it would abort the mission in so it won't get too high or damaged.
                    self.flight_commands.land()
                    self.safety_protocol = True
                else:
                    self.move_in_direction(self.UP)

            # If left side looks clear.
            elif left_side_distance > right_side_distance + self.DEVIATION:
                self.move_in_direction(self.LEFT)

            # If right side looks clear.
            elif right_side_distance > left_side_distance + self.DEVIATION:
                self.move_in_direction(self.RIGHT)

            # If both left and right gives about the same distance.
            else:
                if self.last_move is not None:
                    self.move_in_direction(self.last_move)

                else:
                    if left_side_distance > right_side_distance:
                        self.move_in_direction(self.LEFT)

                    elif left_side_distance < right_side_distance:
                        self.move_in_direction(self.RIGHT)

        if self.keep_altitude is True:
            # This means the drone tried to pass an obstacle from above.
            # in that case I want to maintain my current altitude for 10 seconds to make sure
            # the drone passed the obstacle, before getting back to regular altitude.
            current_time = int(round(time.time()))
            print("keep altitude elapsed time: %d" % (current_time - self.start_time_measure))
            if current_time - self.start_time_measure > 10.0:
                # 10 Seconds have passed, now before the drone start decending I want to make sure
                # there's nothing below and its safe for him to descend.
                below_distance = self.sensors.check_below()
                if below_distance >= 10.0:
                    self.keep_altitude = False

            if self.keep_altitude is True:
                self.flight_commands.maintain_altitude()

    def need_to_go_up(self):
        # print("right_distance: %d, left_distance: %d, up_distance: %d"
        #       % (self.right_distance, self.left_distance, self.up_distance))
        if self.right_distance >= self.MAX_LEFT_RIGHT or self.left_distance >= self.MAX_LEFT_RIGHT:
            return True
        else:
            return False

    def move_in_direction(self, direction):
        if direction == self.RIGHT:
            self.flight_commands.go_right()

        elif direction == self.LEFT:
            self.flight_commands.go_left()

        elif direction == self.UP:
            self.flight_commands.go_up()
            self.keep_altitude = True
            self.start_time_measure = round(time.time())

        self.update_distance(direction)
        self.last_move = direction

    def update_distance(self, direction):
        # Get current location data.
        current_latitude = self.location.get_current_latitude()
        current_longitude = self.location.get_current_longitude()
        current_height = self.location.get_current_height()

        delta = self.location.calculate_distance(
            self.last_latitude, self.last_longitude, current_latitude, current_longitude)

        # Update the distance travelled in certain direction
        if direction == self.RIGHT:
            self.right_distance += delta
            self.left_distance = 0
            print("Distance went right: %f" % self.right_distance)
        elif direction == self.LEFT:
            self.left_distance += delta
            self.right_distance = 0
            print("Distance went left: %f" % self.left_distance)
        elif direction == self.UP:
            self.up_distance += current_height - self.last_height
            self.left_distance = self.right_distance = 0
            print("Distance went up: %f" % self.up_distance)

        # Update last known location attributes
        self.last_latitude = current_latitude
        self.last_longitude = current_longitude
        self.last_height = current_height


def get_number_of_line_in_file():
    i = 0
    with open('Sensors Data\\SensorData.txt') as file:
        for i, l in enumerate(file):
            pass
        # The number of lines is devided by 3 since every 3 lines represents one point in time
        return (i + 1) / 3
