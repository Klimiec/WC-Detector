

import logging 
import time
import RPi.GPIO as GPIO
from sensors import Sensors

gpio = Sensors()
GPIO.wait_for_edge(gpio.WC2_DOOR_sensor, GPIO.RISING)

open_door_time = time.time()
while gpio.is_wc1_motion_detected_by_PIR():
	pass

logging.debug('@Wc_1 duration of move detection after door opened: %s sec', round((time.time() - open_door_time), 2))