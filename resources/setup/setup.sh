#!/usr/bin/env bash

curl -sSL https://raw.githubusercontent.com/21isenough/PaPiRus/master/install | sudo bash
wget https://raw.githubusercontent.com/21isenough/LightningATM/master/resources/setup/show_ip.py
python3 show_ip.py
sudo shutdown -r now
