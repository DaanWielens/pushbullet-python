# pushbullet-python
This repo contains all Python-based Pushbullet scripts.

###### Dependencies for all scripts
Make sure that a file `pb_token.txt` is in the same folder as the python script. This textfile needs to contain your pushbullet token (no encoding or whatever, just plain text).

###Pushbullet.py
A GUI version of the Pushbullet application.

Current features:
* list received pushes
* send notes to self
* list (active) devices
* list (active) chats

To run, simply type
```bash
python Pushbullet.py
```

###pbcli.py
Python module that can be used in any Python script to send Pushbullet notes or files easily.

*Note: pbcli can also be used as a standalone script!*

Usage (as a function):
```
python
import pbcli
pbcli.note(title, message)
pbcli.file(filename, pathtofile, message)
```

Usage (standalone):
```
python -n title message
python -f filename pathtofile message
```
