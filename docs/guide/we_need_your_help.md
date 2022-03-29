## We need your help for testing!!! 🙏

With this update comes a change of the GPIO inputs and outputs. This makes the inputs less sensitive to EMI interference that could lead to unwanted pulses. So if you had sporadic problems with your ATM, you should definitely try this update.

In addition, the function of a lockout relay for the coin acceptor was also implemented with the update. A useful function that one or the other has certainly wished for after the coin impulses were lost or the coin value was incorrectly recognized. A detailed documentation can be found in the new chapter [option: lockout relay](/docs/guide/relay.md).

We have added some display messages and button functions and now need beta testers that have one of the following display versions.

- Waveshare 2in7
- PaPiRusZero 2in
- Inky pHAT

The Waveshare 2in13v2, 2in13d and 2in66 has already been tested, but it never hurts if someone else tests it too. 😉
  
For help testing you need the button. _`Note:`If you don't have it yet, you can quickly "simulate" it yourself. Just short-circuit like pin 17 and 29 from the [wiring](/docs/guide/wiring.md)._ We added two new display messages and a button function that shows all display messages if you push the button 9 times. All button functions a described [here](/docs/guide/button.md). We want to know if everything works and, above all, if the last two display messages no. 14 and 15 are shown correctly.

To participate, you must update your AMT software once with our trial version. Don't worry, I've written step-by-step instructions for this that really anyone can use and all your configuration data such as wallet and settings will be retained. You can easily undo the whole thing afterwards

--- 

### 1. Update to the new trial version

Log into the RPi and then stop the ATM service once, make a backup from directory LightningATM, clone the new Github to "temp", sync once from "temp" to "LightningAMT" and then delete the "temp" directory that is no longer needed.

    $ sudo systemctl stop LightningATM.service
    $ mv LightningATM LightningATM_Backup
    $ git clone https://github.com/21isenough/LightningATM.git
   
### 2. Start and test the trial version

    $ cd LightningATM
    $ ./app.py

- It takes a few seconds for the display to update, but then..
- The ATM has started and you can use it normally or test the functions.
- `Note:` If you "simulate" the button you may have to set the `payoutdelay = 0` in the `config.ini` to aktivate the button. See [edit_config](/docs/guide/edit_config.md). 
- `Note:` Be careful not to press the button 7 times. This will delete your wallet data and you will have to re-enter or scan it.
- If you press the button 9 times, all 16 messages should be displayed once. You can also track this in the terminal. 
- You can ignore the first message. The message looks a bit strange. 😜 There is still work to do!
- Stop the ATM with `CTRL+C`

### 3. If you don't like this version and want to get rid of it 

Make the backup the major version again and then delete the backup.

    $ cd
    $ rsync -a LightningATM_Backup/ LightningATM/
    $ sudo rm -r LightningATM_Backup

- Everthing should now be as befor. Even the wallat data.
- Check if you have set a temporary button and reset it with `payoutdelay = 12` in the `config.ini`

### 4. Final step

Restart the LightningATM service

    $ sudo systemctl start LightningATM.service

- Your ATM should now restart as usual
- If you find some issues or have some suggestions call @AxelHamburch in the telegram group or on Github

## Thank you for your support! ❤️