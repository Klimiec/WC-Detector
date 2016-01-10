
import RPi.GPIO as GPIO
import time
import logging 
import threading 

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


WC2_DOOR_sensor = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(WC2_DOOR_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)


lock = threading.Lock()
counter = 0


def closed_callback(channel): 
	global lock
	with lock:
		global counter
		counter += 1
	    logging.debug('@WC1 Door CLOSED counter:  %s ', counter)


def opened_callback(channel): 
	global lock
	with lock:
		global counter
		counter += 1
		logging.debug('@WC1 Door OPENED counter:  %s ', counter)

# 0->1 
GPIO.add_event_detect(WC2_DOOR_sensor, GPIO.RISING, callback=opened_callback)  
# 1->0
GPIO.add_event_detect(WC2_DOOR_sensor, GPIO.FALLING, callback=closed_callback)  


# Main Loop
while True:
	pass