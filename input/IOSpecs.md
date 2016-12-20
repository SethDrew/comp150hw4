#IO Specifications

##Input

The input consists of two files. The `config.json` file defines the components 
to  be created for the simulation. The `events.json` file contains all external
stimuli events (motion, human-cloud interaction, etc).

### config.json

Contains details about the components of the system.

        [{ "type": 'device'
           "name": "LIGHT-1",
           "parameters": {
                            "standby-usage": 5, 
                            "max-lumens": 809, 
                            "network-node": "NET-1", 
                            "lumens-per-watt": 70.3, 
                            "default-brightness": 1
                          }
        }]

- `type`: type of component, currently only `device` is supported.
- `name`: name of the component (string)
- `parameters`: the parameters required for a particular component

### events.json

Contains a list of events to fire

        [{ "fire_time": 3, 
          "event_type": 0,                // Motion Event
          "source": "LIGHT-1", 
          "destination": "CLOUD",
          "parameter": {"brightness": 1}}]


- `fire_time`: time event will fire in micro-seconds (int)
- `event_type`: event to fire (int, see events.py for definitions)
- `source`: source name (string)
- `destination`: destination name (string)
- `parameters`: list of message parameter items

### Input Generator

To generate config & event files, run the included python script:

        python generate.py [mode] [number of events]

Modes supported:
- `simple`: generates cloud created on and off events for 1 light every second
- `random`: generates random brightness events for random lights at random times
- `control`: generates a control scenario for 1 person
- `one-person`: generates an IOT scenario for 1 person