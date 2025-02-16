from abstract.signals import Enum, Unsigned,Float
from abstract.modules import Module
from abstract.message import Message

## VESC6 CAN messages
# These command numbers are
# put in the second byte of the 29
# bit ID for the extended CAN
# frame. You need an extended
# frame (29 bits) vs. standard
# frame (11 bits) since bits 0-7 are
# reserved for numbering the
# individual speed controllers (0-
# 255). With only 3 bits left, only 8
# commands would be available if
# you used a standard frame.

CAN_PACKET_SET_DUTY = 0
CAN_PACKET_SET_CURRENT = 1
CAN_PACKET_SET_CURRENT_BRAKE = 2
CAN_PACKET_SET_RPM = 3
CAN_PACKET_SET_POS = 4

# CAN_PACKET_FILL_RX_BUFFER = 5
# CAN_PACKET_FILL_RX_BUFFER_LONG = 6
# CAN_PACKET_PROCESS_RX_BUFFER = 7
# CAN_PACKET_PROCESS_SHORT_BUFFER = 8

CAN_PACKET_STATUS = 9

CAN_PACKET_SET_CURRENT_REL = 10
CAN_PACKET_SET_CURRENT_BRAKE_REL = 11
CAN_PACKET_SET_CURRENT_HANDBRAKE = 12
CAN_PACKET_SET_CURRENT_HANDBRAKE_REL = 13

# CAN_PACKET_STATUS_2 = 14
# CAN_PACKET_STATUS_3 = 15
# CAN_PACKET_STATUS_4 = 16
CAN_PACKET_PING = 17
CAN_PACKET_PONG = 18
# CAN_PACKET_DETECT_APPLY_ALL_FOC = 19
# CAN_PACKET_DETECT_APPLY_ALL_FOC_RES = 20
# CAN_PACKET_CONF_CURRENT_LIMITS = 21
# CAN_PACKET_CONF_STORE_CURRENT_LIMITS = 22
# CAN_PACKET_CONF_CURRENT_LIMITS_IN = 23
# CAN_PACKET_CONF_STORE_CURRENT_LIMITS_IN = 24
# CAN_PACKET_CONF_FOC_ERPMS = 25
# CAN_PACKET_CONF_STORE_FOC_ERPMS = 26
# CAN_PACKET_STATUS_5 = 27

## FRAME FORMAT
# | B28 - B16 |  B15 - B8  | B7 - B0 |
# |-----------|------------|---------|
# |   Unused  | Command ID | VESC ID |


## BASE VESC IDS
VESC_FRONT_LEFT = 10
VESC_FRONT_RIGHT = 11
VESC_REAR_LEFT = 12
VESC_REAR_RIGHT = 13

def vc(command_id:int, vesc_id:int):
    return (command_id << 8) | vesc_id

def make_database_from_vesc(vesc_id,name_str):
  base_db = [
    Message(vc(CAN_PACKET_SET_DUTY,vesc_id), name_str+'_set_duty', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Float('duty_cycle', 0,scale=100000)],extended_frame=True),

    Message(vc(CAN_PACKET_SET_CURRENT,vesc_id), name_str+'_set_current', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Float('current', 0,scale=1000)],extended_frame=True),

    Message(vc(CAN_PACKET_SET_CURRENT_BRAKE,vesc_id), name_str+'_set_current_brake', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Float('current', 0,scale=1000)],extended_frame=True),

    Message(vc(CAN_PACKET_SET_RPM,vesc_id), name_str+'_set_rpm', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Float('rpm', 0,scale=1)],extended_frame=True),

    Message(vc(CAN_PACKET_SET_POS,vesc_id), name_str+'_set_pos', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Float('position', 0,scale=1)],extended_frame=True),
        
    Message(vc(CAN_PACKET_STATUS,vesc_id), name_str+'_status', senders=[Module.VESC], receivers=[Module.JETSON], signals=[
      Unsigned('erpm',0,24,'rpm',scale=1),
      Unsigned('current',24,16,'A',scale=10),
      Unsigned('duty',40,16,'%',scale=1000)]
      ,extended_frame=True),

    Message(vc(CAN_PACKET_SET_CURRENT_REL,vesc_id), name_str+'_set_current_rel', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Float('current', 0,scale=100000)],extended_frame=True),
    
    Message(vc(CAN_PACKET_SET_CURRENT_BRAKE_REL,vesc_id), name_str+'_set_current_brake_rel', senders=[Module.JETSON], receivers=[Module.VESC], signals=[  
      Float('current', 0,scale=100000)],extended_frame=True),

    Message(vc(CAN_PACKET_SET_CURRENT_HANDBRAKE,vesc_id), name_str+'_set_current_handbrake', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Float('current', 0,scale=1000)],extended_frame=True),
    
    Message(vc(CAN_PACKET_SET_CURRENT_HANDBRAKE_REL,vesc_id), name_str+'_set_current_handbrake_rel', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Float('current', 0,scale=100000)],extended_frame=True),

  ]
  return base_db


def make_databses(nodes:dict):
  db = []
  for names in nodes.keys():
    db.extend(make_database_from_vesc(nodes[names],names))
  return db

vesc = {
  'vesc_fleft': VESC_FRONT_LEFT,
  'vesc_fright': VESC_FRONT_RIGHT,
  'vesc_rleft': VESC_REAR_LEFT,
  'vesc_rright': VESC_REAR_RIGHT
}

db = make_databses(vesc)