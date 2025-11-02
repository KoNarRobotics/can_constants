from abstract.signals import Bool, Enum, Float, Unsigned
from abstract.modules import Module
from abstract.message import Message
from abstract.generic_msg import STATUS_SIGNAL_LIST


db = [
  Message(0x1311, 'suspension_status', senders=[Module.SUSPENSION], receivers=[Module.JETSON], signals=[
    Enum('status', 0, 8,  list=STATUS_SIGNAL_LIST)  
  ]),

  # wheel are indexed in clockwise order from front right to to frot left
  # so if a  car has 4 wheels:
  # wheel_index: 0 -> front right
  # wheel_index: 1 -> rear right
  # wheel_index: 2 -> rear left
  # wheel_index: 3 -> front left

	Message(0x1312, 'suspension_read_forces', senders=[Module.JETSON], receivers=[Module.SUSPENSION], signals=[
		Float('wheel_force', 0, scale=1, unit='N'),
    Unsigned('wheel_index', 32,16, unit=''),
	]),

  Message(0x1313, 'suspension_read_positions', senders=[Module.JETSON], receivers=[Module.SUSPENSION], signals=[
    Float('suspension_angle', 0, scale=1, unit='rad'),
    Unsigned('wheel_index', 32,16, unit=''),
  ]),
]