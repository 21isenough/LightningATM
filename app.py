#!/usr/bin/python3

import logging
import os
import sys
import time
import math
import subprocess

from gpiozero import Button, LED

import config
import lndrest
import lntxbot
import qr

import utils
import importlib
from PIL import Image

# Initialize inputs and outputs
button_signal = Button(5, False)
coin_signal = Button(6)
button_led = LED(13)
lockout_relay = LED(12)

display_config = config.conf["atm"]["display"]
display = getattr(__import__("displays", fromlist=[display_config]), display_config)

logger = logging.getLogger("MAIN")


def check_connectivity(interface="wlan0"):
    output_lines=subprocess.check_output(["wpa_cli","-i",interface,"status"])
    for output_line in output_lines.decode("utf8").split("\n"):
        if output_line[0:4]=="ssid":
            # We have an SSID
            return output_line[5:]
    return None


def softreset():
    """Displays startup screen and deletes fiat amount
    """
    # Inform about coin, bill and sat amounts
    if config.COINCOUNT > 0:
        logger.info("Last payment:")
        logger.info("%s Coin(s), XX Bill(s), %s Sats", config.COINCOUNT, config.SATS)

    config.SATS = 0
    config.FIAT = 0
    config.COINCOUNT = 0
    config.PUSHES = 0
    # Turn off button LED
    button_led.off()
    
    display.update_startup_screen()
    logger.info("Softreset executed")


def button_event():
    """Registers a button push event
    """
    config.LASTPUSHES = time.time()
    config.PUSHES = config.PUSHES + 1


def coin_event():
    """Registers a coin insertion event
    """
    config.LASTIMPULSE = time.time()
    config.PULSES = config.PULSES + 1


def button_pushed():
    """Actions button pushes by number
    """
    print("Push button: ", config.PUSHES, " times")
    logger.info("Call function button_pushed with pushes: ")
    logger.info(config.PUSHES)
    
    if config.PUSHES == 1 or config.FIAT > 0:
        """If no coins inserted, update the screen.
        If coins inserted, scan a qr code for the exchange amount
        """
        
        # Clarify if exception FIAT > 0 was TRUE => set pulses 1
        if config.PUSHES > 1:
            config.PUSHES = 1
            logger.info("Restriction for the button => Set pulses = 1")

        # If no wallet is configured
        if not config.conf["atm"]["activewallet"]:
            logger.error("No wallet has been configured for the ATM.")
            logger.error("Please configure your Lightning Wallet first.")
            # "no wallet setup" message
            display.update_wallet_fault()
            time.sleep(5)

            # Softreset and startup screen
            softreset()
            return

        # If no FIAT has been deposited yet
        if config.FIAT == 0:
            display.update_nocoin_screen()
            time.sleep(3)
            display.update_startup_screen()
            config.PUSHES = 0
            return

        lnurlproxy = config.conf["lnurl"]["lnurlproxy"]
        activewallet = config.conf["atm"]["activewallet"]
        camera = config.conf["atm"]["camera"]

        if config.conf["atm"]["activewallet"] == "lnbits":
            # Process QR code scan
            # Only implemented for LND BTCPay so far
            logger.info("No option for LNURL. Continue with scan...")
            display.update_qr_request()
            if config.PUSHES == 1:
                qrcode = qr.scan()
                config.INVOICE = lnbits.evaluate_scan(qrcode)
                while config.INVOICE is False:
                    display.update_qr_failed()
                    time.sleep(1)
                    display.update_qr_request()
                    qrcode = qr.scan()
                    config.INVOICE = lnbits.evaluate_scan(qrcode)
                display.update_payout_screen()
                lnbits.handle_invoice()
                softreset()
                return
            if config.PUSHES > 1:
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
                lnbits.handle_invoice()
                softreset()
                return

        # Determine if LNURL Withdrawls are possible
        elif lnurlproxy == "active" or activewallet == "lntxbot":
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
                    config.INVOICE = lnbits.evaluate_scan(qrcode)
                    while config.INVOICE is False:
                        display.update_qr_failed()
                        time.sleep(1)
                        display.update_qr_request()
                        qrcode = qr.scan()
                        config.INVOICE = lnbits.evaluate_scan(qrcode)
                    display.update_payout_screen()
                    lnbits.handle_invoice()
                    softreset()
                    return
        else:
            logger.error("No valid wallet configured")

    if config.PUSHES == 9:
        """Reset Wallet and Scan new wallet credentials
        """
        logger.info("Wallet reset and new scan (9 times button)")
        
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

    if config.PUSHES == 3:
        """Simulates adding a coin (for testing)
        """
        logger.info("Simulate coin for test with pulses (3 times button)")
        print("Simulate coin for test with pulses (3 times button)")
        config.PULSES = 2
        config.PUSHES = 0
        return

    if config.PUSHES == 7:
        """Shutdown the host machine
        """
        display.update_shutdown_screen()
        logger.warning("ATM shutdown (7 times button)")
        os.system("sudo shutdown -h now")

    if config.PUSHES == 5:
        """Show all displays once
        """
        logger.info("Show all displays once (5 times button)")

        print("1. display.error_screen(message=ERROR)")
        display.error_screen(message="ERROR")
        time.sleep(2)

        print("2. display.update_qr_request()")
        display.update_qr_request()
        time.sleep(2)

        print("3. display.update_qr_failed()")
        display.update_qr_failed()
        time.sleep(2)

        print("4. display.update_payout_screen()")
        display.update_payout_screen()
        time.sleep(2)

        print("5. display.update_payment_failed()")
        display.update_payment_failed()
        time.sleep(2)

        print("6. display.update_thankyou_screen()")
        display.update_thankyou_screen()
        time.sleep(2)

        print("7. display.update_nocoin_screen()")
        display.update_nocoin_screen()
        time.sleep(2)

        print("8. display.update_lnurl_generation()")
        display.update_lnurl_generation()
        time.sleep(2)

        print("9. display.update_shutdown_screen()")
        display.update_shutdown_screen()
        time.sleep(2)

        print("10. display.update_wallet_scan()")
        display.update_wallet_scan()
        time.sleep(2)

        print("11. display.update_lntxbot_balance(balance)")
        display.update_lntxbot_balance(123)
        time.sleep(2)

        print("12. display.update_btcpay_lnd()")
        display.update_btcpay_lnd()
        time.sleep(2)

        print("13. display.draw_lnurl_qr(qr_img)")
        qrImage = Image.new('1', (122, 122), 255)
        display.draw_lnurl_qr(qrImage)
        time.sleep(2)

        print("14. display.update_amount_screen()")
        display.update_amount_screen()
        time.sleep(2)

        print("15. display.update_lnurl_cancel_notice()")
        display.update_lnurl_cancel_notice()
        time.sleep(2)

        print("16. display.update_button_fault()")
        display.update_button_fault()
        time.sleep(2)

        print("17. display.update_wallet_fault()")
        display.update_wallet_fault()
        time.sleep(2)

        print("18. display.update_startup_screen()")
        display.update_startup_screen()
        time.sleep(2)

        print("That's it, have fun!")

        config.PUSHES = 0
        return

    else:
        # If pushes not defined
        logger.info("Show pushes not defined  (x times button)")
        display.update_button_fault()
        time.sleep(3)
        display.update_startup_screen()

    # Reset pulses
    config.PUSHES = 0


