import RPi.GPIO as GPIO
import time

def button_pressed(channel):
    print "button pressed"
    time.sleep(0.2)

button_pin = 11

GPIO.setmode(GPIO.BOARD)

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_pressed)

while True:
    time.sleep(5)