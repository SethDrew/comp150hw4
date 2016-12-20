# Device Class
#
# comp 150 IOT yeah
# Updated by Ashton Knight on 12/11/2016
#
# Implementation of device object
import events


LOAD = 60 #standard lightbulb operates at 60 Watts
STANDBY_USAGE = 5 #each sensor uses approx. 5 watts for detection. 
#We always want to know where people are in the house so we can control very finely where they move

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
        self.brightness = 0 #initialize all lights to off
        self.last_modified = 0
        self.node = node
    def _update_power(self, time_now):
        self._power += (
                        (time_now-self.last_modified) *   #change in time. microseconds
                        (
                            (MAX_LUMENS * self.brightness)/LPW + #watts from bulb
                            STANDBY_USAGE                        #watts from sensor

                        ) * events.TIMESTEP                      #scaling to seconds
                    )
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

