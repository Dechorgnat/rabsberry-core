#!/usr/bin/python

"""This module ."""

import argparse
import urllib
import subprocess


def play_tts(message, lang):
    print lang, "-", message
    # "http://translate.google.com/translate_tts?tl=lang&client=tw-ob&q=message"
    params = urllib.urlencode({'tl':lang, 'client':'tw-ob','q':message})
    uri = "http://translate.google.com/translate_tts?"+params
    print uri
    args = ["mpg321",
            "-q",
            uri]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, output, error)
    return None

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
        description='''Text to speech utility ''',
        epilog="""All's well that ends well.""")
    parser.add_argument('--lang', default='fr', choices=['fr', 'en'])
    parser.add_argument('msg', nargs='+',  help='utf8 text message')
    args=parser.parse_args()
    for message in args.msg:
        play_tts(message,args.lang)
