#!/usr/bin/python3

from abstract.signals import Enum, Signed, Unsigned
from abstract.modules import Module
from abstract.message import Message

channel_status = [
	(1, 'ok'), 
	(2, 'disconnected'), 
	(3, 'error')
]

db = [

	Message(0x441, 'metal_detector_status', senders=[Module.METAL_DETECTOR], receivers=[Module.JETSON], signals=[
		Enum('channel_1', 0, 2, list=channel_status),
		Enum('channel_2', 2, 2, list=channel_status),
		Enum('channel_3', 4, 2, list=channel_status),
		Enum('channel_4', 6, 2, list=channel_status),
		Enum('channel_5', 8, 2, list=channel_status),
		Enum('channel_6', 10, 2, list=channel_status),
		Enum('channel_7', 12, 2, list=channel_status),
		Enum('channel_8', 14, 2, list=channel_status)
	]),

	Message(0x442, 'metal_detector_value_1234', senders=[Module.METAL_DETECTOR], receivers=[Module.JETSON], signals=[
		Unsigned('channel_1', 0, 16, range=[0, 4095]),
		Unsigned('channel_2', 16, 16, range=[0, 4095]),
		Unsigned('channel_3', 32, 16, range=[0, 4095]),
		Unsigned('channel_4', 48, 16, range=[0, 4095])
	]),

	Message(0x443, 'metal_detector_value_5678', senders=[Module.METAL_DETECTOR], receivers=[Module.JETSON], signals=[
		Unsigned('channel_5', 0, 16, range=[0, 4095]),
		Unsigned('channel_6', 16, 16, range=[0, 4095]),
		Unsigned('channel_7', 32, 16, range=[0, 4095]),
		Unsigned('channel_8', 48, 16, range=[0, 4095])
	]),

	Message(0x444, 'metal_detector_estimated_position', senders=[Module.METAL_DETECTOR], receivers=[Module.JETSON], signals=[
		Signed('x', 0, 16, unit='m', scale=0.001),
		Signed('y', 16, 16, unit='m', scale=0.001),
		Signed('z', 32, 16, unit='m', scale=0.001)
	])

]
