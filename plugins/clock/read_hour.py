#!/usr/bin/python

import datetime
import random
import os

from Rabsberry.core.tools.config import getConfig
from Rabsberry.core.functions.play_audio import play_audio_files

conf = getConfig()
print(conf)

if __name__ == "__main__":
    hour = datetime.datetime.now().strftime('%H').lstrip("0")

    files = os.listdir( conf['CORE_ROOT'] + "/resources/mp3/clock/fr/" + hour )
    random.shuffle(files)
    print files[0]
    play_audio_files([
        conf['CORE_ROOT'] + "/resources/mp3/clock/fr/signature.mp3",
        conf['CORE_ROOT'] + "/resources/mp3/clock/fr/" + hour + "/"+files[0],
        conf['CORE_ROOT'] + "/resources/mp3/clock/fr/signature.mp3"])