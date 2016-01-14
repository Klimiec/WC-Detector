
import threading 
import time
import logging 
import pygame
from sensors import Sensors
from rest import Rest
import RPi.GPIO as GPIO

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

# Global state of places under detection 
state = {
	'wc1' : False, 
	'wc2' : False, 
	'urinal' : False
}

gpio = Sensors()
rest = Rest()


###################### WC1 door Worker #############################

lock_wc1 = threading.Lock()
counter_wc1 = 0
wc1_door_state = True
wc1_start_time = 0
wc1_end_time = 0

def wc1_open_callback(channel): 
	global lock_wc1
	global counter_wc1
	with lock_wc1:
		gpio.wc1_led_free()
		counter_wc1 -= 1
		logging.debug('@WC1 door OPEN: %s | counter_wc1: %s', time.strftime("%H:%M:%S"), counter_wc1)


def wc1_close_callback(channel): 	
	global lock_wc1
	global counter_wc1
	with lock_wc1:
		gpio.wc1_led_occupied()
		counter_wc1 +=1
		logging.debug('@WC1 door CLOSE: %s | counter_wc1: %s', time.strftime("%H:%M:%S"), counter_wc1)
			

def wc1_both_callback(channel): 
	global lock_wc1
	global counter_wc1
	global wc1_start_time 
	global wc1_end_time
	global wc1_door_state 
	logging.debug(' ################# @WC1 THREAD Start')
	with lock_wc1:
		if wc1_door_state == True:  # check previous state
			wc1_door_state = False  #door closed
			wc1_start_time = time.time()
			counter_wc1 +=1
			logging.debug('@WC1 CLOSE the door: %s | counter_wc1: %s', time.strftime("%H:%M:%S"), counter_wc1)
			gpio.wc1_led_occupied()
		else:
			wc1_door_state = True  # door opened
			counter_wc1 -=1
			wc1_end_time = time.time()
			gpio.wc1_led_free()
			logging.debug('@WC1 door OPEN: %s | counter_wc1: %s | Total time: %s \n\n', time.strftime("%H:%M:%S"), counter_wc1, round((wc1_end_time- wc1_start_time), 2))
			wc1_start_time = 0
			wc1_end_time = 0

##################################################################


# Door WC1
GPIO.add_event_detect(gpio.WC1_DOOR_sensor, GPIO.BOTH, callback=wc1_both_callback) 


# Main
while True:
	pass
	