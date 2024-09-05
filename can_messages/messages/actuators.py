#!/usr/bin/python3

from abstract.signals import Bool
from abstract.modules import Module
from abstract.message import Message

db = [

	Message(0x0C1, 'actuators_status', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Bool('servos', 7),
		Bool('magnet', 6),
		Bool('fan',	5),
		Bool('horn', 4),
		Bool('light4', 3),
		Bool('light3', 2),
		Bool('light2', 1),
		Bool('light1', 0)
	]),

	Message(0x0C2, 'actuators_set', senders=[Module.JETSON], receivers=[Module.SENSOR], signals=[
		Bool('servos', 7),
		Bool('magnet', 6),
		Bool('fan',	5),
		Bool('horn', 4),
		Bool('light4', 3),
		Bool('light3', 2),
		Bool('light2', 1),
		Bool('light1', 0)
	]),

	Message(0x0C3, 'actuators_reset', senders=[Module.JETSON], receivers=[Module.SENSOR], signals=[
		Bool('servos', 7),
		Bool('magnet', 6),
		Bool('fan',	5),
		Bool('horn', 4),
		Bool('light4', 3),
		Bool('light3', 2),
		Bool('light2', 1),
		Bool('light1', 0)
	])

]
