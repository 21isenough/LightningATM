import os, zbarlight, sys
from PIL import Image
from datetime import datetime

def scan():

    qr_count = len(os.listdir('resources/qr_codes'))
    qr_countup = qr_count

    print('Taking picture..')
    try:
        scan = True
        for i in range(0,3):
            os.system('sudo fswebcam -d /dev/video0 -r 800x600 -q resources/qr_codes/qr_'+str(qr_countup)+'.jpg')
            qr_countup += 1
            print('Picture saved..')
    except:
        scan = False
        print('Picture couldn\'t be taken..')
    if(scan):
        codes = []
        qr_countup = qr_count
        print('Scanning image..')
        for i in range(0,3):
            with open('resources/qr_codes/qr_'+str(qr_countup)+'.jpg','rb') as f:
                qr = Image.open(f)
                qr.load()
                code = zbarlight.scan_codes('qrcode',qr)
                if code:
                    codes.append(code)
                qr_countup += 1
                print(codes)
                print(type(codes))

        if not codes:
            print('No QR code found in the picture')
            return False
        else:
            code = codes[0][0]
            print(code)
            code = code.decode()
            print(code)
            code = code.lower()
            print(code)

            with open('resources/qr_codes/qr_code_scans.txt','a+') as f:
                f.write(code + ' ' + str(datetime.now()) + '\n')

            return code
