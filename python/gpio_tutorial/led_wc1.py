

import RPi.GPIO as GPIO
import time


WC1_LED_RED = 2
WC1_LED_GREEN = 3
URINAL_LED_BLUE = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(WC1_LED_RED, GPIO.OUT)
GPIO.setup(WC1_LED_GREEN, GPIO.OUT)
GPIO.setup(URINAL_LED_BLUE, GPIO.OUT)

while True:
	# all leds are turned on
	GPIO.output(WC1_LED_RED, GPIO.LOW)
	GPIO.output(WC1_LED_GREEN, GPIO.LOW)
	GPIO.output(URINAL_LED_BLUE, GPIO.LOW)

	# turn off red
	time.sleep(2)
	GPIO.output(WC1_LED_RED, GPIO.HIGH)

	# turn off green
	time.sleep(2)
	GPIO.output(WC1_LED_GREEN, GPIO.HIGH)

	# turn off blue
	time.sleep(2)
	GPIO.output(URINAL_LED_BLUE, GPIO.HIGH)

	time.sleep(2)