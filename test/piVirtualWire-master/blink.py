import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(12, GPIO.IN) ## Setup GPIO Pin 7 to OUT

while 1:
    k=GPIO.input(12)
    print  k
GPIO.cleanup()

## Ask user for total number of blinks and length of each blink