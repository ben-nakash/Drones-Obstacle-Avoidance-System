import simulator
# from vehicle import Vehicle

class FlightCommands:

    TIME_TO_COLLISION = 10

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
        # self.__vehicle.landing()
        return

    def maintain_altitude(self):
        # self.__vehicle.keep_altitude()
        return

    def go_left(self):
        simulator.change_longitude_latitude()
        # self.__vehicle.move_left()
        return

    def go_right(self):
        simulator.change_longitude_latitude()
        # self.__vehicle.move_right()
        return

    def go_up(self):
        simulator.go_up()
        # self.__vehicle.move_up()
        return

    def go_down(self):
        # self.__vehicle.move_down()
        simulator.go_down()
        return

    def slow_down(self, distance):
        if isinstance(distance, float) is False and isinstance(distance, int) is False:
            raise TypeError('Expected variable of type float and got a variable of type ' + type(distance).__name__)
        elif distance <= 0:
            raise ValueError('Illegal value. Cannot be 0')

        #  # Calculating a new velocity for the drone to give it 10 seconds before colliding. 10 Seconds should be
        #  # a sufficient amount of time to avoid colliding with the detected object.
        #
        # velocity = distance/self.TIME_TO_COLLISION
        # self.__vehicle.set_groundspeed(velocity)
        return

    def go_back_to_base(self):
        print("Destination changed: going back home")
        # self.__vehicle.get_back_to_station()