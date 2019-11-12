#!/usr/bin/python3

import os, qrcode, time, logging, display
from PIL import Image, ImageFont, ImageDraw
from papirus import Papirus

import requests, json
from config import *
from utils import *

######### Just for scanning ########
import os, zbarlight, sys, logging
from PIL import Image
from datetime import datetime
####################################



def generate_lnurl(amt):
    display.update_lnurl_generation()

    logging.info('LNURL requested')
    print('LNURL requested')

    data = {
            'satoshis': str(round(amt)),
    }

    response = requests.post(
        'https://lntxbot.alhur.es/generatelnurlwithdraw',
        headers = {'Authorization' : 'Basic %s' %  LNTXBOTCRED},
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
    response = requests.post(
        'https://lntxbot.alhur.es/balance',
        headers = {'Authorization' : 'Basic %s' %  LNTXBOTCRED},
        )

    response = json.loads(response.text)
    response = response['BTC']

    balance = response['AvailableBalance']
    print(balance)

    newbalance = balance

    while balance == newbalance:
        response = requests.post(
            'https://lntxbot.alhur.es/balance',
            headers = {'Authorization' : 'Basic %s' %  LNTXBOTCRED},
            )

        response = json.loads(response.text)
        response = response['BTC']

        newbalance = response['AvailableBalance']
        print('Balance: ' + str(balance) +' (no changes)')
        time.sleep(3)

    print('Balance: ' + str(balance) +' | New Balance:' + str(newbalance))

    logging.info('Withdrawl succeeded')
    print('Withdrawl succeeded')

    display.update_thankyou_screen()
    logging.info('Initiating restart...')
    os.execv('/home/pi/LightningATM/app.py', [''])

def scancreds():

    attempts = 0
    qrfolder = '/home/pi/LightningATM/resources/qr_codes'

    while attempts < 4:
        try:
            scan = True
            qr_count = len(os.listdir(qrfolder))
            print('Taking picture..')
            ## Take picture (make sure RaspberryPi camera is focused correctly - manually adjust it, if not)
            os.system('sudo fswebcam -d /dev/video0 -r 700x525 -q '+qrfolder+'/lntxcred_'+str(qr_count)+'.jpg')
            print('Picture saved..')

        except:
            scan = False
            print('Picture couldn\'t be taken..')

        if scan:
            invoice = ''

            print('Scanning image..')
            with open(qrfolder+'/lntxcred_'+str(qr_count)+'.jpg','rb') as f:
                qr = Image.open(f)
                qr.load()
                invoice = zbarlight.scan_codes('qrcode',qr)

            if not invoice:
                logging.info('No QR code found')
                print('No QR code found')
                os.remove(qrfolder+'/lntxcred_'+str(qr_count)+'.jpg')
                attempts += 1

            else:
                ## exctract invoice from list
                logging.info('Invoice detected')
                invoice = invoice[0]
                invoice = invoice.decode()
                #invoice = invoice.lower()
                #print(invoice)

                #with open(qrfolder+'/qr_code_scans.txt','a+') as f:
                #    f.write(invoice + ' ' + str(datetime.now()) + '\n')

                ## remove "lightning:" prefix
                #if 'lightning:' in invoice:
                #    invoice = invoice[10:]

                return invoice

    ## return False after 4 failed attempts
    logging.info('4 failed scanning attempts.')
    print('4 failed attempts ... try again.')
    return False
