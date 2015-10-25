import RPi.GPIO as GPIO
import time

class PINS:

	WC1_LED_RED = 2
	WC1_LED_GREEN = 3
	DOOR_WC1_sensor = 26
	PIR = 19
	TRIG = 20
	ECHO = 21
	RELAY = 16

	WC2_LED_RED = 10
	WC2_LED_GREEN = 17

	URINAL_LED_RED = 27
	URINAL_LED_GREEN = 22


	def __init__(self):

		GPIO.cleanup()
		print 'run constructor'
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		# WC1 
		GPIO.setup(self.WC1_LED_RED, GPIO.OUT)
		GPIO.setup(self.WC1_LED_GREEN, GPIO.OUT)

		# WC2
		GPIO.setup(self.WC2_LED_RED, GPIO.OUT)
		GPIO.setup(self.WC2_LED_GREEN, GPIO.OUT)
	
		# URINAL
		GPIO.setup(self.URINAL_LED_RED, GPIO.OUT)
		GPIO.setup(self.URINAL_LED_GREEN, GPIO.OUT)
		
		#PIR
		GPIO.setup(self.PIR, GPIO.IN)

		# DOOR WC1 Sensor
		GPIO.setup(self.DOOR_WC1_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		# Relay Board
		GPIO.setup(self.RELAY, GPIO.OUT)
		print 'Constructor end'
		
		#Czujnik odlegosci
		GPIO.setup(self.TRIG, GPIO.OUT)#TRIG
		GPIO.setup(self.ECHO, GPIO.IN)#ECHO	

	def odleglosc(self):
		GPIO.output(self.TRIG, False)
		time.sleep(2)
		GPIO.output(self.TRIG, True)
		time.sleep(0.00001)
		GPIO.output(self.TRIG, False)

		while GPIO.input(self.ECHO) == 0:
			pulse_start = time.time()

		while GPIO.input(self.ECHO) == 1:
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance, 2)
		
		print 'Distance: ', distance
		
		
		
		
	def is_motion_detected(self):
		if GPIO.input(self.PIR):
			print 'Move Detected'
			# return True
		else:
			print '# clean'
			# return False

	def is_doorWC1_closed(self):
		if GPIO.input(self.DOOR_WC1_sensor) != 1:
			print '[True] Door WC1 closed: ', GPIO.input(self.DOOR_WC1_sensor)
		else:
			print '[False] Door WC1 open: ', GPIO.input(self.DOOR_WC1_sensor)

	def test(self):
		print 'LOW'
		GPIO.output(self.RELAY, GPIO.LOW)
		time.sleep(5)
		print 'HIGH'
		GPIO.output(self.RELAY, GPIO.HIGH)
		time.sleep(5)
		print 'LOW'
		GPIO.output(self.RELAY, GPIO.LOW)
		time.sleep(5)
		print 'HIGH'
		GPIO.output(self.RELAY, GPIO.HIGH)
		time.sleep(2)
		print 'LOW'
		GPIO.output(self.RELAY, GPIO.LOW)
		time.sleep(2)
		print 'HIGH'
		GPIO.output(self.RELAY, GPIO.HIGH)


	def WC1LedOccupied(self):
		#toilet occupied
		print 'WC1 - LED Red'
		GPIO.output(self.WC1_LED_RED, GPIO.HIGH)
		GPIO.output(self.WC1_LED_GREEN, GPIO.LOW)

	def WC1LedFree(self):
		#toilet free
		print 'WC1 - LED Green'
		GPIO.output(self.WC1_LED_RED, GPIO.LOW)
		GPIO.output(self.WC1_LED_GREEN, GPIO.HIGH)

	def WC2LedOccupied(self):
		#toilet occupied
		print 'WC2 - LED Red'
		GPIO.output(self.WC2_LED_RED, GPIO.HIGH)
		GPIO.output(self.WC2_LED_GREEN, GPIO.LOW)

	def WC2LedFree(self):
		#toilet free
		print 'WC2 - LED Green'
		GPIO.output(self.WC2_LED_RED, GPIO.LOW)
		GPIO.output(self.WC2_LED_GREEN, GPIO.HIGH)

	def UrinalLedOccupied(self):
		#toilet occupied
		print 'Urinal - LED Red'
		GPIO.output(self.URINAL_LED_RED, GPIO.HIGH)
		GPIO.output(self.URINAL_LED_GREEN, GPIO.LOW)

	def UrinalLedFree(self):
		#toilet free
		print 'Urinal - LED Green'
		GPIO.output(self.URINAL_LED_RED, GPIO.LOW)
		GPIO.output(self.URINAL_LED_GREEN, GPIO.HIGH)


	def isDoorWc2Closed(self):
		return True
	def isMoveDetectedInWc2(self):
		return True

	def turnOnLedWc1(self):
		print 'LED in WC1 is turned on'

	def turnOffLedWc1(self):
		print 'LED in WC1 is turned off'

	def turnOnLedWc2(self):
		print 'LED in WC2 is turned on'
		
	def turnOffLedWc2(self):
		print 'LED in WC2 is turned off'

	def turnOnLedUrinal(self):
		print 'LED in Urinal is turned on'
		
	def turnOffLedUrinal(self):
		print 'LED in Urinal is turned off'

	def turnOnFun(self):
		print 'Fun in wc1 is turned on'

	def turnOffFun(self):
		print 'Fun in wc1 is turned off'

	def getDistance(self):
		return 40


# Test 
g = PINS()

g.WC1LedOccupied()
g.WC2LedOccupied()
g.UrinalLedOccupied()
time.sleep(3)
g.WC1LedFree()
g.WC2LedFree()
g.UrinalLedFree()
time.sleep(3)
g.WC1LedOccupied()
g.WC2LedOccupied()
g.UrinalLedOccupied()
time.sleep(3)
g.WC1LedFree()
g.WC2LedFree()
g.UrinalLedFree()
