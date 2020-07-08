import logging
import os
import requests
import sys
import config
import math
import qrcode

from PIL import ImageFont
from pathlib import Path

logger = logging.getLogger("UTILS")


def check_epd_size():
    """Check EPD_SIZE is defined
    """
    if os.path.exists("/etc/default/epd-fuse"):
        exec(open("/etc/default/epd-fuse").read(), globals())

    if EPD_SIZE == 0.0:
        print("Please select your screen size by running 'papirus-config'.")
        sys.exit()


def create_font(font, size):
    """Create fonts from resources
    """
    # Construct paths to foder with fonts
    pathfreemono = Path.cwd().joinpath("resources", "fonts", "FreeMono.ttf")
    pathfreemonobold = Path.cwd().joinpath("resources", "fonts", "FreeMonoBold.ttf")
    pathsawasdee = Path.cwd().joinpath("resources", "fonts", "Sawasdee-Bold.ttf")
    pathdotmbold = Path.cwd().joinpath("resources", "fonts", "DOTMBold.ttf")

    if font == "freemono":
        return ImageFont.truetype(pathfreemono.as_posix(), size)
    if font == "freemonobold":
        return ImageFont.truetype(pathfreemonobold.as_posix(), size)
    if font == "sawasdee":
        return ImageFont.truetype(pathsawasdee.as_posix(), size)
    if font == "dotmbold":
        return ImageFont.truetype(pathdotmbold.as_posix(), size)
    else:
        print("Font not available")


def get_btc_price(fiat_code):
    """Get BTC -> FIAT conversion
    """
    url = config.COINGECKO_URL_BASE + "simple/price"
    price = requests.get(
        url, params={"ids": "bitcoin", "vs_currencies": fiat_code}
    ).json()
    return price["bitcoin"][fiat_code]


def get_sats():
    return config.FIAT * 100 * config.SATPRICE


def get_sats_with_fee():
    return math.floor(config.SATS * (float(config.conf["atm"]["fee"]) / 100))


def generate_lnurl_qr(lnurl):
    """Generate an lnurl qr code from a lnurl
    """
    lnurlqr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=1,
    )
    lnurlqr.add_data(lnurl.upper())
    logger.info("LNURL QR code generated")
    return lnurlqr.make_image()
