

import RPi.GPIO as GPIO
import time

WC1_DOOR_sensor = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(WC1_DOOR_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
	while True:
		if GPIO.input(WC1_DOOR_sensor) == 0:
			print 'Door closed: ', GPIO.input(WC1_DOOR_sensor)
		else:
			print 'Door open: ', GPIO.input(WC1_DOOR_sensor)
			
		time.sleep(0.5)
finally:
	GPIO.cleanup()
