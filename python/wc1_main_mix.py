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

def wc1_worker():

	global gpio
	global usage_counter
	
	# Check door 
	logging.debug('   #STEP 1 (check door) ------------')
	start_first_check = time.time()

	door_detection = GPIO.wait_for_edge(gpio.WC1_DOOR_sensor, GPIO.RISING, timeout=3000)
	# check if door has been opened after 3 seconds
	if  door_detection is None:
		logging.debug('   @Wc_1 door still closed, check first time duration: %.2f ',round((time.time() - start_first_check), 2))
	else:
		logging.debug('   @Wc_1 door opened, stop procedure, stop time: %s ', time.strftime("%H:%M:%S"))
		return
 
	# Check if there is a move for 10 second and door are still closed
	logging.debug('   #STEP 2  (check move) ------------')
	start_second_check = time.time()

	GPIO.add_event_detect(gpio.WC1_DOOR_sensor, GPIO.RISING)
	GPIO.add_event_detect(gpio.WC1_MOVE_sensor, GPIO.FALLING)
	is_move_detected = False
	for i in range(100):
		if GPIO.event_detected(gpio.WC1_DOOR_sensor):
			logging.debug('   @Wc_1 door opened while checking move for the first time, stop procedure, duration of second check: %.2f | ', (time.time() - start_second_check))
			GPIO.remove_event_detect(gpio.WC1_DOOR_sensor)
			GPIO.remove_event_detect(gpio.WC1_MOVE_sensor)
			return
		elif GPIO.event_detected(gpio.WC1_MOVE_sensor):
			logging.debug('   @Wc_1 move detected after time duration: %.2f ', (time.time() - start_second_check))
			is_move_detected = True
			break
		else:
			time.sleep(0.1)

	if is_move_detected == False:
		logging.debug('   @Wc_1 no move detected for: %.2f  sec, no door opened, stop procedure', (time.time() - start_second_check))
		GPIO.remove_event_detect(gpio.WC1_DOOR_sensor)
		GPIO.remove_event_detect(gpio.WC1_MOVE_sensor)
		return

	# Wait foor door to be open 
	logging.debug('   #Step 3 (main loop) ------------')
	start_third_check = time.time()
	last_time_move_detected = time.time()

	usage_counter += 1
	logging.debug('   @Wc1 #Usage number:  %s ',usage_counter)

	while True:
		no_move_time = round((time.time() - last_time_move_detected), 2)

		if GPIO.event_detected(gpio.WC1_DOOR_sensor):
			logging.debug('   @Wc_1 door opened, stop procedure, stop time: %s, Main loop duration: %s', time.strftime("%H:%M:%S"), round((time.time() - start_third_check), 2))
			break 
		elif GPIO.event_detected(gpio.WC1_MOVE_sensor):
			logging.debug('   @Wc_1 move detected after: %s seconds ,keep going...', round((time.time() - last_time_move_detected), 2))
			last_time_move_detected = time.time()
			time.sleep(1)
		elif no_move_time > 180:
			logging.debug('   @Wc_1 no move detected for 3 minutes, stop procedure')
			break
		else:
			time.sleep(0.1)

	# things to do after wc1 is free
	GPIO.remove_event_detect(gpio.WC1_DOOR_sensor)
	GPIO.remove_event_detect(gpio.WC1_MOVE_sensor)

# Main Loop of the program

GPIO.add_event_detect(gpio.WC1_DOOR_sensor, GPIO.FALLING)
while True:
	if  WC1_OCCUPIED == False and GPIO.event_detected(gpio.WC1_DOOR_sensor):
		GPIO.remove_event_detect(gpio.WC1_DOOR_sensor)
		# change state of the WC1 to occupied
		WC1_OCCUPIED = True
		# SEND REST
		gpio.wc1_led_occupied()
		detection_counter += 1
		logging.debug('#Main Thread |  change state of the WC1 (Free --> Occupied) | time:  %s | detection counter: %s', time.strftime("%H:%M:%S"), detection_counter)
		
		# start new thread
		start_thread = time.time()
		t = threading.Thread(target=wc1_worker, args=[])
		t.start()
		t.join()
		
		logging.debug('#Main Thread |  change state of the WC1 (Occupied --> Free) | thread total time(duration):  %.2f  \n\n\n', (time.time() - start_thread))
		gpio.wc1_led_free()
		# SEND REST
		WC1_OCCUPIED = False
		GPIO.add_event_detect(gpio.WC1_DOOR_sensor, GPIO.FALLING)
	else:
		time.sleep(0.1)
