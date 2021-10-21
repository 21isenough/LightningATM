#!/usr/bin/python3

import time
import math

import config
import utils

from displays import messages

from PIL import Image, ImageFont, ImageDraw

def update_lnurl_cancel_notice():
    image, width, height, draw = init_screen(color=config.WHITE)
    # English
    draw.text(
        (5, 12),
        messages.lnurl_cancel_notice_1,
        fill=config.BLACK,
        font=utils.create_font("sawasdee", 22),
    )
    draw.text(
        (5, 42),
        messages.lnurl_cancel_notice_2,
        fill=config.BLACK,
        font=utils.create_font("sawasdee", 16),
    )
    draw.text(
        (4, 62),
        messages.lnurl_cancel_notice_3,
        fill=config.BLACK,
        font=utils.create_font("sawasdee", 16),
    )
    # Vietnamese
    draw.text(
        (5, 90),
        messages.lnurl_cancel_notice_1_vi,
        fill=config.BLACK,
        font=utils.create_font("freemono", 22),
    )
    draw.text(
        (5, 120),
        messages.lnurl_cancel_notice_2_vi,
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )
    draw.text(
        (4, 140),
        messages.lnurl_cancel_notice_3_vi,
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )
    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))

def show_rate_screen():
    """Show the bitcoin rate
    """
    image, width, height, draw = init_screen(color=config.WHITE)
    # English
    draw.text(
        (8, 10),
        messages.rate_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 24)
    )
    draw.text(
        (8, 40),
        messages.rate_screen_2 +
        str("{:,}".format(config.BTCPRICE)) +
        " " + config.conf["atm"]["cur"].upper(),
        fill=config.BLACK,
        font=utils.create_font("freemono", 18)
    )
    draw.text(
        (8, 60),
        messages.rate_screen_3 +
        str(round(config.BTCPRICE * 0.00000001, 2)) +
        " " + config.conf["atm"]["cur"].upper(),
        fill=config.BLACK,
        font=utils.create_font("freemono", 18)
    )
    # Vietnamese
    draw.text(
        (8, 90),
        messages.rate_screen_4,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 24)
    )
    draw.text(
        (8, 120),
        messages.rate_screen_2 +
        str("{:,}".format(config.BTCPRICE).replace(",", ".")) + " " +
        config.conf["atm"]["cur"].upper(),
        fill=config.BLACK,
        font=utils.create_font("freemono", 18)
    )
    draw.text(
        (8, 140),
        messages.rate_screen_3 +
        str("{:,}".format(round(config.BTCPRICE * 0.00000001, 2)).replace(".", ",")) +
        " " +
        config.conf["atm"]["cur"].upper(),
        fill=config.BLACK,
        font=utils.create_font("freemono", 18)
    )
    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_restart_screen():
    """Restart screen on eInk Display
    """
    image, width, height, draw = init_screen(color=config.WHITE)
    # English
    draw.text(
        (10, 10),
        messages.restart_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    draw.text(
        (10, 40),
        messages.restart_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 22),
    )
    draw.text(
        (10, 60),
        messages.restart_screen_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 22),
    )
    # Vietnamese
    draw.text(
        (10, 90),
        messages.restart_screen_4,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    draw.text(
        (10, 120),
        messages.restart_screen_5,
        fill=config.BLACK,
        font=utils.create_font("freemono", 22),
    )
    draw.text(
        (10, 140),
        messages.restart_screen_6,
        fill=config.BLACK,
        font=utils.create_font("freemono", 22),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))

def update_startup_screen():
    """Show startup screen on eInk Display
    """
    image, width, height, draw = init_screen(color=config.WHITE)
    draw.text(
        (10, 10),
        messages.startup_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    draw.text(
        (10, 35),
        messages.startup_screen_4,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    draw.text(
        (10, 60),
        messages.startup_screen_2,
        fill=config.BLACK,
        font=utils.create_font("sawasdee", 36),
    )
    draw.text(
        (10, 120),
        messages.startup_screen_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )
    draw.text(
        (10, 140),
        messages.startup_screen_5,
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
    # English
    draw.text(
        (30, 10),
        messages.qr_request_1,
        fill=config.BLACK,
        font=utils.create_font("sawasdee", 24),
    )
    draw.text(
        (30, 30),
        messages.qr_request_2,
        fill=config.BLACK,
        font=utils.create_font("sawasdee", 24),
    )
    # Vietnamese
    draw.text(
        (30, 65),
        messages.qr_request_1_vi,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    draw.text(
        (30, 85),
        messages.qr_request_2_vi,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))
    # Draw the number of countdown
    for i in range(0, 3):
        draw.text(
            (120, 100),
            str(3 - i),
            fill=config.BLACK,
            font=utils.create_font("sawasdee", 55),
        )
        config.WAVESHARE.init()
        config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))
        draw.rectangle((100, 110, width - 4, height - 4), fill=config.WHITE, outline=config.WHITE)
        time.sleep(0.5)
    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    # English
    draw.text(
        (20, 15),
        messages.qr_request_3,
        fill=config.BLACK,
        font=utils.create_font("sawasdee", 25),
    )
    draw.text(
        (20, 45),
        messages.qr_request_4 + str(math.floor(config.SATS)) + messages.qr_request_5,
        fill=config.BLACK,
        font=utils.create_font("sawasdee", 25),
    )
    # Vietnamese
    draw.text(
        (20, 90),
        messages.qr_request_3_vi,
        fill=config.BLACK,
        font=utils.create_font("freemono", 25),
    )
    draw.text(
        (20, 120),
        messages.qr_request_4_vi + str(math.floor(config.SATS)) + messages.qr_request_5_vi,
        fill=config.BLACK,
        font=utils.create_font("freemono", 25),
    )
    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))

