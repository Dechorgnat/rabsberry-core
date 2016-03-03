import RPi.GPIO as GPIO
import time
import math
from ear import Ear

control_pin = 13
current_milli_time = lambda: int(round(time.time() * 1000))
bouncetime = 20
last_tick = 0
list_delay = []
list_delay.append(200)
num = 0

# il y avait 20 dents sur la roue mais 3 ont ete enlevees

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

GPIO.setup(control_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(control_pin, GPIO.FALLING, callback=front_detected)

last_tick = current_milli_time()

if GPIO.input(control_pin):
    print('Input was HIGH')
else:
    print('Input was LOW')

right_ear = Ear(12, 16, 18, control_pin)
<<<<<<< HEAD
#left_ear = Ear(23, 19, 21, control_pin)

#right_ear.start(Ear.forward)
while True:
    if GPIO.input(control_pin):
        print('Input was HIGH')
    else:
        print('Input was LOW')
    time.sleep(1)
=======
right_ear.start(Ear.FORWARD)
time.sleep(6)
>>>>>>> 9d2eab17deda4658ee1803b41551504f1bd5928e
right_ear.stop()
right_ear.cleanup()

GPIO.cleanup(control_pin)
