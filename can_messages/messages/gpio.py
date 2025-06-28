from abstract.signals import Bool, Enum
from abstract.modules import Module
from abstract.message import Message

gpio_board_status = [
	(0, 'ok'), 
	(1, 'fault')
]

db = [

  Message(0x1111, 'gpio_status', senders=[Module.GPIO], receivers=[Module.JETSON], signals=[
    Enum('status', 0, 8, list=gpio_board_status)  
  ]),

	Message(0x1112, 'gpio_set', senders=[Module.JETSON], receivers=[Module.GPIO], signals=[
		Bool('ch1', 0),
		Bool('ch2', 1),
		Bool('ch3',	2),
		Bool('ch4', 3),
	]),

  Message(0x1113, 'gpio_read', senders=[Module.GPIO], receivers=[Module.JETSON], signals=[
    Bool('ch1', 0),
    Bool('ch2', 1),
    Bool('ch3',	2),
    Bool('ch4', 3)
  ]),
]