#!/usr/bin/python3

# Relay Test - Toggles every 2 seconds
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
relay = 12
GPIO.setup(relay, GPIO.OUT)
try:
  print("The relay now toggles every 2 seconds")
  print("Exit with CTRL+C")
  while True:
    GPIO.output(relay,1)
    time.sleep(2.0)
    GPIO.output(relay,0)
    time.sleep(2.0)
except KeyboardInterrupt:
  GPIO.cleanup()
  print(" Bye Bye")
