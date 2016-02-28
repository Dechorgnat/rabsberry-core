import RPi.GPIO as GPIO
from time import sleep
from ear import Ear

GPIO.setmode(GPIO.BOARD)

left_ear = Ear(23, 19, 21)
right_ear = Ear(12, 16, 18)




print "Going forwards"
left_ear.start(Ear.forward)
right_ear.start(Ear.forward)

sleep(5)
 
print "Going backwards"
left_ear.start(Ear.backward)
right_ear.start(Ear.backward)
 
sleep(5)
 
print "Now stop"
left_ear.stop()
right_ear.stop()

GPIO.cleanup()
