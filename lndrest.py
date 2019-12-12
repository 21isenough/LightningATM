#!/usr/bin/python3

# TODO: Add the "verify=False" param to all post and get requests for local api queries
# TODO: Add option to use LNtxbot with the ATM

import codecs
import json
import logging
import os.path
import requests
import config
import display
from datetime import datetime

logger = logging.getLogger("LIGHTNING")


class InvoiceDecodeError(BaseException):
    pass


with open(os.path.expanduser("~/admin.macaroon"), "rb") as f:
    macaroon_bytes = f.read()
    macaroon = codecs.encode(macaroon_bytes, "hex")


def payout(amt, payment_request):
    """Attempts to pay a BOLT11 invoice
    """
    data = {
        "payment_request": payment_request,
        "amt": round(amt),
    }

    response = requests.post(
        str(config.conf["btcpay"]["url"]) + "/channels/transactions",
        headers={"Grpc-Metadata-macaroon": macaroon},
        data=json.dumps(data),
    )
    res_json = response.json()

    if res_json.get("payment_error"):
        errormessage = res_json.get("payment_error")
        logger.error("Payment failed (%s)" % errormessage)
        print("Error: " + res_json.get("payment_error"))


def last_payment(payment_request):
    """Returns whether the last payment attempt succeeded or failed
    """
    url = str(config.conf["btcpay"]["url"]) + "/payments"

    data = {
        "include_incomplete": True,
    }

    response = requests.get(
        url, headers={"Grpc-Metadata-macaroon": macaroon}, data=json.dumps(data)
    )

    json_data = response.json()
    payment_data = json_data["payments"]
    _last_payment = payment_data[-1]

    if (_last_payment["payment_request"] == payment_request) and (
        _last_payment["status"] == "SUCCEEDED"
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
    if payment_request:
        url = str(config.conf["btcpay"]["url"]) + "/payreq/" + str(payment_request)
        response = requests.get(url, headers={"Grpc-Metadata-macaroon": macaroon})
        # successful response
        if response.status_code != 200:
            raise InvoiceDecodeError(
                "Invoice {} got bad decode response {}".format(
                    payment_request, response.text
                )
            )
        json_data = response.json()
        if "lnbc1" in payment_request:
            print("Zero sat invoice")
            return 0
        else:
            return json_data["num_satoshis"]
    else:
        pass


def handle_invoice():
    """Decode a BOLT11 invoice. Ensure that amount is correct or 0, then attempt to
    make the payment.
    """
    decode_req = decode_request(config.INVOICE)
    if decode_req in (round(config.SATS), 0):
        payout(config.SATS, config.INVOICE)
        result = last_payment(config.INVOICE)

        if result is True:
            display.update_thankyou_screen()
        else:
            display.update_payment_failed()
            time.sleep(120)

        logger.info("Initiating softreset...")
    else:
        print("Please show correct invoice")


def evaluate_scan(qrcode):
    """Evaluates the scanned qr code for Lightning invoices.
    """
    if not qrcode:
        logging.error("QR code scanning failed")
        return False
    # check for a lightning invoice
    else:
        if "lnbc" in qrcode:
            logging.info("Lightning invoice detected")
            invoice = qrcode
            # Write Lightning invoice into a text file
            now = datetime.now()
            with open(config.conf["qr"]["scan_dir"] + "/qr_code_scans.txt", "a+") as f:
                f.write(invoice + " " + str(now.strftime("%d/%m/%Y %H:%M:%S")) + "\n")
            # if invoice preceded with "lightning:" then chop it off so that we can
            # handle it correctly
            if "lightning:" in invoice:
                invoice = invoice[10:]
            return invoice
        else:
            logging.error("This QR does not contain a Lightning invoice")
            return False
