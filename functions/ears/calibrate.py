import RPi.GPIO as GPIO
import time
import math
from ear import Ear

control_pin = 11
current_milli_time = lambda: int(round(time.time() * 1000))
bouncetime = 20
last_tick = 0
list_delay = []
num = 0

def front_detected(channel):
    global last_tick
    global list_delay
    global num
    delay = current_milli_time() - last_tick
    if delay>bouncetime:
        last_tick = current_milli_time()
        num = num+1
        mean = sum(list_delay) / float(len(list_delay))
        if math.fabs(delay-mean)>100:
            print "missing tooth (", num, ") ", delay, "ms / mean : ",mean, " ms"
        else:
            print "tooth (", num, ") ", delay, "ms / mean : ",mean, " ms"
            list_delay.append(delay)
    else:
        print "bounce ", delay, " ms"


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(control_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(control_pin, GPIO.FALLING, callback=front_detected)

last_tick = current_milli_time()
right_ear = Ear(12, 16, 18, control_pin)
right_ear.start(Ear.forward)
time.sleep(6)
right_ear.stop()
right_ear.cleanup()

GPIO.cleanup(control_pin)
