#!/usr/bin/python3

## Displays QR codes on the e-Ink

import os
import qrcode
from PIL import Image, ImageFont, ImageDraw
from papirus import Papirus

def createfont(font, size):
    pathfreemono = os.path.expanduser('~/LightningATM/resources/fonts/FreeMono.ttf')
    pathfreemonob = os.path.expanduser('~/LightningATM/resources/fonts/FreeMonoBold.ttf')
    pathsawasdee = os.path.expanduser('~/LightningATM/resources/fonts/Sawasdee-Bold.ttf')

    if font == 'freemono':
        return ImageFont.truetype(pathfreemono, size)
    if font == 'freemonob':
        return ImageFont.truetype(pathfreemonob, size)
    if font == 'sawasdee':
        return ImageFont.truetype(pathsawasdee, size)
    else:
        print('Font not available')


WHITE = 1
BLACK = 0
PAPIRUSROT = 0
PAPIRUS = Papirus(rotation = PAPIRUSROT)

if os.path.exists('/etc/default/epd-fuse'):
    exec(open('/etc/default/epd-fuse').read())

image = Image.new('1', PAPIRUS.size, BLACK)

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=2,
    border=2,
)
qr.add_data('lnurl1dp68gurn8ghj7ctsdyhxc6t8dp6xu6twvuhxw6txw3ej7mrww4exctesxdnxyerrvvmk2e3svdjkye3hxuenyvtyx3jr2erzxcmrxvfj893xvd3cxu6xgdrxv56n2e3jvdnqs3t6l7'.upper())


img = qr.make_image()


print(type(img))
print(img.size)

img = img.resize((96,96), resample=0)

print(img.size)

draw = ImageDraw.Draw(image)
draw.bitmap((0, 0), img, fill=WHITE)
draw.text((110, 25), 'Scan to', fill=WHITE, font=createfont('freemonob',16))
draw.text((110, 45), 'receive', fill=WHITE, font=createfont('freemonob',16))

PAPIRUS.display(image)
PAPIRUS.update()
