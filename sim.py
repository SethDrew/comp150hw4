import events
import device
import network
import cloud
import sys 
import json

import heapq

DEBUG = 1
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
    def __init__(self, config_file):
            
        with open(config_file) as data_file:    
                config_data = json.load(data_file)
        
        print(config_data)
        
        routes = {}
        hosts = {}
        self.objects = {}
        
        #Process all components
        for item in config_data:
            
            # Add networks to routes, they'll be added as objects later
            if(item["type"] == "network"):
                routes[item["name"]] = item["name"]
           
            # Add cloud
            elif(item["type"] == "cloud"):
                self.objects[item["name"]] = cloud.Cloud(item["parameters"]["network-node"])
                hosts[item["name"]] = item["parameters"]["network-node"]
            
            # Add device and host network node
            elif(item["type"] == "device"):
                self.objects[item["name"]] = device.Device(item["type"], item["parameters"]["network-node"])
                hosts[item["name"]] = item["parameters"]["network-node"]
                
        #Add network nodes
        for host in hosts:
            self.objects[hosts[host]] = network.NetworkNode(hosts[host], host, routes, hosts)
        
        print(hosts)
        print(self.objects)
            

#         #Each object has a unique network node associated with it. 
#         #We are assuming only one hop is neccessary for now
#         hosts = {
#             "LIGHT-1" : "NET-1",
#             "LIGHT-2" : "NET-2",
#             "cloud"   : "NET-3",
#         }
#         self.objects = {
#             "NET-1" : network.NetworkNode("NET-1", "LIGHT-1", routes, hosts),
#             "NET-2" : network.NetworkNode("NET-2", "LIGHT-2", routes, hosts),
#             "NET-3" : network.NetworkNode("NET-3", "cloud", routes, hosts),
#             "cloud" : cloud.Cloud("NET-3"),
#             "LIGHT-1" : device.Device("LIGHT-1", "NET-1"),
#             "LIGHT-2" : device.Device("LIGHT-2", "NET-2"),
#         }
    def run(self, event_file):
        
        eventq = EventQueue()
        # m = events.Event(events.MOTION_EVENT, 
        #           0, "LIGHT-1", "LIGHT-1", {"light_id" : "LIGHT-1"})
#         user_control_event = events.Event(events.BRIGHTNESS_CONTROL_EVENT, 
#                         0, "CLOUD", "CLOUD", {"light_id" : "LIGHT-1", "light_brightness" : .7})
#         
#         eventq.push(user_control_event)
                        
                        
        with open(event_file) as data_file:    
            event_data = json.load(data_file)
           
        # Add every event to the queue
        for event in event_data: 
            print(event)               
            temp = events.Event(int(event["event_type"]),
                                int(event["fire_time"]),
                                event["source"],
                                event["destination"],
                                event["parameters"])            
            eventq.push(temp)            
                        
        
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

        for k, o in self.objects.iteritems():
            print "{} used {} Watts".format(k, o.power())
            


config_file = sys.argv[1]
event_file = sys.argv[2]

s = Simulator(config_file)
s.run(event_file)