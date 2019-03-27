#!/usr/bin/env python3

from guizero import App, TextBox, Text, PushButton, CheckBox
from subprocess import call

def startprocess():
    print("starting process")
    spraytime = str(float(stime.value)/1000)
    plungedelay = str(float(pdelay.value)/1000)
    arguments = ["python3","SIOcontrol.py","--stime",spraytime,"--pdelay",plungedelay]
    if donotplunge.value==1:
        arguments.append("--donotplunge")
    #print(arguments)
    call(arguments)

def cleanprocess():
    print("starting clean process")
    spraytime  = str(float(cleantime.value)/1000)
    cycles = cleancycles.value
    arguments = ["python3","cleancontrol.py","--stime",spraytime,"--cycles",cycles]
    #print(arguments)
    call(arguments)
    #call(["python3","cleancontrol.py","--stime",stime,"--cycles",cycles])

app = App(title="Shake-it-off", layout="grid")

stimelabel  = Text(app, text="Spray time (ms)", grid=[0,1])
stime       = TextBox(app, grid=[1,1], text="5")
pdelaylabel = Text(app, text="Plunge delay (ms)", grid=[0,2])
pdelay      = TextBox(app, grid=[1,2], text="5")
donotplunge = CheckBox(app, text="Do not plunge", grid=[0,3])
start       = PushButton(app, command=startprocess, text="Start Process", grid=[0,4])

cleancycleslabel = Text(app, text="Cleaning cycles", grid=[3,1])
cleancycles      = TextBox(app, text="5",grid=[4,1])   
cleantimelabel   = Text(app, text="Cleaning pulse (ms)", grid=[3,2])
cleantime        = TextBox(app, text="200",grid=[4,2]) 
clean            = PushButton(app, command=cleanprocess, text="Clean", grid=[3,3])

app.display()
