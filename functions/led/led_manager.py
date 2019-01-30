#!/usr/bin/python
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
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
LED_BRIGHTNESS = 40  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)

NOSE = 0
LEFT = 1
CENTER = 2
RIGHT = 3
BOTTOM = 4

broker="127.0.0.1"


def signal_handler(sig, frame):
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


def fixedColor(t, color):
    return color


def clearStrip(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()


#define MQTT callback
def on_message(client, userdata, message):
    message =str(message.payload.decode("utf-8"))
    print("received message =", message)
    if message == "stop":
        signal_handler(None, None)
    if message == "on":
        func_table[0] = (waveOneColor, (4., 0, 255, 0, 0))
        func_table[1] = (waveOneColor, (4., 0, 255, 0, 0))
        func_table[2] = (waveOneColor, (4., 0, 255, 0, 0))
    if message == "off":
        func_table[0] = (waveOneColor, (3., 0, 255, 0, 0))
        func_table[1] = (waveOneColor, (3., 1.0, 255, 255, 0))
        func_table[2] = (waveOneColor, (3., 2.0, 0, 0, 255))
    if message == "random":
        func_table[0] = (occultationOneColor, (2., 1.0, 1.0, BLUE))
        func_table[1] = (occultationOneColor, (2.5, 0.5, 0., YELLOW1))
        func_table[2] = (occultationOneColor, (1.0, 2., 0.5, RED1))


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
        0: (fixedColor, BLACK),
        1: (fixedColor, BLACK),
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
    signal.signal(signal.SIGKILL, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)

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
