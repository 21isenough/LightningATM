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

import lnurl
from urllib.parse import urlparse
from lnurl import Lnurl

# import display
display_config = config.conf["atm"]["display"]
display = getattr(__import__("displays", fromlist=[display_config]), display_config)

logger = logging.getLogger("LNTXBOT")

# TODO: Add variable to set certificate check to true or false
# TODO: Add evaluation for credentials after scanning
# TODO: Remove display calls from here to app.py

def process_lnurl(amt, inv):
    """Processes pay an amount using the lnurl scheme
    """
    pr = convert_ln(amt, inv)
    data = {
        "invoice": pr,
        "amount": math.floor(amt)
    }
    response = requests.post(
        str(config.conf["lntxbot"]["url"]) + "/payinvoice",
        headers={"Authorization": "Basic %s" % config.conf["lntxbot"]["creds"]},
        data=json.dumps(data)
    )
    response = response.json()
    logger.info("Payout Response: %s", json.dumps(response))
    if ("error" in response and response["error"]) or ("payment_error" in response and response["payment_error"]):
        display.update_payment_failed()
    else:
        # get the balance? back from the bot
        start_balance = get_lnurl_balance()
        print("Start balance: {0}".format(start_balance))
        logger.info("Start balance: %s", start_balance)
        # loop while we wait for a balance update or until timeout reached
        success = wait_for_balance_update(start_balance, timeout=config.TIMEOUT)
        if success:
            display.update_thankyou_screen()
            logger.info("LNURL payment succeeded")
            return
        else:
            logger.error("LNURL payment failed (within 90 seconds)")
            display.update_payment_failed()


def convert_ln(amt, inv):
    """Will convert LNURL to BOLT11 invoice
    """
    logger.info("Amount: %s", str(amt))
    logger.info("Input inv: %s", inv)
    pr = str(inv)
    amt = math.floor(amt)
    logger.info("Floored amount: %s", amt)
    data = {"amount":amt}
    lnurl = Lnurl(inv)
    logger.info("Detected LNURL: %s", inv)
    rsp = requests.get(lnurl.decoded, verify=True)
    dic = rsp.json()
    logger.info("Dict from request: %s", json.dumps(dic))
    url = urlparse(dic['callback'])
    logger.info("Callback URL: %s", json.dumps(url))
    r = requests.post("https://lnurl.bigsun.xyz/lnurl-pay/callback/?"+url.query+"&amount="+str(amt),headers=None,data=json.dumps(data))
    logger.info("Result: %s", json.dumps(r.json()))
    if "pr" in r.json():
        pr = r.json()["pr"]
    logger.info("Parsed PR: %s", pr)
    return pr

def payout(amt, payment_request):
    """Attempts to pay a BOLT11 invoice
    """
    data = {
        "invoice": payment_request,
        "amount": math.floor(amt),
    }
    logger.info("Input: %s", json.dumps(data))
    response = requests.post(
        str(config.conf["lntxbot"]["url"]) + "/payinvoice",
        headers={"Authorization": "Basic %s" % config.conf["lntxbot"]["creds"]},
        data=json.dumps(data)
    )
    response = response.json()
    logger.info("Payout Response: %s", json.dumps(response))
    if ("error" in response and response["error"]) or ("payment_error" in response and response["payment_error"]):
        display.update_payment_failed()
    else:
        display.update_thankyou_screen()


def request_lnurl(amt):
    """Request a new lnurl for 'amt' from the server
    """
    data = {
        "satoshis": str(math.floor(amt)),
    }
    response = requests.post(
        str(config.conf["lntxbot"]["url"]) + "/generatelnurlwithdraw",
        headers={"Authorization": "Basic %s" % config.conf["lntxbot"]["creds"]},
        data=json.dumps(data)
    )
    return response.json()


def get_lnurl_balance():
    """Query the lnurl balance from the server and return the
    ["BTC"]["AvailableBalance"] value
    """
    response = requests.post(
        str(config.conf["lntxbot"]["url"]) + "/balance",
        headers={"Authorization": "Basic %s" % config.conf["lntxbot"]["creds"]},
        files=None,
        verify=True,
        timeout=10
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
        ks = time.time()
        new_balance = get_lnurl_balance()
        if start_balance == new_balance:
            print("Balance: " + str(start_balance) + " (no changes)")
            remain = timeout - math.floor(ks - start_time)
            print("Remain: {}".format(remain))
            display.update_payment_status(remain)
            time.sleep(4)
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
    lnurl = request_lnurl(amt)
    logger.info("LN requested: %s", json.dumps(lnurl))
    # Check EPD_SIZE is defined
    utils.check_epd_size()

    # create a qr code image and print it to terminal
    qr_img = utils.generate_lnurl_qr(lnurl["lnurl"])

    # draw the qr code on the e-ink screen
    display.draw_lnurl_qr(qr_img)

    # get the balance? back from the bot
    start_balance = get_lnurl_balance()
    logger.info("Start balance: %s", start_balance)

    # loop while we wait for a balance update or until timeout reached
    success = wait_for_balance_update(start_balance, timeout=config.TIMEOUT)

    if success:
        display.update_thankyou_screen()
        logger.info("LNURL withdrawal succeeded")
        return
    else:
        display.update_payment_failed()
        # TODO: I think we should handle a failure here
        logger.error("LNURL withdrawal failed (within {0} seconds)".format(config.TIMEOUT))

def process_lnurl_directly(amt, timeout):
    """Processes receiving an amount using the lnurl scheme
    """
    lnurl = request_lnurl(amt)
    logger.info("LN requested: %s", json.dumps(lnurl))
    # Check EPD_SIZE is defined
    utils.check_epd_size()

    # create a qr code image and print it to terminal
    qr_img = utils.generate_lnurl_qr(lnurl["lnurl"])

    # draw the qr code on the e-ink screen
    display.draw_lnurl_qr(qr_img)

    
    # get the balance? back from the bot
    start_balance = get_lnurl_balance()
    #print(start_balance)
    logger.info("Start balance: %s", start_balance)

    # loop while we wait for a balance update or until timeout reached
    success = wait_for_balance_update(start_balance, timeout)

    if success:
        display.update_thankyou_screen()
        print("Successful withdrawal.")
        logger.info("LNURL withdrawal succeeded")
        return
    else:
        display.update_payment_failed()
        # TODO: I think we should handle a failure here
        print("Failed withdrawal.")
        logger.error("LNURL withdrawal failed (within {0} seconds)".format(timeout))

