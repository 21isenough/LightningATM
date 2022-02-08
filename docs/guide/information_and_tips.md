
## Aditional information and tips

- You can get more help in the Telegram group: [https://t.me/lightningatm_building](https://t.me/lightningatm_building)
- When making entries in the Command Line Interface (CLI), it is best to copy and paste the commands:
- -> To do this, copy the command to the clipboard with `STRG+C` and then point to the blinking cursor in the CLI window and press the right mouse button to paste the clipboard into the CLI.
- If you get the error `bash: $: command not found` then you copied the dollar sign `$` in front of the command. Don't do that!
- If you get the error `bash: cd: too many arguments`, you may have to go back one level with `$ cd ~`.
- When logging in via SSH, make sure to use the correct user `pi`. If you accidentally use `admin` or make a typo, you will not see an error, but the password will not be accepted.
- You can change WiFi parameters later with the command: `$ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`
