#!/usr/bin/python3
import logging
import os
import sys
import time
import importlib

import RPi.GPIO as GPIO
from PIL import Image, ImageDraw

import display
import lightning
import lntxbot
import qr
import config
import utils


logger = logging.getLogger("MAIN")


def button_event(channel):
    """Registers a button push event
    """
    config.LASTPUSHES = time.time()
    config.PUSHES = config.PUSHES + 1


def coin_event(channel):
    """Registers a coin insertion event
    """
    config.LASTIMPULSE = time.time()
    config.PULSES = config.PULSES + 1
    print(config.PULSES)


def init_screen(color):
    """Prepare the screen for drawing and return the draw variables
    """
    image = Image.new("1", config.PAPIRUS.size, color)
    # Set width and height of screen
    width, height = image.size
    # prepare for drawing
    draw = ImageDraw.Draw(image)
    return image, width, height, draw


def update_amount_screen():
    """Update the amount screen to reflect new coins inserted
    """
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (13, 10),
        str(round(config.SATS)) + " sats",
        fill=config.BLACK,
        font=utils.create_font("freemono", 28),
    )
    draw.text(
        (11, 37),
        "(" + "%.2f" % round(config.FIAT, 2) + " " + config.CURRENCY + ")",
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (11, 70),
        "(1 cent = " + str(round(config.SATPRICE)) + " sats)",
        fill=config.BLACK,
        font=utils.create_font("freemono", 14),
    )

    config.PAPIRUS.display(image)
    config.PAPIRUS.partial_update()


def handle_invoice(draw, image):
    """Decode a BOLT11 invoice. Ensure that amount is correct or 0, then attempt to
    make the payment.
    """
    decode_req = lightning.decode_request(config.INVOICE)
    if decode_req == str(round(config.SATS)) or str(0):
        lightning.payout(config.SATS, config.INVOICE)
        result = lightning.last_payment(config.INVOICE)

        draw.text(
            (15, 70),
            str(result),
            fill=config.BLACK,
            font=utils.create_font("freemono", 15),
        )

        config.PAPIRUS.display(image)
        config.PAPIRUS.partial_update()
        time.sleep(1)

        if result is True:
            display.update_thankyou_screen()
        else:
            display.update_payment_failed()
            time.sleep(120)

        logger.info("Initiating restart...")
        os.execv("/home/pi/LightningATM/app.py", [""])
    else:
        print("Please show correct invoice")


def update_payout_screen():
    """Update the payout screen to reflect balance of deposited coins.
    Scan the invoice??? I don't think so!
    Handle the invoice??? I also don't think so!
    """
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.rectangle(
        (2, 2, width - 2, height - 2), fill=config.WHITE, outline=config.BLACK
    )
    draw.text(
        (15, 30),
        str(round(config.SATS)) + " sats",
        fill=config.BLACK,
        font=utils.create_font("freemono", 20),
    )
    draw.text(
        (15, 50),
        "on the way!",
        fill=config.BLACK,
        font=utils.create_font("freemono", 15),
    )

    config.PAPIRUS.display(image)
    config.PAPIRUS.update()

    # scan the invoice
    # TODO: I notice this is commented out, I presume this function should _not_ be
    #   scanning a QR code on each update?
    # config.INVOICE = qr.scan()

    # handle the invoice
    handle_invoice(draw, image)


