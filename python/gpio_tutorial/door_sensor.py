

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
DOOR_sensor = 10
GPIO.setup(DOOR_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
	if GPIO.input(DOOR_sensor) != 1:
		print 'Door closed: ', GPIO.input(DOOR_sensor)
	else:
		print 'Door open: ', GPIO.input(DOOR_sensor)

