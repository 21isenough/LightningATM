import kivy
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

import time
import math

import config
import utils


class Page(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_label = Label(text='Hallo World')
        self.add_widget(self.main_label)

    def update_startup_screen(self):
        self.main_label.text = "LightningATM\n\n" \
                               " please insert coins"

    def update_qr_request(self):
        self.main_label.text = "Please scan your Invoice in"
        time.sleep(1)

        for i in range(0, 3):
            self.main_label.text = str(3-i)
            time.sleep(0.5)

        self.main_label.text = "Scanning for " + str(math.floor(config.SATS)) + " sats"

    def update_qr_failed(self):
        self.main_label.text = "Scanning failed. Try again"

    def update_payout_screen(self):
        self.main_label.text = str(math.floor(config.SATS)) + " sats on the way!"

    def update_payout_failed(self):
        self.main_label.text = "Payment failed!\n\n" \
                               "Please contact operator"

    def update_thankyou_screen(self):
        self.main_label.text = "Enjoy your new satoshis\n\n" \
                               "#bitcoin #lightning"

    def update_nocoin_screen(self):
        self.main_label.text = "No coins added!\n\n" \
                               "Please add coins first"

    def update_lnurl_generation(self):
        self.main_label.text = "Generating...\n\n" \
                               "Qr code to scan"

    def update_shutdown_screen(self):
        self.main_label.text = "Shut down ATM!\n\n" \
                               "Please contact operator"

    def update_lntxbot_scan(self):
        self.main_label.text = "Please scan your lntxbot credentials"

    def update_lntxbot_balance(self, balance):
        self.main_label.text = "Success!\n\n" \
                               "Your current balance:\n\n" + str("{:,}".format(balance)) + " sats"

    def update_amount_screen(self):
        self.main_label.text = str("{:,}".format(math.floor(config.SATS))) \
                               + " sats\n\n" \
                               + "%.2f" % round(config.FIAT, 2) \
                               + " " + config.conf["atm"]["cur"].upper() \
                               + "\n\nFee" \
                               + "= " \
                               + config.conf["atm"]["fee"] \
                               + "% (" \
                               + str(math.floor(config.SATSFEE)) \
                               + " sats)"

    def update_blank_screen(self):
        self.main_label.text = ""

    def menu_screen(self):
        self.main_label.text = "Start\n\n" \
                               "Menu 1\n\n" \
                               "Menu 2"