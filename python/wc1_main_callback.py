


















######### Urinal Worker #########
# Urinal event callback
GPIO.add_event_detect(gpio.URINAL_DISTANCE_sensor, GPIO.FALLING, callback=urinal_callback)

# Main Loop of the program
while True:
        time.sleep(1)
        pass