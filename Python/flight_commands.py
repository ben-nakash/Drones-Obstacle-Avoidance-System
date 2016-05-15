# This class sends the correct command to the drone to correct its flight path.
# It only prints on the screen since of 2 reasons:
# 1. I simulate the entire program.
# 2. Someone else is in charge or creating the library that actually talks with the drones computer and
#    tells it to change its flight path. Since we're not connected I cant import a library which I don't have.

class FlightCommands:

    def dont_move_forward(self):
        print("standing still")

    def land(self):
        print("landing")

    def maintain_altitude(self):
        print("maintaining altitude")

    def go_left(self):
        print("going left")

    def go_right(self):
        print("going right")

    def go_up(self):
        print("going up")
