from configparser import ConfigParser
import logging
import os
import math
from shutil import copyfile

from papirus import Papirus

import utils

home = os.path.expanduser("~")
ATM_data_dir = home + "/.lightningATM/"
config_file_path = ATM_data_dir + "config.ini"
# check the config directory exists, create it if not
if not os.path.exists(ATM_data_dir):
    os.makedirs(ATM_data_dir)

logging.getLogger("requests").setLevel(logging.INFO)
logging.basicConfig(
    filename="{}/debug.log".format(ATM_data_dir),
    format="%(asctime)-23s %(name)-9s %(levelname)-7s | %(message)s",
    datefmt="%Y/%m/%d %I:%M:%S %p",
    level=logging.DEBUG,
)
logger = logging.getLogger("CONFIG")


yes = ["yes", "ye", "y"]
no = ["no", "n"]


def ask_scan_config_val(section, variable):
    while True:
        try:
            res = input(
                "Do you want to scan to input {} {}".format(section, variable)
            ).lower()
            if res in yes:
                # value = scan the qr for the value
                # update_config(section, variable, value
                ...
            elif res in no:
                return
            else:
                print("Input invalid, please try again or KeyboardInterrupt to exit")
        except KeyboardInterrupt:
            return


def check_config():
    """Checks the config and prompt the user to provide values for missing keys
    """
    if conf["lnd"]["macaroon"] is (None or ""):
        logger.warning("Missing value for lnd macaroon in config")
        ask_scan_config_val("lnd", "macaroon")
    if conf["lntxbot"]["creds"] is (None or ""):
        logger.warning("Missing value for lntxbot credential in config")
        ask_scan_config_val("lntxbot", "creds")


def update_config(section, variable, value):
    """Update the config with the new value for the variable.
    If dangermode is on, we save them to config.ini, else we write them to the temporary
    dictionary
    """
    if conf["atm"]["dangermode"].lower() == "on":
        config = create_config()
        config[section][variable] = value

        with open(CONFIG_FILE, "w") as configfile:
            config.write(configfile)
    else:
        conf[section][variable] = value


def check_dangermode():
    if conf["atm"]["dangermode"].lower() == "on":
        return True
    else:
        return False


# config file handling
def get_config_file():
    # check that the config file exists, if not copy over the example_config
    if not os.path.exists(ATM_data_dir + "config.ini"):
        example_config = os.path.join(os.path.dirname(__file__), "example_config.ini")
        copyfile(example_config, ATM_data_dir + "config.ini")
    return os.environ.get("CONFIG_FILE", config_file_path)


def create_config(config_file=None):
    parser = ConfigParser(allow_no_value=True)
    parser.read(config_file or CONFIG_FILE)
    return parser


CONFIG_FILE = get_config_file()
conf = create_config()

######################################################
### (Do not change and of these parameters unless  ###
### you know exactly what you are doing.           ###
######################################################

# TODO: Add variable to set certificate check to true or false

# Papirus eInk size is 128 x 96 pixels
WHITE = 1
BLACK = 0
PAPIRUSROT = 0
PAPIRUS = Papirus(rotation=PAPIRUSROT)

# Fiat and satoshi variables
FIAT = 0
SATS = 0
SATSFEE = 0
INVOICE = ""

# Set btc and sat price
BTCPRICE = utils.get_btc_price(conf["atm"]["cur"])
SATPRICE = math.floor((1 / (BTCPRICE * 100)) * 100000000)

# Button / Acceptor Pulses
LASTIMPULSE = 0
PULSES = 0
LASTPUSHES = 0
PUSHES = 0
