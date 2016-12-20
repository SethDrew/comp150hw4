import json
import random
import sys

MICROSECONDS_IN_SECOND = 1000000;


if(sys.argv[1] == "simple"):
        events = []
        for i in range(0,int(sys.argv[2])):
                events.append({"fire_time": i*MICROSECONDS_IN_SECOND,
                               "event_type": 2,
                               "source": "cloud",
                               "destination": "cloud",
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
                        "parameters": { "default-brightness": 1,
                                        "max-lumens": 800,
                                        "lumens-per-watt": 14,
                                        "standby-usage": 5,
                                        "network-node": "NET-1"}
                     },
                     { "type": "cloud",
                       "name": "cloud",
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
                               "source": "cloud",
                               "destination": "cloud",
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
                       "name": "cloud",
                       "parameters": {"network-node": "NET-0"}
                     }]
                     
        for i in range(0,5):
                components.append({ "type": 'device',
                        "name": "LIGHT-"+str(i+1),
                        "parameters": { "default-brightness": random.random(),
                                        "max-lumens": 800,
                                        "lumens-per-watt": 14,
                                        "standby-usage": 5,
                                        "network-node": "NET-"+str(i+1)}
                     })
                components.append({ "type": "network", "name": "NET-"+str(i+1)})
                     
        text_file = open("components-random.json", "w")
        text_file.write(json.dumps(components,indent=4))
        text_file.close()
        
# Control sequence
if(sys.argv[1] == "control"):
        events = []
        
        lights = ["LIGHT-BEDROOM", "LIGHT-BATHROOM", "LIGHT-KITCHEN", "LIGHT-LIVING"]
        
        for i in range(0,int(sys.argv[2])):
                events.append({"fire_time": 7*3600*MICROSECONDS_IN_SECOND,
                               "event_type": 2,
                               "source": lights[i],
                               "destination": lights[i],
                               "parameters": {"light_brightness": 1}})
        
                events.append({"fire_time": 9*3600*MICROSECONDS_IN_SECOND,
                               "event_type": 2,
                               "source": lights[i],
                               "destination": lights[i],
                               "parameters": {"light_brightness": 0}})
                               
                events.append({"fire_time": 18*3600*MICROSECONDS_IN_SECOND,
                               "event_type": 2,
                               "source": lights[i],
                               "destination": lights[i],
                               "parameters": {"light_brightness": 1}})
                
                events.append({"fire_time": 23*3600*MICROSECONDS_IN_SECOND,
                               "event_type": 2,
                               "source": lights[i],
                               "destination": lights[i],
                               "parameters": {"light_brightness": 0}})
                               
        events.append({"fire_time": 24*3600*MICROSECONDS_IN_SECOND, # One day
               "event_type": 5,
               "source": "",
               "destination": "",
               "parameters": {}});
        
        text_file = open("events-control.json", "w")
        text_file.write(json.dumps(events,indent=4))
        text_file.close()
        
        components = []     
                     
        for i in range(0,int(sys.argv[2])):
                components.append({ "type": 'device',
                        "name": lights[i],
                        "parameters": { "default-brightness": 1,
                                        "max-lumens": 850,
                                        "lumens-per-watt": 14,
                                        "standby-usage": 0,
                                        "network-node": ""}
                     })
                     
        text_file = open("components-control.json", "w")
        text_file.write(json.dumps(components,indent=4))
        text_file.close()
        
        
if(sys.argv[1] == "motion"):
        events = []
        
        for i in range(0,int(sys.argv[2])):
                events.append({"fire_time": 3600*MICROSECONDS_IN_SECOND,
                               "event_type": 0,
                               "source": "LIGHT-"+str(i+1),
                               "destination": "cloud",
                               "parameters": {}})
                
                events.append({"fire_time": 2*3600*MICROSECONDS_IN_SECOND,
                               "event_type": 2,
                               "source": "LIGHT-"+str(i+1),
                               "destination": "LIGHT-"+str(i+1),
                               "parameters": {"light_brightness": 0}})
        
                               
        events.append({"fire_time": 3*3600*MICROSECONDS_IN_SECOND, # 3 hours
               "event_type": 5,
               "source": "",
               "destination": "",
               "parameters": {}});
        
        text_file = open("events-motion.json", "w")
        text_file.write(json.dumps(events,indent=4))
        text_file.close()
        
        components = [
                     { "type": "cloud",
                       "name": "cloud",
                       "parameters": {"network-node": "NET-0"}
                     }]            
                     
        for i in range(0,int(sys.argv[2])):
                components.append({ "type": 'device',
                        "name": "LIGHT-"+str(i+1),
                        "parameters": { "default-brightness": 1,
                                        "max-lumens": 850,
                                        "lumens-per-watt": 14,
                                        "standby-usage": 5,
                                        "network-node": "NET-"+str(i+1)}
                     })
                components.append({ "type": "network", "name": "NET-"+str(i+1)})
                     
        text_file = open("components-motion.json", "w")
        text_file.write(json.dumps(components,indent=4))
        text_file.close()
        
        
