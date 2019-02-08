#!/usr/bin/python

from ear import Ear
import paho.mqtt.client as paho
import time
import signal
import sys
import json
import logging
from core.tools.config import getConfig
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG, filename='/var/log/rabsberry/ear_manager.log')

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
    try:
        message =str(message.payload.decode("utf-8"))
        logging.info("received message: "+ message)
        event = json.loads(message)
        
        # goto command
        if event['command'] == 'goto':
            logging.info(event['command'])
            if event['ear'] == 'left':
                left_ear.goto(event['pos'], event['dir'])
            if event['ear'] == 'right':
                right_ear.goto(event['pos'], event['dir'])
            if event['ear'] == 'both':
                right_ear.goto(event['pos'], event['dir'])
                left_ear.goto(event['pos'], event['dir'])
        return
        # step command
        if event['command'] == 'step':
            logging.info(event['command'])
            if event['ear'] == 'left':
                left_ear.step(event['pos'], event['dir'])
            if event['ear'] == 'right':
                right_ear.step(event['pos'], event['dir'])
            if event['ear'] == 'both':
                right_ear.step(event['pos'], event['dir'])
                left_ear.step(event['pos'], event['dir'])
        return
        # stop command
        if event['command'] == 'stop':
            logging.info(event['command'])
            if event['ear'] == 'left':
                left_ear.stop()
            if event['ear'] == 'right':
                right_ear.stop()
            if event['ear'] == 'both':
                right_ear.stop()
                left_ear.stop()

    except Exception as e:
        logging.info(e)

if __name__ == "__main__":
    conf = getConfig()

    right_ear_enable = conf["RIGHT_EAR_ENABLE"]
    right_ear_in_one = conf["RIGHT_EAR_IN1"]
    right_ear_in_two = conf["RIGHT_EAR_IN2"]
    right_ear_indexer = conf["RIGHT_EAR_INDEXER"]

    right_ear = Ear(right_ear_enable, right_ear_in_one, right_ear_in_two, right_ear_indexer)
    right_ear.calibrate()

    left_ear_enable = conf["LEFT_EAR_ENABLE"]
    left_ear_in_one = conf["LEFT_EAR_IN1"]
    left_ear_in_two = conf["LEFT_EAR_IN2"]
    left_ear_indexer = conf["LEFT_EAR_INDEXER"]

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
    signal.signal(signal.SIGTERM, signal_handler)

    # waiting for calibration
    time.sleep(10)
    
    logging.info("Ready to receive message")

    while True:
        time.sleep(1)
