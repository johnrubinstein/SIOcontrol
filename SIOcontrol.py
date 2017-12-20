#!/usr/bin/env python


# Uncomment for use of pi
import RPi.GPIO as GPIO
import Adafruit_DHT
import time, threading

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
    
    # Define pins
    pin_cannon  = 12
    pin_plunger = 19
    pin_dht22   = 24
    GPIO.setwarnings(False)
    GPIO.cleanup()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_cannon,GPIO.OUT)
    GPIO.setup(pin_plunger,GPIO.OUT)

    #humidity, temperature = readenvironment(pin_dht22)

    
    
    # apply sample
    sample = threading.Thread(target=applysample, args=(pin_cannon,0,0.1))  # defines the thread
    sample.start()   # starts the thread

    # release plunger
    plunger = threading.Thread(target=releaseplunger, args=(pin_plunger,0.2))  # defines the thread
    plunger.start()


    # Exit with reset of plunger
    raw_input("Press Enter to continue...")
    resetplunger(pin_plunger)
    #GPIO.output(pin_cannon,GPIO.LOW)
    
    print "Done!"
    

    

