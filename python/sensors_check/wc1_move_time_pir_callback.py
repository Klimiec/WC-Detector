

from sensors import Sensors
import time
import RPi.GPIO as GPIO

gpio = Sensors()
detection_counter = 0
last_time_move_detected= time.time() 

GPIO.add_event_detect(GPIO.WC1_MOVE_sensor, GPIO.RISING)

while True:
	if GPIO.event_detected(gpio.WC1_MOVE_sensor):
		detection_counter += 1
		time_elapsed = time.time() - last_time_move_detected
		last_time_move_detected = time.time() 
		print "Time: %s, | Detection counter: %d | Last time move detected (time elapsed): %.2f" % (time.strftime("%H:%M:%S"), detection_counter, last_time_move_detected)
	else:
		print '# clean'
	time.sleep(0.5)

