#!/usr/bin/python3

import logging
import os
import sys
import time
import math

import RPi.GPIO as GPIO

import config
import lndrest
import lntxbot
import qr

import utils
import importlib

display_config = config.conf["atm"]["display"]
display = getattr(__import__("displays", fromlist=[display_config]), display_config)

led = "off"
logger = logging.getLogger("MAIN")


def softreset():
    """Displays startup screen and deletes fiat amount
    """
    global led
    # Inform about coin, bill and sat amounts
    if config.COINCOUNT > 0:
        logger.info("Last payment:")
        logger.info("%s Coin(s), XX Bill(s), %s Sats", config.COINCOUNT, config.SATS)

    config.SATS = 0
    config.FIAT = 0
    config.COINCOUNT = 0
    config.PUSHES = 0
    # Turn off button LED
    GPIO.output(13, GPIO.LOW)
    led = "off"

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


def button_pushed():
    """Actions button pushes by number
    """
    if config.PUSHES == 1:
        """If no coins inserted, update the screen.
        If coins inserted, scan a qr code for the exchange amount
        """

        if not config.conf["atm"]["activewallet"]:
            logger.error("No wallet has been configured for the ATM.")
            logger.error("Please configure your Lightning Wallet first.")
            # Add "no wallet setup" message

            # Softreset and startup screen
            softreset()
            return

        if config.FIAT == 0:
            display.update_nocoin_screen()
            time.sleep(3)
            display.update_startup_screen()
            return

        lnurlproxy = config.conf["lnurl"]["lnurlproxy"]
        activewallet = config.conf["atm"]["activewallet"]
        # Determine if LNURL Withdrawls are possible
        if lnurlproxy == "active" or activewallet == "lntxbot":
            # 1. Ask if wallet supports LNURL
            # 2. Offer to cancel and switch to normal scan
            # 3. Process payment
            if activewallet == "lntxbot":
                display.update_lnurl_cancel_notice()
                time.sleep(5)
                if config.PUSHES == 1:
                    # Process LNURL
                    logger.info("LNURL process stared")
                    lntxbot.process_using_lnurl(config.SATS)
                    softreset()
                    return
                if config.PUSHES > 1:
                    # Process QR code scan
                    logger.info("QR scan process started")
                    display.update_qr_request()
                    config.INVOICE = qr.scan_attempts(4)
                    display.update_payout_screen()
                    lntxbot.payout(config.SATS, config.INVOICE)
                    softreset()
                    return

            if lnurlproxy == "active":
                display.update_lnurl_cancel_notice()
                time.sleep(5)
                if config.PUSHES == 1:
                    # Process LNURL
                    # Only implemented for LND BTCPay so far
                    import requests, json, qrcode

                    request_url = config.conf["lnurl"]["lnurlproxyurl"]
                    data = {"amount": config.SATS}

                    response = requests.post(request_url, json=data)

                    qr_img = utils.generate_lnurl_qr(response.json()["lnurl"])
                    # TODO Adjust size according to screen used
                    qr_img = qr_img.resize((122, 122), resample=0)

                    # draw the qr code on the e-ink screen
                    display.draw_lnurl_qr(qr_img)
                    invoice = requests.get(response.json()["callback"])

                    config.INVOICE = invoice.json()["invoice"]
                    lndrest.handle_invoice()
                    softreset()
                    return
                if config.PUSHES > 1:
                    # Process QR code scan
                    # Only implemented for LND BTCPay so far
                    display.update_qr_request()
                    qrcode = qr.scan()
                    config.INVOICE = lndrest.evaluate_scan(qrcode)
                    while config.INVOICE is False:
                        display.update_qr_failed()
                        time.sleep(1)
                        display.update_qr_request()
                        qrcode = qr.scan()
                        config.INVOICE = lndrest.evaluate_scan(qrcode)
                    display.update_payout_screen()
                    lndrest.handle_invoice()
                    softreset()
                    return
        elif config.conf["atm"]["activewallet"] == "btcpay_lnd":
            # Process QR code scan
            # Only implemented for LND BTCPay so far
            logger.info("No option for LNURL. Continue with scan...")
            display.update_qr_request()
            qrcode = qr.scan()
            config.INVOICE = lndrest.evaluate_scan(qrcode)
            while config.INVOICE is False:
                display.update_qr_failed()
                time.sleep(1)
                display.update_qr_request()
                qrcode = qr.scan()
                config.INVOICE = lndrest.evaluate_scan(qrcode)
            display.update_payout_screen()
            lndrest.handle_invoice()
            softreset()
            return
        else:
            logger.error("No valid wallet configured")

    if config.PUSHES == 3:
        """Scan and store new wallet credentials
        """
        # Delete current wallet flag and credentials
        config.update_config("atm", "activewallet", "")
        config.update_config("lntxbot", "creds", "")
        config.update_config("lnd", "macaroon", "")

        display.update_wallet_scan()
        qr.scan_credentials()
        importlib.reload(config)

        if config.conf["atm"]["activewallet"] == "btcpay_lnd":
            display.update_btcpay_lnd()
        elif config.conf["atm"]["activewallet"] == "lntxbot":
            balance = lntxbot.get_lnurl_balance()
            display.update_lntxbot_balance(balance)
        else:
            logger.error("Saving of wallet credentials failed.")

        softreset()

    if config.PUSHES == 4:
        """Simulates adding a coin (for testing)
        """
        logger.info("Button pushed four times (add coin)")
        print("Button pushed four times (add coin)")
        config.PULSES = 2

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
    global led

    if config.FIAT == 0:
        config.BTCPRICE = utils.get_btc_price(config.conf["atm"]["cur"])
        config.SATPRICE = math.floor((1 / (config.BTCPRICE * 100)) * 100000000)
        logger.info("Satoshi price updated")

    if config.PULSES == 2:
        config.FIAT += 0.02
        config.COINCOUNT += 1
        config.SATS = utils.get_sats()
        config.SATSFEE = utils.get_sats_with_fee()
        config.SATS -= config.SATSFEE
        logger.info("2 cents added")
        display.update_amount_screen()
    if config.PULSES == 3:
        config.FIAT += 0.05
        config.COINCOUNT += 1
        config.SATS = utils.get_sats()
        config.SATSFEE = utils.get_sats_with_fee()
        config.SATS -= config.SATSFEE
        logger.info("5 cents added")
        display.update_amount_screen()
    if config.PULSES == 4:
        config.FIAT += 0.1
        config.COINCOUNT += 1
        config.SATS = utils.get_sats()
        config.SATSFEE = utils.get_sats_with_fee()
        config.SATS -= config.SATSFEE
        logger.info("10 cents added")
        display.update_amount_screen()
    if config.PULSES == 5:
        config.FIAT += 0.2
        config.COINCOUNT += 1
        config.SATS = utils.get_sats()
        config.SATSFEE = utils.get_sats_with_fee()
        config.SATS -= config.SATSFEE
        logger.info("20 cents added")
        display.update_amount_screen()
    if config.PULSES == 6:
        config.FIAT += 0.5
        config.COINCOUNT += 1
        config.SATS = utils.get_sats()
        config.SATSFEE = utils.get_sats_with_fee()
        config.SATS -= config.SATSFEE
        logger.info("50 cents added")
        display.update_amount_screen()
    if config.PULSES == 7:
        config.FIAT += 1
        config.COINCOUNT += 1
        config.SATS = utils.get_sats()
        config.SATS = utils.get_sats()
        config.SATSFEE = utils.get_sats_with_fee()
        logger.info("100 cents added")
        display.update_amount_screen()
    config.PULSES = 0

    if config.FIAT > 0 and led == "off":
        # Turn on the LED after first coin
        GPIO.output(13, GPIO.HIGH)
        led = "on"
        logger.info("Button-LED turned on (if connected)")


