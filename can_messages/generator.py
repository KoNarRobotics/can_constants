#!/usr/bin/python3

import cantools
import os

from abstract.helper import can_db_builder
from messages import actuators
from messages import battery
from messages import buzzer
from messages import control_mode
from messages import gps
from messages import imu
from messages import metal_detector
from messages import odrive
from messages import temperature
from messages import konarm
from messages import vesc6

if __name__ == '__main__':
  cdb = can_db_builder()
  cdb.add_module(actuators)
  cdb.add_module(battery)
  cdb.add_module(buzzer)
  cdb.add_module(control_mode)
  cdb.add_module(gps)
  cdb.add_module(imu)
  cdb.add_module(metal_detector)
  cdb.add_module(odrive)
  cdb.add_module(temperature)
  cdb.add_module(konarm)
  cdb.add_module(vesc6)
  cdb.db_build()
  cdb.dump_file('can.dbc')
  cdb.generate_C_code('can.dbc', 'output')
  cdb.generate_docs('output/docs.md')
