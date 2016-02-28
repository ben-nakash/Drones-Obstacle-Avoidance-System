import random
import Sensors
import FlightCommands
import time


class ObstacleAvoidance:

	def start(self):
		testCounter = 5

		self.__right_moves = 0
		self.__left_moves = 0
		self.__up_moves = 0
		self.__last_move = -1
		self.__keep_altitude = False
		self.__start_time_measure = 0


		while(testCounter>0):
			testCounter -=1

			__ahead_distance = Sensors.check_ahead()
			print("Ahead: %d" %__ahead_distance)
			if __ahead_distance < 1000:
			# There's an obstacle in less than 10 meters - DANGER!
			# In such case we prefer that the drone would stop moving forward
			# to prevent serious damage to the drone.
				print("Obstacle in less than 10 meters!")
				FlightCommands.dont_move()

			if __ahead_distance < 4000:
				print("Obstacle in less than 40 meters")
				# Get a reading when sensor is 20 degrees to the left.
				__left_side_distance = Sensors.check_left_side()
				# Get a reading when sensor is 20 degrees to the right.
				__right_side_distance = Sensors.check_right_side()
				print("Left: %d, Right: %d" % (__left_side_distance ,__right_side_distance))

				# If already tried going to go to the left/right 15 times and there's still an obstacle ahead.
				# then I want to try from above.
				if self.need_to_go_up():
					if self.__up_moves >= 20:
						# Considering that each up move equals to 0.5 meter
						# If the code reached here it means the drone raised 10 meters up and still see an obstacle.
						# so in this case we prefer it would abort the mission in so it won't get too high or damaged.
						FlightCommands.land()
					else:
						self.go_up()

				# If left side looks clear.
				elif __left_side_distance > __right_side_distance:
					self.go_left()

				# If right side looks clear.
				elif __left_side_distance < __right_side_distance:
					self.go_right()

				# If both left side and right side seems blocked but we still want to try to go sideways.
				else:
					if self.__last_move == "left":
						self.go_left()

					elif self.__last_move == "right":
						self.go_right()

					else:
						print("choosing randomly")
						rand_num = random.randint(0,9)
						if rand_num <= 4:
							self.go_left()
						else:
							self.go_right()

			# In this case, there's no obstacle ahead to the drone.
			else:
				# If upMoves is different than 0, it means I tried to pass an obstacle from above.
				# in that case I want to maintain my current altitude for 15 seconds to make sure
				# the drone passed the obstacle, before getting back to regular altitude.
				__current_time = int(round(time.time() * 1000)) * 1000
				if __current_time - self.__start_time_measure > 15:
					__keep_altitude = False

				if self.__keep_altitude == True:
					FlightCommands.maintain_altitude()

				self.__up_moves = self.__right_moves = self.__left_moves = 0
			print("-----------------------------------------------------------")



	def need_to_go_up(self):
		if self.__right_moves >= 15 or self.__left_moves >=15:
			return True
		else:
			return False


	def go_up(self):
		FlightCommands.go_up()
		self.update_moves_counters("up")
		self.__last_move = "up"


	def go_right(self):
		FlightCommands.go_right()
		self.update_moves_counters("right")
		self.__last_move = "right"


	def go_left(self):
		FlightCommands.go_left()
		self.update_moves_counters("left")
		self.__last_move = "left"


	def update_moves_counters(self, direction):
		if direction == "right":
			self.__right_moves += 1
			self.__left_moves = self.__up_moves = 0
		elif direction == "left":
			self.__left_moves += 1
			self.__right_moves = self.__up_moves = 0
		elif direction == "up":
			self.__up_moves += 1
			self.__right_moves = self.__left_moves = 0

