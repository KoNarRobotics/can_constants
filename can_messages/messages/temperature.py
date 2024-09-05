#!/usr/bin/python3

from abstract.signals import Enum, Signed, Bool
from abstract.modules import Module
from abstract.message import Message

sensor_status = [
	(1, 'ok'),
	(2, 'disconnected'),
	(3, 'error')
]

db = [

	Message(0x241, 'temperature_imu_status', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Enum('accelerometer', 0, 8, list=sensor_status)
	]),

	Message(0x242, 'temperature_imu_temperature', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Signed('accelerometer', 0, 8)
	]),

	Message(0x261, 'temperature_external_status', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Enum('external_1', 0, 2, list=sensor_status),
		Enum('external_2', 2, 2, list=sensor_status),
		Enum('external_3', 4, 2, list=sensor_status),
		Enum('external_4', 6, 2, list=sensor_status)
	]),

	Message(0x262, 'temperature_external_temperature', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Signed('external_1', 0, 8),
		Signed('external_2', 8, 8),
		Signed('external_3', 16, 8),
		Signed('external_4', 24, 8)
	]),

	Message(0x281, 'temperature_sensor_board_status', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Enum('ucontroller', 0, 2, list=sensor_status),
		Enum('ambient', 2, 2, list=sensor_status),
		Enum('ldo', 4, 2, list=sensor_status)
	]),

	Message(0x282, 'temperature_sensor_board_temperature', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Signed('ucontroller', 0, 8),
		Signed('ambient', 8, 8),
		Signed('ldo', 16, 8)
	]),

	Message(0x2A1, 'temperature_power_board_status', senders=[Module.POWER], receivers=[Module.JETSON], signals=[
		Enum('ucontroller', 0, 2, list=sensor_status),
		Enum('ambient', 2, 2, list=sensor_status),
		Enum('mosfets', 4, 2, list=sensor_status)
	]),

	Message(0x2A2, 'temperature_power_board_temperature', senders=[Module.POWER], receivers=[Module.JETSON], signals=[
		Signed('ucontroller', 0, 8),
		Signed('ambient', 8, 8),
		Signed('mosfets', 16, 8)
	]),

	Message(0x2C1, 'temperature_metal_detector_board_status', senders=[Module.METAL_DETECTOR], receivers=[Module.JETSON], signals=[
		Enum('ucontroller', 0, 2, list=sensor_status)
	]),

	Message(0x2C2, 'temperature_metal_detector_board_temperature', senders=[Module.METAL_DETECTOR], receivers=[Module.JETSON], signals=[
		Signed('ucontroller', 0, 8)
	])

]
