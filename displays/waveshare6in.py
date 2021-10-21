#!/usr/bin/python3
import datetime
import time
import math
import logging
import config
import utils

#from pathlib import Path
from displays import messages6in

from PIL import Image, ImageFont, ImageDraw

from IT8951 import constants

BLACK = 0x00
WHITE = 0xFF

logger = logging.getLogger("WS6INCH")

def update_lnurl_cancel_notice():
    """ Cancel LNURL generation, should be QR scanning selection
    """
    width, height, draw = init_screen()
    
    # English
    draw.text(
        (50, 50),
        messages6in.lnurl_cancel_notice_1,
        fill=BLACK,
        font=utils.create_font("freemonobold", 80),
    )
    draw.text(
        (50, 150),
        messages6in.lnurl_cancel_notice_2,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    draw.text(
        (50, 250),
        messages6in.lnurl_cancel_notice_3,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    # Vietnamese
    draw.text(
        (50, 400),
        messages6in.lnurl_cancel_notice_1_vi,
        fill=BLACK,
        font=utils.create_font("freemonobold", 80),
    )
    draw.text(
        (50, 500),
        messages6in.lnurl_cancel_notice_2_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    draw.text(
        (50, 600),
        messages6in.lnurl_cancel_notice_3_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    # Timing out
    draw.text(
        (50, 900),
        messages6in.lnurl_cancel_notice_timeout_en,
        fill=BLACK,
        font=utils.create_font("freemono", 60)
    )
    draw.text(
        (50, 950),
        messages6in.lnurl_cancel_notice_timeout_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 60)
    )
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)
    # show time out
    for i in range(10, 0, -1):
        draw.ellipse((1030, 910, 1130, 1010), fill=BLACK, outline=BLACK)
        draw.text(
            (1046, 910),
            "0"+ str(i) if i < 10 else str(i),
            fill=WHITE,
            font=utils.create_font("sawasdeebold", 60)
        )
        config.WAVESHARE.draw_partial(constants.DisplayModes.DU)
        draw.rectangle((1020, 900, width - 20, height - 20), fill=WHITE, outline=WHITE)
        time.sleep(1)
    #time.sleep(60)

def show_rate_screen():
    """Show the bitcoin rate
    """
    width, height, draw = init_screen()
    
    # English
    draw.text(
        (50, 50),
        messages6in.rate_screen_title_en,
        fill=BLACK,
        font=utils.create_font("freemonobold", 100)
    )
    draw.text(
        (50, 160),
        messages6in.rate_screen_1btc +
        str("{:,}".format(config.BTCPRICE)) + " " + config.conf["atm"]["cur"].upper(),
        fill=BLACK,
        font=utils.create_font("freemono", 80)
    )
    draw.text(
        (50, 250),
        messages6in.rate_screen_1sat +
        str(round(config.BTCPRICE * 0.00000001, 2)) +
        " " + config.conf["atm"]["cur"].upper(),
        fill=BLACK,
        font=utils.create_font("freemono", 80)
    )
    # Vietnamese
    draw.text(
        (50, 400),
        messages6in.rate_screen_title_vi,
        fill=BLACK,
        font=utils.create_font("freemonobold", 100)
    )
    draw.text(
        (50, 510),
        messages6in.rate_screen_1btc +
        str("{:,}".format(config.BTCPRICE).replace(",", ".")) + " " +
        config.conf["atm"]["cur"].upper(),
        fill=BLACK,
        font=utils.create_font("freemono", 80)
    )
    draw.text(
        (50, 600),
        messages6in.rate_screen_1sat +
        str("{:,}".format(round(config.BTCPRICE * 0.00000001, 2)).replace(".", ",")) +
        " " +
        config.conf["atm"]["cur"].upper(),
        fill=BLACK,
        font=utils.create_font("freemono", 80)
    )
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)
    
    # show time out
    draw.text(
        (50, 900),
        messages6in.rate_screen_expire_en,
        fill=BLACK,
        font=utils.create_font("freemono", 60)
    )
    draw.text(
        (50, 950),
        messages6in.rate_screen_expire_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 60)
    )
    config.WAVESHARE.draw_partial(constants.DisplayModes.DU)
    
    for i in range(10, 0, -1):
        draw.ellipse((1030, 910, 1130, 1010), fill=BLACK, outline=BLACK)
        draw.text(
            (1046, 910),
            "0"+ str(i) if i < 10 else str(i),
            fill=WHITE,
            font=utils.create_font("sawasdeebold", 60),
        )
        config.WAVESHARE.draw_partial(constants.DisplayModes.DU)
        draw.rectangle((1020, 900, width - 20, height - 20), fill=WHITE, outline=WHITE)
        time.sleep(1)
    
