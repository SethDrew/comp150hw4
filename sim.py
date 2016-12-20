import events
import device
import network
import cloud

import heapq

DEBUG = 0
VERBOSE = 1

class EventQueue:
    def __init__(self):
        self.events = []
    def push(self, event):
        heapq.heappush(self.events, (event.fire_time, event))
    def pop(self):
        return heapq.heappop(self.events)[1]
    def empty(self):
        return len(self.events) == 0
    def string(self):
        return ""
class Simulator:
    def __init__(self):

        #not really sure why we need routes pointing towards themselves
        routes = { "NET-1" : "NET-1" , "NET-2" : "NET-2", "NET-3" :"NET-3" }

        #Each object has a unique network node associated with it. 
        #We are assuming only one hop is neccessary for now
        hosts = {
            "LIGHT-1" : "NET-1",
            "LIGHT-2" : "NET-2",
            "cloud"   : "NET-3",
        }
        self.objects = {
            "NET-1" : network.NetworkNode("NET-1", "LIGHT-1", routes, hosts),
            "NET-2" : network.NetworkNode("NET-2", "LIGHT-2", routes, hosts),
            "NET-3" : network.NetworkNode("NET-3", "cloud", routes, hosts),
            "cloud" : cloud.Cloud("cloud", "NET-3"),
            "LIGHT-1" : device.Device("LIGHT-1", "NET-1"),
            "LIGHT-2" : device.Device("LIGHT-2", "NET-2"),
        }
    def run(self):
        eventq = EventQueue()
        # m = events.Event(events.MOTION_EVENT, 
        #           0, "LIGHT-1", "LIGHT-1", {"light_id" : "LIGHT-1"})
        event = events.Event(events.BRIGHTNESS_CONTROL_EVENT, 
                        0, "cloud", "cloud", {"light_id" : "LIGHT-1", "light_brightness" : .7})
        eventq.push(event)
        while not eventq.empty():
            event = eventq.pop()
            if VERBOSE: 
                print "{} : {} --> {}".format(event._event_to_string[event.type], event.source, event.dest)
            if DEBUG:
                print "{}.onEvent({})".format(event.dest, event._event_to_string[event.type])
            new_events = self.objects[event.dest].onEvent(event)
            
            if DEBUG:
                print "Got resulting events:"
                print new_events

            for event in new_events:
                eventq.push(event)


        #using leftover last event that was registered for the last fire time              
        exit_event = events.Event(events.EXIT_EVENT, event.fire_time+events.ONE_DAY, "", "") 
        for k, o in self.objects.iteritems():
            o.onEvent(exit_event) #tell each object that the game is over. time to go home.
            if(o.id.startswith("cloud")):
                print "{} used {} Dollars".format(k, o.cost()) #each object should have updated power now.

            else:
                print "{} used {} kWH".format(k, o.power()/(1000*3600)) #each object should have updated power now.
            




s = Simulator()
s.run()