#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import requests

current_milli_time = lambda: int(round(time.time() * 1000))

class Ear:
    FORWARD = "forward"
    BACKWARD = "backward"

    def __init__(self, enable, in1, in2, indexer):
        self.enable = enable
        self.indexer = indexer
        self.in1 = in1
        self.in2 = in2
        self.running = False
        self.current_direction = self.FORWARD
        self.position = -1
        self.goal = -1
        self.calibrating = False
        self.last_tick = 0
        self.num = 0
        self.found_missing = False
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.enable,GPIO.OUT)
        GPIO.setup(self.indexer, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.enable,GPIO.LOW)
        GPIO.add_event_detect(self.indexer, GPIO.FALLING, callback=self.front_detected, bouncetime=30)

    def front_detected(self, channel):
        #print "front detected ", self.calibrating, self.running, self.position
        if self.calibrating:
            delay = current_milli_time() - self.last_tick
            self.last_tick = current_milli_time()
            self.num = self.num+1
            if delay>800:
                self.goal = 17 - self.num
                self.num = 0
                self.found_missing = True
                print "missing tooth (", self.num, ") ", delay, "ms"
            else:
                print "tooth (", self.num, ") ", delay, "ms"
            if self.found_missing:
                self.position = self.num
            if self.found_missing and self.num == self.goal:
                self.stop()
                self.goal = -1
                self.calibrating = False
        else:
            # not calibrating
            if self.running:
                if self.current_direction == Ear.FORWARD:
                    self.position += 1
                    if self.position == 17:
                        self.position = 0
                else: # going backward
                    self.position -= 1
                    if self.position == -1:
                        self.position = 16
                #print "position : ", self.position
                if self.position == self.goal:
                    self.stop()
                    self.goal = -1
            else: # manual change of ear position
                # TODO
                print "manual change detected"
                self.manual_change = True

    def calibrate(self):
        print "starting calibration"
        self.calibrating = True
        self.num = 0
        self.found_missing = False
        self.last_tick = current_milli_time()
        self.start()
        
    def start(self, direction=FORWARD):
        self.running = True
        self.current_direction = direction
        if direction == Ear.FORWARD:
            GPIO.output(self.in1,GPIO.HIGH)
            GPIO.output(self.in2,GPIO.LOW)
        else:
            GPIO.output(self.in2,GPIO.HIGH)
            GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.enable,GPIO.HIGH)

    def stop(self):
        GPIO.output(self.enable,GPIO.LOW)
        self.running = False

    def goto(self, position, direction):
        print "going ", direction, " to position ",position
        self.goal = position
        self.start(direction)

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def cleanup(self):
        GPIO.cleanup([self.in1, self.in2, self.enable, self.indexer])


if __name__ == "__main__":

    left_ear = Ear(23, 19, 21, 15)
    right_ear = Ear(18, 16, 22, 13)
    right_ear.calibrate()
    left_ear.calibrate()

    # waiting for calibration
    time.sleep(10)

    print "Left  position : ", left_ear.get_position()
    print "Right position : ", right_ear.get_position()

    print "Left  going forward 1.5s"
    left_ear.start(Ear.FORWARD)
    time.sleep(1.5)
    left_ear.stop()

    print "Right going forward 1.5s"
    right_ear.start(Ear.FORWARD)
    time.sleep(1.5)
    right_ear.stop()

    print "Left  going forward 2s"
    left_ear.start(Ear.FORWARD)
    time.sleep(2)
    left_ear.stop()

    print "Right going forward 2s"
    right_ear.start(Ear.FORWARD)
    time.sleep(2)
    right_ear.stop()

    print "Left  position : ", left_ear.get_position()
    print "Right position : ", right_ear.get_position()

    time.sleep(5)

    print "Left and right going backward 3.5s"
    left_ear.start(Ear.BACKWARD)
    right_ear.start(Ear.BACKWARD)
    time.sleep(3.5)
    left_ear.stop()
    right_ear.stop()

    print "Left  position : ", left_ear.get_position()
    print "Right position : ", right_ear.get_position()

    print "Right going forward to position 3 (vertical)"
    right_ear.goto(3, Ear.FORWARD)
    print "Left  going forward to position 13"
    left_ear.goto(13, Ear.FORWARD)
    time.sleep(5)

    print "Right going backward  to position 13 (horizontal)"
    right_ear.goto(13, Ear.BACKWARD)
    print "Left  going backward to position 3"
    left_ear.goto(3, Ear.BACKWARD)
    time.sleep(5)

    print "Try moving right ear manually"
    time.sleep(5)
    print "End of tests"

    left_ear.cleanup()
    right_ear.cleanup()
