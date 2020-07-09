#!/usr/bin/python3

import json
import os
import logging
import time
import requests
import math
import qr

import config
import utils

# import display
display_config = config.conf["atm"]["display"]
display = getattr(__import__("displays", fromlist=[display_config]), display_config)

logger = logging.getLogger("LNTXBOT")

# TODO: Add variable to set certificate check to true or false
# TODO: Add evaluation for credentials after scanning
# TODO: Remove display calls from here to app.py


def payout(amt, payment_request):
    """Attempts to pay a BOLT11 invoice
    """
    data = {
        "invoice": payment_request,
        "amount": math.floor(amt),
    }
    response = requests.post(
        str(config.conf["lntxbot"]["url"]) + "/payinvoice",
        headers={"Authorization": "Basic %s" % config.conf["lntxbot"]["creds"]},
        data=json.dumps(data),
    )


def request_lnurl(amt):
    """Request a new lnurl for 'amt' from the server
    """
    data = {
        "satoshis": str(math.floor(amt)),
    }
    response = requests.post(
        str(config.conf["lntxbot"]["url"]) + "/generatelnurlwithdraw",
        headers={"Authorization": "Basic %s" % config.conf["lntxbot"]["creds"]},
        data=json.dumps(data),
    )
    return response.json()


def get_lnurl_balance():
    """Query the lnurl balance from the server and return the
    ["BTC"]["AvailableBalance"] value
    """
    response = requests.post(
        str(config.conf["lntxbot"]["url"]) + "/balance",
        headers={"Authorization": "Basic %s" % config.conf["lntxbot"]["creds"]},
    )
    return response.json()["BTC"]["AvailableBalance"]


def wait_for_balance_update(start_balance, timeout):
    """Loops waiting for any balance change on the lnurl and returns True if this
    happens before the timeout
    """
    start_time = time.time()
    success = False
    # loop while we wait for the balance to get updated
    while True and (time.time() < start_time + timeout):
        new_balance = get_lnurl_balance()
        if start_balance == new_balance:
            print("Balance: " + str(start_balance) + " (no changes)")
            time.sleep(3)
        else:
            print(
                "Balance: " + str(start_balance) + " | New Balance:" + str(new_balance)
            )
            success = True
            break
    return success


def process_using_lnurl(amt):
    """Processes receiving an amount using the lnurl scheme
    """
    # get the new lnurl
    display.update_lnurl_generation()
    logger.info("LNURL requested")
    print("LNURL requested")
    lnurl = request_lnurl(amt)
    print(lnurl["lnurl"])

    # Check EPD_SIZE is defined
    utils.check_epd_size()

    # create a qr code image and print it to terminal
    qr_img = utils.generate_lnurl_qr(lnurl["lnurl"])

    # draw the qr code on the e-ink screen
    display.draw_lnurl_qr(qr_img)

    # get the balance? back from the bot
    start_balance = get_lnurl_balance()
    print(start_balance)

    # loop while we wait for a balance update or until timeout reached
    success = wait_for_balance_update(start_balance, timeout=90)

    if success:
        display.update_thankyou_screen()
        logger.info("LNURL withdrawal succeeded")
        return
    else:
        # TODO: I think we should handle a failure here
        logger.error("LNURL withdrawal failed (within 90 seconds)")
