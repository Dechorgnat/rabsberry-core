#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import requests
import signal
import sys
import logging
from core.tools.config import getConfig
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG, filename='/var/log/rabsberry/top_button.log')
 

class Top_button:

    def __init__(self, top_button_pin, callback_short_pressed=None, callback_long_pressed=None):
        self.top_button_pin = top_button_pin
        self.callback_short_pressed = callback_short_pressed
        self.callback_long_pressed = callback_long_pressed
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.top_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def start_listening(self):
        logging.info('Top Button starts listening')
        GPIO.add_event_detect(self.top_button_pin, GPIO.BOTH, callback=self.button_pressed,  bouncetime=800) 

    def stop_listening(self):
        GPIO.remove_event_detect(self.top_button_pin)

    def cleanup(self):
        GPIO.cleanup(self.top_button_pin)

    def button_pressed(self, channel):
        if GPIO.input(channel):
            logging.debug("top button released")
        else:
            logging.debug("top button pressed")
            self.callback_short_pressed()


def signal_term_handler(signal, frame):
    logging.info('Terminating Top Button')
    top_button.stop_listening()
    top_button.cleanup()
    sys.exit(0)

def call_rabsberry_event_api(action):
    url = "http://localhost/api/event"
    payload = { 'actor_type':'TOP_BUTTON', 'actor_id':'TOP_BUTTON', 'action': action}
    requests.post(url, json=payload)


def callback_short_pressed():
    logging.debug("callback_short_pressed")
    call_rabsberry_event_api("SHORT_PRESSED")


def callback_long_pressed():
    logging.debug("callback_long_pressed")
    call_rabsberry_event_api("LONG_PRESSED")


top_button = Top_button(getConfig()['TOP_BUTTON'], callback_short_pressed, callback_long_pressed)
top_button.start_listening()
signal.signal(signal.SIGTERM, signal_term_handler)
signal.signal(signal.SIGINT, signal_term_handler)
while True:
    time.sleep(1)

