
# from __future__ import print_function

import os
import sys
import json
import codecs
import string
import requests
# import lnd_grpc
import RPi.GPIO as GPIO

from PIL import Image
from time import sleep
from PIL import ImageDraw
from PIL import ImageFont
from papirus import Papirus


# Check EPD_SIZE is defined
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    exec(open('/etc/default/epd-fuse').read())
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

# set sat,fiat, currency value
CURRENCY = 'EUR'
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

    btcprice = price_request(CURRENCY)
    satprice = round((1 / (btcprice * 100)) * 100000000, 2)

    while True:

        if GPIO.input(SW1) == False:
            FIAT += 0.01
            SATS = FIAT * 100 * satprice
            update_amount_screen(papirus, SIZE)

        if GPIO.input(SW2) == False:
            FIAT += 0.02
            SATS = FIAT * 100 * satprice
            update_amount_screen(papirus, SIZE)

        if GPIO.input(SW3) == False:
            FIAT += 0.05
            SATS = FIAT * 100 * satprice
            update_amount_screen(papirus, SIZE)

        if GPIO.input(SW4) == False:
            FIAT += 0.1
            SATS = FIAT * 100 * satprice
            update_amount_screen(papirus, SIZE)

        if (GPIO.input(SW5) == False):
            update_payout_screen(papirus, SIZE)
            payout(SATS)

        sleep(0.1)

def update_amount_screen(papirus, size):

    # initially set all white background
    image = Image.new('1', papirus.size, WHITE)

    # Set width and heigt of screen
    width, height = image.size

    # prepare for drawing
    draw = ImageDraw.Draw(image)


    # set font sizes
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', size)
    font1 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 14)

    # set btc and sat price
    btcprice = price_request(CURRENCY)
    satprice = round((1 / btcprice) * 10e5, 2)

    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((15, 10), str(round(SATS)) + ' sats', fill=BLACK, font=font)
    draw.text((15, 30), '(' + '%.2f' % round(FIAT,2) + ' ' + CURRENCY + ')', fill=BLACK, font=font)
    draw.text((15, 70), '(1 cent = ' + str(satprice) + ' sats)', fill=BLACK, font=font1)

    papirus.display(image)
    papirus.partial_update()

def update_payout_screen(papirus, size):

    # initially set all white background
    image = Image.new('1', papirus.size, WHITE)

    # Set width and heigt of screen
    width, height = image.size

    # prepare for drawing
    draw = ImageDraw.Draw(image)


    # set font sizes
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 20)
    font1 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 14)

    # set btc and sat price
#    btcprice = price_request(CURRENCY)
#    satprice = round((1 / btcprice) * 10e5, 2)

    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((15, 10), str(SATS) + 'sats' , fill=BLACK, font=font)
    draw.text((15, 40), 'on the way!' , fill=BLACK, font=font)
#    draw.text((15, 30), '(' + '%.2f' % round(FIAT,2) + ' ' + CURRENCY + ')', fill=BLACK, font=font)
#    draw.text((15, 70), '(1 cent = ' + str(satprice) + ' sats)', fill=BLACK, font=font1)

    papirus.display(image)
    papirus.update()

def price_request(fiatcode):

    request = requests.get('https://apiv2.bitcoinaverage.com/indices/global/ticker/BTC' + fiatcode)
    json_data = json.loads(request.text)
    return json_data['last']

def payout(amt):

    with open(os.path.expanduser('~/admin.macaroon'), 'rb') as f:
        macaroon_bytes = f.read()
        macaroon = codecs.encode(macaroon_bytes, 'hex')

    payment_request = 'lnbc1pwkc2lcpp5dw4k3d793krpx05k72a05e28nwfs3awskxur3vu4pmm8g9njavyqdqu2askcmr9wssx7e3q2dshgmmndp5scqzpgxqrrssndpcdypaj2trxs2jx8fqc6wydzysln2mvdarppslstg030ekhpdkszayvuw5g4s6zsedj5vv2ucqzu4wjmd56dqvx2g5w3kplczj6ssq87txt4'

    data = {
            'payment_request': payment_request,
            'amt': round(amt),
    }

    response =  requests.post(
        'https://btcpay.21isenough.me/lnd-rest/btc/v1/channels/transactions',
        headers = {'Grpc-Metadata-macaroon': macaroon},
        data=json.dumps(data),
    )
    print(response)

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
