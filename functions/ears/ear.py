import RPi.GPIO as GPIO
from time import sleep

class Ear:
    forward=0
    backward=1

    def __init__(self, enable, in1, in2):
        self.enable = enable
        self.in1 = in1
        self.in2 = in2
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.enable,GPIO.OUT)


    def start (self, direction):
        if direction == Ear.forward:
            GPIO.output(self.in1,GPIO.HIGH)
            GPIO.output(self.in2,GPIO.LOW)
        else:
            GPIO.output(self.in2,GPIO.HIGH)
            GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.enable,GPIO.HIGH)


    def stop(self):
        GPIO.output(self.enable,GPIO.LOW)
