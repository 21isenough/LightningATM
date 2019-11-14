import os
import sys

import RPi.GPIO as GPIO

from PIL import Image
from time import sleep
from PIL import ImageDraw
from PIL import ImageFont
from papirus import Papirus

# Check EPD_SIZE is defined
EPD_SIZE = 0.0
if os.path.exists("/etc/default/epd-fuse"):
    exec(open("/etc/default/epd-fuse").read())
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

# set sat,fiat, currency value
CURRENCY = "EUR"
FIAT = 0
SATS = 0

WHITE = 1
BLACK = 0
SIZE = 27

# Assign GPIO pins for PaPiRus Zero
SW1 = 21
SW2 = 16
SW3 = 20
SW4 = 19
SW5 = 26


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

    papirus = Papirus(rotation=int(argv[0]) if len(sys.argv) > 1 else 0)

    # Use smaller font for smaller displays
    if papirus.height <= 96:
        SIZE = 18

    papirus.clear()

    while True:

        if GPIO.input(SW1) == False:
            update_img_screen(papirus)

        if GPIO.input(SW2) == False:
            pass

        if GPIO.input(SW3) == False:
            pass

        if GPIO.input(SW4) == False:
            pass

        if GPIO.input(SW5) == False:
            pass

        sleep(0.1)


def update_img_screen(papirus):
    image = Image.new("1", papirus.size, WHITE)
    papirus.display("~/LightningATM/resources/startup.png")
    # papirus.display(image)
    papirus.update()


def update_amount_screen(papirus, size):
    # initially set all white background
    image = Image.new("1", papirus.size, WHITE)

    # Set width and heigt of screen
    width, height = image.size

    # prepare for drawing
    draw = ImageDraw.Draw(image)

    # set font sizes
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", size)
    font1 = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 14)

    # set btc and sat price
    btcprice = price.getbtcprice(CURRENCY)
    satprice = round((1 / btcprice) * 10e5, 2)

    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((15, 10), str(round(SATS)) + " sats", fill=BLACK, font=font)
    draw.text(
        (15, 30),
        "(" + "%.2f" % round(FIAT, 2) + " " + CURRENCY + ")",
        fill=BLACK,
        font=font,
    )
    draw.text((15, 70), "(1 cent = " + str(satprice) + " sats)", fill=BLACK, font=font1)

    papirus.display(image)
    papirus.partial_update()


def update_payout_screen(papirus, size):
    # initially set all white background
    image = Image.new("1", papirus.size, WHITE)

    # Set width and heigt of screen
    width, height = image.size

    # prepare for drawing
    draw = ImageDraw.Draw(image)

    # set font sizes
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 20)
    font1 = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 15)

    # set btc and sat price
    #    btcprice = price.getbtcprice(CURRENCY)
    #    satprice = round((1 / btcprice) * 10e5, 2)

    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((15, 30), str(round(SATS)) + " sats", fill=BLACK, font=font)
    draw.text((15, 50), "on the way!", fill=BLACK, font=font1)
    #    draw.text((15, 30), '(' + '%.2f' % round(FIAT,2) + ' ' + CURRENCY + ')', fill=BLACK, font=font)
    #    draw.text((15, 70), '(1 cent = ' + str(satprice) + ' sats)', fill=BLACK, font=font1)

    papirus.display(image)
    papirus.update()


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit("interrupted")
