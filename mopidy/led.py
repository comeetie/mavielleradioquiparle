#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import subprocess
import json
LedPin = 17
LedPin2 = 5

def setup():
	GPIO.setmode(GPIO.BCM)      
	GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to off led
	GPIO.setup(LedPin2, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.output(LedPin2, GPIO.HIGH) # Set LedPin high(+3.3V) to off led

def parse_status(st)
	return st

def loop():
	while True:
		try:
			proc = subprocess.Popen(["mpc status"], stdout=subprocess.PIPE, shell=True)
			(out, err) = proc.communicate()
			status=parse_status(out)
			if(status[u'status']=="play"):
				GPIO.output(LedPin, GPIO.HIGH)  # led on
				GPIO.output(LedPin2, GPIO.LOW)  # led on
				time.sleep(1)
				print 'led on...'
			else :
				print 'led off'
				GPIO.output(LedPin, GPIO.LOW) # led off
				GPIO.output(LedPin2, GPIO.HIGH) # led off
				time.sleep(1)
		except:
			time.sleep(1)

def destroy():
	GPIO.output(LedPin, GPIO.HIGH)     # led off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
