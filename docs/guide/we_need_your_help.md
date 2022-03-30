## Would you like to help test the new version? 📖🧐

With this update comes a change of the GPIO inputs and outputs. This makes the inputs less sensitive to EMI interference that could lead to unwanted pulses. So if you had sporadic problems with your ATM, you should definitely try this update.

In addition, the function of a lockout relay for the coin acceptor was also implemented with the update. A useful function that one or the other has certainly wished for after the coin impulses were lost or the coin value was incorrectly recognized. A detailed documentation can be found in the new chapter [option: lockout relay](/docs/guide/relay.md).

To participate, you must update your AMT software once with this new version. Don't worry, we have written a step-by-step instructions for this that really anyone can use and all your configuration data such as wallet and settings will be retained. You can easily undo the whole thing afterwards

--- 

### 1. Update to the new version

Log into the RPi and then stop the ATM service once, make a backup from directory LightningATM, clone the new Github to "temp", sync once from "temp" to "LightningAMT" and then delete the "temp" directory that is no longer needed.

    $ sudo systemctl stop LightningATM.service
    $ mv LightningATM LightningATM_Backup
    $ git clone --branch master https://github.com/21isenough/LightningATM.git temp
    $ rsync -a temp/ LightningATM/
    $ sudo rm -r temp
   
### 2. Start and test the version

    $ cd LightningATM
    $ ./app.py

- It takes a few seconds for the display to update, but then..
- The ATM has started and you can use it normally or test the functions.
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
