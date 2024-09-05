#!/usr/bin/python3

import cantools
import math
from cantools.database.can import Signal

class Message(cantools.database.can.Message):
	def __init__(self, id, name, senders, receivers, signals):

		signals_with_receivers = [ Signal(
					name=signal.name, 
					start=signal.start, 
					length=signal.length,
					is_signed=signal.is_signed,
					minimum=signal.minimum,
					maximum=signal.maximum,
					conversion=signal.conversion,
					unit=signal.unit,
					receivers=receivers
				) for signal in signals]
	
		bytes = 0
		try:
			bits = max(s.start + s.length for s in signals_with_receivers)
			bytes = int(math.ceil(bits/8))
		except:
			pass

		if bytes>8:
			raise ValueError('Message payload must be in range [0; 8] bytes')
		
		super().__init__(
			frame_id=id, 
			name=name, 
			length=bytes,
			signals=signals_with_receivers,
			senders=senders
		)

		
