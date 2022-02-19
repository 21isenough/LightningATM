## Autostart

######  Activate the Service:

```
$ cd ~/LightningATM
$ sudo cp LightningATM.service /etc/systemd/system/LightningATM.service
$ sudo systemctl enable LightningATM.service
$ sudo reboot
```

######  Other commands to control the service:

```
$ sudo systemctl status LightningATM.service
$ sudo systemctl stop LightningATM.service
$ sudo systemctl start LightningATM.service
```

- Note: From now on the ATM will start automatically after booting. If you want to observe the app.py in tmux, you should `stop` the "LightningATM.service" manually, bevor you start the app.py in the tmux. Don't forget to `start` the service again afterwards.

---

#### [tmux_monitoring](/docs/guide/tmux_monitoring.md)  ᐊ  previous | next  ᐅ  [camera](/docs/guide/camera.md)
