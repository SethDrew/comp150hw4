
"""
This file has some basic class templates. 
It should probably be split out, but I put it all in one file for conciseness of planning

The design decicions and interfaces here represent a summary of lots of our talk today. 
If you have changes, or if I got something wrong, then we should absolutely talk about it.

"""


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

LOG_MOTION_EVENT = 1 #this is just used to percilate message through network

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


class Lightbulb:
    def __init__(self, id, default_brightness=.50):
        self.id = id
        self.default_brightness = default_brightness


class Event:
    def __init__(self, fire_time, event_type, sender_name, next_target):
        self.fire_time = fire_time
        self.type = event_type

        self.sender_name = sender_name
        self.next_target = next_target
            #light_id, "cloud", "network", "light coordinator"


        self.params = {} 

        """for example, for a message sent from coordinator light --> network, 
            destined for the light with id="kitchen_1"
        params = {
            "light_brightness": .80,
            "light_id"        : "kitchen_1",
        }

        """

class SimObject:
    def onEvent(self, event): 
        #do something based on event
        #generate side effects (event list) to return to the simulator
        return [] #should be list of events


class Simulator:
    def __init__(self, input_events=[]):

        network = Network() #TODO
        cloud = Cloud()     #TODO
        event_queue = input_events
    def run():
        timestep = 0
        while True:


class EventHeap():


class Network(SimObject):
    def __init__(self, coordinator_id=None):
        return []

    def _send_message(self, source, destination, message):
        return [] #event list



class Cloud(SimObject):
    def __init__(self):
        self.log = [] 
    def onEvent(self, event):
        log.append(event)

        if event.type == BRIGHTNESS_CONTROL_EVENT:
            new_event = Event(event.fire_time, BRIGHTNESS_CONTROL_EVENT, "cloud", "network")
            new_event.params = {
                "light_brightness": event.params.light_brightness,
                "light_id"        : event.params.light_id,
            }
            return [new_event]

e = Event(today, MOTION_EVENT, "network")








