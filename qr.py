import os, zbarlight, sys
from PIL import Image
from datetime import datetime

def scan():

    print('Taking picture..')
    try:
        scan = True
        qr_count = len(os.listdir('resources/qr_codes'))
        os.system('sudo fswebcam -d /dev/video0 -r 2952x1944 -q resources/qr_codes/qr_'+str(qr_count)+'.jpg')
        print('Picture saved..')
    except:
        scan = False
        print('Picture couldn\'t be taken..')
    if(scan):
        print('Scanning image..')
        with open('resources/qr_codes/qr_'+str(qr_count)+'.jpg','rb') as f:
            qr = Image.open(f)
            qr.load()

        codes = zbarlight.scan_codes('qrcode',qr)
