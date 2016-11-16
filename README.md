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

Current features:
* Send notes to self (all devices)
* Send file to self
* List active devices
* Send note to a specific device (requires `device_iden` which can be retrieved by running the `listdevices()` module)

*Note: pbcli can be imported as a module or can used as a standalone script!*

Usage (as a function):
```
python
import pbcli
pbcli.note(title, message)
pbcli.file(filename, pathtofile, message)
pbcli.listdevices()
pbcli.notetodevice(title, message, device_identifier)
```

Usage (standalone):
```
python pbcli.py -n title message
python pbcli.py -f filename pathtofile message
python pbcli.py -l
python pbcli.py -d title message device_identifier
```
