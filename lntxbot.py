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
