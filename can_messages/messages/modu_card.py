#
# This file is part of the CAN messages database.
# Created by Patryk Dudziński.
# Date February 18, 2025
#

from abstract.signals import Enum, Unsigned,Float, Signed, BIG_ENDIAN, LITTLE_ENDIAN
from abstract.modules import Module
from abstract.message import Message
from abstract.generic_msg import STATUS_SIGNAL_LIST








################################################
# MODU CARD CAN FRAME ID FORMAT
# FD can frames with 29 bit identifiers are used
# 
#  Identifier format:
#  | 4 bits |      10 bits      |        15 bits        |
#  | Command |    Base ID       |      Command ID       |
#
#
#  Command - base commands for modu card messages system
#  Base ID - base identifier for each modu card module
#  Command ID - command id for each individual message on a module.
#
#
# the CONSTANT VALUE
#
# CAN_MODU_CARD_<your name>_HEARTBEAT_1_FRAME_ID is also equal to Base ID
# used to identify the module in the system
#
#
#
################################################
# MODU CARD CAN messages

CAN_PACKET_HEARTBEAT_1 = 0
CAN_PACKET_HEARTBEAT_2 = 1
CAN_PACKET_RESET = 2
CAN_PACKET_ENABLE = 3
CAN_PACKET_DISABLE = 4
CAN_PACKET_SOFTWARE_VERSION = 5




def vc(command_id:int, base_id:int):
  return (command_id << 25) | base_id

def make_database_from_template(base_id,name,base_name='modu_card_'):
  base_db = [
    Message(vc(CAN_PACKET_HEARTBEAT_1,base_id), base_name+name+'_heartbeat_1', senders=[Module.MODUCARD], receivers=[Module.JETSON], signals=[
      Signed('uid',0 ,32,unit='', scale=1),
      Enum('status', 32, 8,  list=STATUS_SIGNAL_LIST)
      ],
      extended_frame=True),
      
    
    Message(vc(CAN_PACKET_HEARTBEAT_2,base_id), base_name+name+'_heartbeat_2', senders=[Module.MODUCARD], receivers=[Module.JETSON], signals=[
      Signed('uid',0 ,32,unit='', scale=1),
      Enum('status', 32, 8,  list=STATUS_SIGNAL_LIST)
      ],extended_frame=True),

    Message(vc(CAN_PACKET_RESET,base_id), base_name+name+'_reset', senders=[Module.JETSON], receivers=[Module.MODUCARD], signals=[
      Signed('uid',0 ,32,unit='', scale=1)],extended_frame=True),
    
    Message(vc(CAN_PACKET_ENABLE,base_id), base_name+name+'_enable', senders=[Module.JETSON], receivers=[Module.MODUCARD], signals=[
      Signed('uid',0 ,32,unit='', scale=1)],extended_frame=True),
    
    Message(vc(CAN_PACKET_DISABLE,base_id), base_name+name+'_disable', senders=[Module.JETSON], receivers=[Module.MODUCARD], signals=[
      Signed('uid',0 ,32,unit='', scale=1)],extended_frame=True),

    Message(vc(CAN_PACKET_SOFTWARE_VERSION,base_id), base_name+name+'_software_version', senders=[Module.MODUCARD], receivers=[Module.JETSON], signals=[
      Signed('uid',0 ,32,unit='', scale=1),
      Unsigned('software_version_major',32,8,unit='', scale=1),
      Unsigned('software_version_minor',40,16,unit='', scale=1),
      Unsigned('software_version_build',56,8,unit='', scale=1)
      ],extended_frame=True),

  ]
  return base_db


def make_database(nodes:dict):
  try:
    db = []
    for names in nodes.keys():
      db.extend(make_database_from_template(nodes[names],names))
    return db
  except Exception as e:
    print(e)
    raise e

modules = {
  'base': 0, # base module for ids 0
  'suspension': 0x1310, # sensors module for ids 1
}

db = make_database(modules)