#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import string
from papirus import Papirus
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import sleep
import RPi.GPIO as GPIO

# Check EPD_SIZE is defined
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    exec(open('/etc/default/epd-fuse').read())
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

# set sat and fiat value to 0
FIAT = 0
SATS = 0

# Command line usage
# papirus-buttons

hatdir = '/proc/device-tree/hat'

WHITE = 1
BLACK = 0

SIZE = 27

# Assume Papirus Zero
SW1 = 21
SW2 = 16
SW3 = 20
SW4 = 19
SW5 = 26

# Check for HAT, and if detected redefine SW1 .. SW5
if (os.path.exists(hatdir + '/product')) and (os.path.exists(hatdir + '/vendor')) :
   with open(hatdir + '/product') as f :
      prod = f.read()
   with open(hatdir + '/vendor') as f :
      vend = f.read()
   if (prod.find('PaPiRus ePaper HAT') == 0) and (vend.find('Pi Supply') == 0) :
       # Papirus HAT detected
       SW1 = 16
       SW2 = 26
       SW3 = 20
       SW4 = 21
       SW5 = -1

def main(argv):
    global SIZE
    global FIAT
    global SATS

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(SW1, GPIO.IN)
    GPIO.setup(SW2, GPIO.IN)
    GPIO.setup(SW3, GPIO.IN)
    GPIO.setup(SW4, GPIO.IN)
    GPIO.setup(SW5, GPIO.IN)

    papirus = Papirus(rotation = int(argv[0]) if len(sys.argv) > 1 else 0)


    # Use smaller font for smaller displays
    if papirus.height <= 96:
        SIZE = 18

    papirus.clear()

#    update_screen(papirus, "Ready... SW1 + SW2 to exit.", SIZE)

    while True:

        # Exit when SW1 and SW2 are pressed simultaneously
        if (GPIO.input(SW1) == False) and (GPIO.input(SW2) == False) :
            update_screen(papirus, "Exiting ...", SIZE)
            sleep(0.2)
            papirus.clear()
            sys.exit()

        if GPIO.input(SW1) == False:
            FIAT += 0.01
            SATS = FIAT * 100 * 110
            update_screen(papirus, SIZE)

        if GPIO.input(SW2) == False:
            FIAT += 0.02
            SATS = FIAT * 100 * 110
            update_screen(papirus, SIZE)

        if GPIO.input(SW3) == False:
            FIAT += 0.05
            SATS = FIAT * 100 * 110
            update_screen(papirus, SIZE)

        if GPIO.input(SW4) == False:
            FIAT += 0.1
            SATS = FIAT * 100 * 110
            update_screen(papirus, SIZE)

        if (GPIO.input(SW5) == False):
            FIAT += 0.2
            SATS = FIAT * 100 * 110
            update_screen(papirus, SIZE)

        sleep(0.1)

def update_screen(papirus, size):

    # initially set all white background
    image = Image.new('1', papirus.size, WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)

    # set font sizes
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', size)
    font1 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 14)

    width, height = image.size

#    fiat = 0.2
    price = '1 cent = 110 sats'



    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((30, 10), str(SATS) + ' sats', fill=BLACK, font=font)
    draw.text((30, 30), '(' + str(FIAT) + ' EUR)', fill=BLACK, font=font)
    draw.text((30, 70), price, fill=BLACK, font=font1)

    papirus.display(image)
    papirus.partial_update()

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
