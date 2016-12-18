import json

MICROSECONDS_IN_SECOND = 1000000;

events = []

for i in range(0,20):
        events.append({"fire_time": i*MICROSECONDS_IN_SECOND,
                       "event_type": 2,
                       "source": "CLOUD",
                       "destination": "NETWORK",
                       "payload": {"device_id": "LIGHT-1",
                                   "brightness": i%2}
                       })

text_file = open("events1.json", "w")
text_file.write(json.dumps(events,indent=4))
text_file.close()

components = [{ "type": 'device',
                "name": "LIGHT-1",
                "parameters": { "initial_power_level": 1,
                                "load-wattage": 60,
                                "system-wattage": 0.01}
             },
             { "type": "cloud",
               "name": "CLOUD"},
             { "type": "network",
               "name": "NETWORK"}
             ]
             
text_file = open("components1.json", "w")
text_file.write(json.dumps(components,indent=4))
text_file.close()