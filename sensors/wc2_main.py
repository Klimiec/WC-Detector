import threading 
import time
import logging 
from sensors import Sensors
import RPi.GPIO as GPIO


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

# Global State 
WC2_OCCUPIED = False
gpio = Sensors()
detection_counter = 0
usage_counter = 0

def wc2_worker():

	global gpio
	global usage_counter
	
	# Check door 
	logging.debug('   #STEP 1 (check door) ------------')
	start_first_check = time.time()

	door_detection = GPIO.wait_for_edge(gpio.WC2_DOOR_sensor, GPIO.RISING, timeout=4500)
	# check if door has been opened after 3 seconds
	if  door_detection is None:
		logging.debug('   @Wc_2 door still closed, check first time duration: %.2f sec',round((time.time() - start_first_check), 2))
	else:
		logging.debug('   @Wc_2 door opened, stop procedure, stop time: %s  | duration of first check: %.2f ', time.strftime("%H:%M:%S"),round((time.time() - start_first_check), 2))
		return
 
	# Check if there is a move for 10 second and door are still closed
	logging.debug('   #STEP 2  (check move) ------------')
	start_second_check = time.time()

	GPIO.add_event_detect(gpio.WC2_DOOR_sensor, GPIO.RISING)
	is_move_detected = False
	for i in range(100):
		if gpio.is_wc2_motion_detected_by_PIR():
			logging.debug('   @Wc_2 move detected after time duration: %.2f sec', (time.time() - start_second_check))
			is_move_detected = True
			break
		elif GPIO.event_detected(gpio.WC2_DOOR_sensor):
			logging.debug('   @Wc_2 door opened after: %.2f  sec, stop procedure', (time.time() - start_second_check))
			return
		else:
			time.sleep(0.1)

	if is_move_detected == False:
		logging.debug('   @Wc_2 no move detected for: %.2f  sec, stop procedure', (time.time() - start_second_check))
		return

	# Wait foor door to be open 
	logging.debug('   #Step 3 (main loop) ------------')
	start_third_check = time.time()
	last_time_move_detected = time.time()

	usage_counter += 1
	logging.debug('   @wc2 #Usage number:  %s ',usage_counter)

	while True:
		no_move_time = round((time.time() - last_time_move_detected), 2)
		
		if GPIO.event_detected(gpio.WC2_DOOR_sensor):
			logging.debug('   @Wc_2 door opened, stop procedure, stop time: %s, Main loop duration: %s', time.strftime("%H:%M:%S"), round((time.time() - start_third_check), 2))
			break 
		elif gpio.is_wc2_motion_detected_by_PIR():
			logging.debug('   @Wc_2 move detected after: %s seconds ,keep going...', round((time.time() - last_time_move_detected), 2))
			last_time_move_detected = time.time()
			time.sleep(1)
		elif no_move_time > 240:
			logging.debug('   @Wc_2 no move detected for 3 minutes, stop procedure')
			break
		else:
			time.sleep(0.1)


# Main Loop of the program
while True:
	if  WC2_OCCUPIED == False and gpio.is_wc2_door_closed() and gpio.is_wc2_motion_detected_by_PIR():
		# change state of the wc2 to occupied
		WC2_OCCUPIED = True
		gpio.wc2_led_occupied()
		# SEND REST
		detection_counter += 1
		logging.debug('#Main Thread |  change state of the wc2 (Free --> Occupied) | time:  %s | detection counter: %s', time.strftime("%H:%M:%S"), detection_counter)
		
		# start new thread
		start_thread = time.time()
		t = threading.Thread(target=wc2_worker, args=[])
		t.start()
		t.join()
		
		logging.debug('#Main Thread |  change state of the wc2 (Occupied --> Free) | thread total time(duration):  %.2f  \n\n\n', (time.time() - start_thread))
		GPIO.remove_event_detect(gpio.WC2_DOOR_sensor)
		gpio.wc2_led_free()
		# SEND REST
		WC2_OCCUPIED = False
	else:
		time.sleep(0.1)
