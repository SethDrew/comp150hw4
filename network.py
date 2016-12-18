#!/usr/bin/env python
#
# Carter Casey
# Comp 150-IOT, Undergraduate Final Project
# 
# Implementation of Network simulation object.

import events

# DELAYS
TO_NET_DELAY = 5
FROM_NET_DELAY = 5

UDP_SEND_DELAY = 100
UDP_RECEIVE_DELAY = 100



class NetworkNode(events.SimObject):
	def __init__(self, sim_id, routes, hosts, host_id):
		self.sim_id = sim_id #simulation id = unique name of device
		self.host_id = host_id
		self.routing_table = routes #dictionary saying where packets can be routed to/from
		self.hosts = hosts    #list of all network nodes with what they host

	def onEvent(self, event):
		return {
			events.NETWORK_SEND : self._networkSend,
			events.NETWORK_RECEIVE : self._networkReceive,

			events.UDP_SEND : self._udpSend,
			events.UDP_RECEIVE : self._udpReceive,
			events.TCP_SEND : self._tcpSend,
			events.TCP_RECEIVE : self._tcpReceive,
			events.ZIGBEE_SEND : self._zigBeeSend,
			events.ZIGBEE_RECEIVE : self._zigBeeReceive
		}[event.type](event)

	def _networkSend(self, event):
		proto = event.params["proto"]

		send_event = events.Event(
			proto,
			event.fire_time + TO_NET_DELAY,
			event.source,
			self.sim_id,
			params = {
				"src" : event.params["src"],
				"dest" : event.params["dest"],
				"payload" : event.params["payload"]
			}
		)
		return [send_event]

	def _networkReceive(self, event):
		received_event = event.params["payload"]
		print received_event

		received_event.fire_time = event.fire_time + FROM_NET_DELAY

		return [received_event]

	def _udpSend(self, event):
		next_hop = self.routing_table[self.hosts[event.params["dest"]]]
		return [events.Event(
			events.UDP_RECEIVE,
			event.fire_time,
			self.sim_id,
			next_hop,
			event.params
		)]

	def _udpReceive(self, event):
		if self.hosts[event.params["dest"]] == self.sim_id:
			print self.host_id
			return [events.Event(
				events.NETWORK_RECEIVE,
				event.fire_time + UDP_RECEIVE_DELAY,
				self.sim_id,
				self.host_id,
				params = event.params
			)]

		else:
			event.fire_time += UDP_RECEIVE_DELAY
			return self._udpSend(event)
			

	def _tcpSend(self, event):
		raise NotImplementedError("TCP SEND unfinished")

	def _tcpReceive(self, event):
		raise NotImplementedError("TCP RECEIVE unfinished")

	def _zigBeeSend(self, event):
		raise NotImplementedError("ZIGBEE SEND unfinished")

	def _zigBeeReceive(self, event):
		raise NotImplementedError("ZIGBEE RECEIVE unfinished")


def test():
	"""test(): Validates the path of a UDP message between network nodes."""
	hosts = {
		"LIGHT-1" : "NET-1",
		"LIGHT-2" : "NET-2",
		"COORDINATOR" : "NET-1"
	}

	routes = { "NET-1" : "NET-1" , "NET-2" : "NET-2" }

	# Would typically be associated with a host.
	#SETH: why have you not associated these with hosts as in your hosts = {}?
	a = NetworkNode("NET-1", None, routes, hosts) 
	b = NetworkNode("NET-2", None, routes, hosts)

	msg_params = {
		"proto" : events.UDP_SEND, # Additional param for NETWORK_SEND event.

		# Typical network event parameters:
		"src" : "LIGHT-1",
		"dest" : "LIGHT-2",
		"payload" : events.Event(
			events.UPDATE_DEFAULT_BRIGHTNESS_EVENT,
			None,
			"LIGHT-1",
			"LIGHT-2",
			params = { "new-brightness" : .2 }
		)
	}

	net_event = events.Event(
		events.NETWORK_SEND,
		0,
		"LIGHT-1",
		"NET-1",
		msg_params
	)

	#Light 1 tells Net1 to send info
	after_net_send = a.onEvent(net_event)[0]
	assert after_net_send.type == events.UDP_SEND

	#Net1 tells Net2 that its sending info
	after_udp_send = a.onEvent(after_net_send)[0]
	assert after_udp_send.type == events.UDP_RECEIVE

	#Net 2 gets the event
	after_udp_receive = b.onEvent(after_udp_send)[0]
	assert after_udp_receive.type == events.NETWORK_RECEIVE

	#Net 2 tells Light 2 that it should adjust brightness
	after_net_receive = b.onEvent(after_udp_receive)[0]
	assert after_net_receive.type == events.UPDATE_DEFAULT_BRIGHTNESS_EVENT

if __name__ == '__main__':
	test()
