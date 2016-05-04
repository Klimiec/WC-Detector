
from sensors import Sensors
import RPi.GPIO as GPIO

gpio = Sensors()


GPIO.wait_for_edge(gpio.WC2_DOOR_sensor, GPIO.FALLING)
door_close_time= time.time() 

while gpio.is_wc2_motion_detected_by_PIR():
	pass

move_detection_stop = time.time() 


print "Time: %.2f  " % (move_detection_stop - door_close_time)