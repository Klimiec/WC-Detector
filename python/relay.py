

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
WC1_Relay = 4

GPIO.setup(WC1_Relay, GPIO.OUT)

GPIO.output(WC1_Relay, GPIO.HIGH)
time.sleep(3)
GPIO.output(WC1_Relay, GPIO.LOW)
time.sleep(3)
GPIO.output(WC1_Relay, GPIO.HIGH)
time.sleep(3)
GPIO.output(WC1_Relay, GPIO.LOW)