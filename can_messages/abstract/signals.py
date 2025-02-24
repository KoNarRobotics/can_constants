#!/usr/bin/python3

import cantools
import collections

from cantools.database.conversion import BaseConversion
from enum import Enum


#: Signal byte order as ``'little_endian'`` LSB->MSB or ``'big_endian'``. MSB->LSB
LITTLE_ENDIAN = str('little_endian')
BIG_ENDIAN = str('big_endian')

class Unsigned(cantools.database.can.Signal):
	def __init__(self, name, start, length, unit='', scale=1, range=[0, 0],byte_order=LITTLE_ENDIAN):
		super().__init__(name, start, length,byte_order=byte_order, unit=unit, conversion=BaseConversion.factory(scale=scale), minimum=range[0], maximum=range[1])

class Signed(cantools.database.can.Signal):
	def __init__(self, name, start, length, unit='', scale=1, range=[0, 0],byte_order=LITTLE_ENDIAN):
		super().__init__(name, start, length,byte_order=byte_order, unit=unit, conversion=BaseConversion.factory(scale=scale), minimum=range[0], maximum=range[1], is_signed=True)

class Bool(cantools.database.can.Signal):
	def __init__(self, name, start):
		super().__init__(name, start, 1, minimum=0, maximum=1)
		
class Float(cantools.database.can.Signal):
	def __init__(self, name, start, unit='', scale=1, is_double=False,byte_order=LITTLE_ENDIAN):
		super().__init__(name, start, 32,byte_order=byte_order, unit=unit, conversion=BaseConversion.factory(scale=scale,is_float=True) )

		# if is_double:
		# 	self.length = 64
		# else:
		# 	self.length = 32

class Enum(cantools.database.can.Signal):
	def __init__(self, name, start, length, list,byte_order=LITTLE_ENDIAN):

		minimum = min(list, key=lambda tup: tup[0])[0]
		maximum = max(list, key=lambda tup: tup[0])[0]

		super().__init__(
			name, 
			start, 
			length,
			byte_order=byte_order, 
			conversion=BaseConversion.factory(choices=collections.OrderedDict(list), is_float=False), 
			minimum=minimum,
			maximum=maximum
		)

		if self.minimum<0:
			self.is_signed = True
		else:
			self.is_signed = False
