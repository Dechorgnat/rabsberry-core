#!/usr/bin/python

from ear import Ear
import time

#ear = Ear(18,16,22,13)
ear = Ear(23,19,21,15)

ear.calibrate()

ear.cleanup()

