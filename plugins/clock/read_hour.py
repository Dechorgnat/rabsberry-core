#!/usr/bin/python

import sys
import datetime
import subprocess
from StringIO import StringIO

if __name__ == "__main__":
    hour = datetime.datetime.now().strftime('%H')

    args = ["mpg321",
            "-q",
            "resources/mp3/clock/fr/signature.mp3",
            "resources/mp3/clock/fr/"+hour+"/1.mp3",
            "resources/mp3/clock/fr/signature.mp3"]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, output, error)