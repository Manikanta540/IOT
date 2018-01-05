import RPi.GPIO as GPIO
from lib_nrf24 import NRF24

import time, datetime
import spidev


GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF1, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE2]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[1])

radio.printDetails()
#radio.startListening()
#message=list("open")
#while len(message)<32:
#message.append(0)
while 1 :

    t=0
    message=list("open")
    while len(message)<32:
        message.append(0)
    while t==0:
        time.sleep(0.1)
        t = radio.write(message)
        print t

    t=0
    message=list("close")
    while len(message)<32:
        message.append(0)
    while t==0:
        time.sleep(0.1)
        t = radio.write(message)
        print t
        

