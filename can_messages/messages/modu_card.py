#
# This file is part of the CAN messages database.
# Created by Patryk Dudziński.
# Date February 18, 2025
#

from abstract.signals import Enum, Unsigned,Float, Signed, BIG_ENDIAN, LITTLE_ENDIAN
from abstract.modules import Module
from abstract.message import Message

################################################
# MODU CARD CAN messages

CAN_PACKET_HEARTBEAT_1 = 0
CAN_PACKET_HEARTBEAT_2 = 1
CAN_PACKET_RESET = 2
CAN_PACKET_ENABLE = 3
CAN_PACKET_DISABLE = 4


def vc(command_id:int, base_id:int):
  return (command_id << 8) | base_id

def make_database_from_template(base_id,name):
  base_db = [
    Message(vc(CAN_PACKET_HEARTBEAT_1,base_id), name+'_heartbeat_1', senders=[Module.MODUCARD], receivers=[Module.JETSON], signals=[
      Signed('uid',0 ,32,unit='', scale=1)],extended_frame=True),
    
    Message(vc(CAN_PACKET_HEARTBEAT_2,base_id), name+'_heartbeat_2', senders=[Module.MODUCARD], receivers=[Module.JETSON], signals=[
      Signed('uid',0 ,32,unit='', scale=1)],extended_frame=True),

    Message(vc(CAN_PACKET_RESET,base_id), name+'_reset', senders=[Module.JETSON], receivers=[Module.MODUCARD], signals=[
      Signed('uid',0 ,32,unit='', scale=1)],extended_frame=True),
    
    Message(vc(CAN_PACKET_ENABLE,base_id), name+'_enable', senders=[Module.JETSON], receivers=[Module.MODUCARD], signals=[
      Signed('uid',0 ,32,unit='', scale=1)],extended_frame=True),
    
    Message(vc(CAN_PACKET_DISABLE,base_id), name+'_disable', senders=[Module.JETSON], receivers=[Module.MODUCARD], signals=[
      Signed('uid',0 ,32,unit='', scale=1)],extended_frame=True)

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
  'nav': 0x100,
}

db = make_database(modules)