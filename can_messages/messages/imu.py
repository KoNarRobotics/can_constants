#!/usr/bin/python3

from abstract.signals import Enum, Signed
from abstract.modules import Module
from abstract.message import Message

db = [

	Message(0x401, 'imu_status', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Enum('status', 0, 8, list=[
			(1, 'ok'), 
			(2, 'disconnected'), 
			(3, 'error')
		])
	]),

	Message(0x402, 'imu_orientation', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Signed('w', 0, 16, scale=1/(1<<14)),
		Signed('x', 16, 16, scale=1/(1<<14)),
		Signed('y', 32, 16, scale=1/(1<<14)),
		Signed('z', 48, 16, scale=1/(1<<14))
	]),

	Message(0x403, 'imu_linear_acceleration', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Signed('x', 0, 16, scale=0.01, unit='m/s^2'),
		Signed('y', 16, 16, scale=0.01, unit='m/s^2'),
		Signed('z', 32, 16, scale=0.01, unit='m/s^2')
	]),

	Message(0x404, 'imu_magnetic_field', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Signed('x', 0, 16, scale=1/16, unit='uT'),
		Signed('y', 16, 16, scale=1/16, unit='uT'),
		Signed('z', 32, 16, scale=1/16, unit='uT')
	]),

	Message(0x405, 'imu_gyration', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Signed('x', 0, 16, scale=1/900, unit='rad/s'),
		Signed('y', 16, 16, scale=1/900, unit='rad/s'),
		Signed('z', 32, 16, scale=1/900, unit='rad/s')
	])

]
