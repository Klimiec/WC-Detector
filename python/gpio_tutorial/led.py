

import RPi.GPIO as GPIO
import time

LED = 2
GPIO.setup(LED, GPIO.OUT)

while True:
	GPIO.output(LED, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(LED, GPIO.LOW)