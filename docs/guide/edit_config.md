##  Setting the config.ini

Basic settings are made in `config.ini` 

- Login on Raspberry Pi via CLI: `ssh pi@192.168.x.x`

### Start ATM once to create the config.ini

```
$ cd ~/LightningATM/
$ ./app.py
```

- The app.py (the ATM) was started and the config.ini file was created
- The display should now show `LightningATM` (You must have tested the display first!)
- The process or the ATM can be interrupted/stopped with `CTRL+C`
- After a short time, `Manually Interrupted` is shown in the terminal windos and you should see `ATM is turned off` on the display

### Open the config.ini file

```
$ nano ~/.lightningATM/config.ini
```

- Don't be surprised, the spelling is really `~/.lightningATM/config.ini` with a dot and lowercase letters

### Set the config.ini file

###### Enter display type under `[atm]`

```
	display = waveshare2in13v2
```
`Note:` Please compare the display type. Yours may require different settings.

###### *Only for Pocket Version:* Delay time (set from 0 to 12 seconds)

```
	payoutdelay = 12 
```

- Its needed for the the pocket version, because it has no push button for confimrmation. The invoice will be generated automatically after 12 seconds
- Note: If you have a button version, you must keep the 0.

###### Set activate wallet type / example LNTXBOT

- If you would like to set a BTCPayServer wallet, get further information here: [BTCPayServer](https://docs.lightningatm.me/lightningatm-setup/wallet-setup/lnd_btcpay)
- Note: A good guide to getting started with the LNTXBOT can be found here: [coincharge.io](https://coincharge.io/en/lntxbot-telegram-lightning-wallet/)

```
	activewallet = lntxbot
```

###### Under `[lntxbot]` enter the data for the API to the lntxbot

```
[lntxbot]
# base64 encoded lntxbot api credentials
url = https://lntxbot.com
creds = abc..xyz==
```
  
- Note: The LNTXBOT delivers `url` and `creds` with the command `/lightningATM` from you Telegram bot
- The structure from the bot answer is build up like: `<creds>@<url>`

###### Set the coins to the pulses

```
[coins]
# Pulsecount, fiat value, name
coin_types = 2,0.05,5  eur cent
             3,0.10,10 eur cent
             4,0.20,20 eur cent
             5,0.50,50 eur cent
             6,1.00,1 eur
             7,2.00,2 eur
```

- To save and exit the editor: `CTRL+x -> y -> ENTER`
- Note: In version 3.0.0 you still had to make the setting in app.py. I don't know which version you get, but if the settings with the config.ini don't work, you can set them directly in the app.py. I wrote something about that in the next chapter "[edit app.py](edit_app.py)". But if you are lucky, it might be enough to set it here in the config.ini. You have to test it out. With the monitoring system (tmux), explanation see chapter "[tmux monitoring](tmux_monitoring)", you can see that well.

config.ini part 1 (just an example)
![config.ini part 1](https://i.imgur.com/ljIeZj4.png)

config.ini part 2 (just an example)
![config.ini part 2](https://i.imgur.com/YtXtSZC.png)










