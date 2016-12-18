import events
CLOUD_DELAY = 10

class Cloud(events.SimObject):
    def __init__(self, node):
        self.node = node
        self.log = []

    def onEvent(self, event):
        self.log.append(event)


        if event.type == LOG_MOTION_EVENT:
            brightness_control = events.Event(
                events.BRIGHTNESS_CONTROL_EVENT,
                event.fire_time + CLOUD_DELAY,
                "cloud",
                event.source)
            brightness_control.params = {
                "light_brightness" : 0.7,
                "light_id" : event.source
            }

            new_network_send = events.Event(
                events.NETWORK_SEND,
                event.fire_time + INTERNAL_DELAY,
                self.id,
                self.node)
            new_network_send.params = {
                "src" : "cloud",
                "dest" : event.params["src"],
                "payload" : brightness_control,
                "proto" : events.UDP_SEND
            }

            return [new_network_send]

        if event.type == BRIGHTNESS_CONTROL_EVENT:
           
            return []


        if event.type == UPDATE_DEFAULT_BRIGHTNESS_EVENT:
            return []

    def power():
        return self.power #defined in sim_object. you should find out how much power the cloud might take on every operation