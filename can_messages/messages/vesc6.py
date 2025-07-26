#
# This file is part of the CAN messages database.
# Created by Patryk Dudziński.
# Date February 18, 2025
#

from abstract.signals import Enum, Unsigned,Float, Signed, BIG_ENDIAN, LITTLE_ENDIAN
from abstract.modules import Module
from abstract.message import Message

################################################
# VESC6 CAN messages
#
# https://github.com/vedderb/bldc/blob/master/documentation/comm_can.md
#
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
#################################################
#      FRAME FORMAT
#
#      | B28 - B16 |  B15 - B8  | B7 - B0 |
#      |-----------|------------|---------|
#      |   Unused  | Command ID | VESC ID |
#
################################################
# 
# ATTENTION:  all values are integers and are scaled by 1000, most of them are signed, so the Units are in  mili[UNIT] 
# EXCEPTIONS: 
#     - the RPM value is scaled by 1
#     - the Position value is from 0 to 360 degrees  (0 to 360 000 after scaling)
#     - the Status message values are not scaled refere to the 
#
#  So if you want to set a duty cycle to 50% you should set the value to 50 000 
#  or amperage to 1.5A you should set the value to 1500
#  or when you read the value of curent: 15300 then it means 15.3A
#
################################################


CAN_PACKET_SET_DUTY = 0
CAN_PACKET_SET_CURRENT = 1
CAN_PACKET_SET_CURRENT_BRAKE = 2
CAN_PACKET_SET_RPM = 3
CAN_PACKET_SET_POS = 4



CAN_PACKET_STATUS_1 = 9
CAN_PACKET_STATUS_2 = 14
CAN_PACKET_STATUS_3 = 15
CAN_PACKET_STATUS_4 = 16
CAN_PACKET_STATUS_5 = 27
CAN_PACKET_STATUS_6 = 28

CAN_PACKET_SET_CURRENT_REL = 10
CAN_PACKET_SET_CURRENT_BRAKE_REL = 11
CAN_PACKET_SET_CURRENT_HANDBRAKE = 12
CAN_PACKET_SET_CURRENT_HANDBRAKE_REL = 13

# CAN_PACKET_FILL_RX_BUFFER = 5
# CAN_PACKET_FILL_RX_BUFFER_LONG = 6
# CAN_PACKET_PROCESS_RX_BUFFER = 7
# CAN_PACKET_PROCESS_SHORT_BUFFER = 8
# CAN_PACKET_PING = 17
# CAN_PACKET_PONG = 18
# CAN_PACKET_DETECT_APPLY_ALL_FOC = 19
# CAN_PACKET_DETECT_APPLY_ALL_FOC_RES = 20
# CAN_PACKET_CONF_CURRENT_LIMITS = 21
# CAN_PACKET_CONF_STORE_CURRENT_LIMITS = 22
# CAN_PACKET_CONF_CURRENT_LIMITS_IN = 23
# CAN_PACKET_CONF_STORE_CURRENT_LIMITS_IN = 24
# CAN_PACKET_CONF_FOC_ERPMS = 25
# CAN_PACKET_CONF_STORE_FOC_ERPMS = 26
# CAN_PACKET_STATUS_5 = 27

################################################
## BASE VESC IDS
VESC_FRONT_LEFT = 20
VESC_FRONT_RIGHT = 21
VESC_REAR_LEFT = 22
VESC_REAR_RIGHT = 23

def vc(command_id:int, vesc_id:int):
    return (command_id << 8) | vesc_id

