from obstacle_avoidance import ObstacleAvoidance
import time

obstacle_avoidance_system = ObstacleAvoidance()
obstacle_avoidance_system.start()

flag = True

while flag:
    time.sleep(0.1)
    if obstacle_avoidance_system.take_control():
        print("override")

    if obstacle_avoidance_system.isAlive() is False:
        flag = False
        print("Terminated")