import events

class Cloud(events.SimObject):
    def __init__(self, node):
        self.node = node
        self.log = []

    def onEvent(self, event):
        self.log.append(event)


        if event.type == LOG_MOTION_EVENT:
            return []

        if event.type == BRIGHTNESS_CONTROL_EVENT:
           
            return []


        if event.type == UPDATE_DEFAULT_BRIGHTNESS_EVENT:
            return []

    def power():
        return self.power #defined in sim_object. you should find out how much power the cloud might take on every operation