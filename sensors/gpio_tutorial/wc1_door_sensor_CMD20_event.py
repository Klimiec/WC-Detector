


from sensors import Sensors
import time
import RPi.GPIO as GPIO

gpio = Sensors()
detection_counter = 0
last_time_move_detected= time.time() 

GPIO.add_event_detect(gpio.WC1_DOOR_sensor, GPIO.RISING)

while True:
	if GPIO.event_detected(gpio.WC1_DOOR_sensor):
		detection_counter += 1
		print "Time: %s, | Detection counter (door open): %d |" % (time.strftime("%H:%M:%S"), detection_counter)
	else:
		print '# clean'
	time.sleep(0.5)
