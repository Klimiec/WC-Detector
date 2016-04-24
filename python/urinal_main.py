
import threading
import time
import logging
from sensors import Sensors
import RPi.GPIO as GPIO

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

# Global
gpio = Sensors()
lock = threading.Lock()

detection_counter = 0
usage_counter = 0

######### Urinal Worker #########

def urinal_callback(channel):
        global lock
        global detection_counter
        global usage_counter

        logging.debug('Urinal, start new thread, time:  %s ',time.time())
        with lock:
                 detection_counter += 1
                 detection_time = time.time()
                 logging.debug('@URINAL Person detected, detection counter:  %s, detection time: %s', detection_counter, detection_time)
                 time.sleep(0.7)

                 if gpio.is_urinal_person_presence_detected():
                        # Urinal occupied
                        gpio.urinal_led_occupied()
                        gpio.urinal_turn_on_music()
                        # SEND REST
                        usage_counter += 1
                        while True:
                                time.sleep(0.5)
                                if not gpio.is_urinal_person_presence_detected():
                                        # Urinal is free occupied
                                        urinal_free_time = time.time()
                                        usage_time = round(urinal_free_time-detection_time, 2)

                                        logging.debug('@URINAL total usage time: %s ', usage_time)
                                        logging.debug('------------------------------------- Usage counter:  %s \n\n', usage_counter)

                                        gpio.urinal_led_free()
                                        # SEND REST
                                        time.sleep(3)
                                        gpio.urinal_turn_off_music()
                                        break;



######### Urinal Worker #########
# Urinal event callback
GPIO.add_event_detect(gpio.URINAL_DISTANCE_sensor, GPIO.FALLING, callback=urinal_callback)

# Main Loop of the program
while True:
        time.sleep(1)
        pass