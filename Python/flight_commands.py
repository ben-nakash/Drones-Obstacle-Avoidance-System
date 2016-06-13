

class FlightCommands:

    __TIME_TO_COLLISION = 10

    # This module should have this constructor which gets a vehicle object in order to send the proper orders
    # to the drone. Since I can't initialize this object, This section and all vehicle-related commands
    # are under comment.

    # def __init__(self, vehicle):
    #     # Check for correct input
    #     if isinstance(vehicle, Vehicle) is False:
    #         raise TypeError('Expected object of type Vehicle, got '+type(vehicle).__name__)
    #
    #     self.__vehicle = vehicle

    def land(self):
        print("landing")
        # self.__vehicle.landing()

    def maintain_altitude(self):
        print("maintaining altitude")
        # self.__vehicle.keep_altitude()

    def go_left(self):
        print("going left")
        # self.__vehicle.move_left()

    def go_right(self):
        print("going right")
        # self.__vehicle.move_right()

    def go_up(self):
        print("going up")
        # self.__vehicle.move_up()

    def slow_down(self, distance):
        if isinstance(distance, float) is False and isinstance(distance, int) is False:
            raise TypeError('Expected variable of type float and got a variable of type ' + type(distance).__name__)
        elif distance <= 0:
            raise ValueError('Illegal value. Cannot be 0')

        #  # Calculating a new velocity for the drone to give it 10 seconds before colliding. 10 Seconds should be
        #  # a sufficient amount of time to avoid colliding with the detected object.
        #
        # velocity = distance/self.__TIME_TO_COLLISION
        # self.__vehicle.set_groundspeed(velocity)
        print("slowing down")
        return