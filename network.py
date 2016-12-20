#!/usr/bin/env python
#
# Carter Casey
# Comp 150-IOT, Undergraduate Final Project
# 
# Implementation of Network simulation object.

import events

# DELAYS (in microseconds)
TO_NET_DELAY = 5
FROM_NET_DELAY = 5

UDP_SEND_DELAY = 8000
UDP_RECEIVE_DELAY = 2000

TCP_SEND_DELAY = 12000
TCP_RECEIVE_DELAY = 3000

TCP_ACK_DELAY = 500


# POWER CONSUMPTION
HIGH = .750 # mW
LOW = .250  # mW


# PROTOCOLS
UDP = events.UDP_SEND
TCP = events.TCP_SEND

class NetworkNode(events.SimObject):
	"""NetworkNode(sim_id, host_id, routes, hosts)

	An object that sends and receives network events.

	Params:
		sim_id - Unique ID of this object in the simulation.
		host_id - Simulation ID of associated host.
		routes - Mapping from destination to next hop node.
		hosts - Mapping from host ID to node ID.
		high_watts - Power consumption during active transmission and receipt.
		low_watts - Power consumption during passive listening.

	Methods:
		onEvent - Acts on given event, returns resulting list of events. Inherited.
		power - Returns the power usage from the simulation. Inhereted from SimObject
	"""
	def __init__(self, sim_id, host_id, routes, hosts, high_watts=HIGH, low_watts=LOW):
		self.id = sim_id
		self._host_id = host_id
		self._routing_table = routes
		self._hosts = hosts
		self._high = high_watts
		self._low = low_watts

		self._next_seq = 0
		self._pending_messages = {} # Map from seq number to message

		self._last_event_time = 0
		self._power = 0
		self._curpower = 0
		self._delay = 0
	def onEvent(self, event):
		"""onEvent(event)

		Acts on new event on "network layer", registers all resulting events.

		Params:
			event - events.Event object, one of the type given below in EVENTS.

		Returns:
			events - List of resulting events.

		EVENTS: Accepts any of the following events.EVENT types.
			NETWORK_SEND - Used by host to register new message being sent.
			NETWORK_RECEIVE - Used by node to communicate new message to host.
			UDP_SEND - Used by node to register new UDP message with itself.
			UDP_RECEIVE - Used by node to register receipt of UDP message.
			TCP_SEND - Used by node to register new TCP message with itself.
			TCP_RECEIVE - Used by node to register receipt of TCP message.
		"""
		if event.type == events.EXIT_EVENT:
			self._power += self._low * (event.fire_time - self._last_event_time) * events.TIMESTEP
			self._last_event_time = event.fire_time

			return []
			
		new_events = {
			events.NETWORK_SEND : self._networkSend,
			events.NETWORK_RECEIVE : self._networkReceive,

			events.UDP_SEND : self._udpSend,
			events.UDP_RECEIVE : self._udpReceive,
			events.TCP_SEND : self._tcpSend,
			events.TCP_RECEIVE : self._tcpReceive,
		}[event.type](event)

		self._delay = new_events[0].fire_time - event.fire_time

		self._power += (
			self._low * (new_events[0].fire_time - self._last_event_time) +
			self._high * (self._delay / 4) # Estimate a quarter of delay isn't prop
		) * events.TIMESTEP

		self._last_event_time = event.fire_time

		return new_events

	def power(self):
		return self._power

	def current_power(self, event):
		if event.fire_time > self._delay + self._last_event_time:
			return self._low
		else:
			return self._high

	def _networkSend(self, event):
		proto = event.params["proto"]

		send_event = events.Event(
			proto,
			event.fire_time + TO_NET_DELAY,
			event.source,
			self.id,
			params = {
				"src" : event.params["src"],
				"dest" : event.params["dest"],
				"payload" : event.params["payload"]
			}
		)

		return [send_event]

	def _networkReceive(self, event):
		received_event = event.params["payload"]

		received_event.fire_time = event.fire_time + FROM_NET_DELAY

		return [received_event]

	def _udpSend(self, event):
		next_hop = self._routing_table[self._hosts[event.params["dest"]]]

		return [events.Event(
			events.UDP_RECEIVE,
			event.fire_time + UDP_SEND_DELAY,
			self.id,
			next_hop,
			event.params
		)]

	def _udpReceive(self, event):
		event.fire_time += UDP_RECEIVE_DELAY

		if self._hosts[event.params["dest"]] == self.id:
			return [events.Event(
				events.NETWORK_RECEIVE,
				event.fire_time,
				self.id,
				self.id,
				params = event.params
			)]
		else:
			return self._udpSend(event)
			

	def _tcpSend(self, event):
		if not "tcp-type" in event.params:
			syn_event = events.Event(
				events.TCP_SEND,
				event.fire_time,
				self.id,
				event.dest,
				params = {
					"tcp-type" : "SYN",
					"seq-no" : self._next_seq,
					"src" : event.params["src"],
					"dest" : event.params["dest"]
				}
			)

			event.params["tcp-type"] = "MSG"

			self._pending_messages[self._next_seq] = event
			self._next_seq += 1

			event = syn_event

		next_hop = self._routing_table[self._hosts[event.params["dest"]]]

		return [events.Event(
			events.TCP_RECEIVE,
			event.fire_time + TCP_SEND_DELAY,
			self.id,
			next_hop,
			event.params
		)]

	def _tcpReceive(self, event):
		tcp_type = event.params["tcp-type"]

		if tcp_type == "ACK": return []

		event.fire_time += TCP_RECEIVE_DELAY

		if self._hosts[event.params["dest"]] == self.id:
			if tcp_type == "SYN" or tcp_type == "SYN-ACK":
				response = events.Event(
					events.TCP_SEND,
					event.fire_time,
					self.id,
					event.params["src"],
					params = {
						"tcp-type" : "SYN-ACK" if tcp_type == "SYN" else "ACK",
						"seq-no" : event.params["seq-no"], 
						"src" : event.params["dest"],
						"dest" : event.params["src"]
					}
				)

				if tcp_type == "SYN":
					return [response]

				elif tcp_type == "SYN-ACK":
					message = self._pending_messages[event.params["seq-no"]]
					message.fire_time = event.fire_time + TCP_ACK_DELAY

					return [response, message]

			elif tcp_type == "MSG":
				return [events.Event(
					events.NETWORK_RECEIVE,
					event.fire_time,
					self.id,
					self.id,
					params = event.params
				)]
		else:
			return self._tcpSend(event)

