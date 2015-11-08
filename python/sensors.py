import RPi.GPIO as GPIO
import time
import logging 

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

class Sensors:

# WC1 
	WC1_LED_RED = 2
	WC1_LED_GREEN = 3
	WC1_DOOR_sensor = 10
	WC1_PIR = 9
	WC1_FUN = 5

# WC2
	WC2_LED_RED = 4
	WC2_LED_GREEN = 17

# URINAL
	URINAL_LED_RED = 27
	URINAL_LED_GREEN = 22
	URINAL_TRIG = 11
	URINAL_ECHO = 0

	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		# WC1 
		GPIO.setup(self.WC1_LED_RED, GPIO.OUT)
		GPIO.output(self.WC1_LED_RED, GPIO.LOW)
		GPIO.setup(self.WC1_LED_GREEN, GPIO.OUT)
		GPIO.output(self.WC1_LED_GREEN, GPIO.HIGH)
		GPIO.setup(self.WC1_DOOR_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.WC1_PIR, GPIO.IN)
		GPIO.setup(self.WC1_FUN, GPIO.OUT)

		# WC2
		GPIO.setup(self.WC2_LED_RED, GPIO.OUT)
		GPIO.output(self.WC2_LED_RED, GPIO.LOW)
		GPIO.setup(self.WC2_LED_GREEN, GPIO.OUT)
		GPIO.output(self.WC2_LED_GREEN, GPIO.HIGH)
	
		# URINAL
		GPIO.setup(self.URINAL_LED_RED, GPIO.OUT)
		GPIO.output(self.URINAL_LED_RED, GPIO.LOW)
		GPIO.setup(self.URINAL_LED_GREEN, GPIO.OUT)
		GPIO.output(self.URINAL_LED_GREEN, GPIO.HIGH)
		GPIO.setup(self.URINAL_TRIG, GPIO.OUT)
		GPIO.setup(self.URINAL_ECHO, GPIO.IN)
		print 'sensors constructor end'
		
	def wc1_led_occupied(self):
		#toilet occupied
		logging.debug('WC1 - LED Red')
		GPIO.output(self.WC1_LED_RED, GPIO.HIGH)
		GPIO.output(self.WC1_LED_GREEN, GPIO.LOW)

	def wc1_led_free(self):
		#toilet free
		logging.debug('WC1 - LED Green')
		GPIO.output(self.WC1_LED_RED, GPIO.LOW)
		GPIO.output(self.WC1_LED_GREEN, GPIO.HIGH)

	def wc1_fun_on(self):
		logging.debug('turn on fun in wc1')
		GPIO.output(self.WC1_FUN, GPIO.HIGH)

	def wc1_fun_off(self):
		logging.debug('turn off fun in wc1')
		GPIO.output(self.WC1_FUN, GPIO.LOW)

	def is_wc1_door_closed(self):
		#detect if wc1's door is closed
		if GPIO.input(self.WC1_DOOR_sensor) != 1:
			#logging.debug('[True] Door WC1 closed: %s', GPIO.input(self.WC1_DOOR_sensor))
			return True
		else:
			#logging.debug('[False] Door WC1 open: %s', GPIO.input(self.WC1_DOOR_sensor))
			return False

	def is_wc1_motion_detected(self):
		if GPIO.input(self.WC1_PIR) == 1:
			#logging.debug('Move Detected: %s',GPIO.input(self.WC1_PIR))
			return True
		else:
			#logging.debug('# clean: %s', GPIO.input(self.WC1_PIR))
			return False

	def wc2_led_occupied(self):
		#toilet occupied
		logging.debug('WC2 - LED Red')
		GPIO.output(self.WC2_LED_RED, GPIO.HIGH)
		GPIO.output(self.WC2_LED_GREEN, GPIO.LOW)

	def wc2_led_free(self):
		#toilet free
		logging.debug('WC2 - LED Green')
		GPIO.output(self.WC2_LED_RED, GPIO.LOW)
		GPIO.output(self.WC2_LED_GREEN, GPIO.HIGH)

	def wc2_fun_on(self):
		logging.debug('turn on fun in wc2')
		# add implementation here 

	def wc2_fun_off(self):
		logging.debug('turn off fun in wc2')
		# add implementation here 

	def is_wc2_door_closed(self):
		#detect if wc2's door is closed
		# to be implemented
		return False

	def is_wc2_motion_detected(self):
		#detect if there is move in wc2
		# to be implemented
		return False

	def urinal_led_occupied(self):
		#toilet occupied
		logging.debug('Urinal - LED Red')
		GPIO.output(self.URINAL_LED_RED, GPIO.HIGH)
		GPIO.output(self.URINAL_LED_GREEN, GPIO.LOW)

	def urinal_led_free(self):
		#toilet free
		logging.debug('Urinal - LED Green')
		GPIO.output(self.URINAL_LED_RED, GPIO.LOW)
		GPIO.output(self.URINAL_LED_GREEN, GPIO.HIGH)

	def get_distance(self):
		GPIO.output(self.URINAL_TRIG, False)
		time.sleep(0.3)
		GPIO.output(self.URINAL_TRIG, True)
		time.sleep(0.00001)
		GPIO.output(self.URINAL_TRIG, False)

		while GPIO.input(self.URINAL_ECHO) == 0:
			pulse_start = time.time()

		while GPIO.input(self.URINAL_ECHO) == 1:
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance, 2)
		return distance

		
