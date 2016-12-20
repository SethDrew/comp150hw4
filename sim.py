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
                self.objects[item["name"]] = cloud.Cloud(item["name"], item["parameters"]["network-node"])
                hosts[item["name"]] = item["parameters"]["network-node"]
            
            # Add device and host network node
            elif(item["type"] == "device"):
                self.objects[item["name"]] = device.Device(item["type"], 
                                                           item["parameters"]["network-node"],
                                                           item["parameters"]["lumens-per-watt"],
                                                           item["parameters"]["max-lumens"],
                                                           item["parameters"]["standby-usage"])
                hosts[item["name"]] = item["parameters"]["network-node"]
                
        #Add network nodes
        for host in hosts:
            self.objects[hosts[host]] = network.NetworkNode(hosts[host], host, routes, hosts)
            

    def run(self, event_file):
        
        eventq = EventQueue()
                 
        with open(event_file) as data_file:    
            event_data = json.load(data_file)
           
        # Add every event to the queue
        for event in event_data:
            if(event["event_type"] != 5): # Don't do this for exit events 
                temp = events.Event(int(event["event_type"]),
                                    int(event["fire_time"]),
                                    event["source"],
                                    event["destination"],
                                    event["parameters"])            
                eventq.push(temp)
            else:                           # but store the exit time for later
                end_time = int(event["fire_time"])            
        with open("results/power_bytime.txt", "w") as f:
            while not eventq.empty():
                event = eventq.pop()
                if VERBOSE: 
                    print "{} : {} --> {}".format(event._event_to_string[event.type], event.source, event.dest)
                if DEBUG:
                    print "{}.onEvent({})".format(event.dest, event._event_to_string[event.type])
                new_events = self.objects[event.dest].onEvent(event)
                
                #object is outputting x watts for y seconds.
                #if it is a network object, I need to say for "delay" seconds
                for k, o in self.objects.iteritems():
                    f.write("{}:{}:{}\n".format(k, o.current_power(event), event.fire_time / events.ONE_SECOND))

                if DEBUG:
                    print "Got resulting events:"
                    print new_events

                for event in new_events:
                    eventq.push(event)



        #using leftover last event that was registered for the last fire time              
        exit_event = events.Event(events.EXIT_EVENT, end_time, "", "") 
        with open("results/exit_power_totals.txt", "w") as f:

            for k, o in self.objects.iteritems():
                o.onEvent(exit_event) #tell each object that the game is over. time to go home.
                if(o.id.startswith("cloud")):
                    print "{} used {} Dollars".format(k, o.cost(exit_event.fire_time)) #each object should have updated power now.
                    f.write("{}:{}\n".format(k, o.cost(exit_event.fire_time)))
                else:
                    kwh = o.power()/(1000 * 3600)
                    print "{} used {} kWH".format(k, kwh) #each object should have updated power now.
                    f.write("{}:{}\n".format(k, kwh))


config_file = sys.argv[1]
event_file = sys.argv[2]

s = Simulator(config_file)
s.run(event_file)