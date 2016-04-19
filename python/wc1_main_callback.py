
import threading 
import time
import logging 
from sensors import Sensors


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


# Global
lock = threading.Lock()
WC1_OCCUPIED = False
gpio = Sensors()

######### WC1 Worker #########

def wc1_callback(channel):

	# Check if there is thread already
	if WC1_OCCUPIED != False:
		logging.debug('   @Wc_1 kill new thread, one is already running, time: %s ',time.time())
		return

	global lock
	with lock:

		# Check door 
		logging.debug('#STEP 1 ------------')
		GPIO.add_event_detect(gpio.WC1_DOOR_sensor, GPIO.RISING)
		start_first_check = time.time()
		time.sleep(3)

		# check if door has been opened after 3 seconds
		if GPIO.event_detected(channel):
			logging.debug('@Wc_1 door opened, stop procedure, stop time: %s ',time.time())
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
			logging.debug('@Wc_1 door opened while checking move for the first time, stop procedure: %s', time.time())
			WC1_OCCUPIED = False
			return
	

		# Wait foor door to be open 
		logging.debug('#Step 3 ------------')
		start_third_check = time.time()
		last_time_move_detected = time.time()
		GPIO.add_event_detect(GPIO.WC1_MOVE_sensor, GPIO.FALLING)

		while True:
			no_move_time = round((time.time() - last_time_move_detected), 2)

			if GPIO.event_detected(gpio.WC1_DOOR_sensor):
				logging.debug('@Wc_1 door opened, stop procedure, stop time: %s, total time: %s',time.time(), round((time.time() - start_third_check), 2))
				GPIO.remove_event_detect(gpio.WC1_DOOR_sensor)
				GPIO.remove_event_detect(gpio.WC1_MOVE_sensor)
				gpio.wc1_led_free();
				# send REST
				return 
			elif GPIO.event_detected(gpio.WC1_MOVE_sensor):
				logging.debug('@Wc_1 move detected after %s seconds ,keep going...', round((time.time() - last_time_move_detected), 2))
				last_time_move_detected = time.time()
				time.sleep(0.1)
			elif no_move_time > 3:
				logging.debug('@Wc_1 no move detected for 3 minutes, stop procedure')
				GPIO.remove_event_detect(channel)
				GPIO.remove_event_detect(GPIO.WC1_MOVE_sensor)
				gpio.wc1_led_free();
				# send REST
				return
			else:
				time.sleep(0.1)




######### Urinal Worker #########
# WC1 event callback
GPIO.add_event_detect(gpio.WC1_DOOR_sensor, GPIO.FALLING, callback=wc1_callback, bouncetime=200)

# Main Loop of the program
while True:
        time.sleep(10)
        pass