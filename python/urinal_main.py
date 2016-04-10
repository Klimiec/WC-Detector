


import threading 
import time
import logging 
from sensors import Sensors


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

# Global State 
URINAL_OCCUPIED = False
gpio = Sensors()



def urinal_worker(state, gpio):
	# wait to determine if sb is using urinal
	time.sleep(1.5)
	if gpio.is_urinal_person_presence_detected():
		# change LED
		gpio.urinal_led_occupied()
		# send REST 
			#rest.urinal_occupied()
		# turn on music
		gpio.urinal_turn_on_music()

		while True:
			if  gpio.is_urinal_person_presence_detected() == False:
				# change LED
				gpio.urinal_led_free()
				# send REST 
					# rest.urinal_free()
				# turn off music
				gpio.urinal_turn_off_music()
				# change global state of urinal
				state = False
				break;
			else:
				time.sleep(0.5)
	else:
		# change global state of urinal
		state = False



# Main Loop of the program
while True:
	if  URINAL_OCCUPIED == False and gpio.is_urinal_person_presence_detected():
		# change state of the URINAL to occupied
		logging.debug('#Main Thread: change state of the URINAL (Free --> Occupied)')
		# change global state of urinal
		URINAL_OCCUPIED = True
		# start new thread
		t = threading.Thread(target=urinal_worker, args=(URINAL_OCCUPIED,gpio,))
		t.start()
	else:
		time.sleep(0.5)

	
