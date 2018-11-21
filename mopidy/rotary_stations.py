#!/usr/bin/env python

"""
The daemon responsible for changing the volume in response to a turn or press
of the volume knob.
The volume knob is a rotary encoder. It turns infinitely in either direction.
Turning it to the right will increase the volume; turning it to the left will
decrease the volume. The knob can also be pressed like a button in order to
turn muting on or off.
The knob uses two GPIO pins and we need some extra logic to decode it. The
button we can just treat like an ordinary button. Rather than poll
constantly, we use threads and interrupts to listen on all three pins in one
script.
"""

import os
import signal
import subprocess
import sys
import threading
import json
import time

from RPi import GPIO
from Queue import Queue
from os import listdir,system

DEBUG = False

# SETTINGS
# ========

# The two pins that the encoder uses (BCM numbering).
GPIO_A = 12   
GPIO_B = 6

# The pin that the knob's button is hooked up to. If you have no button, set
# this to None.
GPIO_BUTTON = None

PLAYLISTS=['FranceInter','FranceInfo', 'Nova','fip-reggae','fip-rock','fip-jazz', 'Skyrock','Lavieestbelle','Familly']
print(PLAYLISTS)
LAST = time.time()
print(LAST)

# When the knob is turned, the callback happens in a separate thread. If
# those turn callbacks fire erratically or out of order, we'll get confused
# about which direction the knob is being turned, so we'll use a queue to
# enforce FIFO. The callback will push onto a queue, and all the actual
# volume-changing will happen in the main thread.
QUEUE = Queue()

# When we put something in the queue, we'll use an event to signal to the
# main thread that there's something in there. Then the main thread will
# process the queue and reset the event. If the knob is turned very quickly,
# this event loop will fall behind, but that's OK because it consumes the
# queue completely each time through the loop, so it's guaranteed to catch up.
EVENT = threading.Event()

def debug(str):
  if not DEBUG:
    return
  print(str)

class RotaryEncoder:
  """
  A class to decode mechanical rotary encoder pulses.
  Ported to RPi.GPIO from the pigpio sample here: 
  http://abyz.co.uk/rpi/pigpio/examples.html
  """
  
  def __init__(self, gpioA, gpioB, callback=None, buttonPin=None, buttonCallback=None):
    """
    Instantiate the class. Takes three arguments: the two pin numbers to
    which the rotary encoder is connected, plus a callback to run when the
    switch is turned.
    
    The callback receives one argument: a `delta` that will be either 1 or -1.
    One of them means that the dial is being turned to the right; the other
    means that the dial is being turned to the left. I'll be damned if I know
    yet which one is which.
    """
    
    self.lastGpio = None
    self.gpioA    = gpioA
    self.gpioB    = gpioB
    self.callback = callback
    
    self.gpioButton     = buttonPin
    self.buttonCallback = buttonCallback
    
    self.levA = 0
    self.levB = 0
    
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(self.gpioA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(self.gpioB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.add_event_detect(self.gpioA, GPIO.BOTH, self._callback)
    GPIO.add_event_detect(self.gpioB, GPIO.BOTH, self._callback)
    
    if self.gpioButton:
      GPIO.setup(self.gpioButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.add_event_detect(self.gpioButton, GPIO.FALLING, self._buttonCallback, bouncetime=1000)
    
    
  def destroy(self):
    GPIO.remove_event_detect(self.gpioA)
    GPIO.remove_event_detect(self.gpioB)
    GPIO.cleanup()
    
  def _buttonCallback(self, channel):
    self.buttonCallback(GPIO.input(channel))
    
  def _callback(self, channel):
    level = GPIO.input(channel)
    if channel == self.gpioA:
      self.levA = level
    else:
      self.levB = level
      
    # Debounce.
    if channel == self.lastGpio:
      return
    
    # When both inputs are at 1, we'll fire a callback. If A was the most
    # recent pin set high, it'll be forward, and if B was the most recent pin
    # set high, it'll be reverse.
    self.lastGpio = channel
    if channel == self.gpioA and level == 1:
      if self.levB == 1:
        self.callback(1)
    elif channel == self.gpioB and level == 1:
      if self.levA == 1:
        self.callback(-1)


class Playlist:
  """
  A wrapper API for interacting with the playlist.
  """
  current = 0
  old = 0
  last = time.time()

  def __init__(self):
    # Set an initial value for last_volume in case we're muted when we start.
    self.current = 1
    
  def up(self):
    print("++++")
    self.current = (self.current+1) % len(PLAYLISTS)
    print(self.current)
    return self.set_playlist()
    
  def down(self):
    print("----")
    self.current = (self.current-1) % len(PLAYLISTS)
    print(self.current)
    return self.set_playlist()
  def parse_status(st):
    return st
  
  def parse_status(self,out):
    lines = out.split("\n")
    res = {}
    if len(lines) > 2 :
      res["status"]=lines[1].split("#")[0].replace(" ","")[1:-1]
      res["track"]=lines[0]
      sl = lines[2]
    else:
      res["status"]="stop"
      res["track"]=""
      sl = lines[0]
    st = sl.split("   ")
    res["volume"]=int(st[0].split(":")[1][:-1])
    return res
    

  def set_playlist(self):
    try:
        print("change")
	proc = subprocess.Popen(["mpc status"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	status=self.parse_status(out)
	if(status[u'status']=="playing"):
		try:
			self.old=self.current  
			print("playing {} N: {}".format(PLAYLISTS[self.current],self.current))
			system("mpc stop")
			system("aplay /home/pi/mavielleradioquiparle/mopidy/sounds/{}.wav".format(PLAYLISTS[self.current]))	
			system("mpc clear")	
			system("mpc load {}".format(PLAYLISTS[self.current]))
			system("mpc play")
		
		except:
			print("change error")
			system("mpc stop")
			system("aplay /home/pi/mavielleradioquiparle/mopidy/sounds/error.wav")		
			system("mpc clear")	
			system("mpc load Nova")
			system("mpc play")

	
	if(status[u'status']!="play"):
		print("reseting N: {}".format(self.old))
		self.current = self.old
    except:
	print("pbr acces status")
    return self.current

  def dt(self):
    dt = time.time()-self.last
    print(dt)
    self.last=time.time()
    return dt

if __name__ == "__main__":
  
  gpioA = GPIO_A
  gpioB = GPIO_B
  gpioButton = GPIO_BUTTON
  
  
  v = Playlist() 
  def on_press(value):
    EVENT.set()
  
  # This callback runs in the background thread. All it does is put turn
  # events into a queue and flag the main thread to process them. The
  # queueing ensures that we won't miss anything if the knob is turned
  # extremely quickly.
  def on_turn(delta):
    dt = v.dt()
    if dt > 0.7:
      QUEUE.put(delta)
      EVENT.set()
    
  def consume_queue():
    while not QUEUE.empty():
      delta = QUEUE.get()
      handle_delta(delta)
  
  def handle_delta(delta):
      if delta == 1:
        playlist = v.up()
      else:
        playlist = v.down()
    
  def on_exit(a, b):
    print("Exiting...")
    encoder.destroy()
    sys.exit(0)
    

  encoder = RotaryEncoder(GPIO_A, GPIO_B, callback=on_turn, buttonPin=GPIO_BUTTON, buttonCallback=on_press)
  signal.signal(signal.SIGINT, on_exit)
  
  while True:
    EVENT.wait(1200)
    consume_queue()
    EVENT.clear()
