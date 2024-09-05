/**
 * @file warnings_threshold.h
 * @author Eryk Możdżeń
 * @date 2022-01-21
 * */

#ifndef WARNINGS_THRESHOLD_H_
#define WARNINGS_THRESHOLD_H_

//#define WARNING_POWER_ENABLE									/*< if defined warning is active */
#define WARNING_POWER_OVERVOLTAGE_THRESHOLD				24.f	/*< upper threshold value for battery voltage in volts (float) */
#define WARNING_POWER_UNDERVOLTAGE_THRESHOLD			18.f	/*< lower threshold value for battery voltage in volts (float) */

//#define WARNING_TEMPERATURE_ENABLE								/*< if defined warning is active */
#define WARNING_TEMPERATURE_OVERTEMPERATURE_THRESHOLD	30.f	/*< upper threshold value for operating temperature in Celsius (float) */
#define WARNING_TEMPERATURE_UNDERTEMPERATURE_THRESHOLD	5.f		/*< lower threshold value for operating temperature in Celsius (float) */

#endif
