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
        if(codes==None):
            print('No QR code found in the picture')
        else:
            code = codes[0]

            with open('resources/qr_codes/qr_code_scans.txt','a+') as f:
                f.write(code.decode() + ' ' + str(datetime.now()) + '\n')

            return code.decode()
