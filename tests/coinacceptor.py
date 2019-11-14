import RPi.GPIO as GPIO
import time
from threading import Thread

# GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

global count
global counting

counting = 0


def firstFunction():
    global counter
    global ts
    global counting
    count = 1
    counter = 0
    ts = time.time()
    while True:
        if count == 1:
            GPIO.wait_for_edge(6, GPIO.FALLING)
            counting = 1
            counter += 1
            print(f"Pulse comming ! {counter}")
            ts = time.time()


def secondFunction():
    global count
    global counting
    global counter
    while True:
        cts = ts + 2
        if cts < time.time():
            print(f"Counting looks like finished with {counter} pulses")
            count = 0
            counting = 0
            print("We process accepted the coins")

            # urllib2.urlopen is just for testing in my case, you can do whatever you want here, i just used this to test the functions
            if counter == 1:
                print("Counter 1")
            if counter == 2:
                print("Counter 2")
            if counter == 3:
                print("Counter 3")
            if counter == 4:
                print("Counter 4")
            if counter == 5:
                print("Counter 5")

            counter = 0
            count = 1
            print("Ready for the next coin")
            time.sleep(1)


def thirdFunction():
    while True:
        if counting == 0:
            global ts
            ts = time.time()
            time.sleep(1)


try:
    t1 = Thread(target=firstFunction)
    t2 = Thread(target=secondFunction)
    t3 = Thread(target=thirdFunction)

    t1.start()
    t2.start()
    t3.start()

except KeyboardInterrupt:
    t1.stop()
    t2.stop()
    t3.stop()
    GPIO.cleanup()
