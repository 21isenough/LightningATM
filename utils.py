import logging
import os
import requests
import sys
import config
import math

from PIL import ImageFont
from pathlib import Path

logger = logging.getLogger("UTILS")


class ScanError(Exception):
    pass


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
    # I think here, you will want to get the current directory, as not everybody will
    # have saved the LightningATM folder in ~/LightningATM/
    # something like?
    # os.path(__file__.resources/fonts/...
    pathfreemono = Path("resources/fonts/FreeMono.ttf")
    pathfreemonobold = Path("resources/fonts/FreeMonoBold.ttf")
    pathsawasdee = Path("resources/fonts/Sawasdee-Bold.ttf")

    if font == "freemono":
        return ImageFont.truetype(pathfreemono.as_posix(), size)
    if font == "freemonobold":
        return ImageFont.truetype(pathfreemonobold.as_posix(), size)
    if font == "sawasdee":
        return ImageFont.truetype(pathsawasdee.as_posix(), size)
    else:
        print("Font not available")


def get_btc_price(fiat_code):
    """Get BTC -> FIAT conversion
    """
    return requests.get(
        "https://apiv2.bitcoinaverage.com/indices/global/ticker/BTC" + fiat_code.upper()
    ).json()["last"]


def get_sats():
    return config.FIAT * 100 * config.SATPRICE


def get_sats_with_fee():
    return math.floor(config.SATS * (float(config.conf["atm"]["fee"]) / 100))
