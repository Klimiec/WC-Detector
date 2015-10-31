


import threading 
import time
import logging 
from gpio import GPIO
from rest import Rest

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

# Global state of setectinmg places
state = {
	'wc1' : False, 
	'wc2' : True, 
	'urinal' : True
}
gpio = GPIO()
rest = Rest()

def wc1_worker(state, gpio):
	logging.debug('@Wc 1 monitoring in other thread, states: %s', state)
	gpio.turnOnLedWc1() # Red
	while True:
		if gpio.isDoorWc1Closed() == False:
			state['wc1'] = False
			logging.debug('wc1 is now Free')
			# send REST 
			rest.update("wc1", "free")
			# change LED
			gpio.turnOffLedWc1()
			# trun on fun for 30 sek
			gpio.turnOnFun()
			# sleep for 30 sek 
			time.sleep(30)
			# turn off fun 
			gpio.turnOffFun()
			#break
		else:
			time.sleep(1)


def wc2_worker(state):
	logging.debug('@Wc 1 monitoring in other thread, states: %s', state)
	gpio.turnOnLedWc2()
	while True:
		if gpio.isDoorWc2Closed() == False:
			state['wc2'] = False
			logging.debug('wc2 is now Free')
			# send REST 
			rest.update("wc2", "free")
			# change LED
			gpio.turnOffLedWc2()
			# trun on fun for 30 sek
			# sleep for 30 sek 
			# time.sleep(30)
			# turn off fun 
			#break
		else:
			time.sleep(1)



def urinal_worker(state):
	time.sleep(2)
	if gpio.getDistance() < 50:
		state['urinal'] = True
		rest.update("urinal", "occupied")
		logging.debug('@urinal monitoring in other thread, states: %s', state)
		gpio.turnOnLedUrinal()
		# wlacz muzyke 
		while True:
			if gpio.getDistance() > 50:
				state['urinal'] = False
				logging.debug('urinal is now Free')
				# send REST 
				rest.update("urinal", "free")
				# change LED
				gpio.turnOffLedUrinal()
				# send REST 
				# wylacz muzyke
			else:
				time.sleep(1)




	state['urinal'] = True
	logging.debug('@Wc 2 monitoring in other thread')

# Main Loop of the program
counter = 0;
while True and counter < 10:
	counter = counter + 1 
	logging.debug('#Main Thread state: %s', state)

	if state['wc1'] == False and gpio.isDoorWc1Closed() == True and gpio.isMoveDetectedInWc1() == True:
		state['wc1'] = True
		rest.update("wc1", "occupied")
		logging.debug('Wc1 is Free, start detecting WC1 - new thread')
		t = threading.Thread(target=wc1_worker, args=(state,gpio,))
		t.start()

	elif state['wc2'] == False and gpio.isDoorWc2Closed() == True and gpio.isMoveDetectedInWc2() == True:
		state['wc2'] = True
		rest.update("wc2", "occupied")
		logging.debug('Wc2 is Free, start detecting WC2 - new thread')
		t = threading.Thread(target=wc2_worker, args=(state,))
		t.start()

	elif state['urinal'] == False and gpio.getDistance() < 50:
		logging.debug('Urinal is Free, start detecting Urinal  - new thread')
		t = threading.Thread(target=urinal_worker, args=(state,))
		t.start()




