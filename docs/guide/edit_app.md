### Special settings in the app.py file

##### Open the app.py

```
$ cd ~/LightningATM/
$ nano app.py
```

##### Optional setting: Skip the "Prepare for LNURL" page:

- Search for `display.update_lnurl_cancel_notice()` with `CTRL+W`. (It exists twice)
- There is a place where it says `if activewallet == "lntxbot"`, please edit the two lines

###### Comment out the following two lines with `#`

```
	# display.update_lnurl_cancel_notice()
	# time.sleep(5)
```

-> This will skip the LNURL "query page" as it is not relevant for the pocket version (without push button).

#####  Alternative setting: coin preselection if the setting in config.ini does not work:

###### Adjustment of the pulses for the respective coins

- Search for `if config.PULSES == 2` in app.py with `CTRL+W`
- There you will find the setting options for the coins. 
- Note: If you can't find `if config.PULSES == 2` in the app.py file, then you might have a higher version then V3.0.0 and the coin settings are in the config.ini. You can skip this point.

######  For example:

```
	if config.PULSES == 2:
			config.FIAT += 0.02
			..
			logger.info("2 cents added")
			..
```

The settings are now set in the same way as the coin validator is parameterized:

###### For the example, two pulses = 5 cents

```
	if config.PULSES == 2:
			config.FIAT += 0.05
			..
			logger.info("5 cents added")
			..
```

- Repead the change up to 2 euros = 2.00 (200 cents)
- Note: As I said, you only have to do this if the setting in config.ini doesn't work

![edit app](https://i.imgur.com/MTiekSX.png)
app.py - Skip the "Prepare for LNURL" (just an example)