def monitor_coins_and_button():
    """Monitors coins inserted and buttons pushed
    """
    time.sleep(0.2)

    # Potentially new way of detecting coin insertions
    # if config.COINLIST:
    #     time.sleep(1)
    #     if config.COINLIST.count("0") > 1:
    #         print(config.COINLIST[1 : config.COINLIST.index("0", 1)])
    #         print(len(config.COINLIST[1 : config.COINLIST.index("0", 1)]))
    #     else:
    #         print(config.COINLIST[1:])
    #         print(len(config.COINLIST[1:]))
    #         if len(config.COINLIST[1:]) > 0:
    #             config.PULSLIST.append(len(config.COINLIST[1:]))
    #             del config.COINLIST[: len(config.COINLIST[1:])]
    #
    # print(config.PULSLIST)

    # Detect when coins are being inserted
    if (time.time() - config.LASTIMPULSE > 0.5) and (config.PULSES > 0):
        coins_inserted()

    # Detect if the button has been pushed
    if (time.time() - config.LASTPUSHES > 1) and (config.PUSHES > 0):
        button_pushed()

    # Automatic payout if specified in config file
    if (int(config.conf["atm"]["payoutdelay"]) > 0) and (config.FIAT > 0):
        if time.time() - config.LASTIMPULSE > int(config.conf["atm"]["payoutdelay"]):
            config.PUSHES = config.PUSHES + 1


def setup_coin_acceptor():
    """Initialises the coin acceptor parameters and sets up a callback for button pushes
    and coin inserts.
    """
    # Defining GPIO BCM Mode
    GPIO.setmode(GPIO.BCM)

    # Setup GPIO Pins for coin acceptor, button and button-led
    GPIO.setwarnings(False)
    GPIO.setup(13, GPIO.OUT)
    GPIO.output(13, GPIO.LOW)
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Setup coin interrupt channel (bouncetime for switch bounce)
    GPIO.add_event_detect(5, GPIO.RISING, callback=button_event, bouncetime=300)
    GPIO.add_event_detect(6, GPIO.FALLING, callback=coin_event)


# def check_dangermode():
#     """Check for DANGERMODE and wipe any saved credentials if off"
#     """
#     # if dangermode is NOT on
#     if config.conf["atm"]["dangermode"].lower() != "on":
#         logger.warning("DANGERMODE off")
#
#         # wipe any saved values from the config by saving an empty value to it
#         config.update_config("lntxbot", "creds", "")
#         config.update_config("lnd", "macaroon", "")
#         config.update_config("atm", "activewallet", "")
#
#         # get the static dict from within the conf and overwrite it to config.conf
#         config.conf = config.conf._sections
#
#         # get new lntxbot creds from qr code scan
#         print("Scan lntxbot creds now\n")
#         print("            +---+")
#         print("+-----------+---+")
#         print("|      .-.      |")
#         print("|     (   )     |")
#         print("|      `-'      |")
#         print("+---------------+\n")
#         time.sleep(2)
#         try:
#             config.conf["lntxbot"]["creds"] = lntxbot.scan_creds()
#             logger.info("Credentials saved in volatile memory (deleted after reboot)")
#         except utils.ScanError:
#             logger.error("Error scanning lntxbot creds with dangermode off")
#             return
#     else:
#         logger.info("DANGERMODE on. Loading values from config.ini...")
#         # config.check_config()


def main():
    utils.check_epd_size()
    logger.info("Application started")

    # Checks dangermode and start scanning for credentials
    # Only activate once software ready for it
    # check_dangermode()

    # # For testing
    # config.PULSES = 2

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
