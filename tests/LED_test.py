#!/usr/bin/python3

# LED Test
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED = 13
GPIO.setup(LED, GPIO.OUT)
try:
  print("LED is now flashing..")
  print("Exit with CTRL+C")
  while True:
    GPIO.output(LED,1)
    time.sleep(0.5)
    GPIO.output(LED,0)
    time.sleep(0.5)
except KeyboardInterrupt:
  GPIO.cleanup()
  print(" Bye Bye")
