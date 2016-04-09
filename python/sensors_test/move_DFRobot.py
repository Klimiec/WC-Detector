

import RPi.GPIO as GPIO
import time

MOVE_OUT = 2

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOVE_OUT, GPIO.IN)

while True:
	if GPIO.input(MOVE_OUT) == 1:
		print '# clean'
	else:
		print 'Object Detected: ', GPIO.input(MOVE_OUT)
		
	time.sleep(0.5)