def update_qr_failed():
    # initially set all white background
    image, width, height, draw = init_screen(color=config.WHITE)
    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    # English
    draw.text(
        (25, 30),
        messages.qr_failed_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 28),
    )
    draw.text(
        (30, 50),
        messages.qr_failed_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 28),
    )
    # Vietnamese
    draw.text(
        (25,90),
        messages.qr_failed_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 28),
    )
    draw.text(
        (30, 110),
        messages.qr_failed_4,
        fill=config.BLACK,
        font=utils.create_font("freemono", 28),
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
    # English
    draw.text(
        (20, 30),
        str(math.floor(config.SATS)) + messages.payout_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 30),
    )
    draw.text(
        (20, 60),
        messages.payout_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    # Vietnamese
    draw.text(
        (20, 110),
        str(math.floor(config.SATS)) + messages.payout_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 30),
    )
    draw.text(
        (20, 140),
        messages.payout_screen_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))
    # scan the invoice TODO: I notice this is commented out, I presume this function should _not_ be
    #   scanning a QR code on each update? config.INVOICE = qr.scan()

def update_payment_failed():
    image, width, height, draw = init_screen(color=config.WHITE)
    # English
    draw.text(
        (5, 10),
        messages.payment_failed_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 22),
    )
    draw.text(
        (5, 40),
        messages.payment_failed_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )
    draw.text(
        (5, 60),
        messages.payment_failed_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )
    # Vietnamese
    draw.text(
        (5, 90),
        messages.payment_failed_1_vi,
        fill=config.BLACK,
        font=utils.create_font("freemono", 22),
    )
    draw.text(
        (5, 120),
        messages.payment_failed_2_vi,
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )
    draw.text(
        (5, 140),
        messages.payment_failed_3_vi,
        fill=config.BLACK,
        font=utils.create_font("freemono", 16),
    )
    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))

