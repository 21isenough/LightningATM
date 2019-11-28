#!/usr/bin/python3

import os
import time
import logging
import requests
import json

from PIL import ImageDraw

# import qrcode

# TODO: Should this be `import qr`? Otherwise this is missing from requirements.txt
import config
import display
import utils

# Just for scanning
import logging
from datetime import datetime
from PIL import Image
import zbarlight


logger = logging.getLogger("LNTXBOT")


def request_lnurl(amt):
    """Request a new lnurl for 'amt' from the server
    """
    data = {
        "satoshis": str(round(amt)),
    }
    response = requests.post(
        "https://lntxbot.alhur.es/generatelnurlwithdraw",
        headers={"Authorization": "Basic %s" % config.conf["lntxbot"]["cred"]},
        data=json.dumps(data),
    )
    return response.json()


def generate_lnurl_qr(lnurl):
    """Generate an lnurl qr code from a lnurl
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=1,
    )
    qr.add_data(lnurl.upper())
    return qr.make_image()


def draw_lnurl_qr(qr_img):
    """draw a lnurl qr code on the e-ink screen
    """
    image = Image.new("1", config.PAPIRUS.size, config.BLACK)
    draw = ImageDraw.Draw(image)
    draw.bitmap((0, 0), qr_img, fill=config.WHITE)
    draw.text(
        (110, 25),
        "Scan to",
        fill=config.WHITE,
        font=utils.create_font("freemonobold", 16),
    )
    draw.text(
        (110, 45),
        "receive",
        fill=config.WHITE,
        font=utils.create_font("freemonobold", 16),
    )

    config.PAPIRUS.display(image)
    config.PAPIRUS.update()


def get_lnurl_balance():
    """Query the lnurl balance from the server and return the
    ["BTC"]["AvailableBalance"] value
    """
    response = requests.post(
        "https://lntxbot.alhur.es/balance",
        headers={"Authorization": "Basic %s" % config.conf["lntxbot"]["cred"]},
    )
    return response.json()["BTC"]["AvailableBalance"]


def wait_for_balance_update(start_balance, timeout):
    """Loops waiting for any balance change on the lnurl and returns True if this
    happens before the timeout
    """
    start_time = time.time()
    success = False
    # loop while we wait for the balance to get updated
    while True and (time.time() < start_time + timeout):
        new_balance = get_lnurl_balance()
        if start_balance == new_balance:
            print("Balance: " + str(start_balance) + " (no changes)")
            time.sleep(3)
        else:
            print(
                "Balance: " + str(start_balance) + " | New Balance:" + str(new_balance)
            )
            logger.info("LNURL withdrawal succeeded")
            print("LNURL withdrawal succeeded")
            success = True
            break
    return success


def process_using_lnurl(amt):
    """Processes receiving an amount using the lnurl scheme
    """
    # get the new lnurl
    display.update_lnurl_generation()
    logger.info("LNURL requested")
    print("LNURL requested")
    lnurl = request_lnurl(amt)
    print(lnurl["lnurl"])

    # Check EPD_SIZE is defined
    utils.check_epd_size()

    # create a qr code image and print it to terminal
    qr_img = generate_lnurl_qr(lnurl["lnurl"])
    print(type(qr_img))
    print(qr_img.size)
    qr_img = qr_img.resize((96, 96), resample=0)
    print(qr_img.size)

    # draw the qr code on the e-ink screen
    draw_lnurl_qr(qr_img)

    # get the balance? back from the bot
    start_balance = get_lnurl_balance()
    print(start_balance)

    # loop while we wait for a balance update or until timeout reached
    success = wait_for_balance_update(start_balance, timeout=90)

    if success:
        display.update_thankyou_screen()
        logger.info("Initiating restart...")
        os.execv("/home/pi/LightningATM/app.py", [""])
    else:
        # TODO: I think we should handle a failure here
        pass


def photograph_qr_code(qr_count):
    """Take a new image of a qr code
    """
    try:
        print("Taking picture..")
        # Take picture (make sure RaspberryPi camera is focused correctly - manually
        # adjust it, if not)
        os.system(
            "sudo fswebcam -d /dev/video0 -r 700x525 -q "
            + config.conf["qr"]["scan_dir"]
            + "/lntxcred_"
            + str(qr_count)
            + ".jpg"
        )
        print("Picture saved..")
        return True
    except:
        logger.exception("Exception in lntxbot.scan_creds")
        print("Picture couldn't be taken..")
        return False


def extract_qr_from_image(qr_count):
    """Attempt to read the QR code from the image
    """
    print("Scanning image..")
    with open(
        config.conf["qr"]["scan_dir"] + "/lntxcred_" + str(qr_count) + ".jpg", "rb"
    ) as f:
        qr = Image.open(f)
        qr.load()
        invoice = zbarlight.scan_codes("qrcode", qr)

    if not invoice:
        logger.info("No QR code found")
        print("No QR code found")
        os.remove(config.conf["qr"]["scan_dir"] + "/lntxcred_" + str(qr_count) + ".jpg")
        return False

    else:
        # extract invoice from list
        logger.info("Invoice detected")
        invoice = invoice[0]
        invoice = invoice.decode()
        # invoice = invoice.lower()
        # print(invoice)

        # with open(config.CONFIG["qr"]["scan_dir"]+'/qr_code_scans.txt','a+') as f:
        #    f.write(invoice + ' ' + str(datetime.now()) + '\n')

        # remove "lightning:" prefix
        # if 'lightning:' in invoice:
        #    invoice = invoice[10:]

        return invoice


def scan_creds():
    """Scan lntxbot credentials?
    """
    attempts = 0

    while attempts < 4:
        qr_count = len(os.listdir(config.conf["qr"]["scan_dir"]))
        qr_image = photograph_qr_code(qr_count)
        if qr_image:
            invoice = extract_qr_from_image(qr_count)
            if not invoice:
                attempts += 1
            else:
                return invoice

    logger.info("4 failed scanning attempts.")
    print("4 failed attempts ... try again.")
    return False
