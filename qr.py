import os, zbarlight, sys
from PIL import Image
from datetime import datetime

def scan():

    attempts = 0

    while attempts <= 4:
        try:
            scan = True
            qr_count = len(os.listdir('resources/qr_codes'))
            print('Taking picture..')
            os.system('sudo fswebcam -d /dev/video0 -r 1200x900 -q resources/qr_codes/qr_'+str(qr_count)+'.jpg')
            print('Picture saved..')

        except:
            scan = False
            print('Picture couldn\'t be taken..')

        if(scan):
            codes = []

            print('Scanning image..')
            with open('resources/qr_codes/qr_'+str(qr_count)+'.jpg','rb') as f:
                qr = Image.open(f)
                qr.load()
                code = zbarlight.scan_codes('qrcode',qr)
                if code:
                    codes.append(code)
                    # qr_countup += 1
                print(codes)

            if not codes:
                print('No QR code found in the picture')
                attempts += 1

            else:
                ## exctract invoice from list
                code = codes[0][0]
                code = code.decode()
                code = code.lower()

                ## remove "lightning:" prefix
                if 'lightning:' in code:
                    code = code[10:]

                with open('resources/qr_codes/qr_code_scans.txt','a+') as f:
                    f.write(code + ' ' + str(datetime.now()) + '\n')

                return code
    print('4 failed attempts ... try again.')
    return False
