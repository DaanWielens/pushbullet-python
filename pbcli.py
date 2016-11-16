#!/usr/local/bin/python
import requests
import sys
import os.path

# Get pushbullet token from text file (file should contain token only)
if os.path.isfile('pb_token.txt') == False:
    print('The file pb_token.txt seems to be missing.')
    sys.exit()
global TOKEN
with open('pb_token.txt', 'r') as file:
    TOKEN = file.read().replace('\n','')

# Function to send a note. Usage: import pbcli --> pbcli.note(ttl,msg)
def note(ttl,msg):
    url = "https://api.pushbullet.com/v2/pushes"
    data = dict(type="note", title=ttl, body=msg)
    nreq = requests.post(url, json=data, auth=(TOKEN, '')).json()

# Function to send a file
def pfile(fname,fpath,msg):
    # First request authorization to upload a file
    url = "https://api.pushbullet.com/v2/upload-request"
    ext = fpath.split('.')[-1]
    if ext == 'jpg':
        f_type = 'image/jpeg'
    elif ext == 'png':
        f_type = 'image/png'
    elif ext == 'pdf':
        f_type = 'application/pdf'
    else:
        print('Supported file types:\njpg, png, pdf')
        sys.exit()

    f_name = fpath.split('/')[-1]
    data = dict(file_name=f_name, file_type=f_type)
    nreq = requests.post(url, json=data, auth=(TOKEN, '')).json()
    rf_name = nreq['file_name']
    rf_type = nreq['file_type']
    rf_durl = nreq['file_url']
    rf_uurl = nreq['upload_url']

    # Upload the file_url
    f = {'file': open(fpath,'rb')}
    ureq = requests.post(rf_uurl, files=f)

    # Push the file
    url = "https://api.pushbullet.com/v2/pushes"
    data = dict(type="file", body=msg, file_name=fname, file_type = rf_type, file_url = rf_durl)
    freq = requests.post(url, json=data, auth=(TOKEN, '')).json()

# Function to list active devices
def listdevices():
    url = "https://api.pushbullet.com/v2/devices?active=true"
    ldreq = requests.get(url, auth=(TOKEN, '')).json()
    Devices = ldreq['devices']
    for i in range(0,len(Devices)):
        print(Devices[i]['iden'] + ' ' + Devices[i]['nickname'])

# Function to send a note to a specific device
def notetodevice(ttl,msg,iden):
    url = "https://api.pushbullet.com/v2/pushes"
    data = dict(type="note", title=ttl, body=msg, device_iden=iden)
    nreq = requests.post(url, json=data, auth=(TOKEN, '')).json()

# Standalone python script:
correct_input = 0
if len(sys.argv) > 1:
    if '-' in sys.argv[1]:
        if (sys.argv[1] == '-n') and (len(sys.argv) == 4):
            note(sys.argv[2], sys.argv[3])
        if (sys.argv[1] == '-f') and (len(sys.argv) == 5):
            pfile(sys.argv[2], sys.argv[3], sys.argv[4])
        if (sys.argv[1] == '-l') and (len(sys.argv) == 2):
            listdevices()
        if (sys.argv[1] == '-d') and (len(sys.argv) == 5):
            notetodevice(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            correct_input = 1
else:
    correct_input = 1

if correct_input == 1:
    print('\nPushbullet Command Line Interface - Standalone usage:')
    print('----------------------------------------------------------------------')
    print('Send a note:         python pbcli.py -n title message')
    print('Send a file:         python pbcli.py -f filename /path/to/file message')
    print('List active devices: python pbcli.py -l')
    print('Send note to device: python pbcli.py -d title message device_identifier')
    print('')
