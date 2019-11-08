#!/usr/bin/python3

import os, qrcode, time, logging
from PIL import Image, ImageFont, ImageDraw
from papirus import Papirus

import requests, json
from config import *
from utils import *

def generate_lnurl(amt):

    data = {
            'satoshis': str(round(amt)),
    }

    response = requests.post(
        'https://lntxbot.alhur.es/generatelnurlwithdraw',
        auth=(USER, PASS),
        data=json.dumps(data),
        )

    response = json.loads(response.text)
    print(response['lnurl'])

    if os.path.exists('/etc/default/epd-fuse'):
        exec(open('/etc/default/epd-fuse').read())

    image = Image.new('1', PAPIRUS.size, BLACK)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=1,
    )
    qr.add_data(response['lnurl'].upper())


    img = qr.make_image()


    print(type(img))
    print(img.size)

    img = img.resize((96,96), resample=0)

    print(img.size)

    draw = ImageDraw.Draw(image)
    draw.bitmap((0, 0), img, fill=WHITE)
    draw.text((110, 25), 'Scan to', fill=WHITE, font=createfont('freemonobold',16))
    draw.text((110, 45), 'receive', fill=WHITE, font=createfont('freemonobold',16))

    PAPIRUS.display(image)
    PAPIRUS.update()
