

from sensors import Sensors
import time

gpio = Sensors()
detection_counter = 0


while True:
	if gpio.is_wc1_door_closed():
		detection_counter += 1
		print "Time: %s, | Detection counter (door closed): %d " % (time.strftime("%H:%M:%S"), detection_counter)
	else:
		print '# clean (door open)'
	time.sleep(0.5)


