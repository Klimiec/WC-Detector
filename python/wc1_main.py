

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
	logging.debug('@Wc_1 monitoring in other thread, current state of the system:  %s', state)

	# Check if door are closed for duration of 4 seconds
	is_door_open = False
	start = time.time()
	end = time.time()

	for i in range(10):
		logging.debug('@Wc_1 monitoring iteracja door:  %s', i)
		if gpio.is_wc1_door_closed() == False:
			is_door_open = True
			end = time.time()
			logging.debug('Otwarto drzwi WC1 po takim czasie!! :  %s', round((end - start), 2))
		else:
			logging.debug('Czy drzwi WC1 sa zamkniete?:  %s', gpio.is_wc1_door_closed())
			end = time.time()
			time.sleep(0.1)

	pulse= end - start
	distance = round(pulse, 2)
	logging.debug('WC1 Czas trwaia 10 iteracji:  %s', distance )
	logging.debug('WC1 Czy drzwi zostaly otwarte w ciagu 10 iteracji?: %s',  is_door_open)

	is_motion_detected = False
	if is_door_open == True:
		pass
	else:
		# Check if WC is still ocupied after 4 seconds
		for i in range(10):
			logging.debug('@Wc_1 monitoring iteracja PIR:  %s', i)
			a = time.time()
			if gpio.is_wc1_motion_detected():
				is_motion_detected = True
				logging.debug('@Wc_1 Wykryto ruch w iteracji PIR:  %s', i)
				b = time.time()
				logging.debug('@Wc_1 Czas wykrycia ruchu! :  %s', round((b - a), 2))
				break
			else:
				time.sleep(0.1)

	if is_door_open == True or is_motion_detected == False:
		# change LED
		gpio.wc1_led_free()
		# send REST
		state['wc1'] = False
		rest.wc1_free()
	else:
		while True:
			if gpio.is_wc1_door_closed() == False:
				logging.debug('Wc_1 is now Free - change state')
				# change LED
				gpio.wc1_led_free()
				# send REST
				#time.sleep(6)
				state['wc1'] = False
				rest.wc1_free()
				# trun on fun for 30 sek
				gpio.wc1_fun_on()
				time.sleep(30)
				logging.debug('Wc_1 Fun is on for 30 sec .....')
				# turn off fun 
				gpio.wc1_fun_off()
				break
			else:
				time.sleep(0.05)


# Main Loop of the program
while True:
	if  WC1_OCCUPIED == False and gpio.is_wc1_door_closed() and gpio.is_wc1_motion_detected_by_Microwave():
		# change state of the WC1 to occupied
		logging.debug('#Main Thread: change state of the WC1 (Free --> Occupied)')
		WC1_OCCUPIED = True
		# start new thread
		t = threading.Thread(target=wc1_worker, args=(WC1_OCCUPIED,gpio,))
		t.start()
	else:
		time.sleep(0.5)

