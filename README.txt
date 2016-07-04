Obstacle Avoidance System 
-------------------------------------------------------------------------------
Created by Ben Nakash
Jerusalem College of Engineering
-------------------------------------------------------------------------------

Project Modules:
------------------
	- stoppable_thread.py
	- obstacle_avoidance.py
	- flight_commands.py
	- flight_data.py
	- lidar_lite.py
	- simulator.py
	- tester.py
	
-------------------------------------------------------------------------------

Modules Description:
-----------------------
1. stoppable_thread.py:
	This module gives the ability to stop the obstacle_avoidance object 
	thread when its no longer needed.
	
2. obstacle_avoidance.py:
	In this module lies the ObstacleAvoidance class. This class is the main
	part of the system and holds the avoidance algorithm.
	
3. flight_commands.py:
	In this module lies the FlightCommands class. This class holds all the
	needed flight commands that the system might send to the drone.
	
4. flight_data.py:
	In this module lies the FlightData class. This class supply all the needed
	data about the drone to the main algorithm such as speed and location.
	
5. lidar_lite.py:
	In this module lies the LidarLite class. This class represents one sensor
	within the system. From within this class its possible to get a distance
	reading.
	
6. simulator.py:
	This module is designed for testing the algorithm. It sends distances
	to the main algorithm from files and supply other data that is being
	generated from within the module.
	
7. tester.py:
	Test module.

-------------------------------------------------------------------------------

Using the system
-------------------
In order to use the system, the user should first create an object of type
ObstacleAvoidance. Since this object is of type Thread, it needs to be 
started. To do so, one should call the method start().
In order to stop the thread from working, the user should call the function
stopit().
The next lines demonstrates how these instructions should look like:

oas = ObstacleAvoidance()
oas.start()
oas.stopit()

The system is delivered along with an API that supplies the knowledgment 
if this system is working and should have full control of the drone.
To know if it should take control, one should call the method 

oas.take_control()

If it returns True - the system is activated and need full control over the UAV
If it returns False - no need to grant full control of the UAV to this system.

-------------------------------------------------------------------------------