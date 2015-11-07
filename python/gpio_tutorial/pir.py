
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIR = 9
GPIO.setup(PIR, GPIO.IN)

while True:
	if GPIO.input(PIR) == 1:
		print 'Move Detected: ',GPIO.input(PIR)
	else:
		print '# clean: ', GPIO.input(PIR)
	time.sleep(0.1)
	

