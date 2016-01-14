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
	WC2_DOOR_sensor = 13
	WC2_PIR = 6
	WC2_FUN = 19


# URINAL
	URINAL_LED_BLUE = 27
	URINAL_TRIG = 11
	URINAL_ECHO = 0

	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		# WC1 
		GPIO.setup(self.WC1_LED_RED, GPIO.OUT)
		GPIO.output(self.WC1_LED_RED, GPIO.HIGH) 
		GPIO.setup(self.WC1_LED_GREEN, GPIO.OUT)
		GPIO.output(self.WC1_LED_GREEN, GPIO.HIGH)
		GPIO.setup(self.WC1_DOOR_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.WC1_PIR, GPIO.IN)
		GPIO.setup(self.WC1_FUN, GPIO.OUT)
		GPIO.output(self.WC1_FUN, GPIO.HIGH)

		# WC2
		GPIO.setup(self.WC2_LED_RED, GPIO.OUT)
		GPIO.output(self.WC2_LED_RED, GPIO.HIGH)
		GPIO.setup(self.WC2_LED_GREEN, GPIO.OUT)
		GPIO.output(self.WC2_LED_GREEN, GPIO.HIGH)
		GPIO.setup(self.WC2_DOOR_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.WC2_PIR, GPIO.IN)
		GPIO.setup(self.WC2_FUN, GPIO.OUT)
		GPIO.output(self.WC2_FUN, GPIO.HIGH)

		# URINAL
		GPIO.setup(self.URINAL_LED_BLUE, GPIO.OUT)
		GPIO.output(self.URINAL_LED_BLUE, GPIO.HIGH)
		GPIO.setup(self.URINAL_TRIG, GPIO.OUT)
		GPIO.output(self.URINAL_TRIG, False)
		GPIO.setup(self.URINAL_ECHO, GPIO.IN)
		logging.debug('sensors constructor end')
	
	################################### WC1	
	def wc1_led_occupied(self):
		#toilet occupied
		#logging.debug('WC1 - LED Red')
		logging.debug('WC1 - turn off LED Green')
		GPIO.output(self.WC1_LED_GREEN, GPIO.HIGH)
		#GPIO.output(self.WC1_LED_RED, GPIO.LOW)

	def wc1_led_free(self):
		#toilet free
		logging.debug('WC1 - turn on LED Green')
		#GPIO.output(self.WC1_LED_RED, GPIO.HIGH)
		GPIO.output(self.WC1_LED_GREEN, GPIO.LOW)

	def wc1_fun_on(self):
		logging.debug('turn on FUN in WC1')
		GPIO.output(self.WC1_FUN, GPIO.LOW)

	def wc1_fun_off(self):
		logging.debug('turn off FUN in WC1')
		GPIO.output(self.WC1_FUN, GPIO.HIGH)

	def is_wc1_door_closed(self):
		#detect if wc1's door is closed
		if GPIO.input(self.WC1_DOOR_sensor) == 0:
			return True
		else:
			return False

	def is_wc1_motion_detected(self):
		#detect if there is move in wc2
		if GPIO.input(self.WC1_PIR) == 1:
			return True
		else:
			return False

	################################### WC2
	def wc2_led_occupied(self):
		#toilet occupied
		logging.debug('WC2 - LED Red')
		GPIO.output(self.WC2_LED_GREEN, GPIO.HIGH)
		#GPIO.output(self.WC2_LED_RED, GPIO.LOW)

	def wc2_led_free(self):
		#toilet free
		logging.debug('WC2 - LED Green')
		#GPIO.output(self.WC2_LED_RED, GPIO.HIGH)
		GPIO.output(self.WC2_LED_GREEN, GPIO.LOW)

	def wc2_fun_on(self):
		logging.debug('turn on FUN in WC2')
		GPIO.output(self.WC2_FUN, GPIO.LOW)

	def wc2_fun_off(self):
		logging.debug('turn off FUN in WC1')
		GPIO.output(self.WC1_FUN, GPIO.HIGH)

	def is_wc2_door_closed(self):
		#detect if wc1's door is closed
		if GPIO.input(self.WC2_DOOR_sensor) == 0:
			return True
		else:
			return False

	def is_wc2_motion_detected(self):
		#detect if there is move in wc2
		if GPIO.input(self.WC2_PIR) == 1:
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

	def urinal_get_distance(self):

		time.sleep(0.3)

		GPIO.output(self.URINAL_TRIG, True)
		time.sleep(0.00001)
		GPIO.output(self.URINAL_TRIG, False)

		while GPIO.input(self.URINAL_ECHO) == 0:
			pass
		pulse_start = time.time()

		while GPIO.input(self.URINAL_ECHO) == 1:
			pass
		pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17000
		distance = round(distance, 2)

		if distance >= 2 and distance <= 400:
			return distance
		else:
			return -1
		
