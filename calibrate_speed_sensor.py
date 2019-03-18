#!/usr/bin/env python
import RPi.GPIO as GPIO

pin    = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setwarnings(False)

print 'status of the sensor is ', GPIO.input(pin)

raw_input("Press Enter to continue...")
print 'lower solenoid to down position and adjust sensor until program advances'
    
while GPIO.input(pin)==0:
    pass
print "obstacle detected"
    

print 'done'


GPIO.cleanup()
