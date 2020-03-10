#!/usr/bin/env python
#
# Analog Input with ADC0831 chip
#
# Datasheet: http://www.ti.com/lit/ds/symlink/adc0838-n.pdf
# Part of SunFounder LCD StarterKit
# http://www.sunfounder.com/index.php?c=show&id=21&model=LCD%20Starter%20Kit
#

import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
PIN_CLK = 11
PIN_DO  = 9
PIN_CS  = 22

# set up the SPI interface pins
GPIO.setup(PIN_DO,  GPIO.IN)
GPIO.setup(PIN_CLK, GPIO.OUT)
GPIO.setup(PIN_CS,  GPIO.OUT)

# read SPI data from ADC8032
def getADC():
	# 1. CS LOW.
        GPIO.output(PIN_CS, True)      # clear last transmission
        GPIO.output(PIN_CS, False)     # bring CS low

	# 2. Start clock
        GPIO.output(PIN_CLK, False)  # start clock low

        # 4. read 8 ADC bits
        ad = 0
        for i in range(8):
                GPIO.output(PIN_CLK, True)
                GPIO.output(PIN_CLK, False)
                ad <<= 1 # shift bit
                if (GPIO.input(PIN_DO)):
                        ad |= 0x1 # set first bit

        # 5. reset
        GPIO.output(PIN_CS, True)

        return ad

if __name__ == "__main__":
        while True:
                print "ADC: {}".format(getADC())
                time.sleep(1)
