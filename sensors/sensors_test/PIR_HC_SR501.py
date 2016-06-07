

import RPi.GPIO as GPIO
import time

PIR_OUT = 2

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_OUT, GPIO.IN)

while True:
	if GPIO.input(PIR_OUT) == 1:
		print 'Move Detected: ',GPIO.input(PIR_OUT)
	else:
		print '# clean'
	time.sleep(0.5)

