#!/usr/bin/python3

import time

from utils import *
from config import *

from PIL import Image, ImageFont, ImageDraw


# PaPiRus eInk size is 128 x 96 pixels


def update_startup_screen():
    image = Image.new("1", PAPIRUS.size, WHITE)

    draw = ImageDraw.Draw(image)

    draw.text((20, 10), "Welcome to the", fill=BLACK, font=create_font("freemono", 18))
    draw.text((10, 20), "LightningATM", fill=BLACK, font=create_font("sawasdee", 30))
    draw.text(
        (7, 75), "- please insert coins -", fill=BLACK, font=create_font("freemono", 14)
    )

    PAPIRUS.display(image)
    PAPIRUS.update()


def update_qr_request(amt):
    # initially set all white background
    image = Image.new("1", PAPIRUS.size, WHITE)

    # Set width and height of screen
    width, height = image.size

    # prepare for drawing
    draw = ImageDraw.Draw(image)

    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((25, 10), "Please scan", fill=BLACK, font=create_font("freemono", 20))
    draw.text((10, 30), "your invoice in", fill=BLACK, font=create_font("freemono", 20))

    PAPIRUS.display(image)
    PAPIRUS.update()

    for i in range(0, 3):
        draw.text((80, 45), str(3 - i), fill=BLACK, font=create_font("freemono", 50))
        PAPIRUS.display(image)
        PAPIRUS.partial_update()
        draw.rectangle((75, 50, 115, 90), fill=WHITE, outline=WHITE)
        time.sleep(1)

    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((25, 10), "Scanning...", fill=BLACK, font=create_font("freemono", 20))
    draw.text(
        (15, 35),
        "for " + str(round(amt)) + " sats.",
        fill=BLACK,
        font=create_font("freemono", 20),
    )
    PAPIRUS.display(image)
    PAPIRUS.partial_update()


def update_qr_failed():
    # initially set all white background
    image = Image.new("1", PAPIRUS.size, WHITE)

    # Set width and height of screen
    width, height = image.size

    # prepare for drawing
    draw = ImageDraw.Draw(image)

    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((25, 10), "Scanning...", fill=BLACK, font=create_font("freemono", 20))
    draw.text((25, 30), "Scan failed.", fill=BLACK, font=create_font("freemono", 20))
    draw.text((25, 50), "Try again.", fill=BLACK, font=create_font("freemono", 20))
    PAPIRUS.display(image)
    PAPIRUS.partial_update()


def update_payment_failed():
    image = Image.new("1", PAPIRUS.size, WHITE)

    draw = ImageDraw.Draw(image)

    draw.text((15, 10), "Payment failed!", fill=BLACK, font=create_font("freemono", 19))
    draw.text((25, 45), "Please contact", fill=BLACK, font=create_font("freemono", 17))
    draw.text((45, 65), "operator.", fill=BLACK, font=create_font("freemono", 17))

    PAPIRUS.display(image)
    PAPIRUS.update()


def update_thankyou_screen():
    image = Image.new("1", PAPIRUS.size, WHITE)

    draw = ImageDraw.Draw(image)

    draw.text((15, 10), "Enjoy your new", fill=BLACK, font=create_font("freemono", 19))
    draw.text((40, 35), "satoshis!!", fill=BLACK, font=create_font("freemono", 19))
    draw.text(
        (15, 70), "#bitcoin #lightning", fill=BLACK, font=create_font("freemono", 14)
    )

    PAPIRUS.display(image)
    PAPIRUS.update()


def update_nocoin_screen():
    image = Image.new("1", PAPIRUS.size, WHITE)

    draw = ImageDraw.Draw(image)

    draw.text((15, 10), "No coins added!", fill=BLACK, font=create_font("freemono", 19))
    draw.text((25, 45), "Please add", fill=BLACK, font=create_font("freemono", 17))
    draw.text((45, 65), "coins first.", fill=BLACK, font=create_font("freemono", 17))

    PAPIRUS.display(image)
    PAPIRUS.update()


def update_lnurl_generation():
    image = Image.new("1", PAPIRUS.size, WHITE)

    width, height = image.size

    draw = ImageDraw.Draw(image)

    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((30, 20), "Generating", fill=BLACK, font=create_font("freemono", 20))
    draw.text((10, 40), "QR code to scan", fill=BLACK, font=create_font("freemono", 20))

    PAPIRUS.display(image)
    PAPIRUS.partial_update()


def update_shutdown_screen():
    image = Image.new("1", PAPIRUS.size, WHITE)

    draw = ImageDraw.Draw(image)

    draw.text((20, 10), "ATM turned off!", fill=BLACK, font=create_font("freemono", 18))
    draw.text((25, 45), "Please contact", fill=BLACK, font=create_font("freemono", 17))
    draw.text((45, 65), "operator.", fill=BLACK, font=create_font("freemono", 17))

    PAPIRUS.display(image)
    PAPIRUS.update()


def update_lntxbot_scan():
    # initially set all white background
    image = Image.new("1", PAPIRUS.size, WHITE)

    # Set width and heigt of screen
    width, height = image.size

    # prepare for drawing
    draw = ImageDraw.Draw(image)

    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((35, 20), "Please scan", fill=BLACK, font=create_font("freemono", 18))
    draw.text((33, 40), "your lntxbot", fill=BLACK, font=create_font("freemono", 18))
    draw.text((35, 60), "credentials.", fill=BLACK, font=create_font("freemono", 18))

    PAPIRUS.display(image)
    PAPIRUS.update()
    time.sleep(2)


def update_lntxbot_balance(balance):
    # initially set all white background
    image = Image.new("1", PAPIRUS.size, WHITE)

    # Set width and height of screen
    width, height = image.size

    # prepare for drawing
    draw = ImageDraw.Draw(image)

    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((45, 15), "Success!!", fill=BLACK, font=create_font("freemonobold", 20))
    draw.text(
        (10, 45), "Your current balance:", fill=BLACK, font=create_font("freemono", 15)
    )
    draw.text(
        (45, 65),
        str("{:,}".format(balance)) + " sats",
        fill=BLACK,
        font=create_font("freemono", 18),
    )

    PAPIRUS.display(image)
    PAPIRUS.update()
    time.sleep(3)
