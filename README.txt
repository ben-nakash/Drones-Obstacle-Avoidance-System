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
	Delivers the ability to stop the obstacle_avoidance thread when it's no
	longer needed.
	
2. obstacle_avoidance.py:
	Holds the ObstacleAvoidance class. This class is the main
	part of the system and holds the avoidance algorithm.
	
3. flight_commands.py:
	In this module lies the FlightCommands class. This class holds all the
	needed flight commands that the system might send to the drone.
	
4. flight_data.py:
	In this module lies the FlightData class. This class supply all the needed
	data about the drone to the main algorithm such as speed and location.
	
5. lidar_lite.py:
	In this module lies the LidarLite class. This class represents one sensor
	within the system. From within this class it's possible to get a distance
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
The next lines demonstrate how these instructions should look like:

oas = ObstacleAvoidance()
oas.start()
oas.stopit()

The system is delivered along with an API that supplies the ability to know 
if this system is currently active and should have full control of the drone.
To do so, one should call the method 

oas.take_control()

If it returns True - the system is activated and need full control over the UAV
If it returns False - no need to grant full control of the UAV to this system.

-------------------------------------------------------------------------------

Exceptions
------------
In different situations the system will throw exceptions related to its cause.
The one who use this system should handle the following types of exceptions:

1.	ConnectionError:
	Occurs after the system have made several attempts to connect to the 
	sensors without success.
	
2.	TypeError:
	Occurs when a method/function within the software receives a wrong type
	of input.

3. ValueError:
	Occurs when a method/function within the software receives a currect type
	of input	but an illegal value (For example: Method that expects to receive 
	only string constants and receive a different string).
	
4. SystemError:
	Occurs when the system receives a long sequence of illegal inputs from the
	sensors. This error can indicate of a problem with the sensors connectors. 

-------------------------------------------------------------------------------