def update_restart_screen():
    """Restart screen on eInk Display
    """
    width, height, draw = init_screen()
    
    # English
    draw.text(
        (50, 50),
        messages6in.restart_screen_title_en,
        fill=BLACK,
        font=utils.create_font("freemono", 100),
    )
    draw.text(
        (50, 150),
        messages6in.restart_screen_desc_en_1,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    draw.text(
        (50, 250),
        messages6in.restart_screen_desc_en_2,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    # Vietnamese
    draw.text(
        (50, 500),
        messages6in.restart_screen_title_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 100),
    )
    draw.text(
        (50, 600),
        messages6in.restart_screen_desc_vi_1,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    draw.text(
        (50, 700),
        messages6in.restart_screen_desc_vi_2,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)

def update_startup_screen():
    """Show startup screen on eInk Display
    """
    width, height, draw = init_screen()
    
    # English
    draw.text(
        (50, 50),
        messages6in.startup_screen_welcome_en,
        fill=BLACK,
        font=utils.create_font("freemono", 120),
    )
    # Vietnamese
    draw.text(
        (50, 200),
        messages6in.startup_screen_welcome_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 120),
    )
    # draw logo
    draw_logo(draw, 414, 360)
    # Text LightningATM
    draw.text(
        (200, 400),
        messages6in.startup_screen_atm,
        fill=BLACK,
        font=utils.create_font("sawasdeebold", 170),
    )
    draw.text(
        (50, 700),
        messages6in.startup_screen_insert_bills_en,
        fill=BLACK,
        font=utils.create_font("freemono", 85),
    )
    draw.text(
        (50, 850),
        messages6in.startup_screen_insert_bills_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 85),
    )
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)

