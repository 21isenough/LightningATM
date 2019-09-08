#!/usr/bin/python3

import os
import sys
import time

import lightning

import display
import qr

import RPi.GPIO as GPIO

from PIL import Image, ImageFont, ImageDraw
# from time import sleep
from utils import *
from config import *

## Check EPD_SIZE is defined
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    exec(open('/etc/default/epd-fuse').read())
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

## Set sat, fiat, currency value
CURRENCY = 'EUR'
FIAT = 0
SATS = 0
INVOICE = ''

## Set btc and sat price
BTCPRICE = getbtcprice(CURRENCY)
SATPRICE = round((1 / (BTCPRICE * 100)) * 100000000, 2)

## Button / Acceptor Pulses
LASTIMPULSE = 0
PULSES = 0
LASTPUSHES = 0
PUSHES = 0

def main():
    global FIAT
    global SATS
    global PULSES
    global PUSHES
    global INVOICE

    ## Display startup startup_screen
    display.update_startup_screen()

    ## Defining GPIO BCM Mode
    GPIO.setmode(GPIO.BCM)

    ## Setup GPIO Pins for coin acceptor and button
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(6,GPIO.IN, pull_up_down=GPIO.PUD_UP)

    ## Setup coin interrupt channel (bouncetime for switch bounce)
    GPIO.add_event_detect(5, GPIO.RISING,callback=buttonevent, bouncetime=200)
    GPIO.add_event_detect(6,GPIO.FALLING,callback=coinevent)

    while True:
        time.sleep(0.5)
        ## Detect when coins are being inserted
        if((time.time() - LASTIMPULSE > 0.5) and (PULSES > 0)):
            if (PULSES == 1):
                FIAT += 0.02
                SATS = FIAT * 100 * SATPRICE
                update_amount_screen(PAPIRUS)
            if (PULSES == 2):
                FIAT += 0.05
                SATS = FIAT * 100 * SATPRICE
                update_amount_screen(PAPIRUS)
            if (PULSES == 3):
                FIAT += 0.1
                SATS = FIAT * 100 * SATPRICE
                update_amount_screen(PAPIRUS)
            if (PULSES == 4):
                FIAT += 0.2
                SATS = FIAT * 100 * SATPRICE
                update_amount_screen(PAPIRUS)
            if (PULSES == 5):
                FIAT += 0.5
                SATS = FIAT * 100 * SATPRICE
                update_amount_screen(PAPIRUS)
            PULSES = 0

        ## Detect if the buttons has been pushed
        if((time.time() - LASTPUSHES > 0.5) and (PUSHES > 0)):
            if (PUSHES == 1):
                display.update_qr_request()
                INVOICE = qr.scan()
                update_payout_screen(PAPIRUS)
            if (PUSHES == 2):
                FIAT += 0.05
                SATS = FIAT * 100 * SATPRICE
                update_amount_screen(PAPIRUS)
            if (PUSHES == 3):
                os.execv('/home/pi/LightningATM/app.py', [''])
                GPIO.cleanup()
            PUSHES = 0


def buttonevent(channel):
    global LASTPUSHES
    global PUSHES
    LASTPUSHES = time.time()
    PUSHES = PUSHES + 1
    print(PUSHES)

def coinevent(channel):
    global LASTIMPULSE
    global PULSES
    LASTIMPULSE = time.time()
    PULSES = PULSES + 1

def update_amount_screen(papirus):

    ## initially set all white background
    image = Image.new('1', PAPIRUS.size, WHITE)

    ## Set width and heigt of screen
    width, height = image.size

    ## prepare for drawing
    draw = ImageDraw.Draw(image)

    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((13, 10), str(round(SATS)) + ' sats', fill=BLACK, font=createfont('freemono',28))
    draw.text((11, 37), '(' + '%.2f' % round(FIAT,2) + ' ' + CURRENCY + ')', fill=BLACK, font=createfont('freemono',20))
    draw.text((13, 70), '(1 cent = ' + str(SATPRICE) + ' sats)', fill=BLACK, font=createfont('freemono',14))

    PAPIRUS.display(image)
    PAPIRUS.partial_update()

def update_payout_screen(papirus):

    # global INVOICE

    ## initially set all white background
    image = Image.new('1', PAPIRUS.size, WHITE)

    ## Set width and heigt of screen
    width, height = image.size

    ## prepare for drawing
    draw = ImageDraw.Draw(image)


    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((15, 30), str(round(SATS)) + ' sats' , fill=BLACK, font=createfont('freemono',20))
    draw.text((15, 50), 'on the way!' , fill=BLACK, font=createfont('freemono',15))

    PAPIRUS.display(image)
    PAPIRUS.update()

    # INVOICE = qr.scan()

    decodreq = lightning.decoderequest(INVOICE)

    print(decodreq,round(SATS))

    if (decodreq == str(round(SATS))) or (decodreq == True):
            lightning.payout(SATS, INVOICE)

            result = lightning.lastpayment(INVOICE)

            draw.text((15, 70), str(result), fill=BLACK, font=createfont('freemono',15))

            PAPIRUS.display(image)
            PAPIRUS.partial_update()
            time.sleep(1)

            display.update_thankyou_screen()
            #os.execl(os.path.expanduser('~/LightningATM/app.py'), *sys.argv)
            os.execv('/home/pi/LightningATM/app.py', [''])
    else:
        print('Please show correct invoice')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('interrupted')
        GPIO.cleanup()
