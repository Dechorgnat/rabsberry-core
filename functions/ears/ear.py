import RPi.GPIO as GPIO
from time import sleep

class Ear:
    forward=0
    backward=1


    def __init__(self, enable, in1, in2, control):
        self.enable = enable
        self.control = control
        self.in1 = in1
        self.in2 = in2
        self.running = False
        self.current_direction = self.forward
        #
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.enable,GPIO.OUT)
        GPIO.setup(self.control, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.enable,GPIO.LOW)



    def start (self, direction):
        if direction == Ear.forward:
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


    def cleanup(self):
        GPIO.cleanup([self.in1, self.in2, self.enable, self.control])


if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    left_ear = Ear(23, 19, 21, 13)
    right_ear = Ear(12, 16, 18, 11)

    print "Left going forwards 1.5s"
    left_ear.start(Ear.forward)
    sleep(1.5)
    left_ear.stop()

    print "Right going forwards 1.5s"
    right_ear.start(Ear.forward)
    sleep(1.5)
    right_ear.stop()

    print "Left going forwards 1.5s"
    left_ear.start(Ear.forward)
    sleep(1.5)
    left_ear.stop()

    print "Right going forwards 1.5s"
    right_ear.start(Ear.forward)
    sleep(1.5)
    right_ear.stop()

    print "Left and right going backwards 3s"
    left_ear.start(Ear.backward)
    right_ear.start(Ear.backward)
    sleep(3)

    left_ear.stop()
    right_ear.stop()

    left_ear.cleanup()
    right_ear.cleanup()
