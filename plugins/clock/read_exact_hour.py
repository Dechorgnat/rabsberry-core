#!/usr/bin/python

import datetime

from core.tools.config import getConfig
from core.functions.play_tts import play_tts

conf = getConfig()
print(conf)

if __name__ == "__main__":
    hour = datetime.datetime.now().strftime('%H').lstrip("0")
    minute = datetime.datetime.now().strftime('%m').lstrip("0")

    play_tts( str(hour)+ " heures "+ str(minute) )