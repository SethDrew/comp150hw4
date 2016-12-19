import events
CLOUD_DELAY = 10
INTERNAL_DELAY = 10

class Cloud(events.SimObject):
    def __init__(self, node):
        self.node = node
        self.log = []
        self._writeCount = 0
        self._readCount = 0
        self._time = 0

    def onEvent(self, event):
        self.log.append(event)


        if event.type == events.LOG_MOTION_EVENT:
            brightness_control = events.Event(
                events.BRIGHTNESS_CONTROL_EVENT,
                event.fire_time + CLOUD_DELAY,
                "cloud",
                "cloud")
            brightness_control.params = {
                "light_brightness" : 0.7,
                "light_id" : event.source
            }
            writeCount = writeCount + 1
            self._time = fire_time
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
                event.fire_time + INTERNAL_DELAY,
                "cloud",
                self.node)
            new_network_send.params = {
                "src" : "cloud",
                "dest" : event.params["light_id"],
                "payload" : brightness_control,
                "proto" : events.UDP_SEND
            }
            readCount = readCount + 1
            self._time = fire_time
            return [new_network_send]


        if event.type == events.UPDATE_DEFAULT_BRIGHTNESS_EVENT:
            self._time = fire_time
            return []

    def power(self):
        return 0 #so it doesn't crash

    def cost(self):
        #Based on the cost to run a Amazon Database where
        #Write Throughput: $0.0065 per hour for every 10 units of Write Capacity
        #Read Throughput: $0.0065 per hour for every 50 units of Read Capacity
        writeCost = 0.0065 * (self._writeCount/10.0)
        readCost = 0.0065 * (self._readCount/50.0)
        totalCost = (writeCost + readCost)/(self._time/1000000.0/60.0/60.0)
        return totalCost #defined in sim_object. you should find out how much power the cloud might take on every operation