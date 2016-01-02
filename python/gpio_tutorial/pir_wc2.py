
import RPi.GPIO as GPIO
import time

PIR_WC2 = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_WC2, GPIO.IN)

while True:
	if GPIO.input(PIR_WC2) == 1:
		print 'Move Detected: ',GPIO.input(PIR_WC2)
	else:
		print '# clean: '
	time.sleep(0.1)
	