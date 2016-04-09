

import RPi.GPIO as GPIO
import time

URINAL_TRIG = 2
URINAL_ECHO = 3

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(URINAL_TRIG, GPIO.OUT)
GPIO.output(URINAL_TRIG, False)
GPIO.setup(URINAL_ECHO, GPIO.IN)


while True:
	time.sleep(1.5)

	GPIO.output(URINAL_TRIG, True)
	time.sleep(0.00001)
	GPIO.output(URINAL_TRIG, False)

	while GPIO.input(URINAL_ECHO) == 0:
		pass
	pulse_start = time.time()

	while GPIO.input(URINAL_ECHO) == 1:
		pass
	pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17000
	distance = round(distance, 2)

	if distance >= 2 and distance <= 400:
		print 'Distance: ', distance
	else:
		print 'Out of range'