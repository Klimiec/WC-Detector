
import RPi.GPIO as GPIO
import time

WC2_DOOR_sensor = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(WC2_DOOR_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
	while True:
		if GPIO.input(WC2_DOOR_sensor) == 0:
			print 'Door closed: ', GPIO.input(WC2_DOOR_sensor)
		else:
			print 'Door open: '
finally:
	GPIO.cleanup()
