#!/usr/bin/env python
import RPi.GPIO as GPIO
import os

gpio_pin_number=13
gpio_led=4
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
GPIO.setup(gpio_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio_led, GPIO.OUT) 
GPIO.output(gpio_led, GPIO.HIGH) #On l'allume

try:
   GPIO.wait_for_edge(gpio_pin_number, GPIO.RISING)
   print("out")
   GPIO.output(gpio_led, GPIO.LOW) #On l’éteint
except:
    pass