if(sys.argv[1] == "one-person"):
        events = []
        

        events.append({"fire_time": 7*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 2,
                       "source": "cloud",
                       "destination": "cloud",
                       "parameters": {"light_id": "LIGHT-BEDROOM",
                                   "light_brightness": 1}})
        
        events.append({"fire_time": 7.5*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 2,
                       "source": "LIGHT-BEDROOM",
                       "destination": "LIGHT-BEDROOM",
                       "parameters": {"light_brightness": 0}})

        events.append({"fire_time": 7.5*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 0,
                       "source": "LIGHT-BATHROOM",
                       "destination": "cloud",
                       "parameters": {}})
        
        events.append({"fire_time": 8*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 2,
                       "source": "LIGHT-BATHROOM",
                       "destination": "LIGHT-BATHROOM",
                       "parameters": {"light_brightness": 0}})
                       
        events.append({"fire_time": 8*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 0,
                       "source": "LIGHT-KITCHEN",
                       "destination": "cloud",
                       "parameters": {}})
                       
        events.append({"fire_time": 8.5*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 2,
                       "source": "LIGHT-KITCHEN",
                       "destination": "LIGHT-KITCHEN",
                       "parameters": {"light_brightness": 0}})
                       
        events.append({"fire_time": 8*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 0,
                       "source": "LIGHT-LIVING",
                       "destination": "cloud",
                       "parameters": {}})
                       
        events.append({"fire_time": 8.5*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 2,
                       "source": "LIGHT-LIVING",
                       "destination": "LIGHT-LIVING",
                       "parameters": {"light_brightness": 0}})
                       
                       
        events.append({"fire_time": 18*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 2,
                       "source": "cloud",
                       "destination": "cloud",
                       "parameters": {"light_id": "LIGHT-KITCHEN",
                                   "light_brightness": 1}})
        
        events.append({"fire_time": 18.5*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 2,
                       "source": "LIGHT-KITCHEN",
                       "destination": "LIGHT-KITCHEN",
                       "parameters": {"light_brightness": 0}})

        events.append({"fire_time": 18.5*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 0,
                       "source": "LIGHT-LIVING",
                       "destination": "cloud",
                       "parameters": {}})
        
        events.append({"fire_time": 20*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 2,
                       "source": "LIGHT-LIVING",
                       "destination": "LIGHT-LIVING",
                       "parameters": {"light_brightness": 0}})
                       
        events.append({"fire_time": 20*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 0,
                       "source": "LIGHT-KITCHEN",
                       "destination": "cloud",
                       "parameters": {}})
                       
        events.append({"fire_time": 20.25*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 2,
                       "source": "LIGHT-KITCHEN",
                       "destination": "LIGHT-KITCHEN",
                       "parameters": {"light_brightness": 0}})
                       
        events.append({"fire_time": 20.25*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 0,
                       "source": "LIGHT-LIVING",
                       "destination": "cloud",
                       "parameters": {}})
                       
        events.append({"fire_time": 22.5*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 2,
                       "source": "LIGHT-LIVING",
                       "destination": "LIGHT-LIVING",
                       "parameters": {"light_brightness": 0}})
        
        events.append({"fire_time": 22.5*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 0,
                       "source": "LIGHT-BATHROOM",
                       "destination": "cloud",
                       "parameters": {}})
                       
        events.append({"fire_time": 22.75*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 2,
                       "source": "LIGHT-BATHROOM",
                       "destination": "LIGHT-BATHROOM",
                       "parameters": {"light_brightness": 0}})
        
        events.append({"fire_time": 22.75*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 0,
                       "source": "LIGHT-BATHROOM",
                       "destination": "cloud",
                       "parameters": {}})
                       
        events.append({"fire_time": 23*3600*MICROSECONDS_IN_SECOND,
                       "event_type": 2,
                       "source": "cloud",
                       "destination": "cloud",
                       "parameters": {"light_id": "LIGHT-BEDROOM",
                                   "light_brightness": 0}})
        
                               
        events.append({"fire_time": 24*3600*MICROSECONDS_IN_SECOND, # One day
               "event_type": 5,
               "source": "",
               "destination": "",
               "parameters": {}});
        
        text_file = open("events-one-person.json", "w")
        text_file.write(json.dumps(events,indent=4))
        text_file.close()
        
        components = [
                     { "type": "cloud",
                       "name": "cloud",
                       "parameters": {"network-node": "NET-0"}
                     }]            
        
        lights = ["LIGHT-BEDROOM", "LIGHT-BATHROOM", "LIGHT-KITCHEN", "LIGHT-LIVING"]
        
        for i in range(0,len(lights)):
                components.append({ "type": 'device',
                        "name": lights[i],
                        "parameters": { "default-brightness": 1,
                                        "max-lumens": 809,
                                        "lumens-per-watt": 70.3,
                                        "standby-usage": 5,
                                        "network-node": "NET-"+str(i+1)}
                     })
                components.append({ "type": "network", "name": "NET-"+str(i+1)})
                     
        text_file = open("components-one-person.json", "w")
        text_file.write(json.dumps(components,indent=4))
        text_file.close()