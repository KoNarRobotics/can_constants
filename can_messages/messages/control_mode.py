#!/usr/bin/python3

from abstract.signals import Enum
from abstract.modules import Module
from abstract.message import Message

db = [

	Message(0x201, 'control_mode', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Enum('mode', 0, 8, list=[
			(0, 'unknown'),
			(1, 'manual'), 
			(2, 'auto')
		])
	])

]
