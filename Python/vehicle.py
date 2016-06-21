import math
import time

from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil  # Needed for command message definitions

import socket
import sys

class Vehicle:
    #######################################
    # Constructor
    #######################################
    def __init__(self, connectionString):
        print('Connecting to vehicle on: %s' % connectionString)
        self.vehicle = connect(connectionString, baud=57600)
        print('Connected!\n')

    #######################################
    # Arm And TakeOff
    #######################################
    def arm_and_takeoff(self, takeOffAltitude):

        # self.vehicle_pre_arm_check()  # chack if the vehicle is armable
        # print "Basic pre-arm checks"
        # Don't let the user try to arm until autopilot is ready
        # while not self.vehicle.is_armable:
        #    print " Waiting for vehicle to initialise..."
        time.sleep(1)

        self.vehicle_arm()                      # Arm vehicle

        self.vehicle_arming_check()				# Wait for the drone to arm

        time.sleep(1)                           # Sleep for Sec

        self.vehicle_take_off(takeOffAltitude)  # TakeOff

        self.print_vehicle_full_state_info()    # Print the vehicle status

    #######################################################################################################################################################################
    #######################################################################################################################################################################
    #######################################################################################################################################################################

    ##############################################
    #				SETTERS						 #
    ##############################################
    def set_parameters(self, parameter, value):
        self.vehicle.parameters[parameter] = value

    def get_parameters(self, parameter):
        value = self.vehicle.parameters[parameter]
        print("Param: %s" % self.vehicle.parameters[parameter])
        return value

    #Callback function for "any" parameter
    def any_parameter_callback(self, attr_name, value):
        print(" ANY PARAMETER CALLBACK: %s changed to: %s" % (attr_name, value))

    #Add observer for the vehicle's any/all parameters parameter (note wildcard string ``'*'``)
    def set_on_parameter_changed_listener(self):
        self.vehicle.parameters.add_attribute_listener('*', self.any_parameter_callback)

    def set_channel(self, channel_num, value):
        self.vehicle.mode = VehicleMode("STABILIZE")
        channel_value = self.vehicle.channels[str(channel_num)]

        if(channel_value + value) < 0:
            print("<<<<<<<<< value too low")
            return

        print("===================================>channel: " + str(channel_num) + "      " + str(channel_value + value))
        print("==>> " , channel_value)
        self.vehicle.channels.overrides[str(channel_num)] = (channel_value + value)
        #self.vehicle.channel_override = {str(channel_num) : (channel_value + value)}
        self.vehicle.flush()
        print("===> " , self.vehicle.channels)


    def get_channel_info(self):
        # Get all original channel values (before override)
        print("Channel values from RC Tx:", self.vehicle.channels)
        print("Number of channels: %s" % len(self.vehicle.channels))


        # Override channels
        print("\nChannel overrides: %s" % self.vehicle.channels.overrides)


    ##############################################
    #				SETTERS						 #
    ##############################################

    def air_speed(self, speed):
        self.vehicle.airspeed = speed

    def rtlMode(self):
        self.vehicle.mode = VehicleMode("RTL")

    def guidedMode(self):
        self.vehicle.mode = VehicleMode("GUIDED")

    def closeVec(self):
        self.vehicle.close()

    def set_mode(self, mode):
        self.vehicle.mode = mode

    def set_armed(self, bool):
        self.vehicle.armed = bool

    def set_groundspeed(self, speed):
        self.vehicle.groundspeed = speed
        return

    def set_heading(self, heading):
        self.vehicle_condition_yaw(heading)
        return



    ##############################################
    #				GETTERS						 #
    ##############################################

    def get_location(self):
        return self.vehicle.location.global_frame

    def get_location_latitude(self):
        return self.vehicle.location.lat

    def get_location_longitude(self):
        return self.vehicle.location.lon

    def get_location_altitude(self):
        return self.vehicle.location.alt

    def get_location_global_frame(self):
        return self.vehicle.location.global_frame

    def get_location_global_relative(self):
        return self.vehicle.location.global_relative_frame

    def get_location_local_frame(self):
        return self.vehicle.location.local_frame

    def get_attitude(self):
        return self.vehicle.attitude

    def get_velocity(self):
        return self.vehicle.velocity

    def get_gps(self):
        return self.vehicle.gps_0

    def get_heading(self):
        return self.vehicle.heading

    def is_armable(self):
        return self.vehicle.is_armable

    def get_system_status(self):
        return self.vehicle.system_status.state

    def get_groundspeed(self):
        return self.vehicle.groundspeed

    def get_airspeed(self):
        return self.vehicle.airspeed

    def get_mode(self):
        return self.vehicle.mode.name

    def get_home_location(self):
        return self.vehicle.home_location

    def get_battery_voltage(self):
        return self.vehicle.battery.voltage

    def get_battery_current(self):
        return self.vehicle.battery.current

    def get_battery_level(self):
        if self.vehicle.battery.level is None:
            return -1
        return self.vehicle.battery.level

    def get_distance_metres(aLocation1, aLocation2):
        dlat = aLocation2.lat - aLocation1.lat
        dlong = aLocation2.lon - aLocation1.lon
        return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5

    ##############################################
    #				PRINTS						 #
    ##############################################

    def print_vehicle_state(self):
        print('|  Pitch: $%.2f  |  Yaw: $%.2f  |  Roll: $%.2f  |  Heading: $%.2f  |' % (
            self.vehicle.attitude.pitch, self.vehicle.attitude.yaw, self.vehicle.attitude.roll, self.vehicle.heading))

    """
    Get all vehicle attributes (state)
    """
    def print_vehicle_full_state_info(self):

        print("\nGet all vehicle attribute values:")
        print(" Global Location: ...................... %s" % self.vehicle.location.global_frame)
        print(" Global Location (relative altitude): .. %s" % self.vehicle.location.global_relative_frame)
        print(" Local Location: ....................... %s" % self.vehicle.location.local_frame)
        print(" Attitude: ............................. %s" % self.vehicle.attitude)
        print(" Velocity: ............................. %s" % self.vehicle.velocity)
        print(" GPS: .................................. %s" % self.vehicle.gps_0)
        print(" Gimbal status: ........................ %s" % self.vehicle.gimbal)
        print(" Battery: .............................. %s" % self.vehicle.battery)
        print(" EKF OK?: .............................. %s" % self.vehicle.ekf_ok)
        print(" Last Heartbeat: ....................... %s" % self.vehicle.last_heartbeat)
        print(" Rangefinder: .......................... %s" % self.vehicle.rangefinder)
        print(" Rangefinder distance: ................. %s" % self.vehicle.rangefinder.distance)
        print(" Rangefinder voltage: .................. %s" % self.vehicle.rangefinder.voltage)
        print(" Heading: .............................. %s" % self.vehicle.heading)
        print(" Is Armable?: .......................... %s" % self.vehicle.is_armable)
        print(" System status: ........................ %s" % self.vehicle.system_status.state)
        print(" Groundspeed: .......................... %s" % self.vehicle.groundspeed)  # settable
        print(" Airspeed: ............................. %s" % self.vehicle.airspeed)  # settable
        print(" Mode: ................................. %s" % self.vehicle.mode.name)  # settable
        print(" Armed: ................................ %s" % self.vehicle.armed)  # settable
        print("\n \n")

    """
    Print vehicle parameters
    """
    def print_vehicle_parameters(self):
        print("\nPrint all parameters (iterate `vehicle.parameters`):")
        for key, value in self.vehicle.parameters.iteritems():
            print(" Key:%s \tValue:%s" % (key,value))



    ##############################################
    #				VEHICLE						 #
    ##############################################

    """
    Movements
    """
    def move_up(self):
        print("moving up")

    def move_down(self):
        print("moving down")

    def move_left(self):
        print("moving left")

    def move_right(self):
        print("moving right")

    def move_foreword(self):
        print("moving foreword")

    def move_backward(self):
        print("moving backward")

    def stop_moving(self):
        print("stop moving")

    def landing(self):
        print("landing")

    def keep_altitude(self):
        print("keeping altitude")

    def get_back_to_station(self):
        print("Going back to station")
    """
    Loop until the drone is initialise
    """
    def vehicle_pre_arm_check(self):
        while not self.vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

    """
    Start to arm the motors
    """
    def vehicle_arm(self):
        print("==> Vehicle Start Arming")
        self.vehicle.mode = VehicleMode("GUIDED")  # Copter should arm in GUIDED mode
        self.vehicle.armed = True
        return 1

    """
    Loop until the the motors are armed
    """
    def vehicle_arming_check(self):
        while not self.vehicle.armed:
            print("==> Waiting for vehicle to arm")
            time.sleep(1)
            self.vehicle_arm()
            # self.vehicle.armed = True
        print("\n==> Vehicle ARMED!\n")

    """
    Taking off the drone to the given altitude - Loof until the the drone reaches the altitude
    """
    def vehicle_take_off(self, takeOffAltitude):
        print("Vehicle Taking Off!")
        self.vehicle.simple_takeoff(takeOffAltitude)  # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto
        while True:
            print(" Altitude: ", self.vehicle.location.global_relative_frame.alt)
            if self.vehicle.location.global_relative_frame.alt >= takeOffAltitude * 0.95:  # Trigger just below target alt.
                print("Reached target altitude")
                break
            time.sleep(1)

    """
    Take the drone to the specified location,
    """
    def simpleGoTo(self, lat, lng, alt, velocity=-1):
        # dest = LocationGlobalRelative(lat, lon, height)
        # set the default travel speed
        if velocity == -1:
            self.vehicle.airspeed = 1
        else:
            self.vehicle.airspeed = velocity

        dest = LocationGlobalRelative(lat, lng, alt)
        self.vehicle.simple_goto(dest)

    """
    Set vehicle mode to RTL
    """
    def vehicle_RTL(self):
        self.vehicle.mode = VehicleMode("RTL")
        self.vehicle.flush()

    """
    Take the drone to given location
    """
    def vehicle_goto_location(self, location):
        currentLocation = self.vehicle.location
        targetDistance = self.get_distance_metres(currentLocation, location)
        self.gotoFunction(location)
        self.vehicle.flush()
        while not self.api.exit and self.vehicle.mode.name == "GUIDED":  # Stop action if we are no longer in guided mode.
            remainingDistance = self.get_distance_metres(self.vehicle.location, location)
            if remainingDistance <= targetDistance * 0.01:  # Just below target, in case of undershoot.
                print("Reached target")
                break
            time.sleep(2)

    """
    Send MAV_CMD_CONDITION_YAW message to point vehicle at a specified heading (in degrees).
    This method sets an absolute heading by default, but you can set the `relative` parameter
    to `True` to set yaw relative to the current yaw heading.
    By default the yaw of the vehicle will follow the direction of travel. After setting
    the yaw using this function there is no way to return to the default yaw "follow direction
    of travel" behaviour
    """
    def vehicle_condition_yaw(self, heading, relative=False):
        if relative:
            is_relative = 1  # yaw relative to direction of travel
        else:
            is_relative = 0  # yaw is an absolute angle
        # create the CONDITION_YAW command using command_long_encode()
        msg = self.vehicle.message_factory.command_long_encode(
                0, 0,  # target system, target component
                mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
                0,  # confirmation
                heading,  # param 1, yaw in degrees
                0,  # param 2, yaw speed deg/s
                1,  # param 3, direction -1 ccw, 1 cw
                is_relative,  # param 4, relative offset 1, absolute angle 0
                0, 0, 0)  # param 5 ~ 7 not used

        # send command to vehicle
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()


    """
    Send MAV_CMD_DO_SET_ROI message to point camera gimbal at a
    specified region of interest (LocationGlobal).
    The vehicle may also turn to face the ROI.
    """
    def vehicle_rotate_camera_gimbal(self, location):
        # create the MAV_CMD_DO_SET_ROI command
        msg = self.vehicle.message_factory.command_long_encode(
                0, 0,  # target system, target component
                mavutil.mavlink.MAV_CMD_DO_SET_ROI,  # command
                0,  # confirmation
                0, 0, 0, 0,  # params 1-4
                location.lat,
                location.lon,
                location.alt
        )
        # send command to vehicle
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()




    ###########################################
    #               DISTANCE                  #
    ###########################################
        """
		Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the
		specified `original_location`. The returned LocationGlobal has the same `alt` value
		as `original_location`.
		The function is useful when you want to move the vehicle around specifying locations relative to
		the current vehicle position.
		The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
		"""
    def get_location_metres(original_location, dNorth, dEast):

        earth_radius = 6378137.0  # Radius of "spherical" earth
        # Coordinate offsets in radians
        dLat = dNorth / earth_radius
        dLon = dEast / (earth_radius * math.cos(math.pi * original_location.lat / 180))

        # New position in decimal degrees
        newlat = original_location.lat + (dLat * 180 / math.pi)
        newlon = original_location.lon + (dLon * 180 / math.pi)
        if type(original_location) is LocationGlobal:
            targetlocation = LocationGlobal(newlat, newlon, original_location.alt)
        elif type(original_location) is LocationGlobalRelative:
            targetlocation = LocationGlobalRelative(newlat, newlon, original_location.alt)
        else:
            raise Exception("Invalid Location object passed")

        return targetlocation


        # Returns the ground distance in metres between two LocationGlobal objects.


    def get_distance_metres(aLocation1, aLocation2):

        dlat = aLocation2.lat - aLocation1.lat
        dlong = aLocation2.lon - aLocation1.lon
        return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5

        # Returns the bearing between the two LocationGlobal objects passed as parameters

    def get_bearing(aLocation1, aLocation2):
        off_x = aLocation2.lon - aLocation1.lon
        off_y = aLocation2.lat - aLocation1.lat
        bearing = 90.00 + math.atan2(-off_y, off_x) * 57.2957795
        if bearing < 0:
            bearing += 360.00
        return bearing;




    ###########################################
    #               MOVE VEHICLE              #
    ###########################################

    def send_ned_velocity(self, velocity_x, velocity_y, velocity_z):
        """
		Move vehicle in direction based on specified velocity vectors and
		for the specified duration.
		This uses the SET_POSITION_TARGET_LOCAL_NED command with a type mask enabling only 
		velocity components 
		(http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_local_ned).
		
		Note that from AC3.3 the message should be re-sent every second (after about 3 seconds
		with no message the velocity will drop back to zero). In AC3.2.1 and earlier the specified
		velocity persists until it is canceled. The code below should work on either version 
		(sending the message multiple times does not cause problems).
		
		See the above link for information on the type_mask (0=enable, 1=ignore). 
		At time of writing, acceleration and yaw bits are ignored.
		"""
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
                0,  # time_boot_ms (not used)
                0, 0,  # target system, target component
                mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
                0b0000111111000111,  # type_mask (only speeds enabled)
                0, 0, 0,  # x, y, z positions (not used)
                velocity_x, velocity_y, velocity_z,  # x, y, z velocity in m/s
                0, 0, 0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
                0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()

    def send_global_velocity(self, velocity_x, velocity_y, velocity_z):
        """
		Move vehicle in direction based on specified velocity vectors.
		This uses the SET_POSITION_TARGET_GLOBAL_INT command with type mask enabling only 
		velocity components 
		(http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_global_int).
		
		Note that from AC3.3 the message should be re-sent every second (after about 3 seconds
		with no message the velocity will drop back to zero). In AC3.2.1 and earlier the specified
		velocity persists until it is canceled. The code below should work on either version 
		(sending the message multiple times does not cause problems).
		
		See the above link for information on the type_mask (0=enable, 1=ignore). 
		At time of writing, acceleration and yaw bits are ignored.
		"""
        msg = self.vehicle.message_factory.set_position_target_global_int_encode(
                0,      # time_boot_ms (not used)
                0, 0,   # target system, target component
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,  # frame
                0b0000111111000111,  # type_mask (only speeds enabled)
                0,      # lat_int - X Position in WGS84 frame in 1e7 * meters
                0,      # lon_int - Y Position in WGS84 frame in 1e7 * meters
                0,      # alt - Altitude in meters in AMSL altitude(not WGS84 if absolute or relative)
                # altitude above terrain if GLOBAL_TERRAIN_ALT_INT
                velocity_x,  # X velocity in NED frame in m/s
                velocity_y,  # Y velocity in NED frame in m/s
                velocity_z,  # Z velocity in NED frame in m/s
                0, 0, 0,  # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
                0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

        # send command to vehicle on 1 Hz cycle
        self.vehicle.send_mavlink(msg)


