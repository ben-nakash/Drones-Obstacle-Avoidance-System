from obstacle_avoidance import ObstacleAvoidance


class MyTester:

    def __init__(self):
        self.counter = 0

    def run_test(self):
        oa = ObstacleAvoidance()
        oa.start_avoiding_obstacles()


test = MyTester()
test.run_test()
