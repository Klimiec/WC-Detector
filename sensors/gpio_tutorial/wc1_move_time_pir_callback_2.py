

from sensors import Sensors
import time
import RPi.GPIO as GPIO

gpio = Sensors()

channel = GPIO.wait_for_edge(gpio.WC1_MOVE_sensor, GPIO.RISING, timeout=5000)

if channel is None:
    print('Timeout occurred')
else:
    print('Edge detected on channel', channel, '| PIR state: ', GPIO.input(gpio.WC1_MOVE_sensor))

time.sleep(5)

channel = GPIO.wait_for_edge(gpio.WC1_MOVE_sensor, GPIO.RISING, timeout=5000)

if channel is None:
    print('Timeout occurred')
else:
    print('Edge detected on channel', channel)