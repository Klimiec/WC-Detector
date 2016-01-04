
import threading 
import time
import logging 
import pygame
from sensors import Sensors
from rest import Rest

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

# Global state of places under detection 
state = {
	'wc1' : False, 
	'wc2' : False, 
	'urinal' : False
}

gpio = Sensors()
rest = Rest()


def wc1_worker(state, gpio):
	logging.debug('@Wc_1 monitoring in other thread, current state of the system:  %s', state)

	# Check if WC is still ocupied after 4 seconds
	time.sleep(4)
	is_motion_detected = False
	for i in range(10):
		if gpio.is_wc1_motion_detected():
			is_motion_detected = True
			break
		else:
			time.sleep(0.1)

	if is_motion_detected == False:
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
				time.sleep(6)
				state['wc1'] = False
				rest.wc1_free()
				# trun on fun for 30 sek
				gpio.wc1_fun_on()
				time.sleep(30)
				logging.debug('Wc_1 Fun is on for 30 sec .....')
				# turn off fun 
				gpio.wc1_fun_off()
				break


def wc2_worker(state, gpio):
	logging.debug('@Wc_2  monitoring in other thread, current state of the system: %s', state)

	# Check if WC is still ocupied after 4 seconds
	time.sleep(4)
	is_motion_detected = False
	for i in range(10):
		if gpio.is_wc2_motion_detected():
			is_motion_detected = True
			break
		else:
			time.sleep(0.1)
	
	if is_motion_detected == False:
		# change LED
		gpio.wc2_led_free()
		# send REST
		state['wc2'] = False
		rest.wc2_free()
	else:
		while True:
			if gpio.is_wc2_door_closed() == False:
				# change LED
				gpio.wc2_led_free()
				# send REST 
				time.sleep(6)
				state['wc2'] = False
				rest.wc2_free()
				# trun on fun for 30 sek
				gpio.wc2_fun_on()
				time.sleep(30)
				logging.debug('Wc_2 Fun is on for 30 sec .....')
				# turn off fun 
				gpio.wc2_fun_off()
				break




def urinal_worker(state, gpio):
	# wait to determine if sb is using urinal
	time.sleep(2)
	if gpio.urinal_get_distance() < 50:
		# change LED
		gpio.urinal_led_occupied()
		# send REST 
		rest.urinal_occupied()
		# turn on music - to be implemented
		pygame.mixer.init()
		pygame.mixer.music.load("/home/pi/raspberry_project/music/gm.mp3")
		pygame.mixer.music.play()
		logging.debug('Urinal turn on music')
		while True:
			if gpio.urinal_get_distance() > 50:
				# change LED
				gpio.urinal_led_free()
				# send REST 
				state['urinal'] = False
				rest.urinal_free()
				# turn off music
				pygame.mixer.music.stop()
				pygame.mixer.music.pause()
				pygame.quit()
				break;
			else:
				time.sleep(0.5)
	else:
		state['urinal'] = False


# Main Loop of the program
while True:
	
	if state['wc1'] == False and gpio.is_wc1_door_closed() and gpio.is_wc1_motion_detected():
		logging.debug('#Main Thread: change state of WC1 (free --> occupied)')
		# change state of WC1 to occupied
		gpio.wc1_led_occupied() # Red
		# send REST 
		state['wc1'] = True
		rest.wc1_occupied()
		# start new thread
		t = threading.Thread(target=wc1_worker, args=(state,gpio,))
		t.start()

	elif state['urinal'] == False and gpio.urinal_get_distance() < 50:
		state['urinal'] = True
		t = threading.Thread(target=urinal_worker, args=(state,gpio, ))
		t.start()    
	
	elif state['wc2'] == False and gpio.is_wc2_door_closed() and gpio.is_wc2_motion_detected():
		logging.debug('#Main Thread: change state of WC2 (free --> occupied)')
		# change state of WC2 to occupied
		gpio.wc2_led_occupied() # Red
		# send REST 
		state['wc2'] = True
		rest.wc2_occupied()
		# start new thread
		t = threading.Thread(target=wc2_worker, args=(state,gpio,))
		t.start()

	



