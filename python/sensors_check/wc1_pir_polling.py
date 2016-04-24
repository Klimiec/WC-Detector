
from sensors import Sensors
import time

gpio = Sensors()
detection_counter = 0

while True:
	if gpio.is_wc1_motion_detected_by_PIR():
		detection_counter += 1
		print "Time: %s, | Detection counter: %d" % (time.strftime("%H:%M:%S"), detection_counter)
	else:
		print '# clean'
	time.sleep(0.5)