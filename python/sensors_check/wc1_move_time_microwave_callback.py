
from sensors import Sensors
import RPi.GPIO as GPIO
import time

gpio = Sensors()
detection_counter = 0

GPIO.add_event_detect(GPIO.WC1_MOVE_sensor, GPIO.FALLING)

while True:
	if GPIO.event_detected(gpio.WC1_MOVE_sensor):
		detection_counter += 1
		time_elapsed = time.time() - last_time_move_detected
		last_time_move_detected = time.time() 
		print "Time: %s, | Detection counter: %d | Last time move detected (time elapsed): %.2f" % (time.strftime("%H:%M:%S"), detection_counter, last_time_move_detected)
	else:
		print '# clean'
	time.sleep(0.5)


	