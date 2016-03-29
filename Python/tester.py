from obstacle_avoidance import ObstacleAvoidance
import time

class my_tester:

    def __init__(self, scenario):
        self.scenario = scenario
        self.counter = 0

    def run_test(self):
        oa = ObstacleAvoidance(self.scenario)
        oa.start_avoiding_obstacles()

# millis = round(time.time())
# print(millis)
# time.sleep(5)
# newmillis = round(time.time())
# print(newmillis)
# print("delay= %ds" % (newmillis-millis))

test = my_tester(1)
test.run_test()