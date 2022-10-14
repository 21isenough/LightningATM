## Set up and test the display

### Update display software

```
$ cd
$ git clone https://github.com/AxelHamburch/e-Paper/
$ cd ~/e-Paper/RaspberryPi*/python
$ sudo python3 setup.py install
```
`Info:` Normally cloning is done from the current Waveshare repository [https://github.com/waveshare/e-Paper](https://github.com/waveshare/e-Paper), but the new version currently still has problems with the recommended ATM configuration. Therefore, an older backup of "AxelHamburch" is recommended here for the time being.

###  Testing the display

`Note:` This is special for the "Waveshare 2in13 V2". Yours may be different, **check your version** carefully!

```
$ cd ~/e-Paper/RaspberryPi_JetsonNano/python/examples
$ sudo python3 ./epd_2in13_V2_test.py
```

If everything has been correctly connected and installed, the display will now show a demonstration and finally the screen will cleare.

`Help:`If it dosn't work, try the D-Version (flexible): `$ sudo python3 ./epd_2in13d_test.py`. Another option is the display "Waveshare 2in13 V3",  it is a new display. `$ sudo python3 ./epd_2in13_V3_test.py`. (Work is in progress to fully support the V3).
If you have a display from waveshare not listed here, try to find the right display type in the [waveshare repository](https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python/examples).

display demo

<img src="../pictures/display_demo.jpg" width="500">

`Note:` If it dose not work, check the wiring and your display version again.

---

#### [sdcard_and_wifi](/docs/guide/sdcard_and_wifi.md)  ᐊ  previous | next  ᐅ  [edit_config](/docs/guide/edit_config.md)