def button_pushed():
    """Actions button pushes by number
    """
    if config.PUSHES == 1:
        if config.FIAT == 0:
            display.update_nocoin_screen()
            time.sleep(3)
            display.update_startup_screen()
        else:
            display.update_qr_request(config.SATS)
            config.INVOICE = qr.scan()
            while config.INVOICE is False:
                display.update_qr_failed()
                time.sleep(1)
                display.update_qr_request(config.SATS)
                config.INVOICE = qr.scan()
            update_payout_screen()

    if config.PUSHES == 2:
        if config.FIAT == 0:
            display.update_nocoin_screen()
            time.sleep(3)
            display.update_startup_screen()
        else:
            lntxbot.process_using_lnurl(config.SATS)

    if config.PUSHES == 3:
        display.update_lntxbot_scan()
        lntxcreds = lntxbot.scan_creds()
        utils.update_config("LNTXBOTCRED", lntxcreds)
        balance = lntxbot.get_lnurl_balance()
        display.update_lntxbot_balance(balance)
        GPIO.cleanup()
        os.execv("/home/pi/LightningATM/app.py", [""])

    if config.PUSHES == 4:
        logger.info("Button pushed three times (add coin)")
        print("Button pushed three times (add coin)")
        config.PULSES = 2

    if config.PUSHES == 5:
        logger.warning("Button pushed three times (restart)")
        print("Button pushed three times (restart)")
        GPIO.cleanup()
        os.execv("/home/pi/LightningATM/app.py", [""])

    if config.PUSHES == 6:
        display.update_shutdown_screen()
        GPIO.cleanup()
        logger.info("ATM shutdown (5 times button)")
        os.system("sudo shutdown -h now")
    config.PUSHES = 0


def coins_inserted():
    """Actions coins inserted
    """
    if config.PULSES == 2:
        config.FIAT += 0.02
        config.SATS = config.FIAT * 100 * config.SATPRICE
        logger.info("2 cents added")
        update_amount_screen()
    if config.PULSES == 3:
        config.FIAT += 0.05
        config.SATS = config.FIAT * 100 * config.SATPRICE
        logger.info("5 cents added")
        update_amount_screen()
    if config.PULSES == 4:
        config.FIAT += 0.1
        config.SATS = config.FIAT * 100 * config.SATPRICE
        logger.info("10 cents added")
        update_amount_screen()
    if config.PULSES == 5:
        config.FIAT += 0.2
        config.SATS = config.FIAT * 100 * config.SATPRICE
        logger.info("20 cents added")
        update_amount_screen()
    if config.PULSES == 6:
        config.FIAT += 0.5
        config.SATS = config.FIAT * 100 * config.SATPRICE
        logger.info("50 cents added")
        update_amount_screen()
    if config.PULSES == 7:
        config.FIAT += 1
        config.SATS = config.FIAT * 100 * config.SATPRICE
        logger.info("100 cents added")
        update_amount_screen()
    config.PULSES = 0


def monitor_coins_and_button():
    """Monitors coins inserted and buttons pushed
    """
    time.sleep(0.2)
    # Detect when coins are being inserted
    if (time.time() - config.LASTIMPULSE > 0.5) and (config.PULSES > 0):
        coins_inserted()

    # Detect if the button has been pushed
    if (time.time() - config.LASTPUSHES > 0.5) and (config.PUSHES > 0):
        button_pushed()


def setup_coin_acceptor():
    """Initialises the coin acceptor parameters
    """
    # Defining GPIO BCM Mode
    GPIO.setmode(GPIO.BCM)

    # Setup GPIO Pins for coin acceptor and button
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Setup coin interrupt channel (bouncetime for switch bounce)
    GPIO.add_event_detect(5, GPIO.RISING, callback=button_event, bouncetime=200)
    GPIO.add_event_detect(6, GPIO.FALLING, callback=coin_event)


def main():
    utils.check_epd_size()

    logger.info("Application started")

    # Check for DANGERMODE and scan credentials
    if config.DANGERMODE == "NO":
        utils.update_config("LNTXBOTCRED", "*****")
        utils.update_config("LNDMACAROON", "*****")
        print(config.LNTXBOTCRED, config.LNDMACAROON)
        importlib.reload(config)
        print(config.LNTXBOTCRED, config.LNDMACAROON)
        # config.LNTXBOTCRED = "*****"
        # config.LNDMACAROON = "*****"

    # Display startup startup_screen
    display.update_startup_screen()

    setup_coin_acceptor()

    while True:
        monitor_coins_and_button()


if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            display.update_shutdown_screen()
            GPIO.cleanup()
            logger.info("Application finished (Keyboard Interrupt)")
            sys.exit("Manually Interrupted")
        except Exception:
            logger.exception("Oh no, something bad happened! Restarting...")
            GPIO.cleanup()
            # anything else needs to happen for a clean restart?
