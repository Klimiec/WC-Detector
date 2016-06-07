
import RPi.GPIO as GPIO
import time

PIR_WC2 = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_WC2, GPIO.IN)

while True:
	if GPIO.input(PIR_WC2) == 0:
		print 'Move Detected: '
	else:
		print '# clean: '
	time.sleep(0.3)
	