# from simulator import Simulator
# from vehicle import Vehicle

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

    # def __init__(self, sim):
    #     if isinstance(sim, Simulator) is False:
    #         raise TypeError('Expected variable of type "Simulator" and got a variable of type ' +
    #                         type(sim).__name__)
    #
    #     self.__simulator = sim

    def land(self):
        # print("landing")
        # self.__vehicle.landing()
        return

    def maintain_altitude(self):
        # print("maintaining altitude")
        # self.__vehicle.keep_altitude()
        return

    def go_left(self):
        # print("going left")
        # self.__vehicle.move_left()
        return

    def go_right(self):
        # print("going right")
        # self.__vehicle.move_right()
        return

    def go_up(self):
        # print("going up")
        # self.__vehicle.move_up()
        return

    def go_down(self):
        # print("going down")
        # self.__vehicle.move_down()
        return

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
        # print("slowing down")
        return

    def go_back_to_base(self):
        print("Destination changed: going back home")
        # self.__vehicle.get_back_to_station()