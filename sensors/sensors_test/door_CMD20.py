

import RPi.GPIO as GPIO
import time

DOOR_OUT = 2


GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(DOOR_OUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
	if GPIO.input(DOOR_OUT) == 0:
		print 'Door closed: ', GPIO.input(DOOR_OUT)
	else:
		print 'Door open: ', GPIO.input(DOOR_OUT)

	time.sleep(1)




