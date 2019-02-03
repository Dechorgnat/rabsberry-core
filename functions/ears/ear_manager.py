#!/usr/bin/python

from ear import Ear
import paho.mqtt.client as paho
import time
import signal
import sys
import json
from core.tools.config import getConfig

broker="127.0.0.1"

def signal_handler(sig, frame):
    # clean ears GPIO
    right_ear.cleanup()
    left_ear.cleanup()
    # close MQTT connection
    client.disconnect()  # disconnect
    client.loop_stop()  # stop loop

    sys.exit(0)

# define callback
def onmessage(client, userdata, message):
    message =str(message.payload.decode("utf-8"))
    print "received message: "+ message
    event = json.loads(message)
        
    if event['command'] == 'goto':
        print event['command']
        if event['ear'] == 'left':
            left_ear.goto(event['pos'], event['sens'])
        if event['ear'] == 'right':
            right_ear.goto(event['pos'], event['sens'])
        if event['ear'] == 'both':
            right_ear.goto(event['pos'], event['sens'])
            left_ear.goto(event['pos'], event['sens'])
    

if __name__ == "__main__":
    conf = getConfig()

    right_ear_enable = getConfig()["RIGHT_EAR_ENABLE"]
    right_ear_in_one = getConfig()["RIGHT_EAR_IN1"]
    right_ear_in_two = getConfig()["RIGHT_EAR_IN2"]
    right_ear_indexer = getConfig()["RIGHT_EAR_INDEXER"]

    right_ear = Ear(right_ear_enable, right_ear_in_one, right_ear_in_two, right_ear_indexer)
    right_ear.calibrate()

    left_ear_enable = getConfig()["LEFT_EAR_ENABLE"]
    left_ear_in_one = getConfig()["LEFT_EAR_IN1"]
    left_ear_in_two = getConfig()["LEFT_EAR_IN2"]
    left_ear_indexer = getConfig()["LEFT_EAR_INDEXER"]

    left_ear = Ear(left_ear_enable, left_ear_in_one, left_ear_in_two, left_ear_indexer)
    left_ear.calibrate()


    # init mqtt connection and subscribe
    client = paho.Client("ears_manager")  # create client
    client.on_message = onmessage # Bind function to callback
    client.connect(broker)  # connect
    client.loop_start()  # start loop to process received messages
    client.subscribe("ears")  # subscribe

    # set signal handler to catch ctrl C
    signal.signal(signal.SIGINT, signal_handler)

    # waiting for calibration
    time.sleep(10)
    
    while True:
        time.sleep(1)
