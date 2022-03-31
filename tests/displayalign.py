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

    print("1. display.error_screen(message=ERROR)")
    display.error_screen(message="ERROR")
    sleep(2)
    print("2. display.update_qr_request()")
    display.update_qr_request()
    sleep(3)
    print("3. display.update_qr_failed()")
    display.update_qr_failed()
    sleep(2)
    print("4. display.update_payout_screen()")
    display.update_payout_screen()
    sleep(2)
    print("5. display.update_payment_failed()")
    display.update_payment_failed()
    sleep(2)
    print("6. display.update_thankyou_screen()")
    display.update_thankyou_screen()
    sleep(2)
    print("7. display.update_nocoin_screen()")
    display.update_nocoin_screen()
    sleep(2)
    print("8. display.update_lnurl_generation()")
    display.update_lnurl_generation()
    sleep(2)
    print("9. display.update_shutdown_screen()")
    display.update_shutdown_screen()
    sleep(2)
    print("10. display.update_wallet_scan()")
    display.update_wallet_scan()
    sleep(2)
    print("11. display.update_lntxbot_balance(balance)")
    display.update_lntxbot_balance(123)
    sleep(2)
    print("12. display.update_btcpay_lnd()")
    display.update_btcpay_lnd()
    sleep(2)
    print("13. display.draw_lnurl_qr(qr_img)")
    qrImage = Image.new('1', (122, 122), 255)
    display.draw_lnurl_qr(qrImage)
    sleep(2)
    print("14. display.update_amount_screen()")
    display.update_amount_screen()
    sleep(2)
    print("15. display.update_lnurl_cancel_notice()")
    display.update_lnurl_cancel_notice()
    sleep(2)
    print("16. display.update_button_fault()")
    display.update_button_fault()
    sleep(2)
    print("17. display.update_wallet_fault()")
    display.update_wallet_fault()
    sleep(2)
    print("18. display.update_startup_screen()")
    display.update_startup_screen()
    sleep(2)
    print("19. display.update_blank_screen()")
    display.update_blank_screen()
    sleep(2)
    print("12. init_screen(0)")
    display.init_screen(0)
    sleep(2)
    
    if startService == 1:
        print("LightningATM.service will be started now.")
        os.system('sudo systemctl start LightningATM.service')

if __name__ == "__main__":
   main()