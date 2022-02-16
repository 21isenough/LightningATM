## Monitoring system "tmux" to control the processes

This allows the terminal window to be split vertically into two parts to observe two processes at the same time.

###### Command overview for the terminal multiplexer (tmux) 

```
CTRL + b -> % = split window
CTRL + b -> right or left arrow = change the window
CTRL + b -> CTRL + right or left arrow = move dividing line
CTRL + b -> d = back to single window
```

###### Install tmux

```
$ cd ~
$ sudo apt install tmux    
```

###### Start and use tmux

```
$ tmux
```

- Split tmux windows: `CTRL+b -> %`
- Switch between left and right window: `CTRL + b -> right or left arrow`

###### Start the `app.py` process (ATM) in the left window

```
	$ cd ~/LightningATM
	$ ./app.py
```

- Note: If the ATM is already started (check with `$ sudo systemctl status LightningATM.service`), you should stop it (with `$ sudo systemctl stop LightningATM.service`) before starting it in manually (with `.app.py`) in the tmux terminal window. Otherwise strange phenomena may occur. 

######  Start `debug.log`

- Switch to the right window and paste or type

```
	$ tail -f ~/.lightningATM/debug.log
```

- If necessary, move the dividing line: `CTRL+b -> CTRL + arrow right or left`
- Back to single window: `CTRL+b -> d`

Example tmux window

![tmux window](https://i.imgur.com/sJ68zFW.png)

Left side you see the pulses. Right side you see the coins to it. 5, 2, 7, 2 => 50 Cent, 5 Cent, 2 Euro, 5 Cent
