

import RPi.GPIO as GPIO
import time

DOOR_sensor = 10
GPIO.setup(DOOR_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
	if GPIO.input(self.DOOR_WC1_sensor) != 1:
		print 'Door closed: ', GPIO.input(self.DOOR_WC1_sensor)
	else:
		print 'Door open: ', GPIO.input(self.DOOR_WC1_sensor)

