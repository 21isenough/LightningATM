### Configure validator checker (6 coins, 5 cents to 2 euros)

- Set the switches on the coin validator to "NO" and "Medium".
- Apply the 12V to the coin validator (without Raspberry Pi) => The coin validator will flash and show 0
- Press and hold simultaneously the ADD and MINUS buttons until A appears in the display
- When B appears, switch back to A by ADD or MINUS
- Press and hold the SET button briefly, until E will appears on the display
- This indicates: You are in them menu to set the amount of differnet coin types 
- Set to 6 (6 coins = 5 cents to 2 euros) with ADD (or MINUS) and press SET
- Now the display shows H1 (for the first coin). The first of 6 LEDs has come on
- Now specify how often the coin should be inserted for calibration
- Set to 20 with ADD (or MINUS) and then press SET
- The display now shows P1 for further settings of coin 1 and you can define the output signal
- 5 cents = 2 pulses / 10 cents = 3 / 20 cents = 4 / 50 cents = 5 / 10 euros = 6 / 2 euros = 7
- Set to 2 pulses (for 5 cents) with ADD (or MINUS) and then press SET
- The last thing on the display is F1, which represents the accuracy of the coin recognition. The value 8 worked well
- Set to 8 with ADD (or MINUS) and then press SET
- The parameters for the first coin have now been set 
- Now the second LED is on and the display shows H2
- Now repeat the same steps again for the second coin (e.g. 10 Cent) up to coin 6 vor (e.g. 2 Euro)
- When all coins are set, all LEDs flash briefly to confirm and the display shows A again
- After a short time, 0 (zero) appears again in the display

### Calibrating the coin validator

- Press the SET button twice
- The first LED light and A1 will show in the display
- Now insert the first coin (5 cents) 20 times
- Use as many different coins as posible
- Finally all LEDs flash to confirm and the display shows A2
- Repeat for the remaining coin types
- All LEDs flash briefly again to confirm and the display shows 0 (zero) again
- The coin validator is now ready.

coin validator

<img src="https://i.imgur.com/bnyfBGZ.jpg" width="600">

coin calibration
[coin calibration](https://imgur.com/Xc1TAGF)

