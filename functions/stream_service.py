#!/usr/bin/python
# -*- coding: utf-8 -*-


"""This module ."""

import argparse
import subprocess

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
        description='''Audio streaming utility ''',
        epilog="""""")
    parser.add_argument('action', choices=['start', 'pause', 'resume', 'stop'])
    parser.add_argument('uri', help="URI to stream")
    args=parser.parse_args()
