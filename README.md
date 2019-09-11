# LightningATM

This LightningATM was built to distribute small amounts of BTC - obviously - it only accepts coins. It shall demonstrate the power of Bitcoins Lightning Network. A two cent coin is enough to buy some satoshis at the LightningATM.

A physical coin exchanged into bitcoin and send to your lightning wallet in seconds. Use this project to educate your family and friends or guests at your bitcoin meetup - a convenient and easy on-boarding process for people that are new to bitcoin.

![alt text](https://github.com/21isenough/LightningATM/blob/master/resources/startup_screen.jpg)

### Parts list

1. Raspberry Pi Zero WH - http://bit.ly/2maXBr6
If you can, get the version WH (not just W). It comes with pre soldered headers and can be used out of the box.

2. 16 GB SD Card - http://bit.ly/2kterBb
8 GB SD card will also work and is fine. Just pick any brand with a reasonably good rating.

3. PaPiRus Zero - ePaper / eInk Screen - http://bit.ly/2kdSOVh
This is the 2 inch ePaper display that I'm using in my build. My Python scripts are built to talk to the manufacturers library.

4. Raspberry Pi Zero Camera (5MP) - http://bit.ly/2kuPvt1
Make sure you buy a camera which also comes with the narrower ribbon cable (Pi Zero Ribbon Cable). The Raspberry Pi Zero has a different CSI camera connector than the other versions.

5. Coin Acceptor 616 - http://bit.ly/2lHfoWK
This coin acceptor can accept up to 6 different coins. It can learn what coins you want to use it with. The setup process happens manually on the acceptor itself, not through any software.

6. Button - http://bit.ly/2lK4AqR
Any button that can close a power circuit will do the trick. Don't use a switch that stays permanently in its new position - a click button that is only closed while pressing it.

7. Jumper Cables - http://bit.ly/2kfGns4
You will need a bunch of jumper cables to connect all the components with each other. Make sure you've got some variety (male and female) as you will need to connect different types of pins with each other.

8. Power supply
I'm working on a solution that lets you use just one power supply. For now you need 5V for the Raspberry Pi Zero (supplied through USB) and another 12V power supply to power the coin acceptor (preferably with a balun for easier connecting).

### Todo

- [x] QR code scan function
- [x] Validate requested amount
- [x] Reject to high amounts
- [x] Add config file
- [x] Add parts list to readme
- [ ] Store data in database
- [ ] Inform about failed scan
- [ ] Ask for rescan of QR code
- [ ] Find a faster solution for QR scans (zbarcam)
- [ ] Rethink the design decisions in regards to hardware
- [ ] Find solution to work without jumper cables
- [ ] Add encryption of admin.macaroon in idle mode
- [ ] Add AP option for users to login into their wifis (https://github.com/21isenough/RaspiWiFi)
