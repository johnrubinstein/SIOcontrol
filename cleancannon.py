#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

pin_cannon = 12
cylces     = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_cannon,GPIO.OUT)
GPIO.setwarnings(False)


for x in range(cycles):
    GPIO.output(pin_cannon,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(pin_cannon,GPIO.LOW)
    time.sleep(0.2)
    
GPIO.cleanup()
