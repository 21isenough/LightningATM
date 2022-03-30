## Autostart and start/stop the ATM

######  Install and activate the autostart service:

```
$ cd ~/LightningATM
$ sudo cp LightningATM.service /etc/systemd/system/LightningATM.service
$ sudo systemctl enable LightningATM.service
$ sudo reboot
```

- From now on the ATM will start automatically after booting.

######  Commands to control the ATM:

```
$ sudo systemctl status LightningATM.service
$ sudo systemctl stop LightningATM.service
$ sudo systemctl start LightningATM.service
```

- `Note:` When the autostart service is once installed and activated, you only need to "start" the ATM if you previously stopped the ATM.
- `Note:` If you want to observe the app.py in tmux, you musst `stop` the "LightningATM.service" manually, bevor you start the app.py in the tmux. Then restart the ATM with the "start" command or simply restart the entire ATM afterwards by unplugging the power and plugging it back in.

---

#### [debugging and tmux](/docs/guide/tmux_monitoring.md)  ᐊ  previous | next  ᐅ  [information_and_tips](/docs/guide/information_and_tips.md)
