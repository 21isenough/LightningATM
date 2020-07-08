#!/usr/bin/python3

import time
import math

import config
import utils

from displays import messages

from PIL import Image, ImageFont, ImageDraw


def update_startup_screen():
    """Show startup screen on eInk Display
    """
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (18, 13),
        "Welcome to the",
        fill=config.BLACK,
        font=utils.create_font("freemono", 25),
    )
    draw.text(
        (12, 30),
        "LightningATM",
        fill=config.BLACK,
        font=utils.create_font("sawasdee", 37),
    )
    draw.text(
        (9, 92),
        "- please insert coins -",
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_qr_request():
    # initially set all white background
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (34, 10),
        "Please scan",
        fill=config.BLACK,
        font=utils.create_font("freemono", 25),
    )
    draw.text(
        (10, 30),
        "your invoice in",
        fill=config.BLACK,
        font=utils.create_font("freemono", 25),
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.displayPartBaseImage(config.WAVESHARE.getbuffer(image))

    for i in range(0, 3):
        draw.text(
            (90, 55),
            str(3 - i),
            fill=config.BLACK,
            font=utils.create_font("freemono", 58),
        )
        config.WAVESHARE.init(config.WAVESHARE.PART_UPDATE)
        config.WAVESHARE.displayPartial(config.WAVESHARE.getbuffer(image))
        draw.rectangle((75, 50, 115, 90), fill=config.WHITE, outline=config.WHITE)
        time.sleep(0.5)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (32, 15),
        "Scanning...",
        fill=config.BLACK,
        font=utils.create_font("freemono", 28),
    )
    draw.text(
        (22, 40),
        "for " + str(math.floor(config.SATS)) + " sats.",
        fill=config.BLACK,
        font=utils.create_font("freemono", 28),
    )
    config.WAVESHARE.init(config.WAVESHARE.PART_UPDATE)
    config.WAVESHARE.displayPartial(config.WAVESHARE.getbuffer(image))


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
        font=utils.create_font("freemono", 28),
    )
    draw.text(
        (25, 50),
        messages.qr_failed_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 28),
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
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
        (15, 30),
        str(math.floor(config.SATS)) + " sats",
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (15, 50),
        "on the way!",
        fill=config.BLACK,
        font=utils.create_font("freemono", 15),
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))

    # scan the invoice
    # TODO: I notice this is commented out, I presume this function should _not_ be
    #   scanning a QR code on each update?
    # config.INVOICE = qr.scan()


def update_payment_failed():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (15, 10),
        "Payment failed!",
        fill=config.BLACK,
        font=utils.create_font("freemono", 19),
    )
    draw.text(
        (25, 45),
        "Please contact",
        fill=config.BLACK,
        font=utils.create_font("freemono", 17),
    )
    draw.text(
        (45, 65), "operator.", fill=config.BLACK, font=utils.create_font("freemono", 17)
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_thankyou_screen():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (15, 10),
        "Enjoy your new",
        fill=config.BLACK,
        font=utils.create_font("freemono", 19),
    )
    draw.text(
        (40, 35),
        "satoshis!!",
        fill=config.BLACK,
        font=utils.create_font("freemono", 19),
    )
    draw.text(
        (15, 70),
        "#bitcoin #lightning",
        fill=config.BLACK,
        font=utils.create_font("freemono", 14),
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))
    time.sleep(5)


def update_nocoin_screen():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (15, 10),
        "No coins added!",
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 18),
    )
    draw.text(
        (30, 40),
        "Please add",
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (30, 65),
        "coins first",
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_lnurl_generation():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (30, 20),
        "Generating",
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (10, 40),
        "QR code to scan",
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_shutdown_screen():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (20, 10),
        "ATM turned off!",
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (25, 45),
        "Please contact",
        fill=config.BLACK,
        font=utils.create_font("freemono", 17),
    )
    draw.text(
        (45, 65), "operator.", fill=config.BLACK, font=utils.create_font("freemono", 17)
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_wallet_scan():
    # initially set all white background
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (35, 20),
        "Please scan",
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (33, 40),
        "your wallet",
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (35, 60),
        "credentials.",
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
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
        "Success!!",
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 20),
    )
    draw.text(
        (10, 45),
        "Your current balance:",
        fill=config.BLACK,
        font=utils.create_font("freemono", 15),
    )
    draw.text(
        (45, 65),
        str("{:,}".format(balance)) + " sats",
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))
    time.sleep(3)


def update_btcpay_lnd():
    # initially set all white background
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (45, 15),
        "Success!!",
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 20),
    )
    draw.text(
        (10, 45),
        "Successfuly scanned",
        fill=config.BLACK,
        font=utils.create_font("freemono", 15),
    )
    draw.text(
        (15, 65),
        "BTCPay LND Wallet.",
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))
    time.sleep(3)


def draw_lnurl_qr(qr_img):
    """Draw a lnurl qr code on the e-ink screen
    """
    image, width, height, draw = init_screen(color=config.BLACK)

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

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_amount_screen():
    """Update the amount screen to reflect new coins inserted
    """
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (11, 10),
        str("{:,}".format(math.floor(config.SATS))) + " sats",
        fill=config.BLACK,
        font=utils.create_font("freemono", 27),
    )
    draw.text(
        (13, 37),
        "%.2f" % round(config.FIAT, 2) + " " + config.conf["atm"]["cur"].upper(),
        fill=config.BLACK,
        font=utils.create_font("freemono", 19),
    )
    draw.text(
        (11, 60), "Rate", fill=config.BLACK, font=utils.create_font("freemono", 14),
    )
    draw.text(
        (60, 60),
        "= "
        + str(math.floor(config.SATPRICE))
        + " sats/"
        + config.conf["atm"]["centname"],
        fill=config.BLACK,
        font=utils.create_font("freemono", 14),
    )
    draw.text(
        (11, 75), "Fee", fill=config.BLACK, font=utils.create_font("freemono", 14),
    )
    draw.text(
        (60, 75),
        "= "
        + config.conf["atm"]["fee"]
        + "% ("
        + str(math.floor(config.SATSFEE))
        + " sats)",
        fill=config.BLACK,
        font=utils.create_font("freemono", 14),
    )

    if config.COINCOUNT == 1:
        config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
        config.WAVESHARE.displayPartBaseImage(config.WAVESHARE.getbuffer(image))
    else:
        config.WAVESHARE.init(config.WAVESHARE.PART_UPDATE)
        config.WAVESHARE.displayPartial(config.WAVESHARE.getbuffer(image))


def update_blank_screen():
    image, width, height, draw = init_screen(color=config.WHITE)

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
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
