## Monitoring system (tmux) to control the processes

###### Terminal multiplexer (tmux) command overview:

```
CTRL + b -> % = split window
CTRL + b -> right or left arrow = change the window
CTRL + b -> CTRL + right or left arrow = move dividing line
CTRL + b -> d = back to single window
```

This allows the CLI window to be split vertically into two parts to observe two processes at the same time.

###### install tmx

```
$ cd ~
$ sudo apt install tmux    
```

###### Start and use tmux

```
$ tmux
```

- Split tmux windows: `CTRL+b -> %`

###### Start the `app.py` process (ATM).

```
	$ cd ~/LightningATM
	$ ./app.py
```

- Switch to the right window: `CTRL+b -> right arrow`
- Note: If the ATM is already started (check with `$ sudo systemctl status LightningATM.service`), you should stop it (with `$ sudo systemctl stop LightningATM.service`) before starting it in manually (with `.app.py`) in the tmux terminal window. Otherwise strange phenomena may occur. 

######  Start `debug.log`

```
	$ tail -f ~/.lightningATM/debug.log
```

- If necessary, move the dividing line: `CTRL+b -> CTRL + arrow right or left`
- Back to single window: `CTRL+b -> d`

Example tmux window

![tmux window](https://i.imgur.com/sJ68zFW.png)

Left side you see the pulses. Right side you see the coins to it.
