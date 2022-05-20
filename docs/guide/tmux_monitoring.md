## Monitoring system "tmux" to control the processes

The easiest way to monitor multiple processes at the same time is to open multiple windows. So you can open one for the "app.py" and one for the debug logger `tail -f ~/.lightningATM/debug.log` and then display them side by side. But to watch both processes at the same time in one window, you can use "tmux" (terminal multiplexer). This allows the terminal window to be split vertically into two parts.

###### Install tmux

```
$ cd
$ sudo apt install tmux    
```

###### Necessary commands for the terminal multiplexer (tmux) 

```
CTRL + b -> % = split window
CTRL + b -> right or left arrow = change the window
CTRL + b -> CTRL + right or left arrow = move dividing line
CTRL + b -> d = back to single window
```

###### Start and use tmux

```
$ tmux
```

- Split tmux windows: `CTRL+b -> %`
- Switch between left and right window: `CTRL + b -> right or left arrow`
- If necessary, move the dividing line: `CTRL+b -> CTRL + arrow right or left`

###### Start the `app.py` process (ATM) in the left window

```
	$ cd ~/LightningATM
	$ ./app.py
```

- `Note:`  If you have already activated the autostart function, problems can arise if you start the app.py in the tmux window at the same time. Therefore, it is better to end the service `sudo systemctl stop LightningATM.service` for the tmux and activate it again later `sudo systemctl start LightningATM.service`. See next chapter [`autostart`](/docs/guide/autostart.md).

######  Start `debug.log`

- Switch to the right window and paste or type

```
	$ tail -f ~/.lightningATM/debug.log
```

- Back to single window: `CTRL+b -> d`

Example tmux window

![tmux window](../pictures/tmux_monitoring_terminal.png)

Two withdrawals were made here. Once 5 cents and once 1.60 euros (10 cents + 50 cents + 1 euro). Left side you see the pulses. Right side you see the coins to it. 2 = 5 Cent, 3 = 10 Cent, 5 = 50 Cent, 6 = 1 Euro. The final balance is 152048 satoshis.

---

#### [edit_config](/docs/guide/edit_config.md)  ᐊ  previous | next  ᐅ  [autostart](/docs/guide/autostart.md)

