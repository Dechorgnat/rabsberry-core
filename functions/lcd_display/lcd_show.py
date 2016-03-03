#!/usr/bin/python
# -*- coding: utf-8 -*-


"""This module ."""

import argparse
import urllib
import subprocess
from time import sleep

def lcd_show(message, delay):
    print delay, "s -", message

    args = ["sudo", "lcdclear"]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, output, error)
    args = ["sudo", "lcdprint", "0", "0", message ]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, output, error)
    sleep(delay)
    args = ["sudo", "lcdclear"]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, output, error)
    return None

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
        description='''Lcd display utility ''',
        epilog="""""")
    parser.add_argument('--delay', default=5. , type=float)
    parser.add_argument('msg', nargs='+',  help='text message')
    args=parser.parse_args()
    for message in args.msg:
        lcd_show(message, args.delay*1.0)
