#!/usr/bin/env python
import RPi.GPIO as GPIO
import os

gpio_pin_number=12

GPIO.setmode(GPIO.BCM)

GPIO.setup(gpio_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_callback(channel):
    print("Button was pushed!")
    os.system("dbus-send --system --type=method_call --print-reply --dest=org.bluez /org/bluez/hci0/dev_18_01_F1_4D_CB_15 org.bluez.MediaControl1.Next")

GPIO.add_event_detect(gpio_pin_number,GPIO.RISING,callback=button_callback)
message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up
