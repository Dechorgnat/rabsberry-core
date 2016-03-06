import RPi.GPIO as GPIO
import time
import math
from ear import Ear

control_pin = 13
current_milli_time = lambda: int(round(time.time() * 1000))
bouncetime = 20
last_tick = 0
list_delay = []
list_delay.append(250)
num = 0
found_missing =False

# il y avait 20 dents sur la roue mais 3 ont ete enlevees

def front_detected(channel):
    global last_tick
    global list_delay
    global num
    global right_ear
    global found_missing
    delay = current_milli_time() - last_tick
    if delay>bouncetime:
        last_tick = current_milli_time()
        num = num+1
        mean = sum(list_delay) / float(len(list_delay))
        if math.fabs(delay-mean)>100:
            num = 0
            found_missing = True
            print "missing tooth (", num, ") ", delay, "ms / mean : ",mean, " ms"
        else:
            print "tooth (", num, ") ", delay, "ms / mean : ",mean, " ms"
            list_delay.append(delay)
    else:
        print "bounce ", delay, " ms"
    if found_missing and num == 13:
        right_ear.stop()


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(control_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(control_pin, GPIO.FALLING, callback=front_detected, bouncetime=20)

last_tick = current_milli_time()

if GPIO.input(control_pin):
    print('Input was HIGH')
else:
    print('Input was LOW')

right_ear = Ear(12, 16, 18, control_pin)
#left_ear = Ear(23, 19, 21, control_pin)

'''
while True:
    if GPIO.input(control_pin):
        print('Input was HIGH')
    else:
        print('Input was LOW')
    time.sleep(1)

'''
right_ear.start(Ear.FORWARD)
time.sleep(10)
right_ear.stop()

right_ear.cleanup()

GPIO.cleanup(control_pin)
