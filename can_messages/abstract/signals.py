#!/usr/bin/python3

import cantools
import collections

from cantools.database.conversion import BaseConversion

class Unsigned(cantools.database.can.Signal):
	def __init__(self, name, start, length, unit='', scale=1, range=[0, 0]):
		super().__init__(name, start, length, unit=unit, conversion=BaseConversion.factory(scale=scale), minimum=range[0], maximum=range[1])

class Signed(cantools.database.can.Signal):
	def __init__(self, name, start, length, unit='', scale=1, range=[0, 0]):
		super().__init__(name, start, length, unit=unit, conversion=BaseConversion.factory(scale=scale), minimum=range[0], maximum=range[1], is_signed=True)

class Bool(cantools.database.can.Signal):
	def __init__(self, name, start):
		super().__init__(name, start, 1, minimum=0, maximum=1)
		
class Float(cantools.database.can.Signal):
	def __init__(self, name, start, unit='', scale=1, is_double=False):
		super().__init__(name, start, 32, unit=unit, conversion=BaseConversion.factory(scale=scale,is_float=True) )

		# if is_double:
		# 	self.length = 64
		# else:
		# 	self.length = 32

class Enum(cantools.database.can.Signal):
	def __init__(self, name, start, length, list):

		minimum = min(list, key=lambda tup: tup[0])[0]
		maximum = max(list, key=lambda tup: tup[0])[0]

		super().__init__(
			name, 
			start, 
			length, 
			conversion=BaseConversion.factory(choices=collections.OrderedDict(list), is_float=False), 
			minimum=minimum,
			maximum=maximum
		)

		if self.minimum<0:
			self.is_signed = True
		else:
			self.is_signed = False
