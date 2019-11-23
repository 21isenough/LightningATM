#!/usr/bin/python3

import os
import zbarlight
import logging

from PIL import Image
from datetime import datetime

from config import CONFIG


def scan():

    attempts = 0
    qr_folder = CONFIG["qr"]["SCAN_DIR"]

    while attempts < 4:
        try:
            _scan = True
            qr_count = len(os.listdir(qr_folder))
            print("Taking picture..")
            # Take picture (make sure RaspberryPi camera is focused correctly - manually adjust it, if not)
            os.system(
                "sudo fswebcam -d /dev/video0 -r 700x525 -q "
                + qr_folder
                + "/qr_"
                + str(qr_count)
                + ".jpg"
            )
            print("Picture saved..")

        except:
            _scan = False
            print("Picture couldn't be taken..")

        if _scan:
            invoice = ""

            print("Scanning image..")
            with open(qr_folder + "/qr_" + str(qr_count) + ".jpg", "rb") as f:
                qr = Image.open(f)
                qr.load()
                invoice = zbarlight.scan_codes("qrcode", qr)

            if not invoice:
                logging.info("No QR code found")
                print("No QR code found")
                os.remove(qr_folder + "/qr_" + str(qr_count) + ".jpg")
                attempts += 1

            else:
                # extract invoice from list
                logging.info("Invoice detected")
                invoice = invoice[0]
                invoice = invoice.decode()
                invoice = invoice.lower()
                print(invoice)

                with open(qr_folder + "/qr_code_scans.txt", "a+") as f:
                    f.write(invoice + " " + str(datetime.now()) + "\n")

                # remove "lightning:" prefix
                if "lightning:" in invoice:
                    invoice = invoice[10:]

                return invoice

    # return False after 4 failed attempts
    logging.info("4 failed scanning attempts.")
    print("4 failed attempts ... try again.")
    return False
