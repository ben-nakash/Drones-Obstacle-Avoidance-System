from obstacle_avoidance import ObstacleAvoidance
import time

obstacle_avoidance_system = ObstacleAvoidance()
obstacle_avoidance_system.start()

while True:
    time.sleep(0.1)
    if obstacle_avoidance_system.take_control():
        print("override")
    else:
        print("not overriding")