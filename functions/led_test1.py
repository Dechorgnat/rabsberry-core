#!/usr/bin/python
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import math
from neopixel import *


# LED strip configuration:
LED_COUNT      = 6      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 6       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


def occultationOneColor(on, off, offset, t, r, g, b):
    period = on+off
    phase  = (t+offset) % period
    if phase > on:
        r=g=b=0
    return Color(r, g, b)

def waveOneColor(period, offset, t, r, g, b):
    phase  = (t + offset) * math.pi * 2 / period
    k = (math.sin(phase) + 1) / 2
    return Color(int(k*r), int(k*g), int(k*b))

def waveTwoColor(period, offset, t, r1, g1, b1, r2, g2, b2, fading):
    phase  = (t + offset) * math.pi * 2 / period
    if fading:
        k = (math.sin(phase) + 1) / 2
        kk = 1 - k
        return Color(int(k*r1)+int(kk*r2), int(k*g1)+int(kk*g2), int(k*b1)+int(kk*b2))
    else:
        k = math.sin(phase)
        if k>0: 
            return Color(int(k*r1), int(k*g1), int(k*b1))
        else:
            return Color(int(-k*r2), int(-k*g2), int(-k*b2))


def clearStrip(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()
 
 
# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	strip.begin()
        clearStrip(strip)
        fd = 1/5
        while True:
            t = time.time()
            strip.setPixelColor(0,waveOneColor(4.,0, t, 128, 0, 255))
            #strip.setPixelColor(1,occultationOneColor(2, 2, 0, t, 255, 0, 255))
            #strip.setPixelColor(2,occultationOneColor(0.2, 4.8, 0, t, 128, 128, 128))
            strip.setPixelColor(3,waveTwoColor(4.,0, t, 128, 0, 255, 0, 0, 0, False))
            #strip.setPixelColor(4,waveTwoColor(4.,0, t, 255, 0, 0, 0, 0, 255, True))
            #strip.setPixelColor(5,waveTwoColor(4.,0, t, 255, 0, 0, 0, 0, 255, False))
            strip.show()
            time.sleep(fd)

        clearStrip(strip)
