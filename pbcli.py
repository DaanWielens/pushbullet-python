#!/usr/local/bin/python
import requests

# Get pushbullet token from text file (file should contain token only)
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
