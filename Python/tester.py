from obstacle_avoidance import ObstacleAvoidance

class MyTester:

    def __init__(self):
        self.counter = 0
        self.run_test()
        # self.vehicle = Vehicle("connection string")

    def run_test(self):
        # obstacle_avoidance_system = ObstacleAvoidance(self.vehicle)
        obstacle_avoidance_system = ObstacleAvoidance()

# Script to run the
test = MyTester()
# test.run_test()
