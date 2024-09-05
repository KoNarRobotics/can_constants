#!/usr/bin/python3

from abstract.signals import Enum, Float, Unsigned
from abstract.modules import Module
from abstract.message import Message

db = [

	Message(0x421, 'gps_status', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Enum('status', 0, 8, list=[
			(1, 'ok'), 
			(2, 'disconnected'), 
			(3, 'error')
		]),
		Enum('signal', 8, 8, list=[
			(-1, 'unable_to_fix_position'), 
			(0, 'unaugmented_fix'), 
			(1, 'satellite_based_augmentation'),
			(2, 'ground_based_augmentation')
		])
	]),

	Message(0x422, 'gps_latitude', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Float('latitude', 0, unit='deg', is_double=True)
	]),

	Message(0x423, 'gps_longitude', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Float('longitude', 0, unit='deg', is_double=True),
	]),

    Message(0x424, 'gps_altitude', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
        Float('altitude', 0, unit='m', is_double=False),
    ]),

	Message(0x425, 'gps_date', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Unsigned('year', 0, 16, range=[0, 65535]),
		Unsigned('month', 16, 8, range=[1, 12]),
		Unsigned('day', 24, 8, range=[1, 31]),
		Unsigned('hour', 32, 8, range=[0, 23]),
		Unsigned('minute', 40, 8, range=[0, 59]),
		Unsigned('second', 48, 8, range=[0, 59])
	]),
    Message(0x426, 'gps_covariance', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
        Unsigned('lat', 0, 16, scale=0.01),
        Unsigned('lon', 16, 16, scale=0.01),
        Unsigned('alt', 32, 16, scale=0.01)
    ])
]
