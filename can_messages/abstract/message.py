#!/usr/bin/python3

import cantools
import math
from cantools.database.can import Signal
from abstract.signals import BIG_ENDIAN, LITTLE_ENDIAN

class Message(cantools.database.can.Message):
  def __init__(self, id, name, senders, receivers, signals, extended_frame=True):
    # signals_with_receivers = [
    #   Signal(
    #     name=signal.name, 
    #     start=signal.start, 
    #     length=signal.length,
    #     byte_order=signal.byte_order,
    #     is_signed=signal.is_signed,
    #     minimum=signal.minimum,
    #     maximum=signal.maximum,
    #     conversion=signal.conversion,
    #     unit=signal.unit,
    #     receivers=receivers
    #   ) for signal in signals
    # ]
    
    signals_with_receivers = []
    bytes = 0
    for signal in signals:
      bytes = max(bytes, int(math.ceil((signal.start + signal.length) / 8)))
      if signal.byte_order == BIG_ENDIAN:
        beg = (signal.start//8)*8 + 7 - (signal.start%8)
      else:
        beg = signal.start
      
      s = Signal(
          name=signal.name, 
          start=beg, 
          length=signal.length,
          byte_order=signal.byte_order,
          is_signed=signal.is_signed,
          minimum=signal.minimum,
          maximum=signal.maximum,
          conversion=signal.conversion,
          unit=signal.unit,
          receivers=receivers
        )

      signals_with_receivers.append(s)

  
    # bytes = 0
    # try:
    #   bits = max(s.start + s.length for s in signals_with_receivers)
    #   bytes = int(math.ceil(bits / 8))
    # except:
    #   pass

    if bytes > 8:
      raise ValueError('Message payload must be in range [0; 8] bytes')
    
    super().__init__(
      frame_id=id,
      is_extended_frame=extended_frame, 
      name=name, 
      length=bytes,
      signals=signals_with_receivers,
      senders=senders
    )
