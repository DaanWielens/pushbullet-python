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

# This script is a function to send notes easily from any application/script:
# - Place this file in the project folder
# - import pbcli
# - pbcli.note("title","message")
def note(ttl,msg):
    url = "https://api.pushbullet.com/v2/pushes"
    data = dict(type="note", title=ttl, body=msg)
    nreq = requests.post(url, json=data, auth=(TOKEN, '')).json()

if len(sys.argv)!=3:
    print('Usage: pbcli.py "Title" "Message"')
else:
    note(sys.argv[1],sys.argv[2])
