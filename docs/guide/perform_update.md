## Instruction to update the ATM 📜🧐

We have now added LNbits and Blink as a new funding source for the LightningATM. 🎉

### 1. Quick guide on how to set up an LNbits wallet or Blink wallet

A quick guide how to set up an LNbits wallet find [here](/docs/guide/set_up_an_lnbits_wallet.md)

A quick guide how to set up an Blink wallet find [here](/docs/guide/set_up_a_blink_wallet.md)

### 2. Update the LigthningATM 

Connect the ATM to the power supply and log in to your LightningATM via [Wifi/SSH](https://github.com/21isenough/LightningATM/blob/master/docs/guide/sdcard_and_wifi.md#carry-out-basic-software-settings-and-updates). You may find the IP in the network of your router. Open a command line editor and write the command `ssh pi@192.168.x.x`. Hopefully you still have the assigned password. We will now load the new repository on the ATM and activate it. You have to stop the `LightningATM.service` once, otherwise you will get a strange display and the ATM will not work properly.  

    $ sudo systemctl stop LightningATM.service
    $ cd ~/LightningATM
    $ git pull
    
Now your ATM is set to the new version. Next you have to configure it for the new wallet.
    
### 3. Edit the config.ini

    $ nano ~/.lightningATM/config.ini

#### Add the following lines at the very end for LNbits and 🆕 for Blink

```
[lnbits]
# api credentials
url = https://legend.lnbits.com/api/v1
apikey = 
# One of "invoice" or "lnurlw"
method = lnurlw
# only for lnurlw - millisseconds to redeem the lnurlw
timeout = 90000

[blink]
graphql_endpoint = https://api.blink.sv/graphql
api_key = blink_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
wallet_id = 5dxxxxxxxxxxxxxxxxxxxxx
```

`Note for LNbits:` Customize your `apikey = 8682516eaf0c457...` from the LNbis wallet. See [here](/docs/guide/set_up_an_lnbits_wallet.md)

`Note for Blink:` Customize your `api_key` and `wallet_id` from Blink wallet. See [here](/docs/guide/set_up_a_blink_wallet.md). 

#### Change active wallet to LNbits

    [atm]
    ..
    activewallet = lnbits

#### Or change active wallet to Blink

    [atm]
    ..
    activewallet = blink

and

    [lnurl]
    lnurlproxy = active
    
#### In case you have a very old config.ini. Check this too.

    [atm]
    ..
    # Set language: "en", "de", "fr", "it", "es", "pt", "tr" currently available
    language = en

    # Do you have a camera? "False" or "True"
    camera = False
    
Example, see [here](https://github.com/21isenough/LightningATM/blob/master/example_config.ini).
    
Save and exit editor: `CTRL+x` -> `y` -> `Enter`
   
### 4. Start ATM for testing

    $ cd LightningATM
    $ ./app.py

- It takes a few seconds for the display to update..
- The ATM has started and you can use it normally or test the functions.
- Stop the ATM with `CTRL+C`

To debug: Launch a second terminal window, login with ssh and access logs with 

    $ tail -f ~/.lightningATM/debug.log
    
Log file to debug
![Log file to debug](../pictures/perform_update_logs.png)

### 5. Final step

Restart the LightningATM service by power cycle

    $ sudo systemctl start LightningATM.service

- Your ATM should now restart as usual

#### [README](/README.md)  ᐊ  previous
