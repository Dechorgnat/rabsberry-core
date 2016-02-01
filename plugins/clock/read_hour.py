#!/usr/bin/python

import datetime
import subprocess

from tools.config import getConfig
conf = getConfig()
print(conf)


if __name__ == "__main__":
    hour = datetime.datetime.now().strftime('%H').lstrip("0")
    args = ["mpg321",
            "-q",
            conf['CORE_ROOT']+"/resources/mp3/clock/fr/signature.mp3",
            conf['CORE_ROOT']+"/resources/mp3/clock/fr/"+hour+"/1.mp3",
            conf['CORE_ROOT']+"/resources/mp3/clock/fr/signature.mp3"]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, output, error)
