#!/usr/bin/python
# -*- coding: utf-8 -*-


"""This module ."""

import argparse
import subprocess


def play_audio_file(audio_file):
    play_audio_files([audio_file])


def play_audio_files(audio_files):
    print audio_files

    args = ["mpg321","-q"]+ audio_files
    print args
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, output, error)
    return None

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
        description='''Play music utility ''',
        epilog="""""")
    parser.add_argument('uri', nargs='+',  help='audio file')
    args=parser.parse_args()
    play_audio_files(args.uri)
