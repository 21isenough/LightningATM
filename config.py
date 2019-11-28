from configparser import ConfigParser
import logging
import os
from shutil import copyfile

from papirus import Papirus

import utils


home = os.path.expanduser("~")
ATM_data_dir = home + "/.lightningATM/"
config_file_path = ATM_data_dir + "config.ini"

logging.basicConfig(
    filename="{}/debug.log".format(ATM_data_dir),
    format="%(asctime)-23s %(name)-9s %(levelname)-7s | %(message)s",
    datefmt="%Y/%m/%d %I:%M:%S %p",
    level=logging.INFO,
)


def update_config(section, variable, value):
    """Update the config with the new value for the variable
    """

    config = create_config()
    config[section][variable] = value

    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)


# config file handling
def get_config_file():
    # check the config directory exists, create it if not
    if not os.path.exists(ATM_data_dir):
        logging.debug(
            "Config directory not found, creating directory at: {}".format(ATM_data_dir)
        )
        os.makedirs(ATM_data_dir)
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


# TODO: Add variable to set certificate check to true or false
# TODO: Add var for fee in %

# Papirus
WHITE = 1
BLACK = 0
PAPIRUSROT = 0
PAPIRUS = Papirus(rotation=PAPIRUSROT)

# Set sat, fiat
FIAT = 0
SATS = 0
INVOICE = ""

# Set btc and sat price
BTCPRICE = utils.get_btc_price(conf["atm"]["cur"])
SATPRICE = round((1 / (BTCPRICE * 100)) * 100000000, 2)

# Button / Acceptor Pulses
LASTIMPULSE = 0
PULSES = 0
LASTPUSHES = 0
PUSHES = 0
