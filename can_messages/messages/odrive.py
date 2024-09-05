#!/usr/bin/python3

from numpy import pi
from copy import copy

from abstract.signals import Float, Unsigned, Signed
from abstract.modules import Module
from abstract.message import Message

base_db = [

	Message(0x001, 'heartbeat', senders=[Module.ODRIVE], receivers=[Module.JETSON, Module.SENSOR], signals=[
		Unsigned('axis_error', 0, 32),
		Unsigned('axis_state', 32, 8),
		Unsigned('controller_status', 40, 8)
	]),

	Message(0x002, 'estop', senders=[Module.JETSON, Module.SENSOR], receivers=[Module.ODRIVE], signals=[]),

	Message(0x003, 'get_motor_error', senders=[Module.ODRIVE], receivers=[Module.JETSON, Module.SENSOR], signals=[
		Unsigned('motor_error', 0, 32)
	]),

	Message(0x004, 'get_encoder_error', senders=[Module.ODRIVE], receivers=[Module.JETSON, Module.SENSOR], signals=[
		Unsigned('encoder_error', 0, 32)
	]),

	Message(0x007, 'set_axis_state', senders=[Module.JETSON, Module.SENSOR], receivers=[Module.ODRIVE], signals=[
		Unsigned('axis_requested_state', 0, 32)
	]),

	Message(0x009, 'get_encoder_estimates', senders=[Module.ODRIVE], receivers=[Module.JETSON, Module.SENSOR], signals=[
		Float('pos_estimate', 0, unit='r', scale=2*pi),
		Float('vel_estimate', 32, unit='rps', scale=2*pi)
	]),

	Message(0x00A, 'get_encoder_count', senders=[Module.ODRIVE], receivers=[Module.JETSON, Module.SENSOR], signals=[
		Unsigned('shadow_count', 0, 32),
		Unsigned('count_in_CPR', 32, 32)
	]),

	Message(0x00B, 'set_controller_mode', senders=[Module.JETSON, Module.SENSOR], receivers=[Module.ODRIVE], signals=[
		Unsigned('control_mode', 0, 32),
		Unsigned('input_mode', 32, 32)
	]),

	Message(0x00C, 'set_input_pos', senders=[Module.JETSON, Module.SENSOR], receivers=[Module.ODRIVE], signals=[
		Float('input_pos', 0),
		Signed('vel_FF', 32, 16, scale=0.001),
		Signed('torque_FF', 48, 16, scale=0.001)
	]),

	Message(0x00D, 'set_input_vel', senders=[Module.JETSON, Module.SENSOR], receivers=[Module.ODRIVE], signals=[
		Float('input_vel', 0, scale=2*pi),
		Unsigned('input_torque_FF', 32, 32)
	]),

	Message(0x00E, 'set_input_torque', senders=[Module.JETSON, Module.SENSOR], receivers=[Module.ODRIVE], signals=[
		Float('imput_torque', 0)
	]),

	Message(0x00F, 'set_limits', senders=[Module.JETSON, Module.SENSOR], receivers=[Module.ODRIVE], signals=[
		Float('velocity_limit', 0),
		Float('current_limit', 32)
	]),

	Message(0x017, 'get_vbus_voltage', senders=[Module.ODRIVE], receivers=[Module.JETSON, Module.SENSOR], signals=[
		Float('vbus_voltage', 0)
	]),

	Message(0x018, 'clear_errors', senders=[Module.JETSON, Module.SENSOR], receivers=[Module.ODRIVE], signals=[])

]

def make_database(base, nodes):
	db = []

	for node in nodes:
		for message in base:
			msg = copy(message)
			msg.frame_id = node[0] | message.frame_id
			msg.name = 'odrive_' + node[1] + '_' + message.name

			db.append(msg)

	return db

db = make_database(base_db, [
	(0x020, 'left'),
	(0x060, 'right')
])
