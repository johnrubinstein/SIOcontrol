#!/usr/bin/env python


# Uncomment for use of pi
import RPi.GPIO as GPIO
import Adafruit_DHT
import time, threading
import argparse

def applysample(pin_cannon,wait,duration):
    time.sleep(wait)
    GPIO.output(pin_cannon,GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(pin_cannon,GPIO.LOW)

def cleancannon(pin_cannon):
    for x in range(5):
        GPIO.output(pin_cannon,GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(pin_cannon,GPIO.LOW)
        time.sleep(0.5)
    
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
    parser.add_argument('--stime',     help='Duration of sample application (seconds)',type=float,required=True)
    parser.add_argument('--sdelay',    help='Time to wait before applying (seconds)',default = 0, type=float,required=False)
    parser.add_argument('--pdelay',    help='Time to wait before plunging (seconds)',default = 0, type=float,required=False)
    args = parser.parse_args()

    
    # Define pins
    pin_cannon  = 12
    pin_plunger = 19
    pin_dht22   = 24
    
    GPIO.setwarnings(False)
    GPIO.cleanup()    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_cannon,GPIO.OUT)
    GPIO.setup(pin_plunger,GPIO.OUT)

    # Report environmental conditions
    humidity, temperature = readenvironment(pin_dht22)
    print('{0:0.1f} Temp={1:0.1f}\'C  Humidity={2:0.1f}% RH'.format(tic-starttime,temperature, humidity))

    # Breakpoint
    raw_input("Press Enter to continue...")
    
    # set up processes
    sample = threading.Thread(target=applysample, args=(pin_cannon,args.sdelay,args.stime))  # defines the thread
    plunger = threading.Thread(target=releaseplunger, args=(pin_plunger,args.pdelay))  # defines the thread

    # start processes
    plunger.start()  
    sample.start()  

    
    # Exit with reset of plunger
    raw_input("Press Enter to continue...")
    resetplunger(pin_plunger)
    
    print "Done!"
    

    

