#!/usr/bin/python3

try:
	from enum import StrEnum
except ImportError:
	from enum import Enum
	class StrEnum(str,Enum):
		pass

class Module(StrEnum):
	JETSON = 'Jetson'
	ODRIVE = 'ODrive'
	POWER = 'PowerBoard'
	SENSOR = 'SensorBoard'
	METAL_DETECTOR = 'MetalDetectorBoard'
	KONARM = "KonARM"
	VESC = "VESC"
	GPIO = "GPIO"
	GEIGER = "GEIGER"
	MODUCARD = "ModuCard"
	SUSPENSION = "Suspension"
