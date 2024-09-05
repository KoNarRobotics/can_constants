#!/usr/bin/python3

from copy import copy

from abstract.signals import Float, Unsigned, Enum
from abstract.modules import Module
from abstract.message import Message


konarm_joint_status = [
	(1, 'ok'), 
	(2, 'fault'), 
	(3, 'overheat'),
	(4, 'emergency_stop'),
]


base_db = [
  Message(0x001, 'status', senders=[Module.KONARM], receivers=[Module.JETSON], signals=[
    Enum('status', 0, 8, list=konarm_joint_status)  
  ]),
  
  Message(0x002, 'set_pos', senders=[Module.JETSON], receivers=[Module.KONARM], signals=[
    Float('position', 0, 'rad'),
    Float('velocity', 32, 'rad/s'),
  ]),
  
  Message(0x003, 'get_pos', senders=[Module.KONARM], receivers=[Module.JETSON], signals=[
    Float('position', 0, 'rad'),
    Float('velocity', 32, 'rad/s'),
  ]),

  Message(0x004, 'clear_errors', senders=[Module.JETSON, Module.SENSOR], receivers=[Module.KONARM], signals=[])
]


def make_database(base, nodes):
	db = []

	for node in nodes:
		for message in base:
			msg = copy(message)
			msg.frame_id = node[0] | message.frame_id
			msg.name = 'konarm_' + node[1] + '_' + message.name

			db.append(msg)

	return db

db = make_database(base_db, [
	(0x610, '1'),
	(0x620, '2'),
	(0x630, '3'),
	(0x640, '4'),
	(0x650, '5'),
	(0x660, '6')
])