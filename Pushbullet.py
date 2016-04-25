#!/usr/bin/python
import urllib2
import json
import Tkinter
import ttk
import tkMessageBox
import tkFont
from functools import partial
import requests
import time

### GET PUSHBULLET TOKEN FROM TEXT FILE
global TOKEN
with open('pb_token.txt', 'r') as myfile:
    TOKEN=myfile.read().replace('\n', '')

def clkNote():
    global nttop
    nttop = Tkinter.Toplevel(top)
    nttop.attributes("-topmost", True)
    nttop.title("Send note")

    lblpu = Tkinter.Label(nttop, text="Send a note", fg="white", bg="green", font = ttlFont).grid(row=0, columnspan=2, sticky=Tkinter.W+Tkinter.E)
    lbttl = Tkinter.Label(nttop,text="Title:").grid(row=1)
    global ettl
    ettl = Tkinter.Entry(nttop,exportselection=0)
    ettl.grid(row=1,column=1)
    lbmsg = Tkinter.Label(nttop,text="Message:").grid(row=2)
    global emsg
    emsg = Tkinter.Entry(nttop,exportselection=0)
    emsg.grid(row=2,column=1)
    btnSendNote = Tkinter.Button(nttop, text="Send note", command=clkSendNote).grid(row=3)

def clkSendNote():
    NoteUrl = "https://api.pushbullet.com/v2/pushes"
    NoteTtl = ettl.get()
    NoteMsg = emsg.get()
    NoteData = dict(type="note", title=NoteTtl, body=NoteMsg)
    NoteR = requests.post(NoteUrl, json=NoteData, auth=(TOKEN, '')).json()
    #print NoteR
    nttop.destroy()

def clkPushRefr():
    PushesData = dict(active="true")
    global PushesR
    PushesR = requests.get("https://api.pushbullet.com/v2/pushes?active=true", auth=(TOKEN, '')).json()
    #print PushesR

    PushesList = PushesR['pushes']
    nPushes = len(PushesList)

    txtPushes.delete("1.0",Tkinter.END)
    for i in range(0,nPushes):

        pType = PushesList[i]['type']
        txtPushes.insert(Tkinter.INSERT, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(PushesList[i]['created'])))
        txtPushes.insert(Tkinter.INSERT, "\n-----------------------------------\n")
        if pType == "note":
            txtPushes.insert(Tkinter.INSERT, "Title:\n")
            txtPushes.insert(Tkinter.INSERT, PushesList[i]['title'])
            txtPushes.insert(Tkinter.INSERT, "\nMessage:\n")
            txtPushes.insert(Tkinter.INSERT, PushesList[i]['body'])

        if pType == "file" :
            txtPushes.insert(Tkinter.INSERT, "File:\n")
            txtPushes.insert(Tkinter.INSERT, PushesList[i]['file_name'])
            txtPushes.insert(Tkinter.INSERT, "\nFile URL:\n")
            txtPushes.insert(Tkinter.INSERT, PushesList[i]['file_url'])

        if pType == "link" :
            txtPushes.insert(Tkinter.INSERT, "Link:\n")
            txtPushes.insert(Tkinter.INSERT, PushesList[i]['url'])


        txtPushes.insert(Tkinter.INSERT, "\n\n")

### SET UP GUI
top = Tkinter.Tk()
top.attributes("-topmost", True)
top.title("Pushbullet")

ttlFont = tkFont.Font(family="Helvetica", size=30, weight="bold")
ttl = Tkinter.Label(top, text="Pushbullet", fg="white", bg="green", font=ttlFont).grid(row=0, columnspan=1000, sticky = Tkinter.W+Tkinter.E)
fLine = Tkinter.Frame(top, bg="black", width=800, height=2).grid(row=1, columnspan=1000)
btnNote = Tkinter.Button(top, text="Send note", command=clkNote).grid(row=2,column=0, sticky = Tkinter.W)
btnRefr = Tkinter.Button(top, text="Refresh pushes", command=clkPushRefr).grid(row=2, column=3, sticky = Tkinter.W)
fLine2 = Tkinter.Frame(top, bg="black", width=800, height=2).grid(row=3, columnspan=1000)
fMain = Tkinter.Frame(top, bg="white", width=800, height=600).grid(row=4, columnspan=1000, rowspan=5000)

lblttFont = tkFont.Font(family="Helvetica", size=18, weight="bold")
lblttlmn = Tkinter.Label(fMain, text="Recent pushes", font=lblttFont).grid(row=4,columnspan=1000,sticky=Tkinter.W+Tkinter.N)
lblttlmn2 = Tkinter.Label(fMain, text="-------------------------------------------------------").grid(row=5,columnspan=1000,sticky=Tkinter.W+Tkinter.N)
txtPushes = Tkinter.Text(fMain)
txtPushes.grid(row=6, columnspan=1000, sticky=Tkinter.W+Tkinter.N)


clkPushRefr()


top.mainloop()
