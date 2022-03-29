#!/usr/bin/python3

# Button Test
import RPi.GPIO as GPIO
import time
switch = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
def callback_function(switch):
    print("_______event________")

try:
    print("Push the button..")
    print("Exit with CTRL+C")
    GPIO.add_event_detect(switch, GPIO.RISING, callback=callback_function, bouncetime=300)
    while True:
        print("_______#____________")
        time.sleep(1)
        print("_________#__________")
        time.sleep(1)
        print("___________#________")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.remove_event_detect(switch)
    GPIO.cleanup()
    print(" Bye Bye")
