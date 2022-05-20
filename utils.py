import logging
import os
import requests
import sys
import config
import math
import qrcode
import websocket
import threading
import time
import json

from PIL import ImageFont
from pathlib import Path

logger = logging.getLogger("UTILS")


def check_epd_size():
    """Check EPD_SIZE is defined
    """
    # A pre-set default to avoid error messages at first start and if you run a new OS version without PaPiRus
    # Later we should leave the config.ini "display=papiruszero2in" inital empty to be able to bypass this "def"
    EPD_SIZE=2.0

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


def get_btc_price_socket():
    """Get BTC Price in usd(t)
    """
    def on_open(ws):
        print("==> Get BTC price Websocket OPENED")
        
    def on_message(ws, message):
        json_msg = json.loads(message)
        candle = json_msg['k']
        price = float(candle['c'])
        # print(f'BTC price : {price} $')
        config.BTCPRICE = price
        config.SATPRICE = math.floor((1 / (price * 100)) * 1e8)

    def on_close(ws):
        print("==> Get BTC price Websocket CLOSED")


    config.ws = websocket.WebSocketApp(config.BINANCE_SOCKET,
                                on_open=on_open,
                                on_message=on_message,
                                on_close=on_close)
                                
    wst = threading.Thread(target=config.ws.run_forever)
    wst.start()
    time.sleep(2)


def get_sats():
    return math.floor(config.FIAT * 100 * config.SATPRICE)


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
