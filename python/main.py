
import threading 
import time
import logging 
import pygame
from sensors import Sensors
from rest import Rest

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

# Global state of detecting places
state = {
	'wc1' : False, 
	'wc2' : False, 
	'urinal' : False
}
gpio = Sensors()
rest = Rest()

def wc1_worker(state, gpio):
	logging.debug('@Wc_1 monitoring in other thread, current state of the system:  %s', state)
	gpio.wc1_led_occupied() # Red
	while True:
		if gpio.is_wc1_door_closed() == False:
			state['wc1'] = False
			logging.debug('Wc_1 is now Free - change state')
			# send REST 
			rest.wc1_free()
			logging.debug('Wc_1 REST - change state of WC_1 Occupied -> Free')
			# change LED
			gpio.wc1_led_free()
			# trun on fun for 30 sek
			gpio.wc1_fun_on()
			# sleep for 30 sek 
			time.sleep(30)
			logging.debug('Wc_1 Fun is on for 30 sec .....')
			# turn off fun 
			gpio.wc1_fun_off()
			break
		else:
			logging.debug('Wc_1 is occupied ...')
			time.sleep(0.5)


def wc2_worker(state, gpio):
	logging.debug('@Wc_2  monitoring in other thread, current state of the system: %s', state)
	gpio.wc2_led_occupied() #Red
	while True:
		if gpio.is_wc2_door_closed() == False:
			state['wc2'] = False
			logging.debug('Wc_2 is now Free - change state')
			# send REST 
			rest.wc2_free()
			logging.debug('Wc_2 REST - change state of WC_2 Occupied -> Free')
			# change LED
			gpio.wc2_led_free()
			# trun on fun for 30 sek
			gpio.wc2_fun_on()
			# time.sleep(30)
			time.sleep(30)
			logging.debug('Wc_2 Fun is on for 30 sec .....')
			# turn off fun 
			gpio.wc2_fun_off()
			#break
		else:
			time.sleep(0.5)



def urinal_worker(state, gpio):
	time.sleep(2.5)
	if gpio.get_distance() < 50:
		gpio.urinal_led_occupied()
		# send REST 
		rest.urinal_occupied()
	   	logging.debug('Urinal REST - change state of Urinal Free -> Occupied')
		# turn on music - to be implemented
		pygame.mixer.init()
		pygame.mixer.music.load("/home/pi/raspberry_project/music/team.mp3")
		pygame.mixer.music.play()
		logging.debug('Urinal turn on music')
		while True:
			if gpio.get_distance() > 50:
				state['urinal'] = False
				logging.debug('Urinal is now Free - change state')
				# send REST 
				rest.urinal_free()
				# change LED
				gpio.urinal_led_free()
				logging.debug('Urinal REST - change state of Urinal Occupied -> Free')
				# turn off music - to be implemented
				logging.debug('Urinal turn off the music')
				pygame.mixer.music.stop()
				pygame.mixer.music.pause()
				pygame.quit()
				break;
			else:
				logging.debug('Urinal is occupied, distance: %s', gpio.get_distance())
				time.sleep(0.5)
	else:
		state['urinal'] = False


# Main Loop of the program
while True:
	logging.debug('#Main Thread, state of the system: %s', state)
	time.sleep(1)
	
	if state['wc1'] == False and gpio.is_wc1_door_closed() == True and gpio.is_wc1_motion_detected() == True:
		logging.debug('#Main Thread: change state of WC1 (free --> occupied)')
		state['wc1'] = True
		# send REST 
		rest.wc1_occupied()
		t = threading.Thread(target=wc1_worker, args=(state,gpio,))
		t.start()

	elif state['urinal'] == False and gpio.get_distance() < 50:
		state['urinal'] = True
		logging.debug('#Main Thread: URINAL is possibly Free, start detecting Urinal  - new thread')
		t = threading.Thread(target=urinal_worker, args=(state,gpio, ))
		t.start()    
	
	elif state['wc2'] == False and gpio.is_wc2_door_closed() == True and gpio.is_wc2_motion_detected() == True:
		#state['wc2'] = True
		# send REST 
		rest.wc2_occupied()
		#t = threading.Thread(target=wc2_worker, args=(state,gpio, ))
		#t.start()

	



