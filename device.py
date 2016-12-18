# Device Class
#
# comp 150 IOT yeah
# Updated by Ashton Knight on 12/11/2016
#
# Implementation of device object
import events


LOAD = 60 #standard lightbulb operates at 60 Watts
STANDBY_USAGE = 1 #each bulb uses approx. 1W to run connectivity hardware
LPW = 14 #lumens per watt of incandescant lightbulb
MAX_LUMENS = 800 #typical maximum brightness of household lightbulb

#Delays
TO_NET_DELAY = 5
INTERNAL_DELAY = 6 

class Device(events.SimObject):
	def __init__(self, id, node, default_brightness=.50):
		self.id = id
		self.node = node
		self.default_brightness = default_brightness
		self.brightness = default_brightness
		self.last_modified = 0
		self.node = node

	def onEvent(self, event):
		if event.params["light_id"] == self.id:
			if event.type == events.MOTION_EVENT:
				brightness_control = events.Event(
					events.BRIGHTNESS_CONTROL_EVENT,
					event.fire_time + INTERNAL_DELAY,
					self.id,
					self.id)
				brightness_control.params = {
					"light_brightness" : self.default_brightness,
					"light_id" : self.id
				}

				log_motion = events.Event(
					events.LOG_MOTION_EVENT,
					event.fire_time + INTERNAL_DELAY,
					self.id,
					"cloud")
				log_motion.params = {}

				new_network_send = events.Event(
					events.NETWORK_SEND,
					event.fire_time + INTERNAL_DELAY,
					self.id,
					self.node)
				new_network_send.params = {
					"proto": events.UDP_SEND,
					"src" : self.id,
					"dest" : "cloud",
					"payload" : log_motion
				}

				return [new_network_send, brightness_control]

			if event.type == events.BRIGHTNESS_CONTROL_EVENT:
				# udate power consumed using Riemann sum
				## Power conversion equation:
				###     --->      |              elapsed time (hours)               |           power usage of device mode (kW)            |      
				self._power += (event.fire_time-self.last_modified)/1000000.0/60.0/60.0*((MAX_LUMENS*self.brightness)/LPW + STANDBY_USAGE)/1000.0
				self.last_modified = event.fire_time # update last modified time
				self.brightness = event.params["light_brightness"]

				return []

			if event.type == events.GENERATE_DEFAULT_BRIGHTNESS_EVENT:
				new_default_brightness_event = events.Event(
					events.GENERATE_DEFAULT_BRIGHTNESS_EVENT,
					event.fire_time + TO_NET_DELAY,
					self.id,
					"network")

				return [new_default_brightness_event]

			if event.type == events.UPDATE_DEFAULT_BRIGHTNESS_EVENT:
				self.default_brightness = event.params["light_brightness"]

				return []

