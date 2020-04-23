#!/usr/bin/python3

import zbarlight
import logging
import requests
import time
import config

from PIL import Image
from io import BytesIO
from picamera import PiCamera

logger = logging.getLogger("QR")


def scan():

    with PiCamera() as camera:
        try:
            camera.start_preview()
            time.sleep(1)
            logger.info("Start scanning for QR code")
        except:
            logger.error("PiCamera.start_preview() raised an exception")

        stream = BytesIO()
        qr_codes = None
        # Set timeout to 10 seconds
        timeout = time.time() + 10
        while qr_codes is None and (time.time() < timeout):
            stream.seek(0)
            # Start camera stream (make sure RaspberryPi camera is focused correctly
            # manually adjust it, if not)
            camera.capture(stream, "jpeg")
            qr_codes = zbarlight.scan_codes("qrcode", Image.open(stream))
            time.sleep(0.05)
        camera.stop_preview()
        # break immediately if we didn't get a qr code scan
        if not qr_codes:
            logger.info("No QR within 10 seconds detected")
            return False

        # decode the first qr_code to get the data
        qr_code = qr_codes[0].decode()

        return qr_code


def scan_attempts(target_attempts):
    """Scan and evaluate users credentials
    """
    attempts = 0

    while attempts < target_attempts:
        qrcode = scan()
        if qrcode:
            logger.info("QR code successfuly detected.")
            return qrcode
        else:
            attempts += 1
            logger.error("{}. attempt!".format(attempts))

    logger.error("{} failed scanning attempts.".format(target_attempts))


def scan_credentials():
    credentials = scan_attempts(4)

    if credentials:
        if ("lnd-config" in credentials) and ("lnd.config" in credentials):
            logger.info("BTCPayServer LND Credentials detected.")
            try:
                r = requests.get(credentials.lstrip("config="))
                data = r.json()
                data = data["configurations"][0]

                config.update_config("btcpay", "url", data["uri"] + "v1")
                config.update_config("lnd", "macaroon", data["adminMacaroon"])
                config.update_config("atm", "activewallet", "btcpay_lnd")
            except:
                logger.error("QR not valid (they expire after 10 minutes)")

        elif ("lntxbot" in credentials) and ("@" in credentials):
            logger.info("Lntxbot Credentials detected.")

            config.update_config("lntxbot", "creds", credentials.split("@")[0])
            config.update_config("lntxbot", "url", credentials.split("@")[1])
            config.update_config("atm", "activewallet", "lntxbot")

        else:
            logger.error("No credentials to a known wallet detected.")
    else:
        logger.error("No credentials to a known wallet could be detected.")
