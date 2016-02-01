import os
import json

RABSBERRY_HOME = os.environ.get("RABSBERRY_HOME", None)
default_configfile = RABSBERRY_HOME+"/config.json"
config = None

def getConfig(configfile=None):
    if not config:
        loadconf(configfile)
    return config


def loadconf(configfile=None):
    print ' enter configuration file :',configfile
    if not configfile:
        configfile = default_configfile

    print ' out configuration file :',configfile
    global config
    try :
        with open(configfile) as json_data_file:
            config = json.load(json_data_file)

        # prerequis to check !!
    except :
        print ' can\'t load :',configfile
        pass
    return config
