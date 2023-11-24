#!/usr/bin/python3

import json
import logging
import time
import requests
import math

import config

# import display
display_config = config.conf["atm"]["display"]
display = getattr(__import__("displays", fromlist=[display_config]), display_config)

logger = logging.getLogger("BLINK")

# TODO: Remove display calls from here to app.py


class InvoiceDecodeError(BaseException):
    pass


def payout(amt, payment_request):
    """Attempts to pay a BOLT11 invoice"""
    # Call the payout function with the amount and payment request
    # payout(amount, "your_payment_request_here", config)

    graphql_endpoint = str(config.conf["blink"]["graphql_endpoint"])
    api_key = str(config.conf["blink"]["api_key"])
    wallet_id = str(config.conf["blink"]["wallet_id"])

    # Prepare the GraphQL mutation as a string with placeholders
    graphql_query = """
    mutation LnInvoicePaymentSend($input: LnInvoicePaymentInput!) {
        lnInvoicePaymentSend(input: $input) {
            status
            errors {
                message
                path
                code
            }
        }
    }"""

    # Using string formatting to insert variables into the GraphQL mutation
    payload = {
        "query": graphql_query,
        "variables": {
            "input": {
                "walletId": wallet_id,
                "paymentRequest": payment_request,
                "memo": "LightningATM payout",
            }
        },
    }

    # Convert the payload dictionary to a JSON-formatted string
    payload_json = json.dumps(payload)

    headers = {"Content-Type": "application/json", "X-API-KEY": api_key}

    # Make the POST request to the API
    response = requests.post(graphql_endpoint, headers=headers, data=payload_json)

    # Print the response text
    print(response.text)


def last_payment(payment_request):
    """Fetches the status of the given invoice."""

    # Setup your endpoint and headers
    graphql_endpoint = str(config.conf["blink"]["graphql_endpoint"])
    headers = {
        "Content-Type": "application/json",
    }

    graphql_query = """
    query LnInvoicePaymentStatus($input: LnInvoicePaymentStatusInput!) {
        lnInvoicePaymentStatus(input: $input) {
            status
        }
    }
    """

    variables = {"input": {"paymentRequest": payment_request}}

    payload = {"query": graphql_query, "variables": variables}

    response = requests.post(graphql_endpoint, json=payload, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        if (
            "data" in json_data
            and "lnInvoicePaymentStatus" in json_data["data"]
            and "status" in json_data["data"]["lnInvoicePaymentStatus"]
        ):
            invoice_status = json_data["data"]["lnInvoicePaymentStatus"]["status"]

            if invoice_status == "PAID":
                print("Last transaction was successful.")
                return True
            else:
                print(f"Last transaction was not successful: {invoice_status}")
                return False
        else:
            print("Response JSON structure is not as expected.")
            return False
    else:
        print(f"Error fetching transaction data: HTTP {response.status_code}")
        return False


def decode_request(payment_request):
    """Decodes a BOLT11 invoice"""
    # there is no decode request in the blink api
    # could implement probing here
    if payment_request:
        print({"invoice": payment_request})
        if "lnbc1" in payment_request:
            print("Zero sat invoice detected")
            return 0
        elif "lnbc" in payment_request:
            print("Non-zero sat invoice detected")
            return 0
        elif "lntb" in payment_request:
            print("Signet invoice detected")
            return 0
    else:
        pass


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
    """Evaluates the scanned qr code for Lightning invoices."""
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
        else:
            logger.error("This QR does not contain a Lightning invoice")
            return False
