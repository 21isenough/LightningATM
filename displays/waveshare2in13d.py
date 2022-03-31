#!/usr/bin/python3

import time
import math

import config
import utils

from PIL import Image, ImageFont, ImageDraw

from displays import messages
from displays import messages_de
from displays import messages_es
from displays import messages_fr
from displays import messages_it
from displays import messages_pt
from displays import messages_tr


# Select language from config.ini. If no match => English
if config.conf["atm"]["language"] == "de":
    messages = messages_de
if config.conf["atm"]["language"] == "es":
    messages = messages_es
if config.conf["atm"]["language"] == "fr":
    messages = messages_fr
if config.conf["atm"]["language"] == "it":
    messages = messages_it
if config.conf["atm"]["language"] == "pt":
    messages = messages_pt
if config.conf["atm"]["language"] == "tr":
    messages = messages_tr
else:
    messages = messages


def update_startup_screen():
    """Show startup screen on eInk Display
    """
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (24, 4),
        messages.startup_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (12, 24),
        messages.startup_screen_2,
        fill=config.BLACK,
        font=utils.create_font("sawasdee", 30),
    )
    draw.text(
        (3, 82),
        messages.startup_screen_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 15),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def error_screen(message="ERROR"):
    """Error screen
    """
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (4, 13),
        messages.error_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )
    draw.text(
        (4, 50),
        message,
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_qr_request():
    # initially set all white background
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (30, 10),
        messages.qr_request_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 23),
    )
    draw.text(
        (16, 32),
        messages.qr_request_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))

    for i in range(0, 3):
        draw.text(
            (90, 55),
            str(3 - i),
            fill=config.BLACK,
            font=utils.create_font("freemono", 55),
        )
        config.WAVESHARE.init()
        config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))
        draw.rectangle((75, 50, 115, 90), fill=config.WHITE, outline=config.WHITE)
        time.sleep(0.5)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (20, 15),
        messages.qr_request_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    draw.text(
        (20, 45),
        messages.qr_request_4 + str(math.floor(config.SATS)) + messages.qr_request_5,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_qr_failed():
    # initially set all white background
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )

    draw.text(
        (20, 15),
        messages.qr_failed_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    draw.text(
        (20, 45),
        messages.qr_failed_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_payout_screen():
    """Update the payout screen to reflect balance of deposited coins.
    Scan the invoice??? I don't think so!
    """
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (20, 25),
        str(math.floor(config.SATS)) + messages.payout_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 28),
    )
    draw.text(
        (20, 60),
        messages.payout_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))

    # scan the invoice
    # TODO: I notice this is commented out, I presume this function should _not_ be
    #   scanning a QR code on each update?
    # config.INVOICE = qr.scan()


def update_payment_failed():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (14, 20),
        messages.payment_failed_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 22),
    )
    draw.text(
        (35, 60),
        messages.payment_failed_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 19),
    )
    draw.text(
        (60, 80),
        messages.payment_failed_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 19),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_thankyou_screen():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (25, 15),
        messages.thankyou_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (50, 42),
        messages.thankyou_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (13, 80),
        messages.thankyou_screen_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))
    time.sleep(5)


def update_nocoin_screen():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (10, 10),
        messages.nocoin_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 22),
    )
    draw.text(
        (45, 50),
        messages.nocoin_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (45, 75),
        messages.nocoin_screen_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_lnurl_generation():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (40, 20),
        messages.lnurl_generation_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (14, 60),
        messages.lnurl_generation_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))

def update_shutdown_screen():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (10, 10),
        messages.shutdown_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 22),
    )
    draw.text(
        (19, 50),
        messages.shutdown_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (52, 75),
        messages.shutdown_screen_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_wallet_scan():
    # initially set all white background
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (25, 15),
        messages.wallet_scan_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 23),
    )
    draw.text(
        (25, 40),
        messages.wallet_scan_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 23),
    )
    draw.text(
        (25, 65),
        messages.wallet_scan_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 23),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))
    time.sleep(2)


def update_lntxbot_balance(balance):
    # initially set all white background
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (45, 15),
        messages.lntxbot_balance_1,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 24),
    )
    draw.text(
        (12, 55),
        messages.lntxbot_balance_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 15),
    )
    draw.text(
        (45, 75),
        str("{:,}".format(balance)) + messages.lntxbot_balance_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 22),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))
    time.sleep(3)


def update_btcpay_lnd():
    # initially set all white background
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (45, 20),
        messages.btcpay_lnd_1,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 24),
    )
    draw.text(
        (10, 55),
        messages.btcpay_lnd_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 17),
    )
    draw.text(
        (10, 80),
        messages.btcpay_lnd_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))
    time.sleep(3)


def draw_lnurl_qr(qr_img):
    """Draw a lnurl qr code on the e-ink screen
    """
    image, width, height, draw = init_screen(color=config.BLACK)

    qr_img = qr_img.resize((104, 104), resample=0)

    draw = ImageDraw.Draw(image)
    draw.bitmap((0, 0), qr_img, fill=config.WHITE)
    draw.text(
        (115, 30),
        messages.lnurl_qr_1,
        fill=config.WHITE,
        font=utils.create_font("freemonobold", 20),
    )
    draw.text(
        (115, 50),
        messages.lnurl_qr_2,
        fill=config.WHITE,
        font=utils.create_font("freemonobold", 20),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_amount_screen():
    """Update the amount screen to reflect new coins inserted
    """
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (12, 10),
        str("{:,}".format(math.floor(config.SATS))) + messages.amount_screen_1,
        fill=config.BLACK,
        font=utils.create_font("dotmbold", 28),
    )
    draw.text(
        (12, 40),
        "%.2f" % round(config.FIAT, 2) + " " + config.conf["atm"]["cur"].upper(),
        fill=config.BLACK,
        font=utils.create_font("dotmbold", 23),
    )
    draw.text(
        (12, 65),
        messages.amount_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )
    draw.text(
        (60, 65),
        messages.amount_screen_3
        + str(math.floor(config.SATPRICE))
        + messages.amount_screen_4
        + config.conf["atm"]["centname"],
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )
    draw.text(
        (12, 80),
        messages.amount_screen_5,
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )
    draw.text(
        (60, 80),
        messages.amount_screen_6
        + config.conf["atm"]["fee"]
        + messages.amount_screen_7
        + str(math.floor(config.SATSFEE))
        + messages.amount_screen_8,
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_lnurl_cancel_notice():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (6, 20),
        messages.lnurl_cancel_notice_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (6, 65),
        messages.lnurl_cancel_notice_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 14),
    )
    draw.text(
        (6, 85),
        messages.lnurl_cancel_notice_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 14),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_button_fault():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (10, 10),
        messages.button_fault_1,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 22),
    )
    draw.text(
        (10, 50),
        messages.button_fault_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (10, 75),
        messages.button_fault_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_wallet_fault():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (10, 10),
        messages.wallet_fault_1,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 22),
    )
    draw.text(
        (10, 50),
        messages.wallet_fault_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (10, 75),
        messages.wallet_fault_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))

def update_blank_screen():
    image, width, height, draw = init_screen(color=config.WHITE)

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def init_screen(color):
    """Prepare the screen for drawing and return the draw variables
    """
    image = Image.new("1", (config.WAVESHARE.height, config.WAVESHARE.width), color)
    # Set width and height of screen
    width, height = image.size
    # prepare for drawing
    draw = ImageDraw.Draw(image)
    return image, width, height, draw
