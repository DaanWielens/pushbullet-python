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
    nttop.lift()
    nttop.title("Send note")

    lblpu = Tkinter.Label(nttop, text="Send a note", fg="white", bg="green", font = ttlFont).grid(row=0, columnspan=2, sticky=Tkinter.W+Tkinter.E)
    fLine = Tkinter.Frame(nttop, bg="black", width=290, height=1).grid(row=1, columnspan=2)
    lbttl = Tkinter.Label(nttop,text="Title:").grid(row=2)
    global ettl
    ettl = Tkinter.Entry(nttop,exportselection=0)
    ettl.grid(row=2,column=1)
    lbmsg = Tkinter.Label(nttop,text="Message:").grid(row=3)
    global emsg
    emsg = Tkinter.Entry(nttop,exportselection=0)
    emsg.grid(row=3,column=1)
    btnSendNote = Tkinter.Button(nttop, text="Send note", command=clkSendNote).grid(row=4)

def clkSendNote():
    NoteUrl = "https://api.pushbullet.com/v2/pushes"
    NoteTtl = ettl.get()
    NoteMsg = emsg.get()
    NoteData = dict(type="note", title=NoteTtl, body=NoteMsg)
    NoteR = requests.post(NoteUrl, json=NoteData, auth=(TOKEN, '')).json()
    #print NoteR
    nttop.destroy()

def clkDevsList():
    devtop = Tkinter.Toplevel(top)
    devtop.lift()
    devtop.title("Devices")
    lblpu = Tkinter.Label(devtop, text="Devices", fg="white", bg="green", font = ttlFont).grid(row=0, sticky=Tkinter.W+Tkinter.E)
    fLine = Tkinter.Frame(devtop, bg="black", width=500, height=1).grid(row=1)
    lbttl = Tkinter.Label(devtop,text="List of devices:").grid(row=2, sticky=Tkinter.W)
    lbttl = Tkinter.Label(devtop,text="---------------------------------------------------------------------").grid(row=3, sticky=Tkinter.W)
    txtDevices = Tkinter.Text(devtop, height=20, width=65)
    txtDevices.grid(row=4, sticky=Tkinter.W)

    DevicesR = requests.get("https://api.pushbullet.com/v2/devices?active=true", auth=(TOKEN, '')).json()
    DevicesList = DevicesR['devices']
    nDev = len(DevicesList)

    #print DevicesList
    for i in range(0,nDev):
        txtDevices.insert(Tkinter.INSERT, DevicesList[i]['nickname'])
        txtDevices.insert(Tkinter.INSERT, "\n-----------------------------------\n")
        txtDevices.insert(Tkinter.INSERT, "Identifier:\n")
        txtDevices.insert(Tkinter.INSERT, DevicesList[i]['iden'])
        txtDevices.insert(Tkinter.INSERT, "\nModel:\n")
        txtDevices.insert(Tkinter.INSERT, DevicesList[i]['model'])
        txtDevices.insert(Tkinter.INSERT, "\n\n")

def clkCntsList():
    cnttop = Tkinter.Toplevel(top)
    cnttop.lift()
    cnttop.title("Contacts")
    lblpu = Tkinter.Label(cnttop, text="Devices", fg="white", bg="green", font = ttlFont).grid(row=0, sticky=Tkinter.W+Tkinter.E)
    fLine = Tkinter.Frame(cnttop, bg="black", width=500, height=1).grid(row=1)
    lbttl = Tkinter.Label(cnttop,text="List of contacts:").grid(row=2, sticky=Tkinter.W)
    lbttl = Tkinter.Label(cnttop,text="---------------------------------------------------------------------").grid(row=3, sticky=Tkinter.W)
    txtContacts = Tkinter.Text(cnttop, height=20, width=65)
    txtContacts.grid(row=4, sticky=Tkinter.W)

    ContactsR = requests.get("https://api.pushbullet.com/v2/chats?active=true", auth=(TOKEN, '')).json()
    ContactsList = ContactsR['chats']
    nCnts = len(ContactsList)

    for i in range(0,nCnts):
        txtContacts.insert(Tkinter.INSERT, ContactsList[i]['with']['name'])
        txtContacts.insert(Tkinter.INSERT, "\n-----------------------------------\n")
        txtContacts.insert(Tkinter.INSERT, "Identifier:\n")
        txtContacts.insert(Tkinter.INSERT, ContactsList[i]['iden'])
        txtContacts.insert(Tkinter.INSERT, "\nE-mail:\n")
        txtContacts.insert(Tkinter.INSERT, ContactsList[i]['with']['email'])
        txtContacts.insert(Tkinter.INSERT, "\n\n")

def clkPushRefr():
    global PushesR
    PushesR = requests.get("https://api.pushbullet.com/v2/pushes?active=true", auth=(TOKEN, '')).json()
    #print PushesR

    PushesList = PushesR['pushes']
    PushesList = sorted(PushesList, key=lambda k: k.get('created',0), reverse=True)
    nPushes = len(PushesList)

    txtPushes.delete("1.0",Tkinter.END)
    for i in range(0,nPushes):

        pType = PushesList[i]['type']
        txtPushes.insert(Tkinter.INSERT, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(PushesList[i]['created'])))
        txtPushes.insert(Tkinter.INSERT, "\n---------------------------------------------------------------------------------------------------------\n")
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
top.lift()
top.title("Pushbullet")

ttlFont = tkFont.Font(family="Helvetica", size=30, weight="bold")
ttl = Tkinter.Label(top, text="Pushbullet", fg="white", bg="green", font=ttlFont).grid(row=0, columnspan=1000, sticky = Tkinter.W+Tkinter.E)
fLine = Tkinter.Frame(top, bg="black", width=810, height=1).grid(row=1, columnspan=1000)
btnNote = Tkinter.Button(top, text="Send note", command=clkNote).grid(row=2,column=0, sticky = Tkinter.W)
btnRefr = Tkinter.Button(top, text="Refresh pushes", command=clkPushRefr).grid(row=2, column=3, sticky = Tkinter.W)
btnDevs = Tkinter.Button(top, text="Devices", command=clkDevsList).grid(row=2, column=4, sticky = Tkinter.W)
btnCnts = Tkinter.Button(top, text="Contacts", command=clkCntsList).grid(row=2, column=5, sticky = Tkinter.W)
fLine2 = Tkinter.Frame(top, bg="black", width=810, height=1).grid(row=3, columnspan=1000)
fMain = Tkinter.Frame(top, bg="white", width=810, height=600).grid(row=4, columnspan=1000, rowspan=5000)

lblttFont = tkFont.Font(family="Helvetica", size=18, weight="bold")
lblttlmn = Tkinter.Label(fMain, text="Recent pushes", font=lblttFont).grid(row=4,columnspan=1000,sticky=Tkinter.W+Tkinter.N)
lblttlmn2 = Tkinter.Label(fMain, text="----------------------------------------------------------------------------------------------------------------------------").grid(row=5,columnspan=1000,sticky=Tkinter.W+Tkinter.N)
txtPushes = Tkinter.Text(fMain, height=36, width=114)
txtPushes.grid(row=6, columnspan=1000, sticky=Tkinter.W+Tkinter.N)


clkPushRefr()


top.mainloop()
