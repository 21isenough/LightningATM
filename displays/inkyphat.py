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
elif config.conf["atm"]["language"] == "es":
    messages = messages_es
elif config.conf["atm"]["language"] == "fr":
    messages = messages_fr
elif config.conf["atm"]["language"] == "it":
    messages = messages_it
elif config.conf["atm"]["language"] == "pt":
    messages = messages_pt
elif config.conf["atm"]["language"] == "tr":
    messages = messages_tr
else:
    messages = messages


def update_startup_screen():
    """Show startup screen on eInk Display
    """
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (20, 10),
        messages.startup_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (10, 20),
        messages.startup_screen_2,
        fill=config.BLACK,
        font=utils.create_font("sawasdee", 30),
    )
    draw.text(
        (7, 75),
        messages.startup_screen_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 14),
    )

    config.INKY.set_image(image)
    config.INKY.show()


def error_screen(message="ERROR"):
    """Error screen
    """
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (20, 10),
        messages.error_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (10, 20),
        message,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )

    config.INKY.set_image(image)
    config.INKY.show()


def update_qr_request():
    # initially set all white background
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (25, 10),
        messages.qr_request_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (10, 30),
        messages.qr_request_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )

    config.INKY.set_image(image)
    config.INKY.show()

    for i in range(0, 3):
        draw.text(
            (80, 45),
            str(3 - i),
            fill=config.BLACK,
            font=utils.create_font("freemono", 50),
        )
        config.INKY.set_image(image)
        config.INKY.show()
        draw.rectangle((75, 50, 115, 90), fill=config.WHITE, outline=config.WHITE)
        time.sleep(1)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (25, 10),
        messages.qr_request_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (15, 35),
        "for " + str(math.floor(config.SATS)) + " sats.",
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    config.INKY.set_image(image)
    config.INKY.show()


def update_qr_failed():
    # initially set all white background
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )

    draw.text(
        (25, 30),
        messages.qr_failed_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (25, 50),
        messages.qr_failed_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )

    config.INKY.set_image(image)
    config.INKY.show()


def update_payout_screen():
    """Update the payout screen to reflect balance of deposited coins.
    Scan the invoice??? I don't think so!
    """
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (15, 30),
        str(math.floor(config.SATS)) + messages.payout_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (15, 50),
        messages.payout_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 15),
    )

    config.INKY.set_image(image)
    config.INKY.show()

    # scan the invoice
    # TODO: I notice this is commented out, I presume this function should _not_ be
    #   scanning a QR code on each update?
    # config.INVOICE = qr.scan()


def update_payment_failed():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (15, 10),
        messages.payment_failed_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 19),
    )
    draw.text(
        (25, 45),
        messages.payment_failed_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 17),
    )
    draw.text(
        (45, 65),
        messages.payment_failed_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 17)
    )

    config.INKY.set_image(image)
    config.INKY.show()


def update_thankyou_screen():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (15, 10),
        messages.thankyou_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 19),
    )
    draw.text(
        (40, 35),
        messages.thankyou_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 19),
    )
    draw.text(
        (15, 70),
        messages.thankyou_screen_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 14),
    )
    config.INKY.set_image(image)
    config.INKY.show()
    time.sleep(5)


def update_nocoin_screen():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (15, 10),
        messages.nocoin_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 18),
    )
    draw.text(
        (30, 40),
        messages.nocoin_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (30, 65),
        messages.nocoin_screen_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )

    config.INKY.set_image(image)
    config.INKY.show()


def update_lnurl_generation():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (30, 20),
        messages.lnurl_generation_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (10, 40),
        messages.lnurl_generation_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )

    config.INKY.set_image(image)
    config.INKY.show()


def update_shutdown_screen():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (20, 10),
        messages.shutdown_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (25, 45),
        messages.shutdown_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 17),
    )
    draw.text(
        (45, 65),
       messages.shutdown_screen_3,
       fill=config.BLACK,
       font=utils.create_font("freemono", 17)
    )

    config.INKY.set_image(image)
    config.INKY.show()


