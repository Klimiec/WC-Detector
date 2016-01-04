
import RPi.GPIO as GPIO
import time

# WC1 
WC2_DOOR_sensor = 13
WC2_PIR = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(WC2_DOOR_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(WC2_PIR, GPIO.IN)

while GPIO.input(WC2_DOOR_sensor) == 1:
	pass
start_time = time.time()

while GPIO.input(PIR_WC2) == 1:
	pass
end_time = time.time()

result_time = end_time - start_time
result_time = round(result_time, 2)

print "Time: ", result_time