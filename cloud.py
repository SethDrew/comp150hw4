class Cloud(SimObject):
    def __init__(self):
        self.log = []

    def onEvent(self, event):
        log.append(event)

        if event.type == MOTION_EVENT:
            return []

        if event.type == LOG_MOTION_EVENT:
            return []

        if event.type == BRIGHTNESS_CONTROL_EVENT:
            new_event = Event(event.fire_time, BRIGHTNESS_CONTROL_EVENT, "cloud", "network")
            new_event.params = {
                "light_brightness": event.params.light_brightness,
                "light_id"        : event.params.light_id,
            }
            return [new_event]

        if event.type == GENERATE_UPDATE_DEFAULT_BRIGHTNESS_EVENT:
            new_event = Event(event.fire_time, GENERATE_UPDATE_DEFAULT_BRIGHTNESS_EVENT, "cloud", "network")
            new_event.params = {
                "light_brightness": event.params.light_brightness,
                "light_id"        : event.params.light_id,
            }
            return [new_event]

        if event.type == UPDATE_DEFAULT_BRIGHTNESS_EVENT:
            return []