

import RPi.GPIO as GPIO
import time

URINAL_TRIG = 11
URINAL_ECHO = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(URINAL_TRIG, GPIO.OUT)
GPIO.setup(URINAL_ECHO, GPIO.IN)

while True:
	GPIO.output(URINAL_TRIG, False)
	time.sleep(0.3)

	GPIO.output(URINAL_TRIG, True)
	time.sleep(0.00001)
	GPIO.output(URINAL_TRIG, False)

	while GPIO.input(URINAL_ECHO) == 0:
		pulse_start = time.time()
	while GPIO.input(URINAL_ECHO) == 1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance, 2)

	print 'Distance: ', distance