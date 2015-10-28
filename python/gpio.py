import RPi.GPIO as GPIO
import time

class PINS:

# WC1 
	WC1_LED_RED = 2
	WC1_LED_GREEN = 3
	WC1_DOOR_sensor = 10
	WC1_PIR = 9

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
		GPIO.setup(self.WC1_LED_GREEN, GPIO.OUT)
		GPIO.setup(self.WC1_DOOR_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.WC1_PIR, GPIO.IN)
		# Relay Board
		#GPIO.setup(self.RELAY, GPIO.OUT)

		# WC2
		GPIO.setup(self.WC2_LED_RED, GPIO.OUT)
		GPIO.setup(self.WC2_LED_GREEN, GPIO.OUT)
	
		# URINAL
		GPIO.setup(self.URINAL_LED_RED, GPIO.OUT)
		GPIO.setup(self.URINAL_LED_GREEN, GPIO.OUT)
		GPIO.setup(self.URINAL_TRIG, GPIO.OUT)
		GPIO.setup(self.URINAL_ECHO, GPIO.IN)
		
	def wc1_led_occupied(self):
		#toilet occupied
		print 'WC1 - LED Red'
		GPIO.output(self.WC1_LED_RED, GPIO.HIGH)
		GPIO.output(self.WC1_LED_GREEN, GPIO.LOW)

	def wc1_led_free(self):
		#toilet free
		print 'WC1 - LED Green'
		GPIO.output(self.WC1_LED_RED, GPIO.LOW)
		GPIO.output(self.WC1_LED_GREEN, GPIO.HIGH)

	def wc2_led_occupied(self):
		#toilet occupied
		print 'WC2 - LED Red'
		GPIO.output(self.WC2_LED_RED, GPIO.HIGH)
		GPIO.output(self.WC2_LED_GREEN, GPIO.LOW)

	def wc2_led_free(self):
		#toilet free
		print 'WC2 - LED Green'
		GPIO.output(self.WC2_LED_RED, GPIO.LOW)
		GPIO.output(self.WC2_LED_GREEN, GPIO.HIGH)

	def urinal_led_occupied(self):
		#toilet occupied
		print 'Urinal - LED Red'
		GPIO.output(self.URINAL_LED_RED, GPIO.HIGH)
		GPIO.output(self.URINAL_LED_GREEN, GPIO.LOW)

	def urinal_led_free(self):
		#toilet free
		print 'Urinal - LED Green'
		GPIO.output(self.URINAL_LED_RED, GPIO.LOW)
		GPIO.output(self.URINAL_LED_GREEN, GPIO.HIGH)

	def is_wc1_door_closed(self):
		#detect if wc1's door are closed
		if GPIO.input(self.DOOR_WC1_sensor) != 1:
			print '[True] Door WC1 closed: ', GPIO.input(self.DOOR_WC1_sensor)
			return True
		else:
			print '[False] Door WC1 open: ', GPIO.input(self.DOOR_WC1_sensor)
			return False

	def is_wc1_motion_detected(self):
		if GPIO.input(self.WC1_PIR) == 1:
			print 'Move Detected: ',GPIO.input(self.WC1_PIR)
			return True
		else:
			print '# clean: ', GPIO.input(self.WC1_PIR)
			return False

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
		print 'Distance: ', distance

