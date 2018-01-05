import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import paho.mqtt.client as mqtt
import time, datetime
import spidev
import json
topic = "parking/slotactivity"

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

SlotArr = [ "B1F1W11", "B1F1W12", "B1F2W11", "B1F2W12"]
BIDArr = ["B1","B1","B1","B1"]
FIDArr = ["F1","F1","F2","F2"]
WIDArr = ["W1","W1","W1","W1"]
SIDArr = ["1","2","1","2"]
prev_status = ["0","0","0","0"]

SlotID = " "
BID = " "
FID = " "
WID = " "
SID = " "
status = " "

def publishSlotChanges(SlotID,BID,FID,WID,SID,status,TS):
    send_msg = {
        "Slot_id" : SlotID,
        "Building": BID,
        "Floor": FID,
        "Wing": WID,
        "Slot": SID,
        "Status" : status,
        "Time" : TS
    }
    msg = json.dumps(send_msg)
    client.publish(topic,msg)
    print ("Published status %s  %s", SlotID, status)

client.loop_start() #start the loop
while True:
    start = time.time()
    recived = 1
    #radio.write(message)
    #print("Sent the message: {}".format(message))
    radio.startListening()
    i = sum - i ;
    print pipes[i]
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

        #print("Translating our received Message into unicode characters...")

        s = ""
        
        for n in receivedMessage:
            if (n >= 32 and n <= 126):
                s += chr(n)
        print("Our received message decodes to: {}".format(s))
        #print " "
        #post = '{"author": "Sharad","text": "My first blog post!","tags": ["mongodb", "python"]}'

        print("Subscribing to topic")
        if s[0] == "A" :
            if s[1] == "1" :
                SlotID = "B1F1W11"
                BID = "B1"
                FID = "F1"
                WID = "W1"
                SID = "1"
                status = s[2]

            elif s[1] == "2" :
                SlotID = "B1F1W12"
                BID = "B1"
                FID = "F1"
                WID = "W1"
                SID = "2"
                status = s[2]

            else :
                print ("Wrong Sensor Address")
        elif s[0] == "B" :
            if s[1] == "1" :
                SlotID = "B1F2W11"
                BID = "B1"
                FID = "F2"
                WID = "W1"
                SID = "1"
                status = s[2]

            elif s[1] == "2" :
                SlotID = "B1F2W12"
                BID = "B1"
                FID = "F2"
                WID = "W1"
                SID = "2"
                status = s[2]

            else :
                print ("Wrong Sensor Address")
        else :
            print ("Wrong Adress")
            continue
        
        publishSlotChanges(SlotID,BID,FID,WID,SID,status,str(datetime.datetime.now()))
        
        time.sleep(2) # wait
        
    radio.stopListening()
    time.sleep(1)
client.loop_stop() #stop the loop    
# >