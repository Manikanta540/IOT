import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import paho.mqtt.client as mqtt
import time, datetime
import spidev

GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE2]]

broker_address="iot.eclipse.org"
client = mqtt.Client("P1") #create new instance
client.connect(broker_address) #connect to broker

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

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
radio.printDetails()
#radio.startListening()

message = list("GETSTRING")
while len(message) < 32:
    message.append(0)
sum = 1 + 2
i = 2

while True:
    start = time.time()
    recived = 1
    #radio.write(message)
    #print("Sent the message: {}".format(message))
    radio.startListening()
    i = sum - i ;
    print i
    while not radio.available(pipes[i]):
        time.sleep(1/100)
        if time.time() - start > 2:
            print("Timed out.")
            recived = 0
            break
        
    if recived == 1 :
    
        receivedMessage = []
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        print("Received: {}".format(receivedMessage))

        print("Translating our received Message into unicode characters...")
        string = ""
        
        for n in receivedMessage:
            if (n >= 32 and n <= 126):
                string += chr(n)
        print("Our received message decodes to: {}".format(string))
        print " "
        post = '{"author": "Sharad","text": "My first blog post!","tags": ["mongodb", "python", "pymongo"]}'
        client.loop_start() #start the loop
        print("Publishing message to topic","house/main")
        client.publish("house/main",post)
        time.sleep(4) # wait
        client.loop_stop() #stop the loop
        
        
    radio.stopListening()
    time.sleep(1)

# >