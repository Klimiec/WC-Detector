
import RPi.GPIO as GPIO
import time

WC2_LED_RED = 4
WC2_LED_GREEN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(WC2_LED_RED, GPIO.OUT)
GPIO.setup(WC2_LED_GREEN, GPIO.OUT)

try:
	while True:
		# turn on all leds
		GPIO.output(WC2_LED_RED, GPIO.LOW)
		GPIO.output(WC2_LED_GREEN, GPIO.LOW)
		
		# turn off red
		time.sleep(2)
		GPIO.output(WC2_LED_RED, GPIO.HIGH)		

	    # turn off green
		time.sleep(2)
		GPIO.output(WC2_LED_GREEN, GPIO.HIGH)		

		time.sleep(2)
finally:
	GPIO.cleanup()