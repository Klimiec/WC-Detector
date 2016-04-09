

import RPi.GPIO as GPIO
import time

DISTANCE_OUT = 2

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(DISTANCE_OUT, GPIO.IN)

while True:
	if GPIO.input(DISTANCE_OUT) == 1:
		print 'Object Detected: ', GPIO.input(DISTANCE_OUT)
	else:
		print '# clean'
	time.sleep(0.5)


