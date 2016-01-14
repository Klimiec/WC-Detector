
import threading 
import time
import logging 
import pygame
from sensors import Sensors
from rest import Rest
import RPi.GPIO as GPIO

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


###################### Urinal Worker #############################

lock = threading.Lock()
counter = 0

def urinal_callback(channel): 
	global lock
	global counter
	with lock:
		 counter += 1
		 time_start = time.time()
	   	 logging.debug('@URINAL Move detected!  %s ', counter)
	   	 time.sleep(0.5)
	    	 if GPIO.input(channel) == 0:
	    		logging.debug('@URINAL start: %s', time.strftime("%H:%M:%S"))
	    		# change LED
	    		gpio.urinal_led_occupied()
	    		pygame.mixer.init()
	    		pygame.mixer.music.load("/home/pi/raspberry_project/music/c.mp3")
		        pygame.mixer.music.play()
		    	logging.debug('@URINAL turn on music')
		    	while True:
		    		time.sleep(0.5)
		    		if GPIO.input(channel) == 1:
		    			# change LED
					gpio.urinal_led_free()
					# turn off music
					pygame.mixer.music.stop()
					pygame.mixer.music.pause()
					pygame.quit()
					time_stop = time.time()
					logging.debug('@URINAL stop: %s', time.strftime("%H:%M:%S"))
					logging.debug('@URINAL total time: %s  \n\n', round(time_stop-time_start, 2))
					break;


##################################################################





# Urinal
GPIO.add_event_detect(gpio.URINAL_ECHO, GPIO.FALLING, callback=urinal_callback)  

# Main Loop of the program
while True:
	pass
	