def coins_inserted():
    """Actions coins inserted
    """
    
    print("Coin pulses: ", config.PULSES, " pulses")

    # Intercept and display a loose contact
    if config.PULSES == 1:
        print("Ups.. Just one coin pulses is not allowed!")
        logger.error("Ups.. Just one coin pulses is not allowed!")
        config.PULSES = 0
        return

    # Check if we should update prices
    if config.FIAT == 0:
        # Our counter is 0, meaning we got no fiat in:
        config.BTCPRICE = utils.get_btc_price(config.conf["atm"]["cur"])
        config.SATPRICE = (1 / (config.BTCPRICE * 100)) * 1e8
        logger.debug("Satoshi price updated")

    # We must have gotten pulses!
    config.FIAT +=      float(config.COINTYPES[config.PULSES]['fiat'])
    config.COINCOUNT += 1
    config.SATS =       utils.get_sats()
    config.SATSFEE =    utils.get_sats_with_fee()
    config.SATS -=      config.SATSFEE
    logger.info("Added {}".format(config.COINTYPES[config.PULSES]['name']))
    display.update_amount_screen()

    # Coin was processed -> Release coin acceptor relay switch
    lockout_relay.on()

    # Reset pulse cointer
    config.PULSES = 0

    if config.FIAT > 0 and not button_led.value == 1:
        # Turn on the LED after first coin
        button_led.on()
        logger.debug("Button-LED turned on (if connected)")


def monitor_coins_and_button():
    """Monitors coins inserted and buttons pushed
    """
    
    # 200 ms sleep for CPU idle and other processes
    time.sleep(0.1)
    # Too long a delay will have a negative effect on the coin detection and the lockout relay

    #Wifi monitoring causes undesirable behavior sometimes.
    #ssid=check_connectivity()
    #print(ssid)
    #if not ssid:
    #    # We are not connected!
    #    config.CONNECTIVITY=False
    #    display.error_screen("No connectivity")
    #    logger.error("No connectivity")
    #    time.sleep(5)
    #    return False
    #else:
    #    if not config.CONNECTIVITY:
    #        # We have an SSID now but not before
    #        config.CONNECTIVITY=True
    #        display.update_startup_screen()
    #        return False

    # Detect when coins are being inserted
    if (time.time() - config.LASTIMPULSE > 0.3) and (config.PULSES > 0):
        # New Coin to process -> Relay switch to inhibit
        lockout_relay.off()
        coins_inserted()

    # Detect if the button has been pushed
    if (time.time() - config.LASTPUSHES > 1) and (config.PUSHES > 0):
        # Pulses from push button -> Relay switch to inhibit
        if not config.PUSHES == 3:
            lockout_relay.off()
        button_pushed()

    # Processing pulses finish -> Release coin acceptor relay switch
    lockout_relay.on()

    # Automatic payout if specified in config file
    if (int(config.conf["atm"]["payoutdelay"]) > 0) and (config.FIAT > 0):
        if time.time() - config.LASTIMPULSE > int(config.conf["atm"]["payoutdelay"]):
            config.PUSHES = config.PUSHES + 1


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
    print("Application started")

    # Checks dangermode and start scanning for credentials
    # Only activate once software ready for it
    # check_dangermode()

    # Display startup info
    display.update_shutdown_screen()
    button_led.on()
    time.sleep(1)

    # Display startup startup_screen
    display.update_startup_screen()
    button_led.off()

    # Function call by rising/falling new signal
    button_signal.when_pressed = button_event
    coin_signal.when_released = coin_event

    while True:
        monitor_coins_and_button()


if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            display.update_shutdown_screen()
            logger.info("Application finished (Keyboard Interrupt)")
            sys.exit(" Manually Interrupted")
        except Exception:
            logger.exception("Oh no, something bad happened! Restarting...")
            os.execv("/home/pi/LightningATM/app.py", [""])
