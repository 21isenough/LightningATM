#!/usr/bin/python3

import os
import zbarlight
import sys
import logging
import config
import time

from PIL import Image
from datetime import datetime
from io import BytesIO
from picamera import PiCamera


def scan():

    with PiCamera() as camera:
        try:
            camera.start_preview()
            time.sleep(1)
            logging.info("Start scanning for QR code")
        except:
            logging.info("Picture couldn't be taken..")

        stream = BytesIO()
        qrcodes = None
        # Set timeout to 10 seconds
        timeout = time.time() + 10

        while qrcodes is None and (time.time() < timeout):
            stream.seek(0)
            ## Start camera stream (make sure RaspberryPi camera is focused correctly - manually adjust it, if not)
            camera.capture(stream, "jpeg")
            stream.seek(0)
            qrcodes = zbarlight.scan_codes("qrcode", Image.open(stream))
            time.sleep(0.05)
        camera.stop_preview()

        if qrcodes:
            invoice = qrcodes[0].decode().lower()

        if not (time.time() < timeout):
            logging.info("No QR within 10 seconds detected")
            return False

        elif "lnbc" in invoice:
            logging.info("Lightning invoice detected")
            ## Write Lightning invoice into a text file
            now = datetime.now()
            with open(config.QRFOLDER + "/qr_code_scans.txt", "a+") as f:
                f.write(invoice + " " + str(now.strftime("%d/%m/%Y %H:%M:%S")) + "\n")

            if "lightning:" in invoice:
                invoice = invoice[10:]
            return invoice

        else:
            logging.info("This QR does not contain a Lightning invoice")
            return False
