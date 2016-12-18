import events
import device
import network
import cloud

import heapq

class EventQueue:
    def __init__(self):
        self.events = []
    def push(self, event):
        heapq.heappush(self.events, (event.fire_time, event))
    def pop(self):
        return heapq.heappop(self.events)[1]
    def empty(self):
        return len(self.events) == 0
class Simulator:
    def __init__(self):
        self.routes = { "NET-1" : "NET-1" , "NET-2" : "NET-2" }
        self.hosts = {
            "LIGHT-1" : "NET-1",
            "LIGHT-2" : "NET-2",
            "COORDINATOR" : "NET-1"
        }
        self.objects = {
            "NET-1" : network.NetworkNode("NET-1", "", routes, hosts),
            "NET-2" : network.NetworkNode("NET-2", "", routes, hosts),
            "cloud" : cloud.Cloud(),
            "LIGHT_1" : device.Device("LIGHT_1", "NET-1"),
            "LIGHT_2" : device.Device("LIGHT_2", "NET-2"),
        }
    def run(self):
        eventq = EventQueue()
        m = events.Event(events.MOTION_EVENT, 
                  0, "LIGHT_1", "LIGHT_1", {"light_id" : "LIGHT_1"})
        eventq.push(m)
        while not eventq.empty():
            event = eventq.pop()
            print "Running event on {}".format(event.dest)
            print event
            new_events = self.objects[event.dest].onEvent(event)
            print "Got new events:"
            print new_events
            for event in new_events:
                eventq.push(event)
            




s = Simulator()
s.run()