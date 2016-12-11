#IO Specifications

##Input

The input consists of two files. The `config.json` file defines the components 
to  be created for the simulation. The `events.json` file contains all external
stimuli events (motion, human-cloud interaction, etc).

### config.json

Contains details about the components of the system.

        [{ type: 'device'
           name: "LIGHT-1",
           initial_power_level: 0.5,
           load-wattage: 60,
           system-wattage: 0.01}]

- `type`: type of component, currently only `device` is supported.
- `name`: name of the component (string)
- `initial_power_level`: initial power, expressed as a fraction of total (float)
- `load-wattage`: power in watts used when `initial_power_level` is 1 (float)
- `system-wattage`: power in watts used when control system is active (float)

### events.json

Contains a list of events to fire

        [{ fire_time: 3, 
          event_type: 0,                // Motion Event
          source: "LIGHT-1", 
          destination: "CLOUD"}]


- `fire_time`: time event will fire in micro-seconds (int)
- `event_type`: event to fire (int, see events.py for definitions)
- `source`: source name (string)
- `destination`: destination name (string)

##Output

