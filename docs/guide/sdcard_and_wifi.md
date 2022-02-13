## Create SD card and write WiFi data to it

### Download the image and write it to the SD card

- Download the Raspbian image "2019-04-08-raspbian-stretch-lightningatm.gz" from the LightningATM Docs page
- [https://docs.lightningatm.me/lightningatm-setup/hardware-setup/assembly-and-software](https://docs.lightningatm.me/lightningatm-setup/hardware-setup/assembly-and-software)
- Write SD card image with Balena Etcher
- [https://www.balena.io/etcher/](https://www.balena.io/etcher/)
- Take out the SD card and put it aside

### Set up WiFi for the Raspberry Pi

Create a file named `wpa_supplicant.conf` with the following content:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=DE

network={
	ssid="Home"
	scan_ssid=1
	psk="XXXXXXXXXXXX"
	id_str="Home"
}

network={
	ssid="Mobil"
	scan_ssid=1
	psk="12345678"
	id_str="Mobil"
}
```

- Change country code to your [area code](https://www.arubanetworks.com/techdocs/InstantWenger_Mobile/Advanced/Content/Instant%20User%20Guide%20-%20volumes/Country_Codes_List.htm)
- The file contains two WiFi networks. "Home" for home use and the "Mobil" for mobility
- "Mobil" can be you hotspot on your cell phone 
- Adjust the values ​​for SSID and PSK as you like
- More networks can be added if needed
- Make sure the file ends with `.conf` and **not** in `.conf.txt`
- In the basic setting, Windows has the habit of hiding known file type extensions
- See "Folder Options/View/Advanced Settings"
- -> "Hide extensions for known file types" must be deselected!
- Slide the newly written SD card back into the slot
- -> The BOOT directory of the SD card is displayed
- Copy the new file `wpa_supplicant.conf` into it
- Note: After starting the Raspberry Pi for the first time, the ".conf" file disappears from the directory
- It can then be edited later via CLI by the command:
- `$ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

## Carry out basic software settings and updates

- Insert the SD card into Raspberry Pi
- Check the wiring again and then apply voltage
- Wait for a while and then look for the assigned WiFi IP in your own WiFi router
- Login to Raspberry Pi via CLI: `ssh pi@192.168.x.x`
- Confirm `The authenticity..` with `yes`
- Enter `raspberry` in the password prompt
- If you are logged in correctly you will now see: `pi@raspberrypi:~ $`

#### Adjust password and please remember!

```
	$ passwd
```

- Note: `$` stands for `pi@raspberrypi:~ $` in CLI and does not need to be typed

#### Perform an update, clone the ATM Github and install necessary additional options

```
	$ sudo apt update && sudo apt upgrade
	$ git clone https://github.com/21isenough/LightningATM.git
	$ cd LightningATM
	$ pip3 install -r requirements.txt
```

- Note: When updating, you sometimes have to confirm with `y` or `q`
- Now disconnect the power supply and log in again via SSH with the new password