def make_database_from_vesc(vesc_id,name_str):
  base_db = [
    Message(vc(CAN_PACKET_SET_DUTY,vesc_id), name_str+'_set_duty', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Signed('duty_cycle',0 ,32,unit='m%', scale=1,byte_order=BIG_ENDIAN)],extended_frame=True),

    Message(vc(CAN_PACKET_SET_CURRENT,vesc_id), name_str+'_set_current', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Signed('current', 0,32,unit='mA',scale=1,byte_order=BIG_ENDIAN)],extended_frame=True),

    Message(vc(CAN_PACKET_SET_CURRENT_BRAKE,vesc_id), name_str+'_set_current_brake', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Signed('current', 0,32,unit='mA',scale=1,byte_order=BIG_ENDIAN)],extended_frame=True),

    Message(vc(CAN_PACKET_SET_RPM,vesc_id), name_str+'_set_rpm', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Signed('rpm', 0,32,unit='mRPM',scale=1,byte_order=BIG_ENDIAN)],extended_frame=True),

    Message(vc(CAN_PACKET_SET_POS,vesc_id), name_str+'_set_pos', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Signed('position', 0,32,unit='mDeg',scale=1/10,byte_order=BIG_ENDIAN)],extended_frame=True),
        
    Message(vc(CAN_PACKET_SET_CURRENT_REL,vesc_id), name_str+'_set_current_rel', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Signed('current', 0,32,unit='m%',scale=1,byte_order=BIG_ENDIAN)],extended_frame=True),
    
    Message(vc(CAN_PACKET_SET_CURRENT_BRAKE_REL,vesc_id), name_str+'_set_current_brake_rel', senders=[Module.JETSON], receivers=[Module.VESC], signals=[  
      Signed('current', 0,32,unit='m%',scale=1,byte_order=BIG_ENDIAN)],extended_frame=True),

    Message(vc(CAN_PACKET_SET_CURRENT_HANDBRAKE,vesc_id), name_str+'_set_current_handbrake', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Signed('current', 0,32,unit='mA',scale=1,byte_order=BIG_ENDIAN)],extended_frame=True),
    
    Message(vc(CAN_PACKET_SET_CURRENT_HANDBRAKE_REL,vesc_id), name_str+'_set_current_handbrake_rel', senders=[Module.JETSON], receivers=[Module.VESC], signals=[
      Signed('current', 0,32,unit='m%',scale=1,byte_order=BIG_ENDIAN)],extended_frame=True),
    
    Message(vc(CAN_PACKET_STATUS_1,vesc_id), name_str+'_status_1', senders=[Module.VESC], receivers=[Module.JETSON], signals=[
      Signed('erpm',0,32,'RPM',scale=1,byte_order=BIG_ENDIAN),
      Signed('current',32,16,'A',scale=1/10,byte_order=BIG_ENDIAN),
      Signed('duty',48,16,'%',scale=1/10,byte_order=BIG_ENDIAN)]
      ,extended_frame=True),

    Message(vc(CAN_PACKET_STATUS_2,vesc_id), name_str+'_status_2', senders=[Module.VESC], receivers=[Module.JETSON], signals=[
      Signed('amp_hours',0,32,'mAh',scale=1/100,byte_order=BIG_ENDIAN),
      Signed('amp_hours_chg',32,32,'mAh',scale=1/100,byte_order=BIG_ENDIAN)]
      ,extended_frame=True),
    
    Message(vc(CAN_PACKET_STATUS_3,vesc_id), name_str+'_status_3', senders=[Module.VESC], receivers=[Module.JETSON], signals=[
      Signed('wat_hours',0,32,'mWh',scale=1/100,byte_order=BIG_ENDIAN),
      Signed('wat_hours_chg',32,32,'mWh',scale=1/100,byte_order=BIG_ENDIAN)]
      ,extended_frame=True),

    Message(vc(CAN_PACKET_STATUS_4,vesc_id), name_str+'_status_4', senders=[Module.VESC], receivers=[Module.JETSON], signals=[
      Signed('temp_mosfet',0,16,'C',scale=1/10,byte_order=BIG_ENDIAN),
      Signed('temp_motor',16,16,'C',scale=1/10,byte_order=BIG_ENDIAN),
      Signed('current_in',32,16,'A',scale=1/10,byte_order=BIG_ENDIAN),
      Signed('pid_pos',48,16,'Deg',scale=1/50,byte_order=BIG_ENDIAN)]
      ,extended_frame=True),
  
    Message(vc(CAN_PACKET_STATUS_5,vesc_id), name_str+'_status_5', senders=[Module.VESC], receivers=[Module.JETSON], signals=[
      Signed('tachometer',0,32,'EREV',scale=1/6,byte_order=BIG_ENDIAN),
      Signed('volts_in',32,16,'V',scale=1/10,byte_order=BIG_ENDIAN)]
      ,extended_frame=True),
    
    Message(vc(CAN_PACKET_STATUS_6,vesc_id), name_str+'_status_6', senders=[Module.VESC], receivers=[Module.JETSON], signals=[
      Signed('adc1',0,16,'mV',scale=1,byte_order=BIG_ENDIAN),
      Signed('adc2',16,16,'mV',scale=1,byte_order=BIG_ENDIAN),
      Signed('adc3',32,16,'mV',scale=1,byte_order=BIG_ENDIAN),
      Signed('ppm',48,16,'m%',scale=1,byte_order=BIG_ENDIAN),]
      ,extended_frame=True),
  ]
  return base_db


def make_databses(nodes:dict):
  try:
    db = []
    for names in nodes.keys():
      db.extend(make_database_from_vesc(nodes[names],names))
    return db
  except Exception as e:
    print(e)
    raise e

vesc = {
  'vesc_fleft': VESC_FRONT_LEFT,
  'vesc_fright': VESC_FRONT_RIGHT,
  'vesc_rleft': VESC_REAR_LEFT,
  'vesc_rright': VESC_REAR_RIGHT
}

db = make_databses(vesc)