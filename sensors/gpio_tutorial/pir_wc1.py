
import RPi.GPIO as GPIO
import time

PIR_WC1 = 9

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_WC1, GPIO.IN)

while True:
	if GPIO.input(PIR_WC1) == 1:
		print 'Move Detected: ',GPIO.input(PIR_WC1)
	else:
		print '# clean: '
	time.sleep(0.1)
	

