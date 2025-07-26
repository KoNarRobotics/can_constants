#
# This file is part of the CAN messages database.
# Created by Patryk Dudziński.
# Date May 1, 2025
#

#!/usr/bin/python3

from abstract.signals import Enum, Float
from abstract.modules import Module
from abstract.message import Message


db = [
  Message(0x431,'barometer_status', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
    Enum('status', 0, 8, list=[
      (1, 'ok'), 
      (2, 'error')
    ])]
  ),
	Message(0x432, 'barometer_data', senders=[Module.SENSOR], receivers=[Module.JETSON], signals=[
		Float('temperature', 0, 'C'),
    Float('pressure', 32, 'hPa')
	])
]


