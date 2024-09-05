#!/usr/bin/python3

from abstract.signals import Unsigned
from abstract.modules import Module
from abstract.message import Message

db = [

	Message(0x701, 'buzzer_beep', senders=[Module.JETSON], receivers=[Module.POWER], signals=[]),

	Message(0x702, 'buzzer_play_note', senders=[Module.JETSON], receivers=[Module.POWER], signals=[
		Unsigned('frequency', 0, 16, unit='Hz'),
		Unsigned('duration', 16, 16, unit='ms')
	]),

	Message(0x703, 'buzzer_start', senders=[Module.JETSON], receivers=[Module.POWER], signals=[
		Unsigned('frequency', 0, 16, unit='Hz')
	]),

	Message(0x704, 'buzzer_stop', senders=[Module.JETSON], receivers=[Module.POWER], signals=[])

]
