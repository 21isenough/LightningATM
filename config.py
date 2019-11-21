import os
import logging
import sys

from papirus import Papirus

import utils


logging.basicConfig(
    filename="/home/pi/LightningATM/resources/debug.log",
    format="%(asctime)-23s %(name)-9s %(levelname)-7s | %(message)s",
    datefmt="%Y/%m/%d %I:%M:%S %p",
    level=logging.INFO,
)
# set API URL e.g. https://btcpay.yourdomain.com/lnd-rest/btc/v1
APIURL = "https://btcpay.21isenough.me/lnd-rest/btc/v1"

# Add variable to set certificate check to true or false #

# Papirus Setup
WHITE = 1
BLACK = 0
PAPIRUSROT = 0
PAPIRUS = Papirus(rotation=PAPIRUSROT)

# set currency value
CURRENCY = "EUR"

# Add var for fee in % #

# base64 encoded lntxbot api credentials
LNTXBOTCRED = "#####"


# Set sat, fiat
FIAT = 0
SATS = 0
INVOICE = ""

# Set btc and sat price
BTCPRICE = utils.get_btc_price(CURRENCY)
SATPRICE = round((1 / (BTCPRICE * 100)) * 100000000, 2)

# Button / Acceptor Pulses
LASTIMPULSE = 0
PULSES = 0
LASTPUSHES = 0
PUSHES = 0

# lntxbot
QRFOLDER = "/home/pi/LightningATM/resources/qr_codes"
