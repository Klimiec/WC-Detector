import RPi.GPIO as GPIO
import time
import logging 
import pygame

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

class Sensors:

# WC1 
	WC1_LED_RED = 2
	WC1_LED_GREEN = 3
	WC1_DOOR_sensor = 10
	WC1_MOVE_sensor = 9

# WC2
	WC2_LED_RED = 4
	WC2_LED_GREEN = 17
	WC2_DOOR_sensor = 13
	WC2_MOVE_sensor = 6


# URINAL
	URINAL_LED_BLUE = 27
	URINAL_DISTANCE_sensor = 0

	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		# WC1 
		GPIO.setup(self.WC1_LED_RED, GPIO.OUT)
		GPIO.output(self.WC1_LED_RED, GPIO.HIGH) 
		GPIO.setup(self.WC1_LED_GREEN, GPIO.OUT)
		GPIO.output(self.WC1_LED_GREEN, GPIO.LOW)
		GPIO.setup(self.WC1_DOOR_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.WC1_MOVE_sensor, GPIO.IN)


		# WC2
		GPIO.setup(self.WC2_LED_RED, GPIO.OUT)
		GPIO.output(self.WC2_LED_RED, GPIO.HIGH)
		GPIO.setup(self.WC2_LED_GREEN, GPIO.OUT)
		GPIO.output(self.WC2_LED_GREEN, GPIO.LOW)
		GPIO.setup(self.WC2_DOOR_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.WC2_MOVE_sensor, GPIO.IN)

		# URINAL
		GPIO.setup(self.URINAL_LED_BLUE, GPIO.OUT)
		GPIO.output(self.URINAL_LED_BLUE, GPIO.HIGH)
		GPIO.setup(self.URINAL_DISTANCE_sensor, GPIO.IN)
	
	################################### WC1	
	def wc1_led_occupied(self):
		#toilet occupied
		logging.debug('WC1 - LED Red')
		GPIO.output(self.WC1_LED_GREEN, GPIO.HIGH)
		GPIO.output(self.WC1_LED_RED, GPIO.LOW)

	def wc1_led_free(self):
		#toilet free
		logging.debug('WC1 - LED Green')
		GPIO.output(self.WC1_LED_RED, GPIO.HIGH)
		GPIO.output(self.WC1_LED_GREEN, GPIO.LOW)

	def is_wc1_door_closed(self):
		#detect if wc1's door is closed
		if GPIO.input(self.WC1_DOOR_sensor) == 0:
			return True
		else:
			return False

	def is_wc1_motion_detected_by_PIR(self):
		#detect if there is move in wc1 by PIR sensor
		if GPIO.input(self.WC1_MOVE_sensor) == 1:
			return True
		else:
			return False

	def is_wc1_motion_detected_by_Microwave(self):
		#detect if there is move in wc1 by Microwave sensor
		if GPIO.input(self.WC1_MOVE_sensor) == 0:
			return True
		else:
			return False

	################################### WC2
	def wc2_led_occupied(self):
		#toilet occupied
		logging.debug('WC2 - LED Red')
		GPIO.output(self.WC2_LED_GREEN, GPIO.HIGH)
		GPIO.output(self.WC2_LED_RED, GPIO.LOW)

	def wc2_led_free(self):
		#toilet free
		logging.debug('WC2 - LED Green')
		GPIO.output(self.WC2_LED_RED, GPIO.HIGH)
		GPIO.output(self.WC2_LED_GREEN, GPIO.LOW)

	def is_wc2_door_closed(self):
		#detect if wc1's door is closed
		if GPIO.input(self.WC2_DOOR_sensor) == 0:
			return True
		else:
			return False

	def is_wc2_motion_detected_by_PIR(self):
		#detect if there is move in wc2
		if GPIO.input(self.WC2_MOVE_sensor) == 1:
			return True
		else:
			return False

	def is_wc2_motion_detected_by_Microwave(self):
		#detect if there is move in wc1 by Microwave sensor
		if GPIO.input(self.WC1_MOVE_sensor) == 0:
			return True
		else:
			return False

	################################### URINAL
	def urinal_led_occupied(self):
		#toilet occupied
		logging.debug('Urinal - LED Blue on')
		GPIO.output(self.URINAL_LED_BLUE, GPIO.LOW)

	def urinal_led_free(self):
		#toilet free
		logging.debug('Urinal - LED Blue off')
		GPIO.output(self.URINAL_LED_BLUE, GPIO.HIGH)

	def is_urinal_person_presence_detected(self):
		#detect if there is move in urinal
		if GPIO.input(self.URINAL_DISTANCE_sensor) == 0:
			return True
		else:
			return False

	def urinal_turn_on_music(self):
		#turn on music 
		pygame.mixer.init()
		pygame.mixer.music.load("/home/pi/raspberry_project/music/gm.mp3")
		pygame.mixer.music.play()
		logging.debug('Urinal turn on music')

	def urinal_turn_off_music(self):
		#turn off music 
		pygame.mixer.music.stop()
		pygame.mixer.music.pause()
		pygame.quit()

