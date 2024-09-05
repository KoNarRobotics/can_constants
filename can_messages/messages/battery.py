#!/usr/bin/python3

from abstract.signals import Enum, Unsigned
from abstract.modules import Module
from abstract.message import Message

db = [

	Message(0x221, 'battery_status', senders=[Module.POWER], receivers=[Module.JETSON], signals=[
		Enum('status', 0, 8, list=[
			(0, 'unknown'),
			(1, 'charging'),
			(2, 'discharging'),
			(3, 'not_charging'),
			(4, 'full')
		])
	]),

	Message(0x222, 'battery_estimates', senders=[Module.POWER], receivers=[Module.JETSON], signals=[
		Unsigned('voltage', 0, 16, unit='V', scale=0.001),
		Unsigned('fill_level', 16, 8, unit='%', range=[0, 100]),
	])

]
