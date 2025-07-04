from abstract.signals import Bool, Enum, Float, Unsigned
from abstract.modules import Module
from abstract.message import Message

geiger_status = [
	(0, 'ok'), 
	(1, 'fault'),
  (2, 'disconnected'),
]

db = [
  Message(0x1211, 'geiger_status', senders=[Module.GPIO], receivers=[Module.JETSON], signals=[
    Enum('geiger_status', 0, 8, list=geiger_status)  
  ]),

	Message(0x1212, 'geiger_read', senders=[Module.JETSON], receivers=[Module.GPIO], signals=[
		Float('micro_siwert', 0, scale=1, unit='uSv'),
    Unsigned('cpm', 32,16, unit='cpm'),
	]),
]