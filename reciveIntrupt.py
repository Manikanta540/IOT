import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
#import os
import time, datetime
import spidev

import threading

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE2], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
receivedMessage = []
s = []
i = 0

message=list("open")
while len(message)<32:
    message.append(0)

message1=list("close")
while len(message1)<32:
    message1.append(0)

def turnServo():

    time.sleep(2)
    t=0
    while t==0:
        time.sleep(1)
        t = radio.write(message)
        print ("open",t)
    time.sleep(2)
    t=0
    radio.flush_tx() 
    while t==0:
        time.sleep(1)
        t = radio.write(message1)
        print ("close",t,message1)
        
pi = [0]
def my_callback(channel):
    #maskInterrupt() 
    print "falling edge detected on 16"
    radio.IRQ_ALL()
    if radio.available(pi):
        print ("Pipe : {}".format(pi))
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        s = ""
        for n in receivedMessage:
            if (n >= 32 and n <= 126):
                s += chr(n)
        print("Our received message decodes to: {}".format(s))
        #t1 = threading.Thread(target=turnServo)
	#t1.start()
	#t1.join()
        
    print "End Of Routine"
    radio.IRQ()
    #unmaskInterrupt()       


radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.openReadingPipe(2, pipes[2])
radio.IRQ()
radio.printDetails()

#radio.startListening()
#message=list("open")
#while len(message)<32:
#message.append(0)

GPIO.add_event_detect(16, GPIO.FALLING, callback=my_callback)
#i =0
while True :
    radio.startListening()
    time.sleep(10)
    radio.stopListening()
    #print ("Main Running %d",i)
    #i = i + 1
        
#radio.stopListening()
