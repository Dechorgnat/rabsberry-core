#!/usr/bin/python

import datetime

from Rabsberry.core.tools.config import getConfig
from Rabsberry.core.functions.play_tts import play_tts

conf = getConfig()
print(conf)

if __name__ == "__main__":
    hour = datetime.datetime.now().strftime('%H').lstrip("0")
    minute = datetime.datetime.now().strftime('%M').lstrip("0")
    play_tts( "Il est " + str(hour)+ " heures "+ str(minute) +".", 'fr')
