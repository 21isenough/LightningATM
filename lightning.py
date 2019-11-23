#!/usr/bin/python3

# TODO: Add the "verify=False" param to all post en get requests for local api queries
# TODO: Add option to use LNtxbot with the ATM

import codecs
import json
import logging
import os.path
import requests

from config import conf

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
        str(conf["btcpay"]["url"]) + "/channels/transactions",
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
    url = str(conf["btcpay"]["url"]) + "/payments"

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
        url = str(conf["btcpay"]["url"]) + "/payreq/" + str(payment_request)
        response = requests.get(url, headers={"Grpc-Metadata-macaroon": macaroon})
        # TODO: I don't think we handle failed decoding here
        #   Perhaps something like:
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
