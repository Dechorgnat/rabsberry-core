#!/usr/bin/python

import random
import os

from Rabsberry.core.tools.config import getConfig
from Rabsberry.core.functions.play_audio import play_audio_files

conf = getConfig()
print(conf)

if __name__ == "__main__":
    files = os.listdir( conf['CORE_ROOT'] + "/resources/mp3/surprise/fr/" )
    random.shuffle(files)
    print files[0]
    play_audio_files([conf['CORE_ROOT'] + "/resources/mp3/surprise/fr/" +files[0] ])
