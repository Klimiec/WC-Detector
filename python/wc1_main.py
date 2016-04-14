

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



def wc1_worker(state, gpio):

	#turn on red LED and send REST?

	# Check if door are closed for duration of 2 seconds
	start_first_check = time.time()

	logging.debug('#STEP 1 ------------')
	for i in range(40):
		logging.debug('@Wc_1 door closed monitoring, iteration:  %s', i)
		if gpio.is_wc1_door_closed() == False:
			logging.debug('@Wc_1 door opened, stop wc1 thread, wc is free :  %s', i)
			state = False
			return
		else:
			time.sleep(0.05)

	loop_time = time.time() - start_first_check;
	logging.debug('------------ #STEP 1 | @Wc_1 door closed monitoring total time:  %s', loop_time)



	# Check if there is a move for 10 second and door are still closed
	start_second_check = time.time()

	logging.debug('#STEP 2 ------------')
	for i in range(200):
		if gpio.is_wc1_door_closed() and gpio.is_wc1_motion_detected_by_Microwave():
			logging.debug('@Wc_1 move detected, turn on red LED and send REST :  %s', i)
			state = True;
			gpio.wc1_led_occupied();
			# send REST
			break
		elif gpio.is_wc1_door_closed() == False:
			 logging.debug('@Wc_1 door opened, stop procedure, iteration: %s', i)
			 state = False
			 return
		else:
			time.sleep(0.05)

	loop_time = time.time() - start;
	logging.debug('#Step 2 | @Wc_1 door move detection monitoring total time:  %s', loop_time)


	# Wait foor door to be open 
	start_third_check = time.time()
	last_time_move_detected = time.time()
	
	logging.debug('#Step 3 ------------')
	while True:

		no_move_time = round((time.time() - last_time_move_detected), 2)
		if gpio.is_wc1_door_closed() == False:
			logging.debug('@Wc_1 door opened, stop procedure, stop time: %s, total time: %s',time.time(), round((time.time() - start_third_check), 2))
			# Otwarto drzwi
			gpio.wc1_led_free();
			# send REST
			state = False
			return
		elif gpio.is_wc1_motion_detected_by_Microwave():
			  logging.debug('@Wc_1 move detected after %s seconds ,keep going...', round((time.time() - last_time_move_detected), 2))
			  last_time_move_detected = time.time()
		elif no_move_time > 3:
			logging.debug('@Wc_1 no move detected for 3 minutes, stop procedure')
			# send REST
			state = False

			while True:
				if gpio.is_wc1_door_closed():
					gpio.wc1_led_probably_free()
				else:
		else:
			time.sleep(0.05)



# Main Loop of the program
while True:
	if  WC1_OCCUPIED == False and gpio.is_wc1_door_closed() and gpio.is_wc1_motion_detected_by_Microwave():
		# change state of the WC1 to occupied
		logging.debug('-----------------------------------------------------------------')
		logging.debug('#Main Thread |  change state of the WC1 (Free --> Occupied) | time %s', time.time())
		WC1_OCCUPIED = True
		# start new thread
		t = threading.Thread(target=wc1_worker, args=(WC1_OCCUPIED,gpio,))
		t.start()
	else:
		time.sleep(1)

