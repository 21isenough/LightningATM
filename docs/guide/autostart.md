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
