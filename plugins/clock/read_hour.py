#!/usr/bin/python

import os
import sys
import datetime
import subprocess
from StringIO import StringIO
import json

def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


with open(getScriptPath()+'/../../config.json') as json_data_file:
    conf = json.load(json_data_file)
#print(conf)


if __name__ == "__main__":
    hour = datetime.datetime.now().strftime('%H').strip("0")

    args = ["mpg321",
            "-q",
            conf['CORE_ROOT']+"/resources/mp3/clock/fr/signature.mp3",
            conf['CORE_ROOT']+"/resources/mp3/clock/fr/"+hour+"/1.mp3",
            conf['CORE_ROOT']+"/resources/mp3/clock/fr/signature.mp3"]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, output, error)
