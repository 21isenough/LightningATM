#!/usr/bin/python3
import logging
import os
import sys
import time

import RPi.GPIO as GPIO
from PIL import Image, ImageDraw

import display
import lightning
import lntxbot
import qr
import config
import utils


logger = logging.getLogger("MAIN")


def softreset():
    """Displays startup screen and deletes fiat amount
    """
    config.SATS = 0
    config.FIAT = 0
    display.update_startup_screen()
    logger.info("Softreset executed")


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


def handle_invoice(draw, image):
    """Decode a BOLT11 invoice. Ensure that amount is correct or 0, then attempt to
    make the payment.
    """
    decode_req = lightning.decode_request(config.INVOICE)
    if decode_req in (round(config.SATS), 0):
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

        logger.info("Initiating softreset...")
    else:
        print("Please show correct invoice")


def update_payout_screen():
    """Update the payout screen to reflect balance of deposited coins.
    Scan the invoice??? I don't think so!
    """
    image, width, height, draw = display.init_screen(color=config.WHITE)

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
        """If no coins inserted, update the screen.
        If coins inserted, scan a qr code for the exchange amount
        """
        if config.FIAT == 0:
            display.update_nocoin_screen()
            time.sleep(3)
            display.update_startup_screen()
        else:
            display.update_qr_request()
            config.INVOICE = qr.scan()
            while config.INVOICE is False:
                display.update_qr_failed()
                time.sleep(1)
                display.update_qr_request()
                config.INVOICE = qr.scan()
            update_payout_screen()
            softreset()

    if config.PUSHES == 2:
        """If no coins inserted, update the screen.
        If coins are inserted, return a lnurl for the exchange amount
        """
        if config.FIAT == 0:
            display.update_nocoin_screen()
            time.sleep(3)
            display.update_startup_screen()
        else:
            lntxbot.process_using_lnurl(config.SATS)
            # Softreset and startup screen
            softreset()

    if config.PUSHES == 3:
        """Store new lntxbot credential via a QR code scan
        """
        display.update_lntxbot_scan()

        # scan the credentials
        lntxcreds = lntxbot.scan_creds()
        print(lntxcreds)

        # save them to the current config
        config.update_config("lntxbot", "creds", lntxcreds)
        config.get_config_file()

        # return the current balance to the user on the screen
        balance = lntxbot.get_lnurl_balance()
        display.update_lntxbot_balance(balance)
        softreset()

    if config.PUSHES == 4:
        """Simulates adding a coin
        """
        logger.info("Button pushed four times (add coin)")
        print("Button pushed four times (add coin)")
        config.PULSES = 2

    if config.PUSHES == 5:
        """Restarts the application
        """
        logger.warning("Button pushed five times (restart)")
        print("Button pushed five times (restart)")
        GPIO.cleanup()
        utils.softreset()

    if config.PUSHES == 6:
        """Shutdown the host machine
        """
        display.update_shutdown_screen()
        GPIO.cleanup()
        logger.warning("ATM shutdown (6 times button)")
        os.system("sudo shutdown -h now")
    config.PUSHES = 0


def coins_inserted():
    """Actions coins inserted
    """
    if config.PULSES == 2:
        config.FIAT += 0.02
        config.SATS = config.FIAT * 100 * config.SATPRICE
        logger.info("2 cents added")
        display.update_amount_screen()
    if config.PULSES == 3:
        config.FIAT += 0.05
        config.SATS = config.FIAT * 100 * config.SATPRICE
        logger.info("5 cents added")
        display.update_amount_screen()
    if config.PULSES == 4:
        config.FIAT += 0.1
        config.SATS = config.FIAT * 100 * config.SATPRICE
        logger.info("10 cents added")
        display.update_amount_screen()
    if config.PULSES == 5:
        config.FIAT += 0.2
        config.SATS = config.FIAT * 100 * config.SATPRICE
        logger.info("20 cents added")
        display.update_amount_screen()
    if config.PULSES == 6:
        config.FIAT += 0.5
        config.SATS = config.FIAT * 100 * config.SATPRICE
        logger.info("50 cents added")
        display.update_amount_screen()
    if config.PULSES == 7:
        config.FIAT += 1
        config.SATS = config.FIAT * 100 * config.SATPRICE
        logger.info("100 cents added")
        display.update_amount_screen()
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
    """Initialises the coin acceptor parameters and sets up a callback for button pushes
    and coin inserts.
    """
    # Defining GPIO BCM Mode
    GPIO.setmode(GPIO.BCM)

    # Setup GPIO Pins for coin acceptor and button
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Setup coin interrupt channel (bouncetime for switch bounce)
    GPIO.add_event_detect(5, GPIO.RISING, callback=button_event, bouncetime=200)
    GPIO.add_event_detect(6, GPIO.FALLING, callback=coin_event)


def check_dangermode():
    """Check for DANGERMODE and wipe any saved credentials if off"
    """
    # if dangermode is NOT on
    if config.conf["atm"]["dangermode"].lower() != "on":
        logger.warning("DANGERMODE off")

        # wipe any saved values from the config by saving an empty value to it
        config.update_config("lntxbot", "creds", "")
        config.update_config("lnd", "macaroon", "")
        config.update_config("atm", "activewallet", "")

        # get the static dict from within the conf and overwrite it to config.conf
        config.conf = config.conf._sections

        # get new lntxbot creds from qr code scan
        print("Scan lntxbot creds now\n")
        print("            +---+")
        print("+-----------+---+")
        print("|      .-.      |")
        print("|     (   )     |")
        print("|      `-'      |")
        print("+---------------+\n")
        time.sleep(2)
        try:
            config.conf["lntxbot"]["creds"] = lntxbot.scan_creds()
            logger.info("Credentials saved in volatile memory (deleted after reboot)")
        except utils.ScanError:
            logger.error("Error scanning lntxbot creds with dangermode off")
            return
    else:
        logger.info("DANGERMODE on. Loading values from config.ini...")
        # config.check_config()


def main():
    utils.check_epd_size()
    logger.info("Application started")

    # Checks dangemode and start scanning for credentials
    # Only activate once software ready for it
    # check_dangermode()

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
            os.execv("/home/pi/LightningATM/app.py", [""])
