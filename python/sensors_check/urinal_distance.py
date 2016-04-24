

import threading
import time
import logging
from sensors import Sensors
import RPi.GPIO as GPIO


def urinal_callback(channel):
	logging.debug('Urinal, start new thread, time:  %s ',time.strftime("%H:%M:%S"))
	time.sleep(7)
	logging.debug('		@Urinal, end thread, time:  %s ',time.strftime("%H:%M:%S"))



######### Urinal Worker #########
# Urinal event callback
GPIO.add_event_detect(gpio.URINAL_DISTANCE_sensor, GPIO.FALLING, callback=urinal_callback)

# Main Loop of the program
while True:
        time.sleep(10)
        pass