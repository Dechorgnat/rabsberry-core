import RPi.GPIO as GPIO
import time

button_pin = 11

GPIO.setmode(GPIO.BOARD)

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state=GPIO.input(button_pin)
    if input_state == False:
        print "button pressed"
        time.sleep(0.2)