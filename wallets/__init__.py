import lntxbot
import lndrest

lnurl_support = ["lntxbot"]


class Wallet:
    def __init__(self, name):
        self.wallet = __import__(name)
        self.name = name

        if self.name in lnurl_support:
            self.lnurlsupport = True
        else:
            self.lnurlsupport = False

    def payinvoice(self):
        return self.wallet.payout()
