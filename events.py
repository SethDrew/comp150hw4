#!/usr/bin/env python
#
# Comp 150-IOT, Undergraduate Final Project
# 
# Implementation of Event class, as well as definitions for event constants.

class Event:
    def __init__(self, event_type, fire_time, source, dest, params={}):
        self.type = event_type
        self.fire_time = fire_time

        self.source = source
        self.dest = dest

        self.params = params


##################    EVENT CONSTANTS    ##################

MOTION_EVENT = 0 
"""
OnEvent function:
    What events should happen?

    Lightbulb: 
        New Event: BRIGHTNESS_CONTROL_EVENT
            - Send to self
        New Event: LOG_MOTION_EVENT
            - Send message to network
    Network:   
        New Event: LOG_MOTION_EVENT
            - Send to coordinator lightbulb
            - If received from coordinator lightbulb, then send it to cloud
    Cloud: 
        Store in log
"""

LOG_MOTION_EVENT = 1 #this is just used to percolate message through network

BRIGHTNESS_CONTROL_EVENT = 2 #used by human interaction, or cloud decision
"""
OnEvent function:
    What events should happen?

    Lightbulb: 
        Adjust Brightness
    Network:   
        New Event: BRIGHTNESS_CONTROL_EVENT
            - Send message to Lightbulb
    Cloud: 
        New Event: BRIGHTNESS_CONTROL_EVENT
            - Send message to Network
"""

GENERATE_UPDATE_DEFAULT_BRIGHTNESS_EVENT = 3
"""
OnEvent function:
    What events should happen?

    Lightbulb: 
        Note that this lightbulb MUST be the coordinator
            New Event: UPDATE_BRIGHTNESS_CONTROL_EVENT to network

    Network:   
        New Event: GENERATE_UPDATE_DEFAULT_BRIGHTNESS_EVENT
            - Send message to Lightbulb Coordinator

    Cloud: 
        New Event: BRIGHTNESS_CONTROL_EVENT
            - Send message to Network
"""

UPDATE_DEFAULT_BRIGHTNESS_EVENT = 4
"""
OnEvent function:
    What events should happen?
    
    Lightbulb:
        Modify default brightness
    Network:
        New Event: UPDATE_DEFAULT_BRIGHTNESS_EVENT
            - send to appropriate lightbulb 
    Cloud: N/A
"""


# Network Events
# 
# All network events require params that include "src", "dest", and "payload",
# where "src" and "dest" are device/host names (e.g. "CLOUD" or "LIGHT-1"), and
# "payload" is a list of events to be received by the destination device.

NETWORK_SEND = 8    # Add'l param(s): "proto", one of the following send events.
NETWORK_RECEIVE = 9

UDP_SEND = 90
UDP_RECEIVE = 91
TCP_SEND = 92
TCP_RECEIVE = 93
ZIGBEE_SEND = 94
ZIGBEE_RECEIVE = 95
