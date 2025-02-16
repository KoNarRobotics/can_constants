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
from messages import vesc6


def add_to_db(db, module):
  ids = {}
  for a in db:
    ids[a.frame_id] = a
  messages_to_check = module.db
  for message in messages_to_check:
    if message.frame_id in ids:
      print(f"""\033[91m 
                Collision detected in message: NAME={message.name} in file: {module.__file__}.py
                Existing message ID={message.frame_id} NAME={ids[message.frame_id].name} \033[0m
            """)
      raise ValueError('Collision detected')
  return  db + messages_to_check
  

if __name__ == '__main__':
  messages = actuators.db
  messages = add_to_db(messages,battery)
  messages = add_to_db(messages, buzzer)
  messages = add_to_db(messages, control_mode)
  messages = add_to_db(messages, gps)
  messages = add_to_db(messages, imu)
  messages = add_to_db(messages, metal_detector)
  messages = add_to_db(messages, odrive)
  messages = add_to_db(messages, temperature)
  messages = add_to_db(messages, konarm)
  messages = add_to_db(messages, vesc6)


  db = cantools.database.can.Database(
    messages
  )

  cantools.database.dump_file(db, 'can.dbc')

  os.system('python3 -m cantools generate_c_source --use-float --database-name can can.dbc')

  os.system('mkdir -p output')
  os.system('mv can.dbc output')
  os.system('mv can.h output')
  os.system('mv can.c output')
