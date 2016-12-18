import events
import device
import network
import cloud






class Simulator:
    def __init__(self, input_events):
        routes = { "NET-1" : "NET-1" , "NET-2" : "NET-2" }
        hosts = {
            "LIGHT-1" : "NET-1",
            "LIGHT-2" : "NET-2",
            "COORDINATOR" : "NET-1"
        }
        self.objects = {
            "nn1" : network.NetworkNode("NET-1", "", routes, hosts),
            "nn2" : network.NetworkNode("NET-2", "", routes, hosts),
            "c" : cloud.Cloud(),
            "d1" : device.Device("LIGHT_1"),
            "d2" : device.Device("LIGHT_2"),
            "event_queue" : input_events
        }
    def run(self):
        m = events.Event(events.MOTION_EVENT, 
                  0, "LIGHT_1", "LIGHT_1", {"light_id" : "LIGHT_1"})
        print self.objects["d1"].onEvent(m)




s = Simulator([])
s.run()