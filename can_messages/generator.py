#!/usr/bin/python3

import cantools
import os

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

db = cantools.database.can.Database(
	battery.db 
	+ actuators.db
	+ buzzer.db
	+ control_mode.db
	+ gps.db
	+ imu.db
	+ metal_detector.db
	+ odrive.db
	+ temperature.db
  + konarm.db
)

cantools.database.dump_file(db, 'can.dbc')

os.system('python3 -m cantools generate_c_source --use-float --database-name can can.dbc')

os.system('mkdir -p output')
os.system('mv can.dbc output')
os.system('mv can.h output')
os.system('mv can.c output')
