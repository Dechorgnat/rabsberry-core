#!/usr/bin/python

from ear import Ear
import paho.mqtt.client as paho
import time
import signal
import sys
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
def on_message(client, userdata, message):
    message =str(message.payload.decode("utf-8"))
    print("received message =", message)
    right_ear.goto(10);
    left_ear.goto(10);

if __name__ == "__main__":
    conf = getConfig()

    right_ear_enable = getConfig()["RIGHT_EAR_ENABLE"],
    right_ear_in1 = getConfig()["RIGHT_EAR_IN1"],
    right_ear_in2 = getConfig()["RIGHT_EAR_IN2"],
    right_ear_indexer = getConfig()["RIGHT_EAR_INDEXER"],

    right_ear = Ear(right_ear_enable, right_ear_in1, right_ear_in2, right_ear_indexer)
    right_ear.calibrate()

    left_ear_enable = getConfig()["LEFT_EAR_ENABLE"],
    left_ear_in1 = getConfig()["LEFT_EAR_IN1"],
    left_ear_in2 = getConfig()["LEFT_EAR_IN2"],
    left_ear_indexer = getConfig()["LEFT_EAR_INDEXER"],

    left_ear = Ear(left_ear_enable, left_ear_in1, left_ear_in2, left_ear_indexer)
    left_ear.calibrate()

    # waiting for calibration
    time.sleep(10)

    # init mqtt connection and subscribe
    client = paho.Client("ears_manager")  # create client
    client.on_message = on_message # Bind function to callback
    client.connect(broker)  # connect
    client.loop_start()  # start loop to process received messages
    client.subscribe("ears")  # subscribe

    # set signal handler to catch ctrl C
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        time.sleep(1)