#!/usr/bin/python

import sys
import datetime
from subprocess import call

if __name__ == "__main__":
    hour = datetime.datetime.now().strftime('%H')
    call (["mpg321", "resources/mp3/clock/fr/signature.mp3", "resources/mp3/clock/fr/"+hour+"/1.mp3", "resources/mp3/clock/fr/signature.mp3"])
