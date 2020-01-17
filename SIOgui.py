#!/usr/bin/env python3

from guizero import App, TextBox, Text, PushButton, CheckBox
from subprocess import call, Popen

def startprocess():
    print("starting process")
    spraytime = str(float(stime.value)/1000)
    plungedelay = str(float(pdelay.value)/1000)
    spraydelay  = str(float(sdelay.value)/1000)
    arguments = ["python3","SIOapplyandplunge.py","--stime",spraytime,"--pdelay",plungedelay,"--sdelay",spraydelay]
    if donotplunge.value==1:
        arguments.append("--donotplunge")
    call(arguments)
    button_start.disable()
    
def powerup():
    print("Power up")
    arguments = ["python3","SIOpowerupdown.py","--updown","up"]
    call(arguments)
    button_start.enable()
    
def powerdown():
    print("Power down")
    arguments = ["python3","SIOpowerupdown.py","--updown","down"]
    call(arguments)
    button_start.disable()
    
def cleanprocess():
    print("starting clean process")
    spraytime  = str(float(cleantime.value)/1000)
    cycles = cleancycles.value
    arguments = ["python3","SIOclean.py","--stime",spraytime,"--cycles",cycles]
    #print(arguments)
    #call(arguments)
    Popen(arguments)
    #call(["python3","cleancontrol.py","--stime",stime,"--cycles",cycles])

app = App(title="Shake-it-off", layout="grid")
stimelabel  = Text(app, text="Spray time (ms)", grid=[0,1])
stime       = TextBox(app, grid=[1,1], text="5")
pdelaylabel = Text(app, text="Plunge delay (ms)", grid=[0,2])
pdelay      = TextBox(app, grid=[1,2], text="0")
sdelaylabel = Text(app, text="Spray delay (ms)", grid=[0,3])
sdelay      = TextBox(app, grid=[1,3], text="0")
donotplunge = CheckBox(app, text="Do not plunge", grid=[0,4])
button_up   = PushButton(app, command=powerup,text="Ready", grid=[0,5])
button_down = PushButton(app, command=powerdown, text="Abort", grid=[1,5])
button_start= PushButton(app, command=startprocess, text="Spray & Plunge", grid=[0,6])
button_up.bg="orange"
button_start.bg = "red"
button_start.disable()

cleancycleslabel = Text(app, text="Cleaning cycles", grid=[3,1])
cleancycles      = TextBox(app, text="5",grid=[4,1])   
cleantimelabel   = Text(app, text="Cleaning pulse (ms)", grid=[3,2])
cleantime        = TextBox(app, text="200",grid=[4,2]) 
clean            = PushButton(app, command=cleanprocess, text="Clean", grid=[3,5])

app.display()