def update_wallet_scan():
    # initially set all white background
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (35, 20),
        messages.wallet_scan_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (33, 40),
        messages.wallet_scan_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (35, 60),
        messages.wallet_scan_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )

    config.INKY.set_image(image)
    config.INKY.show()
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
        font=utils.create_font("freemonobold", 20),
    )
    draw.text(
        (10, 45),
        messages.lntxbot_balance_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 15),
    )
    draw.text(
        (45, 65),
        str("{:,}".format(balance)) + messages.lntxbot_balance_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )

    config.INKY.set_image(image)
    config.INKY.show()
    time.sleep(3)


def update_btcpay_lnd():
    # initially set all white background
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (45, 15),
        messages.btcpay_lnd_1,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 20),
    )
    draw.text(
        (10, 45),
        messages.btcpay_lnd_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 15),
    )
    draw.text(
        (15, 65),
        messages.btcpay_lnd_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )

    config.INKY.set_image(image)
    config.INKY.show()
    time.sleep(3)


def draw_lnurl_qr(qr_img):
    """Draw a lnurl qr code on the e-ink screen
    """
    image, width, height, draw = init_screen(color=config.BLACK)

    qr_img = qr_img.resize((96, 96), resample=0)

    draw = ImageDraw.Draw(image)
    draw.bitmap((0, 0), qr_img, fill=config.WHITE)
    draw.text(
        (110, 25),
        messages.lnurl_qr_1,
        fill=config.WHITE,
        font=utils.create_font("freemonobold", 16),
    )
    draw.text(
        (110, 45),
        messages.lnurl_qr_2,
        fill=config.WHITE,
        font=utils.create_font("freemonobold", 16),
    )

    config.INKY.set_image(image)
    config.INKY.show()


def update_amount_screen():
    """Update the amount screen to reflect new coins inserted
    """
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (11, 10),
        str("{:,}".format(math.floor(config.SATS))) + messages.amount_screen_1,
        fill=config.BLACK,
        font=utils.create_font("dotmbold", 27),
    )
    draw.text(
        (13, 37),
        "%.2f" % round(config.FIAT, 2) + " " + config.conf["atm"]["cur"].upper(),
        fill=config.BLACK,
        font=utils.create_font("dotmbold", 19),
    )
    draw.text(
        (11, 60),
        messages.amount_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 14),
    )
    draw.text(
        (60, 60),
        messages.amount_screen_3
        + str(round(config.SATPRICE, 2))
        + messages.amount_screen_4
        + config.conf["atm"]["centname"],
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 14),
    )
    draw.text(
        (11, 75),
        messages.amount_screen_5,
        fill=config.BLACK, 
        font=utils.create_font("freemonobold", 14),
    )
    draw.text(
        (60, 75),
        messages.amount_screen_6
        + config.conf["atm"]["fee"]
        + messages.amount_screen_7
        + str(math.floor(config.SATSFEE))
        + messages.amount_screen_8,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 14),
    )

    config.INKY.set_image(image)
    config.INKY.show()


def update_lnurl_cancel_notice():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (8, 18),
        messages.lnurl_cancel_notice_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (11, 53),
        messages.lnurl_cancel_notice_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 14),
    )
    draw.text(
        (10, 73),
        messages.lnurl_cancel_notice_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 14),
    )

    config.INKY.set_image(image)
    config.INKY.show()


def update_button_fault():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (15, 10),
        messages.button_fault_1,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 18),
    )
    draw.text(
        (15, 40),
        messages.button_fault_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (15, 65),
        messages.button_fault_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )

    config.INKY.set_image(image)
    config.INKY.show()


def update_wallet_fault():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (15, 10),
        messages.wallet_fault_1,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 18),
    )
    draw.text(
        (15, 40),
        messages.wallet_fault_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (15, 65),
        messages.wallet_fault_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )

    config.INKY.set_image(image)
    config.INKY.show()


def update_blank_screen():
    image, width, height, draw = init_screen(color=config.WHITE)

    config.INKY.set_image(image)
    config.INKY.show()


def init_screen(color):
    """Prepare the screen for drawing and return the draw variables
    """
    image = Image.new("P", (config.INKY.WIDTH, config.INKY.HEIGHT), color)
    # Set width and height of screen
    width, height = image.size
    # prepare for drawing
    draw = ImageDraw.Draw(image)
    return image, width, height, draw
