

import threading 
import time
import logging 
from sensors import Sensors
import RPi.GPIO as GPIO


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


# Global
detection_counter = 0


######### WC1 Worker #########

def wc1_callback(channel):
	global detection_counter
	detection_counter += 1
	logging.debug('   @Wc_1 door | new thread started at time:  %s | detection counter: %s', time.strftime("%H:%M:%S"), detection_counter)




# WC1 event callback
GPIO.add_event_detect(gpio.WC1_DOOR_sensor, GPIO.FALLING, callback=wc1_callback, bouncetime=200)

# Main Loop of the program
while True:
        time.sleep(10)
        pass

