import RPi.GPIO as GPIO
import time

# INIT VARIABLES
lastImpulse = 0
pulses = 0


def main():
    global pulses

    ## We're using BCM Mode
    GPIO.setmode(GPIO.BCM)

    ## Setup coin interrupt channel
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(PIN_COIN_INTERRUPT,GPIO.IN)
    GPIO.add_event_detect(6, GPIO.FALLING, callback=coinEventHandler)

    while True:
        time.sleep(0.5)
        if (time.time() - lastImpulse > 0.5) and (pulses > 0):
            if pulses == 1:
                print("Coin 1")
            pulses = 0

    GPIO.cleanup()


# handle the coin event
def coinEventHandler(channel):
    global lastImpulse
    global pulses
    lastImpulse = time.time()
    pulses = pulses + 1


if __name__ == "__main__":
    main()
