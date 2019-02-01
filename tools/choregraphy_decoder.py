#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import sys
import paho.mqtt.client as paho
import json
import time

def not_implemented():
    print('not_implemented', chor[index])
    print("duree:", duree)
    sys.exit(1)


def leds():
    global index
    led_num = chor[index + 1]
    led = ("bottom", "left", "center", "right", "top")[led_num]
    print('led', led, ', rgb(', chor[index+2], ', ', chor[index+3], ', ', chor[index+4], ")")
    # print('led', chor[index+1], ', ', chor[index+2], ', ', chor[index+3], ', ', chor[index+4])
    index = index + 7
    msg = json.dumps({
        'command': 'set',
        'leds': [str(led_num)],
        'r': int(chor[index+2]),
        'g': int(chor[index+3]),
        'b': int(chor[index+4])
    })
    # print(msg)
    mqtt.publish("leds", msg)
    pass


def ears():
    global index
    ear = ("right", "left")[chor[index+1]]
    sens = ("forward", "backward")[chor[index+3]]
    print('ear', ear, ', ', chor[index + 2], ', ', sens)
    # print('ear', chor[index+1], ', ', chor[index+2], ', ', chor[index+3])
    msg = json.dumps({
        'command': 'goto',
        'ear': chor[index + 1],
        'pos': chor[index + 2],
        'dir': chor[index + 3],
    })
    # print(msg)
    # mqtt.publish("leds", msg)
    index = index + 4
    pass


def tempo():
    global index, timescale
    timescale = chor[index+1]
    print('tempo: timescale=', timescale)
    index = index + 2
    pass


def set_led_palette():
    global index
    led = chor[index+1]
    col_ix = chor[index + 2] & 3
    print('set_led_palette', led, col_ix)
    index = index + 3
    pass


def set_led_off():
    global index
    led = chor[index+1]
    print('set_led_off', led)
    index = index + 2
    pass


def decode_command(argument):
    switcher = {
        1: tempo,
        2: not_implemented,
        3: not_implemented,
        4: not_implemented,
        5: not_implemented,
        6: not_implemented,
        7: leds,
        8: ears,
        9: not_implemented,
        10: set_led_off,
        11: not_implemented,
        12: not_implemented,
        13: not_implemented,
        14: set_led_palette,
        15: not_implemented
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, lambda: "Invalid command")
    # Execute the function
    func()


parser = argparse.ArgumentParser(
        description='''Choregraphy utility ''',
        epilog="""""")
parser.add_argument('filename', nargs='+',  help='choregraphy file')
args = parser.parse_args()

# init mqtt connection and subscribe
mqtt = paho.Client("choregraphy")  # create client
mqtt.connect('192.168.1.65')

my_file = open(args.filename[0], "r")
chor = bytearray(my_file.read())

index = 4
timescale = 0
duree = 0

while index < len(chor):
    wait = chor[index]
    # do some wait now
    delay = wait * timescale / 1000.0
    time.sleep(delay)
    print("wait (", wait, ")", delay, "ms")
    duree = duree + delay
    index = index + 1

    command = chor[index]
    decode_command(command)

print("duree:", duree)
