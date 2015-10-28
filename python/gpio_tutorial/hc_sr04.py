

import RPi.GPIO as GPIO
import time

TRIG = 11
ECHO = 0

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

while True:
	GPIO.output(self.URINAL_TRIG, False)
	time.sleep(0.3)

	GPIO.output(self.URINAL_TRIG, True)
	time.sleep(0.00001)
	GPIO.output(self.URINAL_TRIG, False)

	while GPIO.input(self.URINAL_ECHO) == 0:
		pulse_start = time.time()
	while GPIO.input(self.URINAL_ECHO) == 1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance, 2)

	print 'Distance: ', distance