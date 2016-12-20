import json
import random
import sys

MICROSECONDS_IN_SECOND = 1000000;


if(sys.argv[1] == "simple"):
        events = []
        for i in range(0,int(sys.argv[2])):
                events.append({"fire_time": i*MICROSECONDS_IN_SECOND,
                               "event_type": 2,
                               "source": "CLOUD",
                               "destination": "CLOUD",
                               "parameters": {"light_id": "LIGHT-1",
                                           "light_brightness": i%2}
                               })
                               
        events.append({"fire_time": (int(sys.argv[2])-1)*MICROSECONDS_IN_SECOND,
                       "event_type": 5,
                       "source": "",
                       "destination": "",
                       "parameters": {}});
        
        text_file = open("events-on-off.json", "w")
        text_file.write(json.dumps(events,indent=4))
        text_file.close()
        
        components = [{ "type": 'device',
                        "name": "LIGHT-1",
                        "parameters": { "initial_power_level": 1,
                                        "load-wattage": 60,
                                        "system-wattage": 0.01,
                                        "network-node": "NET-1"}
                     },
                     { "type": "cloud",
                       "name": "CLOUD",
                       "parameters": {"network-node": "NET-0"}},
                     { "type": "network",
                       "name": "NET-1"}
                     ]
                     
        text_file = open("components-on-off.json", "w")
        text_file.write(json.dumps(components,indent=4))
        text_file.close()

# Random Dim of Events
if(sys.argv[1] == "random"):
        events = []
        
        for i in range(0,int(sys.argv[2])):
                events.append({"fire_time": random.randint(1, 3600*MICROSECONDS_IN_SECOND),
                               "event_type": 2,
                               "source": "CLOUD",
                               "destination": "CLOUD",
                               "parameters": {"light_id": "LIGHT-"+str(random.randint(1,5)),
                                           "light_brightness": random.random()}
                               })
        
        events.append({"fire_time": 3600*MICROSECONDS_IN_SECOND,
               "event_type": 5,
               "source": "",
               "destination": "",
               "parameters": {}});
        
        text_file = open("events-random.json", "w")
        text_file.write(json.dumps(events,indent=4))
        text_file.close()
        
        components = [
                     { "type": "cloud",
                       "name": "CLOUD",
                       "parameters": {"network-node": "NET-0"}
                     }]
                     
        for i in range(0,5):
                components.append({ "type": 'device',
                        "name": "LIGHT-"+str(i+1),
                        "parameters": { "initial_power_level": random.random(),
                                        "load-wattage": 60,
                                        "system-wattage": 0.01,
                                        "network-node": "NET-"+str(i+1)}
                     })
                components.append({ "type": "network", "name": "NET-"+str(i+1)})
                     
        text_file = open("components-random.json", "w")
        text_file.write(json.dumps(components,indent=4))
        text_file.close()
        
# Control sequence
if(sys.argv[1] == "control"):
        events = []
        
        for i in range(0,int(sys.argv[2])):
                events.append({"fire_time": 7*3600*MICROSECONDS_IN_SECOND,
                               "event_type": 2,
                               "source": "LIGHT-"+str(i+1),
                               "destination": "LIGHT-"+str(i+1),
                               "parameters": {"light_brightness": 1}})
        
                events.append({"fire_time": 9*3600*MICROSECONDS_IN_SECOND,
                               "event_type": 2,
                               "source": "LIGHT-"+str(i+1),
                               "destination": "LIGHT-"+str(i+1),
                               "parameters": {"light_brightness": 0}})
                               
                events.append({"fire_time": 18*3600*MICROSECONDS_IN_SECOND,
                               "event_type": 2,
                               "source": "LIGHT-"+str(i+1),
                               "destination": "LIGHT-"+str(i+1),
                               "parameters": {"light_brightness": 1}})
                
                events.append({"fire_time": 23*3600*MICROSECONDS_IN_SECOND,
                               "event_type": 2,
                               "source": "LIGHT-"+str(i+1),
                               "destination": "LIGHT-"+str(i+1),
                               "parameters": {"light_brightness": 0}})
                               
        events.append({"fire_time": 24*3600*MICROSECONDS_IN_SECOND, # One day
               "event_type": 5,
               "source": "",
               "destination": "",
               "parameters": {}});
        
        text_file = open("events-control.json", "w")
        text_file.write(json.dumps(events,indent=4))
        text_file.close()
        
        components = [
                     { "type": "cloud",
                       "name": "CLOUD",
                       "parameters": {"network-node": "NET-0"}
                     }]            
                     
        for i in range(0,int(sys.argv[2])):
                components.append({ "type": 'device',
                        "name": "LIGHT-"+str(i+1),
                        "parameters": { "initial_power_level": 0,
                                        "load-wattage": 60,
                                        "system-wattage": 0.01,
                                        "network-node": "NET-"+str(i+1)}
                     })
                components.append({ "type": "network", "name": "NET-"+str(i+1)})
                     
        text_file = open("components-control.json", "w")
        text_file.write(json.dumps(components,indent=4))
        text_file.close()