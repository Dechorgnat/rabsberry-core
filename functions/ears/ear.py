#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep

class Ear:
    FORWARD="forward"
    BACKWARD="backward"

    def __init__(self, enable, in1, in2, indexer):
        self.enable = enable
        self.indexer = indexer
        self.in1 = in1
        self.in2 = in2
        self.running = False
        self.current_direction = Ear.FORWARD
        self.position=-1
        #
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.enable,GPIO.OUT)
        GPIO.setup(self.indexer, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.enable,GPIO.LOW)

    def start(self, direction):
        if direction == Ear.FORWARD:
            GPIO.output(self.in1,GPIO.HIGH)
            GPIO.output(self.in2,GPIO.LOW)
        else:
            GPIO.output(self.in2,GPIO.HIGH)
            GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.enable,GPIO.HIGH)
        self.running = True
        self.current_direction = direction

    def stop(self):
        GPIO.output(self.enable,GPIO.LOW)
        self.running = False

    def goto(self, position, direction):
        # TODO
        print "going ", direction, " to position ",position

    def get_position(self):
        return self.position

    def cleanup(self):
        GPIO.cleanup([self.in1, self.in2, self.enable, self.indexer])

    def calibrate(self):
        # TODO
        print "starting calibration"


if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    left_ear = Ear(23, 19, 21, 13)
    right_ear = Ear(12, 16, 18, 11)

    left_ear.calibrate()
    right_ear.calibrate()

    print "Left  position : ", left_ear.get_position()
    print "Right position : ", right_ear.get_position()

    print "Left  going forward 1.5s"
    left_ear.start(Ear.FORWARD)
    sleep(1.5)
    left_ear.stop()

    print "Right going forward 1.5s"
    right_ear.start(Ear.FORWARD)
    sleep(1.5)
    right_ear.stop()

    print "Left  going forward 2s"
    left_ear.start(Ear.FORWARD)
    sleep(2)
    left_ear.stop()

    print "Right going forward 2s"
    right_ear.start(Ear.FORWARD)
    sleep(2)
    right_ear.stop()

    print "Left  position : ", left_ear.get_position()
    print "Right position : ", right_ear.get_position()

    sleep(5)

    print "Left and right going backward 3.5s"
    left_ear.start(Ear.BACKWARD)
    right_ear.start(Ear.BACKWARD)
    sleep(3.5)
    left_ear.stop()
    right_ear.stop()

    print "Left  position : ", left_ear.get_position()
    print "Right position : ", right_ear.get_position()

    print "Right going forward to position 0"
    right_ear.goto(0, Ear.FORWARD)
    print "Left  going forward to position 0"
    left_ear.goto(0, Ear.FORWARD)
    sleep(5)

    print "Right going forward  to position 10"
    right_ear.goto(10, Ear.FORWARD)
    print "Left  going backward to position 10"
    left_ear.goto(10, Ear.BACKWARD)
    sleep(5)


    left_ear.cleanup()
    right_ear.cleanup()
