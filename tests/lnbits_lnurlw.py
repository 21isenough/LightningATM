# Run this test from the root directory of the project with:
# python3 -m tests.lnbits_lnurlw
# Before running this test, make sure you have a config.ini file in ~/.lightningATM/
# with a [lnbits] section and url and apikey values.
# If you run this test on a non-raspi without a display,
# set:
# display = testing


import config
import lnbits
import logging

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger = logging.getLogger()
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

print("config['lnbits']['url']: "+str(config.conf["lnbits"]["url"]))
print("config['lnbits']['apikey']: "+str(config.conf["lnbits"]["apikey"]))

config.SATS = 5
resp_json = lnbits.create_lnurlw()
print("lnurlw: "+str(resp_json["lnurl"]))
print("Redeem within timeout!")
success = lnbits.wait_for_lnurlw_redemption(resp_json["id"])
print("success: "+str(success))