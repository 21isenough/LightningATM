#!/usr/bin/python3

import json
import os.path
import logging
import time
import requests
import math

import config

# import display
display_config = config.conf["atm"]["display"]
display = getattr(__import__("displays", fromlist=[display_config]), display_config)

logger = logging.getLogger("LNBITS")


# TODO: Remove display calls from here to app.py
# TODO: Add the "verify=False" param to all post and get requests for local api queries


class InvoiceDecodeError(BaseException):
    pass


def payout(amt, payment_request):
    """Attempts to pay a BOLT11 invoice
    """
    data = {
        "out": "true",
        "amount": amt,
        "bolt11": payment_request,
    }

    response = requests.post(
        str(config.conf["lnbits"]["url"]) + "/payments",
        headers={"X-Api-Key": str(config.conf["lnbits"]["apikey"])},
        data=json.dumps(data),
    )
    res_json = response.json()

    if res_json.get("detail"):
        errormessage = res_json.get("detail")
        logger.error("Payment failed (%s)" % errormessage)
        print("Error: " + res_json.get("detail"))


def last_payment(payment_request):
    """Returns whether the last payment attempt succeeded or failed
    """
    url = str(config.conf["lnbits"]["url"]) + "/payments?limit=1"
    response = requests.get(
        url,
        headers={"X-Api-Key": str(config.conf["lnbits"]["apikey"])},
    )
    res_json = response.json()
    res_json = res_json[0]

    if (res_json["bolt11"] == payment_request) and (
        res_json["pending"] == False
    ):
        logger.info("Payment succeeded")
        print("Payment succeeded")
        return True
    else:
        logger.info("Payment failed")
        print("Payment failed")
        return False


def decode_request(payment_request):
    """Decodes a BOLT11 invoice
    """
    data = {
        "data": payment_request,
    }

    response = requests.post(
        str(config.conf["lnbits"]["url"]) + "/payments/decode",
        headers={"X-Api-Key": str(config.conf["lnbits"]["apikey"])},
        data=json.dumps(data),
    )

    # successful response
    if response.status_code != 200:
        raise InvoiceDecodeError(
            "Invoice {} got bad decode response {}".format(
                payment_request, response.text
            )
        )
    res_json = response.json()
    if "lnbc1" in payment_request:
        print("Zero sat invoice")
        return 0
    else:
        return int(res_json["amount_msat"]/1000)

def lnurlp_request(lnurlp):
    """Decodes a BOLT11 invoice
    """
    data = {
        "data": lnurlp.upper(),
    }

    response = requests.post(
        str(config.conf["lnbits"]["url"]) + "/payments/decode",
        headers={"X-Api-Key": str(config.conf["lnbits"]["apikey"])},
        data=json.dumps(data),
    )

    # successful response
    if response.status_code != 200:
        raise InvoiceDecodeError(
            "LNURLp {} got bad decode response {}".format(
                response.text
            )
        )

    res_json = response.json()

    if res_json.get("message"):
        errormessage = res_json.get("message")
        logger.error("LNURLp request failed (%s)" % errormessage)
        print("Error: " + res_json.get("message"))
    else:
        response = requests.get(
            res_json["domain"],
        )
        res_json = response.json()
        
        if "kind" in res_json["callback"]:
            res_json["callback"] = res_json["callback"].replace('?kind=', '')

        callback = res_json["callback"] + "?amount=" + str(math.floor(config.SATS * 1000))
        response = requests.get(
            callback,
        )
        res_json = response.json()
        return res_json["pr"]


def handle_invoice():
    """Decode a BOLT11 invoice. Ensure that amount is correct or 0, then attempt to
    make the payment.
    """
    decode_req = decode_request(config.INVOICE)
    if decode_req in (math.floor(config.SATS), 0):
        payout(config.SATS, config.INVOICE)
        result = last_payment(config.INVOICE)

        if result:
            display.update_thankyou_screen()
        else:
            display.update_payment_failed()
            time.sleep(120)
    else:
        print("Please show correct invoice")


def evaluate_scan(qrcode):
    """Evaluates the scanned qr code for Lightning invoices.
    """
    if not qrcode:
        logger.error("QR code scanning failed")
        return False
    # check for a lightning invoice
    else:
        if "lnbc" in qrcode.lower():
            logger.info("Lightning invoice detected")
            invoice = qrcode.lower()
            # if invoice preceded with "lightning:" then chop it off so that we can
            # handle it correctly
            if "lightning:" in invoice:
                invoice = invoice[10:]
            return invoice
        elif "lnurl" in qrcode.lower():
            logger.info("LNURL detected")
            lnurl = qrcode.lower()
            if "lightning:" in lnurl:
                lnurl = lnurl[10:]
            invoice = lnurlp_request(lnurl)
            return invoice
        else:
            logger.error("This QR does not contain a Lightning invoice")
            return False
