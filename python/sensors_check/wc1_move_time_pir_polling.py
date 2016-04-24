
from sensors import Sensors
import time

gpio = Sensors()
detection_counter = 0
last_time_move_detected= time.time() 

while True:
	if gpio.is_wc1_motion_detected_by_Microwave():
		detection_counter += 1
		time_elapsed = time.time() - last_time_move_detected
		last_time_move_detected = time.time() 
		print "Time: %s, | Detection counter: %d | Last time move detected (time elapsed): %.2f" % (time.strftime("%H:%M:%S"), detection_counter, last_time_move_detected)
	else:
		print '# clean'
	time.sleep(0.5)
