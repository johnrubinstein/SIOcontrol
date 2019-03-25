#!/usr/bin/env python3

from guizero import App, TextBox, Text, PushButton

def startprocess():
    print("starting process")
    exit()

def cleanprocess():
    print("starting clean process")


app = App(title="Shake-it-off", layout="grid")

#spraytime = Text(app, text="Spray time",size=12, font="Times New Roman", align="left")
#stime = TextBox(app, text="Spray time", align="left")
#pdelay = TextBox(app, text="Plunger delay", align="left")

stimelabel  = Text(app, text="Spray time (ms)", grid=[0,1])
stime       = TextBox(app, grid=[1,1])
pdelaylabel = Text(app, text="Plunge delay (ms)", grid=[0,2])
pdelay      = TextBox(app, grid=[1,2])
start       = PushButton(app, command=startprocess, text="Start Process", grid=[0,3])

cleancycleslabel = Text(app, text="Cleaning cycles", grid=[3,1])
cleancycles      = TextBox(app, grid=[4,1])   
cleantimelabel   = Text(app, text="Cleaning pulse (ms)", grid=[3,2])
cleantime        = TextBox(app, grid=[4,2]) 
clean            = PushButton(app, text="Clean", grid=[3,3])


app.display()
