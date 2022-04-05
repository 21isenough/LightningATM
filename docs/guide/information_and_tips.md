
## Aditional information and tips

- You can get more help in the Telegram group: [https://t.me/lightningatm_building](https://t.me/lightningatm_building)
- When making entries in the terminal window (CLI = Command Line Interface), it is best to copy and paste the commands: 

  > Copy the command to the clipboard with `STRG+C` and then point to the blinking cursor in the CLI window and press the right mouse button to paste the clipboard into the terminal window. (If it doesn't work, make the terminal window "activ" - with one left click on the window or even move the curser with tap space bar - befor you do the right click.)
- If you get the error `bash: $: command not found`, you may have copied the dollar sign "$" in front of the command. Don't do that!
- When logging in via SSH, make sure to use the correct user `pi`. If you accidentally use `admin` or make a typo, you will not see an error, but the password will not be accepted
- You can change WiFi parameters with the command: `$ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`
- A collection of the most used commands for quick access:

  ```
  cd ~/LightningATM/
  ./app.py
  nano ~/.lightningATM/config.ini
  tail -f ~/.lightningATM/debug.log
  sudo systemctl status LightningATM.service
  sudo systemctl stop LightningATM.service
  sudo systemctl start LightningATM.service
  ```
---

#### [autostart](/docs/guide/autostart.md)  ᐊ  previous | next  ᐅ  [option: language](/docs/guide/languages.md) 
