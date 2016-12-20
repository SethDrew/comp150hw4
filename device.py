# Device Class
#
# comp 150 IOT yeah
# Updated by Ashton Knight on 12/11/2016
#
# Implementation of device object
import events

#Delays
# typical microprocessor takes 100us to read analog input
INTERNAL_DELAY = 100 

class Device(events.SimObject):
    def __init__(self, id, node, lpw, max_lumens, standby_usage, default_brightness=.50):
        self.id = id
        self.node = node
        self.default_brightness = default_brightness
        self.brightness = 0 #initialize all lights to off
        self.last_modified = 0
        self.node = node
        self.lpw = lpw
        self.max_lumens = max_lumens
        self.standby_usage = standby_usage
    def _update_power(self, time_now):
        self._power += (
                        (time_now-self.last_modified) *   #change in time. microseconds
                        (
                            (self.max_lumens * self.brightness)/self.lpw + #watts from bulb
                            self.standby_usage     #watts from sensor

                        ) * events.TIMESTEP                      #scaling to seconds
                    )

    def current_power(self):
    	#return current power usage in watts
    	return (self.max_lumens*self.brightness)/self.lpw + self.standby_usage

    def onEvent(self, event):

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
                events.MOTION_EVENT,
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
            self._update_power(event.fire_time)
            self.last_modified = event.fire_time # update last modified time
            self.brightness = event.params["light_brightness"]

            return []

        if event.type == events.UPDATE_DEFAULT_BRIGHTNESS_EVENT:
            self.default_brightness = event.params["light_brightness"]

            return []
        if event.type == events.EXIT_EVENT:
            self._update_power(event.fire_time)
            return []