def update_qr_request():
    """ Request for QR
    """
    # initially set all white background
    width, height, draw = init_screen()
    
    # English
    draw.text(
        (50, 50),
        messages6in.qr_request_title_en,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    draw.text(
        (50, 150),
        messages6in.qr_request_title_en_2,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    # Vietnamese
    draw.text(
        (50, 300),
        messages6in.qr_request_title_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)
    
    # Draw the number of countdown
    for i in range(0, 3):
        draw.ellipse((width//2 - 60, 400, width//2 + 60, 520), fill=BLACK, outline=BLACK)
        draw.text(
            (width//2 - 26, 390),
            str(3 - i),
            fill=WHITE,
            font=utils.create_font("sawasdeebold", 90),
        )
        config.WAVESHARE.draw_partial(constants.DisplayModes.DU)
        draw.rectangle((width//2 - 100, 370, width - 20, height - 20), fill=WHITE, outline=WHITE)
        time.sleep(1)
    
    # Clear white
    draw.rectangle((0, 0, width - 1, height - 1), fill=WHITE, outline=WHITE)
    config.WAVESHARE.draw_partial(constants.DisplayModes.DU)
    
    # English
    draw.text(
        (50, 50),
        messages6in.qr_request_scanning_en,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    draw.text(
        (50, 150),
        messages6in.qr_request_for_n_sats_en.format("{:,}".format(math.floor(config.SATS))),
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    # Vietnamese
    draw.text(
        (50, 350),
        messages6in.qr_request_scanning_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    draw.text(
        (50, 450),
        messages6in.qr_request_for_n_sats_vi.format("{:,}".format(math.floor(config.SATS)).replace(",",".")),
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    config.WAVESHARE.draw_partial(constants.DisplayModes.DU)

def update_qr_failed():
    """ QR scanning failed
    """
    # initially set all white background
    width, height, draw = init_screen()
    
    # English
    draw.text(
        (60,60),
        messages6in.qr_failed_title_en,
        fill=BLACK,
        font=utils.create_font("freemonobold", 100),
    )
    draw.text(
        (60,210),
        messages6in.qr_failed_desc_en,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    # Vietnamese
    draw.text(
        (60,500),
        messages6in.qr_failed_title_vi,
        fill=BLACK,
        font=utils.create_font("freemonobold", 100),
    )
    draw.text(
        (60,650),
        messages6in.qr_failed_desc_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)

def update_payout_screen():
    """Update the payout screen to reflect balance of deposited coins.
    Scan the invoice??? I don't think so!
    """
    width, height, draw = init_screen()
    
    # English
    draw.text(
        (60, 100),
        messages6in.payout_screen_title_en.format(math.floor(config.SATS)),
        fill=BLACK,
        font=utils.create_font("freemonobold", 100),
    )
    draw.text(
        (60, 250),
        messages6in.payout_screen_title_en_2.format(str("{:,}".format(math.floor(config.SATS)))),
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    # Vietnamese
    draw.text(
        (60, 600),
        messages6in.payout_screen_title_vi.format(str("{:,}".format(math.floor(config.SATS)).replace(",","."))),
        fill=BLACK,
        font=utils.create_font("freemonobold", 100),
    )
    draw.text(
        (60, 750),
        messages6in.payout_screen_title_vi_2.format(math.floor(config.SATS)),
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)
    # scan the invoice TODO: I notice this is commented out, I presume this function should _not_ be
    #   scanning a QR code on each update? config.INVOICE = qr.scan()

def update_payment_failed():
    """ Payment failed
    """
    width, height, draw = init_screen()
    
    # English
    draw.text(
        (50, 50),
        messages6in.payment_failed_title_en,
        fill=BLACK,
        font=utils.create_font("freemonobold", 100),
    )
    draw.text(
        (50, 200),
        messages6in.payment_failed_desc_en,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    # draw logo
    draw_logo(draw, 50, 300, True)
    # Vietnamese
    draw.text(
        (50, 450),
        messages6in.payment_failed_title_vi,
        fill=BLACK,
        font=utils.create_font("freemonobold", 100),
    )
    draw.text(
        (50, 600),
        messages6in.payment_failed_desc_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    # draw logo
    draw_logo(draw, 50, 700, True)
    
    #config.WAVESHARE.draw_full(constants.DisplayModes.GC16)
    
    # Timing out
    draw.text(
        (50, 900),
        messages6in.payment_failed_timeout_en,
        fill=BLACK,
        font=utils.create_font("freemono", 60)
    )
    draw.text(
        (50, 950),
        messages6in.payment_failed_timeout_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 60)
    )
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)
    # show time out
    time_out = 10
    for i in range(time_out, 0, -1):
        draw.ellipse((1030, 910, 1130, 1010), fill=BLACK, outline=BLACK)
        draw.text(
            (1046, 910),
            "0"+ str(i) if i < 10 else str(i),
            fill=WHITE,
            font=utils.create_font("sawasdeebold", 60)
        )
        config.WAVESHARE.draw_partial(constants.DisplayModes.DU)
        draw.rectangle((1020, 900, width - 20, height - 20), fill=WHITE, outline=WHITE)
        time.sleep(1)
    
    #time.sleep(30)

def update_thankyou_screen():
    """ Thank-you screen
    """
    width, height, draw = init_screen()
    # draw logo
    draw_logo(draw, width//2 - 310, 60)
    # English
    draw.text(
        (60, 200),
        messages6in.thankyou_screen_title_en,
        fill=BLACK,
        font=utils.create_font("freemonobold", 100),
    )
    draw.text(
        (60, 350),
        messages6in.thankyou_screen_desc_en,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    
    # Vietnamese
    draw.text(
        (60, 550),
        messages6in.thankyou_screen_title_vi,
        fill=BLACK,
        font=utils.create_font("freemonobold", 100),
    )
    draw.text(
        (60, 700),
        messages6in.thankyou_screen_desc_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    
    # Timing out
    draw.text(
        (50, 900),
        messages6in.thankyou_screen_expire_en,
        fill=BLACK,
        font=utils.create_font("freemono", 60)
    )
    draw.text(
        (50, 950),
        messages6in.thankyou_screen_expire_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 60)
    )
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)
    # show time out
    for i in range(10, 0, -1):
        draw.ellipse((1030, 910, 1130, 1010), fill=BLACK, outline=BLACK)
        draw.text(
            (1046, 910),
            "0"+ str(i) if i < 10 else str(i),
            fill=WHITE,
            font=utils.create_font("sawasdeebold", 60)
        )
        config.WAVESHARE.draw_partial(constants.DisplayModes.DU)
        draw.rectangle((1020, 900, width - 20, height - 20), fill=WHITE, outline=WHITE)
        time.sleep(1)

def update_nocoin_screen():
    """ No coin screen
    """
    width, height, draw = init_screen()
    
    # English
    draw.text(
        (50, 50),
        messages6in.nocoin_screen_title_en,
        fill=BLACK,
        font=utils.create_font("freemonobold", 90),
    )
    draw.text(
        (50, 150),
        messages6in.nocoin_screen_desc_en,
        fill=BLACK,
        font=utils.create_font("freemono", 70),
    )
    # Vietnamese
    draw.text(
        (50, 300),
        messages6in.nocoin_screen_title_vi,
        fill=BLACK,
        font=utils.create_font("freemonobold", 90),
    )
    draw.text(
        (50, 400),
        messages6in.nocoin_screen_desc_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 70),
    )
    # list of accepted bills
    draw.text(
        (50, 530),
        messages6in.nocoin_screen_support_bills_en,
        fill=BLACK,
        font=utils.create_font("freemonobold", 70),
    )
    draw.text(
        (50, 630),
        messages6in.nocoin_screen_support_bills_vi,
        fill=BLACK,
        font=utils.create_font("freemonobold", 70),
    )
    bills = (10000, 20000, 50000, 100000, 200000, 500000)
    y = 680
    odd = True
    for bill in bills:
        odd = not odd
        if odd:
            x = width - 500
            draw.text(
                (x, y),
                str("{:,}".format(bill)) + " VND",
                fill=BLACK,
                font=utils.create_font("freemonobold", 60)
            )
        else:
            x = 80
            y = y + 80
            draw.text(
                (x, y),
                str("{:,}".format(bill)) + " VND",
                fill=BLACK,
                font=utils.create_font("freemonobold", 60)
            )
    
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)
    time.sleep(5)

def update_lnurl_generation():
    """ Generate LNURL
    """
    width, height, draw = init_screen()
    
    # English
    draw.text(
        (50, height//2 - 100),
        messages6in.lnurl_generation_en,
        fill=BLACK,
        font=utils.create_font("freemonobold", 80),
    )
    # Vietnamese
    draw.text(
        (50, height//2 + 100),
        messages6in.lnurl_generation_vi,
        fill=BLACK,
        font=utils.create_font("freemonobold", 80),
    )
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)

def update_shutdown_screen():
    """ Shutdown screen
    """
    width, height, draw = init_screen()

    # English
    draw.text(
        (50, 50),
        messages6in.shutdown_screen_title_en,
        fill=BLACK,
        font=utils.create_font("freemono", 120),
    )
    draw.text(
        (50, 200),
        messages6in.shutdown_screen_desc_en,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    # draw logo
    draw_logo(draw, 50, 300)
    # Vietnamese
    draw.text(
        (50, 600),
        messages6in.shutdown_screen_title_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 120),
    )
    draw.text(
        (50, 750),
        messages6in.shutdown_screen_desc_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    # draw logo
    draw_logo(draw, 50, 850)
    
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)

def update_wallet_scan():
    """ Scan the wallet QR
    """
    # initially set all white background
    width, height, draw = init_screen()

    # English
    draw.text(
        (50, 50),
        messages6in.wallet_scan_en,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    # Vietnamese
    draw.text(
        (50, 400),
        messages6in.wallet_scan_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)
    time.sleep(2)

def update_lntxbot_balance(balance):
    """ LNTXBOT success
    """
    # initially set all white background
    width, height, draw = init_screen()
    
    # English
    draw.text(
        (50, 50),
        messages6in.lntxbot_balance_title_en,
        fill=BLACK,
        font=utils.create_font("freemonobold", 100),
    )
    draw.text(
        (50, 150),
        messages6in.lntxbot_balance_desc_en,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    draw.text(
        (50, 250),
        messages6in.lntxbot_balance_n_sats.format(balance),
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    # Vietnamses
    draw.text(
        (50, 500),
        messages6in.lntxbot_balance_title_vi,
        fill=BLACK,
        font=utils.create_font("freemonobold", 100),
    )
    draw.text(
        (50, 600),
        messages6in.lntxbot_balance_desc_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    draw.text(
        (50, 700),
        messages6in.lntxbot_balance_n_sats.format(balance),
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)
    time.sleep(3)

def update_btcpay_lnd():
    """ BTC Pay success
    """
    # initially set all white background
    width, height, draw = init_screen()
    
    draw.text(
        (50, 50),
        messages6in.btcpay_lnd_title_en,
        fill=BLACK,
        font=utils.create_font("freemonobold", 100),
    )
    draw.text(
        (50, 150),
        messages6in.btcpay_lnd_desc_en,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    draw.text(
        (50, 250),
        messages6in.btcpay_lnd_wallet_en,
        fill=BLACK,
        font=utils.create_font("freemono", 80),
    )
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)
    time.sleep(3)

def wait_for_balance_update(start_balance, timeout=90):
    import lntxbot
    draw = ImageDraw.Draw(config.WAVESHARE.frame_buf)
    width, height = config.WAVESHARE.frame_buf.size
    
    start_time = time.time()
    success = False
    # loop while we wait for the balance to get updated
    i = timeout - 1
    logger.info("Start time: {}".format(start_time))
    while True and (time.time() < start_time + timeout):
        new_balance = lntxbot.get_lnurl_balance()
        draw.ellipse((1030, 910, 1130, 1010), fill=BLACK, outline=BLACK)
        draw.text(
            (1046, 910),
            "0"+ str(i) if i < 10 else str(i),
            fill=WHITE,
            font=utils.create_font("sawasdeebold", 60)
        )
        draw.rectangle((1020, 900, width - 20, height - 20), fill=WHITE, outline=WHITE)
        config.WAVESHARE.draw_partial(constants.DisplayModes.DU)
        if start_balance == new_balance:
            print("Balance: " + str(start_balance) + " (no changes)")
            #time.sleep(3)
        else:
            print(
                "Balance: " + str(start_balance) + " | New Balance:" + str(new_balance)
            )
            success = True
            break
        i-=1
        time.sleep(1)
    config.WAVESHARE.draw_partial(constants.DisplayModes.DU)
    logger.info("End time: {}".format(time.time()))
    return success

def draw_lnurl_qr(qr_img):
    """Draw a lnurl qr code on the e-ink screen
    """
    width, height, draw = init_screen()
    
    # English
    draw.text(
        (50, 50),
        messages6in.lnurl_qr_en.format(str("{:,}".format(math.floor(config.SATS)))),
        fill=BLACK,
        font=utils.create_font("freemonobold", 80)
    )
    # Vietnamese
    draw.text(
        (50, 150),
        messages6in.lnurl_qr_vi.format(str("{:,}".format(math.floor(config.SATS)).replace(",", "."))),
        fill=BLACK,
        font=utils.create_font("freemonobold", 80)
    )
    # QR
    qr_img = qr_img.resize((600, 600), resample=0)
    draw.bitmap((50, 300), qr_img, fill=BLACK)
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)

def update_payment_status(remain):
    width, height = config.WAVESHARE.frame_buf.size
    draw = ImageDraw.Draw(config.WAVESHARE.frame_buf)
    
    # Timing out
    draw.text(
        (700, 530),
        messages6in.lnurl_qr_timeout_en,
        fill=BLACK,
        font=utils.create_font("freemono", 60)
    )
    draw.text(
        (700, 610),
        messages6in.lnurl_qr_timeout_vi,
        fill=BLACK,
        font=utils.create_font("freemono", 60)
    )
    config.WAVESHARE.draw_partial(constants.DisplayModes.DU)
    draw.rectangle((1020, 900, width - 20, height - 20), fill=WHITE, outline=WHITE)
    draw.ellipse((1180, 540, 1300, 660), fill=BLACK, outline=BLACK)
    draw.text(
        (1206, 550),
        "0"+ str(remain) if remain < 10 else str(remain),
        fill=WHITE,
        font=utils.create_font("sawasdeebold", 62),
    )
    config.WAVESHARE.draw_partial(constants.DisplayModes.DU)
    

def update_amount_screen():
    """Update the amount screen to reflect new coins inserted
    """
    width, height, draw = init_screen()
    # show the date time
    dt = datetime.datetime.now()
    draw.text(
        (width - 350, 40),
        dt.strftime("%Y/%b/%d"),
        fill=BLACK,
        font=utils.create_font("sawasdee", 50)
    )
    draw.text(
        (width - 260, 90),
        dt.strftime("%H:%M"),
        fill=BLACK,
        font=utils.create_font("sawasdee", 50)
    )
    # sats amount
    draw.text(
        (60, 10),
        str("{:,}".format(math.floor(config.SATS))) + " " + messages6in.amount_screen_sats,
        fill=BLACK,
        font=utils.create_font("sawasdeebold", 100),
    )
    # vnd amount
    draw.text(
        (60, 130),
        str("{:,}".format(round(config.FIAT, 2))) + " " + config.conf["atm"]["cur"].upper(),
        fill=BLACK,
        font=utils.create_font("sawasdeebold", 80),
    )
    # Rate
    draw.text(
        (60, 300),
        messages6in.amount_screen_rate,
        fill=BLACK,
        font=utils.create_font("freemonobold", 70),
    )
    draw.text(
        (120, 370),
        messages6in.amount_screen_rate_line.format(str(round((config.BTCPRICE / 100000000), 2)) + " " + config.conf["atm"]["cur"].upper()),
        fill=BLACK,
        font=utils.create_font("freemono", 70),
    )

    # Fee
    draw.text(
        (60, 470),
        messages6in.amount_screen_fee,
        fill=BLACK,
        font=utils.create_font("freemonobold", 70),
    )
    draw.text(
        (120, 540),
        messages6in.amount_screen_fee_line.format(config.conf["atm"]["fee"], str(math.floor(config.SATSFEE))),
        fill=BLACK,
        font=utils.create_font("freemono", 70),
    )
    # description
    draw.text(
        (60, 650),
        messages6in.amount_screen_desc_en_1,
        fill=BLACK,
        font=utils.create_font("sawasdee", 60),
    )
    draw.text(
        (60, 730),
        messages6in.amount_screen_desc_en_2,
        fill=BLACK,
        font=utils.create_font("sawasdee", 60),
    )
    draw.text(
        (60, 850),
        messages6in.amount_screen_desc_vi_1,
        fill=BLACK,
        font=utils.create_font("freemono", 60),
    )
    draw.text(
        (60, 930),
        messages6in.amount_screen_desc_vi_2,
        fill=BLACK,
        font=utils.create_font("freemono", 60),
    )
    
    config.WAVESHARE.draw_full(constants.DisplayModes.GC16)
    
def draw_logo(draw, x=0, y=0, lite=False):
    """ Draw Future.Travel logo
    """
    path = config.home
    if lite==True:
        img_path = path + "/LightningATM/resources/images/company-logo/logo-future-travel-lite.jpg"
    else:
        img_path = path + "/LightningATM/resources/images/company-logo/logo-future-travel-black.jpg"
    img = Image.open(img_path)
    config.WAVESHARE.frame_buf.paste(img, [ x, y, x + img.size[0], y + img.size[1] ])

def init_screen():
    """Prepare the screen for drawing and return the draw variables
    """
    # clear to white
    config.WAVESHARE.clear()
    # Set width and height of screen
    width, height = config.WAVESHARE.frame_buf.size
    # prepare for drawing
    draw = ImageDraw.Draw(config.WAVESHARE.frame_buf)
    # draw the border
    draw.rectangle(
        (10, 10, width - 10, height - 10), fill=WHITE, outline=BLACK
    )
    return width, height, draw
    
def print_system_info():
    epd = config.WAVESHARE.epd

    print('*** System info:')
    print('  display size: {}x{}'.format(epd.width, epd.height))
    print('  img buffer address: {:X}'.format(epd.img_buf_address))
    print('  firmware version: {}'.format(epd.firmware_version))
    print('  LUT version: {}'.format(epd.lut_version))


def _place_text(text, fontsize=80, x_offset=0, y_offset=0):
    '''
    Put some centered text at a location on the image.
    '''
    draw = ImageDraw.Draw(config.WAVESHARE.frame_buf)

    font=utils.create_font("freemono", fontsize)
    img_width, img_height = config.WAVESHARE.frame_buf.size
    text_width, _ = font.getsize(text)
    text_height = fontsize

    draw_x = (img_width - text_width)//2 + x_offset
    draw_y = (img_height - text_height)//2 + y_offset

    draw.text((draw_x, draw_y), text, font=font)
