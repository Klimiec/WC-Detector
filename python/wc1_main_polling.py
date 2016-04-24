

import threading 
import time
import logging 
from sensors import Sensors


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

# Global State 
WC1_OCCUPIED = False
gpio = Sensors()
detection_counter = 0
usage_counter = 0


def wc1_worker(state, gpio):

	global usage_counter

	# Check if door are closed for duration of 2 seconds
	# Give time move sensor to stop showing previous state.
	logging.debug('#STEP 1 ------------')

	start_first_check = time.time()
	for i in range(40):
		logging.debug('	@Wc_1 closed door monitoring, iteration:  %s', i)
		if gpio.is_wc1_door_closed() == False:
			logging.debug('	@Wc_1 door opened, stop wc1 thread, wc is free  after iteration number:  %s', i)
			state = False
			return
		else:
			time.sleep(0.05)

	first_check_time = time.time() - start_first_check;
	logging.debug('------------ #STEP 1 | @Wc_1 door closed monitoring total time: %.2f', first_check_time)


	# Check if there is a move for 10 second and door are still closed
	# If move detected and door still closed go to the next step
	logging.debug('#STEP 2 ------------')

	start_second_check = time.time()
	for i in range(200):
		if gpio.is_wc1_motion_detected_by_Microwave() and gpio.is_wc1_door_closed():
			logging.debug('	@Wc_1 move detected, turn on red LED and send REST, iteration :  %s', i)
			gpio.wc1_led_occupied();
			# send REST
			break
		elif gpio.is_wc1_door_closed() == False:
			 logging.debug('  @Wc_1 door opened, stop procedure, iteration: %s', i)
			 state = False
			 return
		else:
			time.sleep(0.05)

	second_check_time = time.time() - start_second_check;
	logging.debug('------------ #Step 2 | @Wc_1 door move detection monitoring total time:  %.2f', second_check_time)


	# Wait foor door to be open 
	logging.debug('#Step 3 ------------')

	start_third_check = time.time()
	last_time_move_detected = time.time()
	no_move_time = 0
	usage_counter += 1
	logging.debug('@Wc1 #Usage number:  %s ',usage_counter)
	
	while True:
		if gpio.is_wc1_door_closed() == False:
			logging.debug('------------@Wc_1 door opened, stop procedure, stop time: %s, total time: %s', time.strftime("%H:%M:%S"), round((time.time() - start_third_check), 2))
			# door opened
			gpio.wc1_led_free();
			# send REST
			state = False
			return
		elif no_move_time > 3:
			logging.debug('------------@Wc_1 no move detected for 3 minutes, stop procedure')
			# no move for more than 3 minutes
			gpio.wc1_led_free();
			# send REST
			state = False
			return
		elif gpio.is_wc1_motion_detected_by_Microwave():
			  logging.debug('	@Wc_1 move detected after %s seconds ,keep going...', round((time.time() - last_time_move_detected), 2))
			  last_time_move_detected = time.time()
			  time.sleep(0.1)
			  no_move_time = 0
		else:
			time.sleep(0.1)
			no_move_time = round((time.time() - last_time_move_detected), 2)



# Main Loop of the program
while True:
	if  WC1_OCCUPIED == False and gpio.is_wc1_door_closed() and gpio.is_wc1_motion_detected_by_Microwave():
		# change state of the WC1 to occupied, only one thread can be started at the time
		WC1_OCCUPIED = True
		detection_counter += 1
		logging.debug('#Main Thread |  change state of the WC1 (Free --> Occupied) | time:  %s | detection counter(threads): %s', time.strftime("%H:%M:%S"), detection_counter)
		# start new thread
		t = threading.Thread(target=wc1_worker, args=(WC1_OCCUPIED,gpio,))
		t.start()
	else:
		time.sleep(1)
