import events
CLOUD_DELAY = 200000

class Cloud(events.SimObject):
    def __init__(self, id, node):
        self.id = id
        self.node = node
        self.log = []
        self._writeCount = 0
        self._readCount = 0
        self._time = 0

    def onEvent(self, event):
        self.log.append(event)


        if event.type == events.MOTION_EVENT:
            brightness_control = events.Event(
                events.BRIGHTNESS_CONTROL_EVENT,
                event.fire_time + CLOUD_DELAY,
                "cloud",
                "cloud")
            brightness_control.params = {
                "light_brightness" : 0.7,
                "light_id" : event.source
            }
            self._writeCount = self._writeCount + 1
            return [brightness_control]

        if event.type == events.BRIGHTNESS_CONTROL_EVENT:
           
            brightness_control = events.Event(
                events.BRIGHTNESS_CONTROL_EVENT,
                event.fire_time + CLOUD_DELAY,
                "cloud",
                event.params["light_id"])
            brightness_control.params = {
                "light_brightness" : event.params["light_brightness"],
                "light_id" : event.params["light_id"]
            }

            new_network_send = events.Event(
                events.NETWORK_SEND,
                event.fire_time + CLOUD_DELAY,
                "cloud",
                self.node)
            new_network_send.params = {
                "src" : "cloud",
                "dest" : event.params["light_id"],
                "payload" : brightness_control,
                "proto" : events.UDP_SEND
            }
            self._readCount = self._readCount + 1
            return [new_network_send]


        if event.type == events.UPDATE_DEFAULT_BRIGHTNESS_EVENT:
            return []
        if event.type == events.EXIT_EVENT:
            self._time = event.fire_time
            return []

    def cost(self, current_time):
        #Based on the cost to run a Amazon Database where
        #Write Throughput: $0.0065 per hour for every 10 units of Write Capacity
        #Read Throughput: $0.0065 per hour for every 50 units of Read Capacity
        writeCost = 0.0065 * (self._writeCount/10.0) / (3600)
        readCost = 0.0065 * (self._readCount/50.0) / (3600)
        totalCost = (writeCost + readCost)/(current_time*events.TIMESTEP)
        return totalCost #defined in sim_object. you should find out how much power the cloud might take on every operation