def update_thankyou_screen():
    image, width, height, draw = init_screen(color=config.WHITE)
    # English
    draw.text(
        (10, 5),
        messages.thankyou_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    draw.text(
        (10, 30),
        messages.thankyou_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    draw.text(
        (10, 60),
        messages.thankyou_screen_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    # Vietnamese
    draw.text(
        (10, 90),
        messages.thankyou_screen_4,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    draw.text(
        (10, 115),
        messages.thankyou_screen_5,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    draw.text(
        (10, 145),
        messages.thankyou_screen_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))
    time.sleep(5)


def update_nocoin_screen():
    image, width, height, draw = init_screen(color=config.WHITE)
    # English
    draw.text(
        (20, 10),
        messages.nocoin_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 24),
    )
    draw.text(
        (50, 40),
        messages.nocoin_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 22),
    )
    draw.text(
        (50, 60),
        messages.nocoin_screen_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 22),
    )
    # Vietnamese
    draw.text(
        (20, 90),
        messages.nocoin_screen_4,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 24),
    )
    draw.text(
        (50, 120),
        messages.nocoin_screen_5,
        fill=config.BLACK,
        font=utils.create_font("freemono", 22),
    )
    draw.text(
        (50, 140),
        messages.nocoin_screen_6,
        fill=config.BLACK,
        font=utils.create_font("freemono", 22),
    )

    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_lnurl_generation():
    image, width, height, draw = init_screen(color=config.WHITE)
    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    # English
    draw.text(
        (40, 35),
        messages.lnurl_generation_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    draw.text(
        (20, 60),
        messages.lnurl_generation_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    # Vietnamese
    draw.text(
        (40, 95),
        messages.lnurl_generation_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    draw.text(
        (20, 120),
        messages.lnurl_generation_4,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))

def update_shutdown_screen():
    image, width, height, draw = init_screen(color=config.WHITE)
    # English
    draw.text(
        (20, 10),
        messages.shutdown_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    draw.text(
        (20, 40),
        messages.shutdown_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (20, 60),
        messages.shutdown_screen_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    # Vietnamese
    draw.text(
        (20, 90),
        messages.shutdown_screen_4,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    draw.text(
        (20, 120),
        messages.shutdown_screen_5,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (20, 140),
        messages.shutdown_screen_6,
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
    # English
    draw.text(
        (10, 10),
        messages.wallet_scan_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 25),
    )
    draw.text(
        (10, 30),
        messages.wallet_scan_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 25),
    )
    draw.text(
        (10, 50),
        messages.wallet_scan_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 25),
    )
    # Vietnamese
    draw.text(
        (10, 80),
        messages.wallet_scan_4,
        fill=config.BLACK,
        font=utils.create_font("freemono", 25),
    )
    draw.text(
        (10, 100),
        messages.wallet_scan_5,
        fill=config.BLACK,
        font=utils.create_font("freemono", 25),
    )
    draw.text(
        (10, 120),
        messages.wallet_scan_6,
        fill=config.BLACK,
        font=utils.create_font("freemono", 25),
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
    # English
    draw.text(
        (50, 15),
        messages.lntxbot_balance_1,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 26),
    )
    draw.text(
        (10, 45),
        messages.lntxbot_balance_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (45, 65),
        str("{:,}".format(balance)) + messages.lntxbot_balance_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
    )
    # Vietnamses
    draw.text(
        (50, 90),
        messages.lntxbot_balance_4,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 26),
    )
    draw.text(
        (10, 125),
        messages.lntxbot_balance_5,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (45, 145),
        str("{:,}".format(balance)) + messages.lntxbot_balance_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 24),
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
        (50, 20),
        messages.btcpay_lnd_1,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 26),
    )
    draw.text(
        (10, 55),
        messages.btcpay_lnd_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (15, 80),
        messages.btcpay_lnd_3,
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))
    time.sleep(3)

def draw_lnurl_qr(qr_img):
    """Draw a lnurl qr code on the e-ink screen
    """
    image, width, height, draw = init_screen(color=config.WHITE)
    qr_img = qr_img.resize((160, 160), resample=0)
    draw = ImageDraw.Draw(image)
    draw.bitmap((2, 8), qr_img, fill=config.BLACK)
    # English
    draw.text(
        (165, 16),
        messages.lnurl_qr_1,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 18)
    )
    draw.text(
        (165, 31),
        messages.lnurl_qr_2,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 18)
    )
    # Show the satoshis
    draw.text(
        (170, 75),
        str("{:,}".format(math.floor(config.SATS))),
        fill=config.BLACK,
        font=utils.create_font("freemono", 18)
    )
    draw.text(
        (165, 100),
        messages.amount_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18)
    )
    # Vietnamese
    draw.text(
        (165, 131),
        messages.lnurl_qr_3,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 18)
    )
    draw.text(
        (165, 146),
        messages.lnurl_qr_4,
        fill=config.BLACK,
        font=utils.create_font("freemonobold", 18)
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
        (11, 15),
        str("{:,}".format(math.floor(config.SATS))) + messages.amount_screen_1,
        fill=config.BLACK,
        font=utils.create_font("dotmbold", 30),
    )
    draw.text(
        (12, 45),
        str("{:,}".format(round(config.FIAT, 2))) + " " + config.conf["atm"]["cur"].upper(),
        fill=config.BLACK,
        font=utils.create_font("dotmbold", 25),
    )
    # Rate
    draw.text(
        (11, 70),
        messages.amount_screen_2,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    # Rate: 1 Dong = x sats
    draw.text(
        (26, 90),
        " 1 sat = "
        + str(round(config.BTCPRICE / 100000000, 2)) + " "
        + config.conf["atm"]["cur"].upper(),
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )

    #draw.text(
    #    (60, 70),
    #    messages.amount_screen_3
    #    + str(math.floor(config.SATPRICE))
    #    + messages.amount_screen_4
    #    + config.conf["atm"]["centname"],
    #    fill=config.BLACK,
    #    font=utils.create_font("freemono", 18),
    #)

    # Fee
    draw.text(
        (11, 110),
        messages.amount_screen_5,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    draw.text(
        (70, 130),
        config.conf["atm"]["fee"]
        + messages.amount_screen_7
        + str(math.floor(config.SATSFEE))
        + messages.amount_screen_1,
        fill=config.BLACK,
        font=utils.create_font("freemono", 18),
    )
    config.WAVESHARE.init()
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))

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
