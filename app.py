#!/usr/bin/python3

## Import python libraries
import RPi.GPIO as GPIO
import os, sys, time, logging
from PIL import Image, ImageFont, ImageDraw

## Import own modules
import lightning, display, qr

## Import utils.py and config.py
from utils import *
from config import *

## Check EPD_SIZE is defined
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    exec(open('/etc/default/epd-fuse').read())
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

## Set sat, fiat
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

    ## Initiating logging instance
    logging.basicConfig(filename='/home/pi/LightningATM/resources/debug.log',
                            format='%(asctime)s %(name)s %(levelname)s %(message)s',
                            datefmt='%Y/%m/%d %I:%M:%S %p',
                            level=logging.INFO)

    logging.info('Application started')

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
        time.sleep(0.2)
        ## Detect when coins are being inserted
        if((time.time() - LASTIMPULSE > 0.5) and (PULSES > 0)):
            if (PULSES == 2):
                FIAT += 0.02
                SATS = FIAT * 100 * SATPRICE
                logging.info('2 cents added')
                update_amount_screen(PAPIRUS)
            if (PULSES == 3):
                FIAT += 0.05
                SATS = FIAT * 100 * SATPRICE
                logging.info('5 cents added')
                update_amount_screen(PAPIRUS)
            if (PULSES == 4):
                FIAT += 0.1
                SATS = FIAT * 100 * SATPRICE
                logging.info('10 cents added')
                update_amount_screen(PAPIRUS)
            if (PULSES == 5):
                FIAT += 0.2
                SATS = FIAT * 100 * SATPRICE
                logging.info('20 cents added')
                update_amount_screen(PAPIRUS)
            if (PULSES == 6):
                FIAT += 0.5
                SATS = FIAT * 100 * SATPRICE
                logging.info('50 cents added')
                update_amount_screen(PAPIRUS)
            if (PULSES == 7):
                FIAT += 1
                SATS = FIAT * 100 * SATPRICE
                logging.info('100 cents added')
                update_amount_screen(PAPIRUS)
            PULSES = 0

        ## Detect if the buttons has been pushed
        if((time.time() - LASTPUSHES > 0.5) and (PUSHES > 0)):
            if (PUSHES == 1):
                if FIAT == 0:
                    display.update_nocoin_screen()
                    time.sleep(3)
                    display.update_startup_screen()
                else:
                    display.update_qr_request()
                    INVOICE = qr.scan()
                    while INVOICE == False:
                        display.update_qr_failed()
                        time.sleep(1)
                        display.update_qr_request()
                        INVOICE = qr.scan()
                    update_payout_screen(PAPIRUS)

            if (PUSHES == 2):
                logging.info('Button pushed twice (add coin)')
                print('Button pushed twice (add coin)')
                PULSES = 2

            if (PUSHES == 3):
                logging.warning('Button pushed three times (restart)')
                print('Button pushed three times (restart)')
                os.execv('/home/pi/LightningATM/app.py', [''])
                GPIO.cleanup()

            if (PUSHES == 4):
                display.update_shutdown_screen()
                GPIO.cleanup()
                logging.info('ATM shutdown (4 times button)')
                os.system('sudo shutdown -h now')
            PUSHES = 0

def buttonevent(channel):
    global LASTPUSHES
    global PUSHES
    LASTPUSHES = time.time()
    PUSHES = PUSHES + 1

def coinevent(channel):
    global LASTIMPULSE
    global PULSES
    LASTIMPULSE = time.time()
    PULSES = PULSES + 1
    print(PULSES)

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
    draw.text((11, 70), '(1 cent = ' + str(SATPRICE) + ' sats)', fill=BLACK, font=createfont('freemono',14))

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

            if result == 'Success':
                display.update_thankyou_screen()
            else:
                display.update_payment_failed()
                time.sleep(120)

            #os.execl(os.path.expanduser('~/LightningATM/app.py'), *sys.argv)
            os.execv('/home/pi/LightningATM/app.py', [''])
    else:
        print('Please show correct invoice')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        display.update_shutdown_screen()
        GPIO.cleanup()
        logging.info('Application finished (Keyboard Interrupt)')
        sys.exit('Manually Interrupted')
