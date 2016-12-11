# Device Class
#
# comp 150 IOT yeah
# Updated by Ashton Knight on 12/11/2016
#
# Implementation of device object

LOAD = 60 #standard lightbulb operates at 60 Watts
STANDBY_USAGE = 1 #each bulb uses approx. 1W to run connectivity hardware
LPW = 14 #lumens per watt of incandescant lightbulb
MAX_LUMENS = 800 #typical maximum brightness of household lightbulb


class Device:
	def __init__(self, id, default_brightness=0.50)
		self.id = id
		self.default_brightness = default_brightness
		self.brightness = default_brightness
		self.power_consumed = 0
		self.last_modified = 0

	def onEvent(self, event):
		if event.params.light_id = self.id:
			if event.type == MOTION_EVENT:
				brightness_control = Event(event.fire_time, BRIGHTNESS_CONTROL_EVENT, "device", "device")
				brightness_control.params = {
					"light_brightness" : self.default_brightness,
					"light_id" : self.id
				}

				log_motion = Event(event.fire_time, LOG_MOTION_EVENT, "device", "network")
				log_motion.params = {}

				return [brightness_control, log_motion]

			if event.type == BRIGHTNESS_CONTROL_EVENT:
				# udate power consumed using Riemann sum
				## Power conversion equation:
				###		--->	  |	             elapsed time (hours) 		        |           power usage of device mode (kW)            |      
				power_consumed += (event.fire_time-self.last_modified)/1000000/60/60*((MAX_LUMENS*self.brightness)/LPW + STANDBY_USAGE)*1000
				self.last_modified = event.fire_time # update last modified time
				self.brightness = event.params.light_brightness

				return []

			if event.type == GENERATE_DEFAULT_BRIGHTNESS_EVENT:
				default_brightness_event = Event(event.fire_time, GENERATE_DEFAULT_BRIGHTNESS_EVENT, "device", "network")

				return [default_brightness_event]

			if event.type == UPDATE_DEFAULT_BRIGHTNESS_EVENT:
				self.default_brightness = event.params.light_brightness

				return []

