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

konarm_error_status = [
	(0, 'ok'), 
	(1, 'fault') 
]


konarm_control_mode = [
	(1, 'velocity_control'), 
	(2, 'position_control'),
	(3, 'torque_control') 
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

  Message(0x004, 'clear_errors', senders=[Module.JETSON], receivers=[Module.KONARM], signals=[]),
	
  Message(0x005, 'get_errors', senders=[Module.JETSON], receivers=[Module.KONARM], signals=[
		Enum('temp_engine_overheating', 0, 1, list=konarm_error_status),
		Enum('temp_driver_overheating', 1, 1, list=konarm_error_status),
		Enum('temp_board_overheating', 2, 1, list=konarm_error_status),
    Enum('temp_engine_sensor_disconnect', 3, 1, list=konarm_error_status),
    Enum('temp_driver_sensor_disconnect', 4, 1, list=konarm_error_status),
    Enum('temp_board_sensor_disconnect', 5, 1, list=konarm_error_status),
    Enum('encoder_arm_disconnect', 6, 1, list=konarm_error_status),
    Enum('encoder_motor_disconnect', 7, 1, list=konarm_error_status),
    Enum('board_overvoltage', 8, 1, list=konarm_error_status),
    Enum('board_undervoltage', 9, 1, list=konarm_error_status),
    Enum('can_disconnected', 10, 1, list=konarm_error_status),
    Enum('can_error', 11, 1, list=konarm_error_status),
    Enum('controler_motor_limit_position', 12, 1, list=konarm_error_status),
  ]),
	
  Message(0x006, 'set_control_mode', senders=[Module.JETSON], receivers=[Module.KONARM], signals=[
		Enum('control_mode', 0, 8, list=konarm_control_mode)
  ])
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