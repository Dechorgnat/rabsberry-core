#!/usr/bin/python
# -*- coding: utf-8 -*-


"""This module ."""

import argparse
import urllib
import subprocess


def lcd_show(message, delay):
    print delay, "s -", message

    args = ["lcdclear"]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, output, error)
        args = ["lcdprint", "0", "0", message ]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, output, error)
        args = ["lcdclear"]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, output, error)
    return None

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
        description='''Lcd display utility ''',
        epilog="""""")
    parser.add_argument('--delay', default=5)
    parser.add_argument('msg', nargs='+',  help='text message')
    args=parser.parse_args()
    for message in args.msg:
        lcd_show(message, args.lang)