def test():
	hosts = {
		"LIGHT-1" : "NET-1",
		"LIGHT-2" : "NET-2",
		"COORDINATOR" : "NET-1"
	}

	routes = { "NET-1" : "NET-1" , "NET-2" : "NET-2" }

	# Would typically be associated with a host, but that requires Devices.
	a = NetworkNode("NET-1", None, routes, hosts) 
	b = NetworkNode("NET-2", None, routes, hosts)

	testUDP(a, b)
	testTCP(a, b)

def testUDP(a, b):
	"""testUDP(a, b) -> Validates the path of a UDP message between a and b."""

	msg_params = {
		"proto" : UDP, # Additional param for NETWORK_SEND event.

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

	# Light 1 tells Net 1 to send info
	after_net_send = a.onEvent(net_event)[0]
	assert after_net_send.type == events.UDP_SEND

	# Net 1 tells Net 2 that its sending info
	after_udp_send = a.onEvent(after_net_send)[0]
	assert after_udp_send.type == events.UDP_RECEIVE

	# Net 2 gets the event
	after_udp_receive = b.onEvent(after_udp_send)[0]
	assert after_udp_receive.type == events.NETWORK_RECEIVE

	# Net 2 tells Light 2 that it should adjust brightness
	after_net_receive = b.onEvent(after_udp_receive)[0]
	assert after_net_receive.type == events.UPDATE_DEFAULT_BRIGHTNESS_EVENT

def testTCP(a, b):
	"""testTCP() -> Validates the path of a TCP message between a and b."""
	msg_params = {
		"proto" : TCP,

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

	after_net_send = a.onEvent(net_event)[0]
	assert after_net_send.type == events.TCP_SEND

	after_syn_send = a.onEvent(after_net_send)[0]
	assert after_syn_send.type == events.TCP_RECEIVE
	assert after_syn_send.params["tcp-type"] == "SYN"

	after_syn_receive = b.onEvent(after_syn_send)[0]
	assert after_syn_receive.type == events.TCP_SEND
	assert after_syn_receive.params["tcp-type"] == "SYN-ACK"

	after_synack_send = b.onEvent(after_syn_receive)[0]
	assert after_synack_send.type == events.TCP_RECEIVE

	after_synack_receive, message = a.onEvent(after_synack_send)
	assert after_synack_receive.type == events.TCP_SEND
	assert after_synack_receive.params["tcp-type"] == "ACK"

	assert message.type == events.TCP_SEND
	assert message.params["tcp-type"] == "MSG"	

	after_message_send = a.onEvent(message)[0]
	assert after_message_send.type == events.TCP_RECEIVE

	after_message_receive = b.onEvent(after_message_send)[0]
	assert after_message_receive.type == events.NETWORK_RECEIVE

	after_net_receive = b.onEvent(after_message_receive)[0]
	assert after_net_receive.type == events.UPDATE_DEFAULT_BRIGHTNESS_EVENT


if __name__ == '__main__':
	test()
