
import RPi.GPIO as GPIO
import time
import logging 
import threading 

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

PIR_WC1 = 9
lock = threading.Lock()
detect_time = time.time()


GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_WC1, GPIO.IN)

def move_callback(channel):  
	global detect_time
	if GPIO.input(channel):
		logging.debug('@WC1 Move detected (0->1) time:  %s  czas trwania CLEAN: %s', round(time.time(), 2), round(time.time() - detect_time , 2))
		detect_time = time.time()
	else: 
		logging.debug('@WC1 Clean (1->0) time:  %s  czas trwania MOVE: %s', round(time.time(), 2),round(time.time() - detect_time , 2))
		detect_time = time.time()


GPIO.add_event_detect(PIR_WC1, GPIO.BOTH, callback=move_callback)  



# Main Loop
while True:
	pass