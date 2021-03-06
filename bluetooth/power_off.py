#!/usr/bin/env python3
import RPi.GPIO as GPIO
import os
import time
gpio_pin_number=13
gpio_led=4
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
GPIO.setup(gpio_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio_led, GPIO.OUT) 

if(GPIO.input(gpio_pin_number)==1):
   print("out")
   GPIO.output(gpio_led, GPIO.LOW) #On l’éteint
else:
   print("in")
   GPIO.output(gpio_led, GPIO.HIGH) #On l’éteint



while True:
      if(GPIO.input(gpio_pin_number)==0):
         GPIO.wait_for_edge(gpio_pin_number, GPIO.RISING)
         print("out")
         GPIO.output(gpio_led, GPIO.LOW) #On l’éteint
         time.sleep(1)
      else:
         GPIO.wait_for_edge(gpio_pin_number, GPIO.FALLING)
         print("in")
         GPIO.output(gpio_led, GPIO.HIGH) #On l’éteint
         time.sleep(1)

