#!/usr/bin/python
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import json
import paho.mqtt.client as paho
import math
from rpi_ws281x import Color, Adafruit_NeoPixel
from collections import Iterable
import signal
import sys
from core.tools.config import getConfig
from colors import *

# LED strip configuration:
LED_COUNT = 5  # Number of LED pixels.
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 100 # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)

NOSE = 3
LEFT = 0
CENTER = 1
RIGHT = 2
BOTTOM = 4

broker="127.0.0.1"


def signal_handler(sig, frame):
    stop_manager()


def stop_manager():
    clearStrip(strip)
    client.disconnect()  # disconnect
    client.loop_stop()  # stop loop
    sys.exit(0)


def occultationOneColor(t, on, off, offset, color):
    period = on + off
    phase = (t + offset) % period
    if phase > on:
        return BLACK
    return color


def occultationTwoColor(t, on_one, off_one, on_two, off_two, offset, color_one, color_two):
    period = on_one + off_one + on_two + off_two
    phase = (t + offset) % period
    if phase < on_one:
        return color_one
    if phase < on_one + off_one:
        return BLACK
    if phase < on_one + off_one + on_two:
        return color_two
    return BLACK


def waveOneColor(t, period, offset, r, g, b):
    phase = (t + offset) * math.pi * 2 / period
    k = (math.sin(phase) + 1) / 2
    return Color(int(k * r), int(k * g), int(k * b))


def waveTwoColor(t, period, offset, r1, g1, b1, r2, g2, b2, fading):
    phase = (t + offset) * math.pi * 2 / period
    if fading:
        k = (math.sin(phase) + 1) / 2
        kk = 1 - k
        return Color(int(k * r1) + int(kk * r2), int(k * g1) + int(kk * g2), int(k * b1) + int(kk * b2))
    else:
        k = math.sin(phase)
        if k > 0:
            return Color(int(k * r1), int(k * g1), int(k * b1))
        else:
            return Color(int(-k * r2), int(-k * g2), int(-k * b2))

def scheme(t, start, loop, tab):
    phase = t - start
    if loop:
        i = 0
        period = 0 
        while i < len(tab):
            period = period +tab[i]
            i = i + 4
        phase = phase % period
    i = 0
    d = 0   
    while i < len(tab):
        d = d + tab[i]  
        if phase < d:        
            r = tab[i+1]
            g = tab[i+2]
            b = tab[i+3]
            return Color(r, g, b)
        i = i + 4

def fixedColor(t, color):
    return color


def clearStrip(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()


#define MQTT callback
def on_message(client, userdata, message):
    message =str(message.payload.decode("utf-8"))
    print "received message: " + message
    event = json.loads(message)
    print event

    if event['command'] == 'stop':
        print event['command']
        return stop_manager()
    if event['command'] == 'scheme':
        print event['command']
        for i in event['leds']:
            func_table[int(i)] = (scheme, (time.time(), event['loop'] , event['scheme'])) 
        return
        return stop_manager()
    if event['command'] == 'pattern':
        print event['command']
        # patterns for meteo
        if event['pattern']=='nuage': # Une bleue, une jaune, une bleue
            func_table[LEFT]   = (waveOneColor, (3., 0, 0, 0, 255))
            func_table[CENTER] = (waveOneColor, (3., 0, 255, 255, 0))
            func_table[RIGHT]  = (waveOneColor, (3., 0, 0, 0, 255))
            return
        if event['pattern']=='brouillard': # Trois bleues qui clignotent en meme temps
            func_table[LEFT]   = (waveOneColor, (3., 0, 0, 0, 255))
            func_table[CENTER] = (waveOneColor, (3., 0, 0, 0, 255))
            func_table[RIGHT]  = (waveOneColor, (3., 0, 0, 0, 255))
            return
        if event['pattern']=='pluie': # Trois bleues qui clignotent alternativement
            func_table[LEFT]   = (occultationOneColor, (3, 2, 0, BLUE))
            func_table[CENTER] = (occultationOneColor, (3, 2, 2, BLUE))
            func_table[RIGHT]  = (occultationOneColor, (3, 2, 1, BLUE))
            return
        if event['pattern']=='orage': # Une bleue et une jaune qui changent de position
            func_table[LEFT]   = (occultationTwoColor, (1, 0, 1, 1, 2, BLUE, YELLOW)) # NBJ
            func_table[CENTER] = (occultationTwoColor, (1, 1, 1, 0, 0, YELLOW, BLUE)) # JNB
            func_table[RIGHT]  = (occultationTwoColor, (1, 0, 1, 1, 0, BLUE, YELLOW)) # BJN
            return
        if event['pattern']=='neige': # Le milieu qui clignote en bleu
            func_table[LEFT]   = (fixedColor, BLACK)
            func_table[CENTER] = (waveOneColor, (3., 0, 0, 0, 255))
            func_table[RIGHT]  = (fixedColor, BLACK)
            return
        if event['pattern']=='soleil': # Trois jaunes (clignotent ensemble)
            period = 3
            func_table[LEFT]   = (waveOneColor, (period, 0, 255, 255, 0))
            func_table[CENTER] = (waveOneColor, (period, 0, 255, 255, 0))
            func_table[RIGHT]  = (waveOneColor, (period, 0, 255, 255, 0))
            return
        # others
        if event['pattern']=='google': 
            freq = 0.7
            func_table[LEFT]   = (occultationOneColor, (freq, 3*freq, 0 , BLUE ))
            func_table[CENTER] = (occultationOneColor, (freq, 3*freq, -freq, RED))
            func_table[RIGHT]  = (occultationOneColor, (freq, 3*freq, -2*freq, YELLOW))
            return
        return
    if event['command'] == 'set':
        for i in event['leds']:
            func_table[int(i)] = (fixedColor, Color(event['r'] , event['g'], event['b'])) 
        return
    if event['command'] == 'unset':
        for i in event['leds']:
            func_table[int(i)] = (fixedColor, BLACK) 
        return

# Main program logic follows:
if __name__ == '__main__':
    conf = getConfig()
    led_pin = getConfig()['LED_PIN']

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, led_pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()
    clearStrip(strip)
    fd = 1 / 5
    func_table = {
        0: (scheme, (time.time(), True , [3, 0, 0, 255, 1, 255, 0, 0,  2, 0, 255, 0, 5, 0, 0, 0])) ,
        1: (waveOneColor, (3., 0, 128, 0, 255)),
        2: (fixedColor, BLACK),
        3: (occultationOneColor, (5, 1, 0, RED1)),
        4: (waveOneColor, (4., 0, 128, 0, 255)),
        #5: (waveTwoColor, (4., 0, 255, 0, 0, 0, 0, 255, False)),
    }

    # init mqtt connection and subscribe
    client = paho.Client("led_manager")  # create client
    client.on_message = on_message # Bind function to callback
    client.connect(broker)  # connect
    client.loop_start()  # start loop to process received messages
    client.subscribe("leds")  # subscribe

    # set signal handler to catch ctrl C
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print 'Ready to receive commands'

    while True:
        t = time.time()
        for i in range(LED_COUNT):
            func, args = func_table[i]
            if isinstance(args, Iterable):
                strip.setPixelColor(i, func(t, *args))
            else:
                strip.setPixelColor(i, func(t, args))
            strip.show()
        time.sleep(fd)
