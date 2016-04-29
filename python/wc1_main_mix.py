

import threading 
import time
import logging 
from sensors import Sensors
import RPi.GPIO as GPIO


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

# Global State 
WC1_OCCUPIED = False
gpio = Sensors()
detection_counter = 0
usage_counter = 0


def wc1_callback(channel):
	
	# Check door 
	logging.debug('#STEP 1 ------------')
	GPIO.add_event_detect(gpio.WC1_DOOR_sensor, GPIO.RISING)
	start_first_check = time.time()
	time.sleep(3)

	# check if door has been opened after 3 seconds
	if GPIO.event_detected(channel):
		logging.debug('@Wc_1 door opened, stop procedure, stop time: %s ', time.strftime("%H:%M:%S"))
		GPIO.remove_event_detect(gpio.WC1_DOOR_sensor)
		WC1_OCCUPIED = False
		return
	else:
		logging.debug('@Wc_1 door still closed, check time:  %s ',round((time.time() - start_first_check), 2))


	# Check if there is a move for 10 second and door are still closed
	logging.debug('#STEP 2 ------------')
	move_detection = GPIO.wait_for_edge(gpio.WC1_MOVE_sensor, GPIO.FALLING, timeout=10000)
	if move_detection is None or GPIO.event_detected(channel):
		GPIO.remove_event_detect(gpio.WC1_DOOR_sensor)
		logging.debug('@Wc_1 door opened while checking move for the first time, stop procedure, stop time: %s', time.strftime("%H:%M:%S"))
		WC1_OCCUPIED = False
		return

	# Wait foor door to be open 
	logging.debug('#Step 3 ------------')
	start_third_check = time.time()
	last_time_move_detected = time.time()
	GPIO.add_event_detect(GPIO.WC1_MOVE_sensor, GPIO.FALLING)

	usage_counter += 1
	logging.debug('@Wc1 #Usage number:  %s ',usage_counter)

	while True:
		no_move_time = round((time.time() - last_time_move_detected), 2)

		if GPIO.event_detected(gpio.WC1_DOOR_sensor):
			logging.debug('@Wc_1 door opened, stop procedure, stop time: %s, total time: %s', time.strftime("%H:%M:%S"), round((time.time() - start_third_check), 2))
			break 
		elif GPIO.event_detected(gpio.WC1_MOVE_sensor):
			logging.debug('@Wc_1 move detected after %s seconds ,keep going...', round((time.time() - last_time_move_detected), 2))
			last_time_move_detected = time.time()
			time.sleep(1)
		elif no_move_time > 200:
			logging.debug('@Wc_1 no move detected for 3 minutes, stop procedure')
			break
		else:
			time.sleep(1)

	# things to do after wc1 is free
	GPIO.remove_event_detect(gpio.WC1_DOOR_sensor)
	GPIO.remove_event_detect(gpio.WC1_MOVE_sensor)
	gpio.wc1_led_free();
	# send REST
	WC1_OCCUPIED = False



# Main Loop of the program
while True:
	if  WC1_OCCUPIED == False and gpio.is_wc1_door_closed() and gpio.is_wc1_motion_detected_by_Microwave():
		# change state of the WC1 to occupied
		WC1_OCCUPIED = True
		detection_counter += 1
		logging.debug('#Main Thread |  change state of the WC1 (Free --> Occupied) | time:  %s | detection counter: %s', time.strftime("%H:%M:%S"), detection_counter)
		# start new thread
		t = threading.Thread(target=wc1_worker, args=(WC1_OCCUPIED,gpio,))
		t.start()
	else:
		time.sleep(1)


