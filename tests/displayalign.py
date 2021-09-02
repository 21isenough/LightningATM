import os
import sys
import getopt
import inspect
import RPi.GPIO as GPIO
import subprocess

from time import sleep
from PIL import Image

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import config
import utils

pwd = os.popen('pwd').read()
pwd = pwd.strip('\n')

if (pwd != '/home/pi/LightningATM') :
    print('This test must be executed in the directory /home/pi/LightningATM')
    print('This test is executed in the directory', pwd)
    sys.exit("Exit python script, because it has executed from the wrong path")

display_config = config.conf["atm"]["display"]
display = getattr(__import__("displays", fromlist=[display_config]), display_config)

print('The config.ini was read out. The following display will be tested:')
print(display)
print()

#systemctl is-active LightningATM.service -> 0 = active 768 = inactive
#sudo systemctl stop LightningATM.service -> inactive

# os.system will return 0 for service is active else inactive.
status = os.system('systemctl is-active --quiet LightningATM.service')

startService = 0

if status == 0:
    print("LightningATM.service is started and will be stopped now.")
    os.system('sudo systemctl stop LightningATM.service')
    startService = 1
else:
    print("LightningATM.service is not started, display test starts now.")


def main():

    display.update_startup_screen()
    sleep(3)
    display.update_qr_request()
    sleep(3)
    display.update_qr_failed()
    sleep(3)
    display.update_payout_screen()
    sleep(3)
    display.update_payment_failed()
    sleep(3)
    display.update_thankyou_screen()
    sleep(3)
    display.update_nocoin_screen()
    sleep(3)
    display.update_lnurl_generation()
    sleep(3)
    display.update_shutdown_screen()
    sleep(3)
    display.update_wallet_scan()
    sleep(3)
    display.update_lntxbot_balance(123)
    sleep(3)
    display.update_btcpay_lnd()
    sleep(3)
    
    qrImage = Image.new('1', (122, 122), 255)
    display.draw_lnurl_qr(qrImage)
    sleep(3)
    display.update_amount_screen()
    sleep(3)
    display.update_lnurl_cancel_notice()
    sleep(3)
    display.update_blank_screen()
    sleep(3)
    display.init_screen(0)
    sleep(3)
    
    if startService == 1:
        print("LightningATM.service will be started now.")
        os.system('sudo systemctl start LightningATM.service')

if __name__ == "__main__":
   main()