# *******************************************************************
# * DUAL MOTOR DRIVER USING A Wii REMOTE CONTROL AND THE GPIO BUS   *
# *******************************************************************
# * This program is designed to control the L298N Dual Full Bridge  *
# * Driver IC, which in turn drives two DC motors.  These could be  *
# * the left and right hand wheels of a small motorised vehicle.    *
# * The L298N has 6 control signals: In1, In2, In3, In4, EnA & EnB. *
# * All of the signals are active high.  See the manufacturers data *
# * sheet for full details of the L298N device.                     *
# *                                                                 *
# * Run the program from a Terminal window (root user).  It will    *
# * not run from within the Python Shell GUI.                       *
# *                                                                 *
# * List of the GPIO pins used:                                     *
# * GPIO25 - Motor 1 (left motor) Enable - EnA - (output - bit 0)   *
# * GPIO24 - Motor 1 (left motor) Forward - In1 -(output - bit 1)   *
# * GPIO23 - Motor 1 (left motor) Reverse - In2 -(output - bit 2)   *
# *                                                                 *
# * GPIO22 - Motor 2 (right motor) Enable - EnB - (output - bit 3)  *
# * GPIO27 - Motor 2 (right motor) Forward - In3 - (output - bit 4) *
# * GPIO18 - Motor 2 (right motor) Reverse - In4 - (output - bit 5) *
# *                                                                 *
# * GPIO17 - Trigger for the ultrasonic sensor (output - bit 6)     *
# *                                                                 *
# * GPIO11 - Spare GPIO output pin (output - bit 7)                 *
# *                                                                 *
# * GPIO10 - Echo input from the ultrasonic sensor (input - bit 8)  *
# *                                                                 *
# * GPIO9  - Spare GPIO Input pin (input - bit 9)                   *
# * GPIO8  - Spare GPIO Input pin (input - bit 10)                  *
# * GPIO7  - Spare GPIO Input pin (input - bit 11)                  *
# *******************************************************************

import RPi.GPIO as GPIO                                                 # Import the GPIO module as 'GPIO'

                                                          # Import the Nintendo Wii controller module

import time                                                             # Import the 'time' module

import random

GPIO.setmode (GPIO.BCM)                                                 # Set the GPIO mode to BCM numbering


# *******************************************************************
# *                       DEFINE THE CONSTANTS                      *
# *******************************************************************
# *  IMPORTANT: For a Rev 1 RPi, replace 27 below with 21 instead   *
# *******************************************************************

output_ports = [25, 24, 23, 22, 27, 17, 11]                         # Define the GPIO output port numbers
input_ports = [10, 9, 8, 7,18]                                             # Define the GPIO input port numbers

trig = 23                                                               # Trigger output for the ultrasonic sensor
echo = 18                                                              # Echo return from the ultrasonic sensor




def get_distance ():
    global trig, echo                                                   # Allow access to 'trig' and 'echo' constants

    if GPIO.input (echo):                                               # If the 'Echo' pin is already high
        return (100)                                                    # then exit with 100 (sensor fault)

    distance = 0                                                        # Set initial distance to zero

    GPIO.output (trig,False)                                            # Ensure the 'Trig' pin is low for at
    time.sleep (0.05)                                                   # least 50mS (recommended re-sample time)

    GPIO.output (trig,True)                                             # Turn on the 'Trig' pin for 10uS (ish!)
    dummy_variable = 0                                                  # No need to use the 'time' module here,
    dummy_variable = 0                                                  # a couple of 'dummy' statements will do fine
    
    GPIO.output (trig,False)                                            # Turn off the 'Trig' pin
    time1, time2 = time.time(), time.time()                             # Set inital time values to current time
    
    while not GPIO.input (echo):                                        # Wait for the start of the 'Echo' pulse
        time1 = time.time()                                             # Get the time the 'Echo' pin goes high
        if time1 - time2 > 0.02:                                        # If the 'Echo' pin doesn't go high after 20mS
            distance = 100                                              # then set 'distance' to 100
            break                                                       # and break out of the loop
        
    if distance == 100:                                                 # If a sensor error has occurred
        return (distance)                                               # then exit with 100 (sensor fault)
    
    while GPIO.input (echo):                                            # Otherwise, wait for the 'Echo' pin to go low
        time2 = time.time()                                             # Get the time the 'Echo' pin goes low
        if time2 - time1 > 0.02:                                        # If the 'Echo' pin doesn't go low after 20mS
            distance = 100                                              # then ignore it and set 'distance' to 100
            break                                                       # and break out of the loop
        
    if distance == 100:                                                 # If a sensor error has occurred
        return (distance)                                               # then exit with 100 (sensor fault)
        
                                                                        # Sound travels at approximately 2.95uS per mm
                                                                        # and the reflected sound has travelled twice
                                                                        # the distance we need to measure (sound out,
                                                                        # bounced off object, sound returned)
                                                                        
    distance = (time2 - time1) / 0.00000295 / 2 / 10                    # Convert the timer values into centimetres
    return (distance)                                                   # Exit with the distance in centimetres
    

while True:
	 
	k=get_distance()       
	print k
