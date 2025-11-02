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
from messages import barometer
from messages import gpio
from messages import geiger
from messages import modu_card
from messages import suspension

if __name__ == '__main__':
  # Init CAN database builder
  cdb = can_db_builder()

  # add CAN messages to the database
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
  cdb.add_module(barometer)
  cdb.add_module(gpio)
  cdb.add_module(geiger)
  cdb.add_module(suspension)
  cdb.add_module(modu_card)

  # Build the database and generate the files
  cdb.db_build()
  cdb.dump_file('can.dbc')
  cdb.generate_C_code('can.dbc', 'output')
  cdb.generate_docs('output/docs.md')
