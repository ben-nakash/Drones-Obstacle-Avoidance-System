import random
import Sensors
import FlightCommands
import time


class ObstacleAvoidance:

	def __init__(self):
		self.__right_moves = 0
		self.__left_moves  = 0
		self.__up_moves    = 0
		self.__last_move   = None
		self.__keep_altitude = False
		self.__start_time_measure = 0
		self.__deviation = 20
		self.__safety_protocol = False

	# This function will create a new thread, run an endless loop within it that would callable
	# the search_and_avoid function each time.
	def run(self):
		return
		
	def search_and_avoid(self):
		print("-----------------------------------------------------------")

		if self.__safety_protocol == True:
			FlightCommands.land()
			return

		__ahead_distance = Sensors.check_ahead()
		print("Ahead: %d" %__ahead_distance)

		# Taking care of false readings
		if __ahead_distance <= 0 or __ahead_distance > 4000:
			self.__last_move = None
			self.reset_counters()
			print("Clear")
			return

		elif __ahead_distance < 4000:
			if __ahead_distance < 1000:
				# There's an obstacle in less than 10 meters - DANGER!
				# In such case we prefer that the drone would stop moving forward
				# to prevent serious damage to the drone.
				print("Obstacle in less than 10 meters!")
				FlightCommands.dont_move_forward() # Another option is to slow down drastically
			else:
				print("Obstacle in less than 40 meters")

			# Get a reading when sensor is 20 degrees to the left.
			__left_side_distance = Sensors.check_left_side()
			# Get a reading when sensor is 20 degrees to the right.
			__right_side_distance = Sensors.check_right_side()
			print("Left: %d, Right: %d" % (__left_side_distance ,__right_side_distance))

			# If already tried going to go to the left/right 10 times and there's still an obstacle ahead.
			# then I want to try from above.
			if self.need_to_go_up():
				if self.__up_moves >= 4:
					# Considering that each up move equals to 5 meter
					# If the code reached here it means the drone raised 20 meters up and still see an obstacle.
					# so in this case we prefer it would abort the mission in so it won't get too high or damaged.
					FlightCommands.land()
					self.__safety_protocol = True
				else:
					self.go_up()
	
			# If left side looks clear.
			elif __left_side_distance > __right_side_distance + self.__deviation:
				self.go_left()

			# If right side looks clear.
			elif __right_side_distance > __left_side_distance + self.__deviation:
				self.go_right()

			# If both left and right gives about the same distance.
			else:
				if self.__last_move != None:
					self.go_in_last_known_direction()

				else:
					if __left_side_distance > __right_side_distance:
						self.go_left()

					elif __left_side_distance < __right_side_distance:
						self.go_right()


		if self.__keep_altitude == True:
			# If upMoves is different than 0, it means the drone tried to pass an obstacle from above.
			# in that case I want to maintain my current altitude for 10 seconds to make sure
			# the drone passed the obstacle, before getting back to regular altitude.
			__current_time = int(round(time.time()))
			print("keep altitude elapsed time: %d" %(__current_time - self.__start_time_measure))
			if __current_time - self.__start_time_measure > 10:
				__keep_altitude = False

			if self.__keep_altitude == True:
				FlightCommands.maintain_altitude()







	def need_to_go_up(self):
		print("right_moves: %d, left_moves: %d, up_moves: %d" %(self.__right_moves, self.__left_moves, self.__up_moves))
		if self.__right_moves >= 10 or self.__left_moves >=10:
			return True
		else:
			return False

	# Move the drone 5 Meters higher
	def go_up(self):
		FlightCommands.go_up()
		self.update_moves_counters("up")
		self.__last_move = "up"
		self.__keep_altitude = True
		self.__start_time_measure = round(time.time())


	# Moves the drone 0.5 meter to the right
	def go_right(self):
		FlightCommands.go_right()
		self.update_moves_counters("right")
		self.__last_move = "right"

	# Moves the drone 0.5 meter to the left
	def go_left(self):
		FlightCommands.go_left()
		self.update_moves_counters("left")
		self.__last_move = "left"


	def go_in_last_known_direction(self):
		print("Going same direction as before")
		if self.__last_move == "left":
			self.go_left()

		elif self.__last_move == "right":
			self.go_right()


	def update_moves_counters(self, direction):
		if direction == "right":
			self.__right_moves += 1
			self.__left_moves = 0
		elif direction == "left":
			self.__left_moves += 1
			self.__right_moves = 0
		elif direction == "up":
			self.__up_moves += 1
			self.__right_moves = self.__left_moves = 0


	def reset_counters(self):
		self.__right_moves = self.__left_moves = self.__up_moves = 0