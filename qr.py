#!/usr/bin/python3

import zbarlight
import logging
import time

from PIL import Image
from datetime import datetime
from io import BytesIO
from picamera import PiCamera

from config import conf


def scan():

    with PiCamera() as camera:
        try:
            camera.start_preview()
            time.sleep(1)
            logging.info("Start scanning for QR code")
        except:
            logging.error("PiCamera.start_preview() raised an exception")

        stream = BytesIO()
        qr_codes = None
        # Set timeout to 10 seconds
        timeout = time.time() + 10

        while qr_codes is None and (time.time() < timeout):
            stream.seek(0)
            # Start camera stream (make sure RaspberryPi camera is focused correctly
            # manually adjust it, if not)
            camera.capture(stream, "jpeg")
            stream.seek(0)
            qr_codes = zbarlight.scan_codes("qrcode", Image.open(stream))
            time.sleep(0.05)
        camera.stop_preview()

        # break immediately if we didn't get a qr code scan
        if not qr_codes:
            logging.info("No QR within 10 seconds detected")
            return False

        # decode the qr_code to get the invoice
        invoice = qr_codes[0].decode().lower()

        # check for a lightning invoice
        if "lnbc" in invoice:
            logging.info("Lightning invoice detected")

            # Write Lightning invoice into a text file
            now = datetime.now()
            with open(conf["qr"]["scan_dir"] + "/qr_code_scans.txt", "a+") as f:
                f.write(invoice + " " + str(now.strftime("%d/%m/%Y %H:%M:%S")) + "\n")

            # if invoice preceded with "lightning:" then chop it off so that we can
            # handle it correctly
            if "lightning:" in invoice:
                invoice = invoice[10:]
            return invoice

        else:
            logging.error("This QR does not contain a Lightning invoice")
            return False
