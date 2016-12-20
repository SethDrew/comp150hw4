#IO Specifications

##Input

The input consists of two files. The `config.json` file defines the components 
to  be created for the simulation. The `events.json` file contains all external
stimuli events (motion, human-cloud interaction, etc).

### config.json

Contains details about the components of the system.

        [{ "type": 'device'
           "name": "LIGHT-1",
           "parameters": {"initial_power_level": 0.5,
                          "load-wattage": 60,
                          "system-wattage": 0.01,
                          "network-node": "NET-1"}
        }]

- `type`: type of component, currently only `device` is supported.
- `name`: name of the component (string)
- `parameters`: the parameters required for a particular component

TODO: Add details on parameters

### events.json

Contains a list of events to fire

        [{ "fire_time": 3, 
          "event_type": 0,                // Motion Event
          "source": "LIGHT-1", 
          "destination": "CLOUD",
          "payload": {"brightness": 1}}]


- `fire_time`: time event will fire in micro-seconds (int)
- `event_type`: event to fire (int, see events.py for definitions)
- `source`: source name (string)
- `destination`: destination name (string)
- `payload`: list of message payload items

### Input Generator

To generate config & event files, run the included python script:

        python generate.py [mode] [number of events]

Modes supported:
- `simple`: generates cloud created on and off events for 1 light every second
- `random`: generates random brightness events for random lights at random times

##Output

One summary output is generated for each run of the simulation.

###usage.json

Contains information about simulation that ran

        {"input-event-file": "events.json",
         "input-config-file": "config.json",
         "simulation-duration": 6000000000,
         "component-power-usage":
                [{ "name": "LIGHT-1", 
                  "control-consumption": 1.34,
                  "load-consumption": 140, 
                }]
        }
- `input-event-file`: input file used for event generation
- `input-config-file`: input file used for component generation
- `simulation-duration`: length of simulation in microseconds
- `component-power-usage`: list of power usage for each component:
        - `name`: name of component
        - `control-consumption`: power in Watts used by the control system
        - `load-consumption`: power in Watts used by the load