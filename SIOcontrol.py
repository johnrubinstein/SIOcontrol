#!/usr/bin/env python

# Uncomment for use of pi
import RPi.GPIO as GPIO
#import Adafruit_DHT
import time, threading
import argparse
import sys, select

def cannonforward(pin_cannonposition):
    print "Advancing the cannon"
    GPIO.output(pin_cannonposition,GPIO.HIGH)

def cannonreverse(pin_cannonposition,cannonreversedelay):
    time.sleep(cannonreversedelay)
    print "reversing the cannon"
    GPIO.output(pin_cannonposition,GPIO.LOW)

def applysample(pin_cannon,wait,duration):
    time.sleep(wait)
    GPIO.output(pin_cannon,GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(pin_cannon,GPIO.LOW)
    
def releaseplunger(pin_plunger,wait):
    time.sleep(wait)
    GPIO.output(pin_plunger,GPIO.HIGH)

def resetplunger(pin_plunger):
    GPIO.output(pin_plunger,GPIO.LOW)
    
def readenvironment(pin_dht22):
    humidity, temperature = Adafruit_DHT.read_retry(22, pin=pin_dht22)
    return humidity, temperature
    
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Arguments for SIOcontrol')
    parser.add_argument('--stime',      help='Duration of sample application (seconds)',type=float,required=True)
    parser.add_argument('--sdelay',     help='Time to wait before applying (seconds)',default = 0, type=float,required=False)
    parser.add_argument('--pdelay',     help='Time to wait before plunging (seconds)',default = 0, type=float,required=False)
    parser.add_argument('--donotplunge',help='Do not fire the plunger (diagnostic)',action = 'store_true')  
    args = parser.parse_args()
    # Define pins
    pin_cannon         = 12
    pin_plunger        = 19
    pin_dht22          = 24
    pin_cannonposition = 20

    # Default timing
    cannontimetoreverse = 0.05
    cannonreversedelay  = args.stime + args.sdelay+ cannontimetoreverse
    timeout             = 1     # withdraw the plunger to avoid overheating
    kuhnketime          = 1

    GPIO.setwarnings(False)
    GPIO.cleanup()    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_cannon,GPIO.OUT)
    GPIO.setup(pin_plunger,GPIO.OUT)
    GPIO.setup(pin_cannonposition,GPIO.OUT)
    # Report environmental conditions
#    humidity, temperature = readenvironment(pin_dht22)
#    print('Temp={0:0.1f}\'C  Humidity={1:0.1f}% RH'.format(temperature, humidity))
    
    # Display timing and avoid crash
    print "Timings:"
    print "Specimen application will start at time: ",args.sdelay
    print "Specimen application will end at time: ",args.sdelay + args.stime
    print "Cannon will reverse at time: ",cannonreversedelay
    print "Plunger will fall at time: ",args.pdelay
    print "Program will exit after: ",kuhnketime+args.pdelay+args.sdelay
    if cannonreversedelay > args.pdelay:
        print "The cannon does not have sufficient time to reverse before plunging!!"
        exit()

    # put cannon into place and wait
    cannonforward(pin_cannonposition)
    raw_input("Press Enter to continue...")

    # set up processes
    sample = threading.Thread(target=applysample, args=(pin_cannon,args.sdelay,args.stime))  
    plunger = threading.Thread(target=releaseplunger, args=(pin_plunger,args.pdelay))  
    cannonposition = threading.Thread(target=cannonreverse, args=(pin_cannonposition,cannonreversedelay)) 
    
    # start processes
    if not args.donotplunge:
        plunger.start()
        
    sample.start()  
    cannonposition.start()
    
    # Kuhnke plunger
    time.sleep(kuhnketime+args.pdelay+args.sdelay)
    resetplunger(pin_plunger)
    
    print "Done!"
    

    

