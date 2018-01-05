import os, time
#import threading
import paho.mqtt.client as mqtt
import picamera
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import spidev
import random
from mydef import SlotUpdate


DEV_ADDR = ["A","B","C","D","E","F"]
slotList = ["B1F1W11","B1F1W22","B1F2W22","B1F2W11"]
INTRUPT_PIN = 16
pipes = [[0xF0, 0xF0, 0xF0, 0xF1, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE2], [0xF0, 0xF0, 0xF0, 0xF0, 0xE3]]
receivedMessage = []
sq = [""]
pi = [0]
setreceivedata = 0

message=list("open")
while len(message)<32:
    message.append(0)

message1=list("close")
while len(message1)<32:
    message1.append(0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(INTRUPT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
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
radio.IRQ()
#radio.printDetails()

camera = picamera.PiCamera()
camera.resolution = (800,600)

broker_address="iot.eclipse.org"
client = mqtt.Client("RP1_MINE") #create new instance

def publish_image() :
    fd = open("img1.jpg",'rb')
    print("Open Image")
    fc = fd.read()
    print("Read Image")
    #bytearr = bytearray(fc)
    client.publish("parking/entrance/camera",fc)
    print("published")

def on_message(client,userdata,msg):
    mess = str(msg.payload.decode("utf-8"))
    if mess != 0 :
        print ("Allocated Slot : "+mess)
        openGate(mess)
        time.sleep(5)
    closeGate()
        
def takeAPic():
    my_file = open('img1.jpg', 'wb')
    print("hello")

    camera.start_preview()
    time.sleep(10)
    camera.stop_preview()
    camera.capture(my_file)
    
    print "Picture 2"
    my_file.flush()
    my_file.close()

def openGate(slotNum):
    time.sleep(2)
    t=0
    radio.flush_tx()
    #slotNum = slotList[random.randint(0,3)]
    while t==0:
        time.sleep(1)
        t =  radio.write(message)
    print ("open, Slot alocated : ",slotNum)
    
def closeGate() :
    time.sleep(2)
    t=0
    radio.flush_tx() 
    while t==0:
        time.sleep(1)
        t =  radio.write(message1)
        print t
    print ("Close The Gate")

def turnServo(s) :
    print "Thread turnSero running...!"
    print s
    if s[0] == "A" :
        if s[1] == "1" and s[2] == "2" :
            print "Taking Picture"
            takeAPic()
            #slotNum = allocSlot()
            publish_image()
            #openGate()
        else :
            #closeGate()
            print 1
    else :
        print ("Adress is : ",s)

"""
class slotUpdate(Thread):
    
    def _init_(self,args=()):
        Thread._init_(self)
"""
def updateSlotStatus(s) :
    print "Thread updateSlotStatus running...!"
    time.sleep(5)
    print s

def my_callback(channel):
    #maskInterrupt()
    #global s
    print ("Falling edge detected on : PIN - ",  INTRUPT_PIN)
    if  radio.available(pi):
        print ("Pipe : {}".format(pi))
        radio.read( receivedMessage, radio.getDynamicPayloadSize())
        #print("Received: {}".format(receivedMessage))
        global sq 
        global setreceivedata
        sq = ""
        for n in  receivedMessage:
            if (n >= 32 and n <= 126):
                sq += chr(n)
        print("Our received message decodes to: {}".format(sq))
        
        if pi[0] == 1 :
            setreceivedata=1
            #print setreceivedata
            #takeAPic()
            
            #t1 = threading.Thread(target=turnServo,args=[s])
        elif pi[0] == 2 :
            setreceivedata= 1
            #t1 = threading.Thread(target=updateSlotStatus,args=[s])
            #t1 = SlotUpdate(s)
        else :
            print ("Recied pipe is : ",pi[0], "I Don't Know Why...!")
        #t1 = threading.Thread(target=turnServo)
	#t1.start()
	#t1.join()

    print "End Of Routine"
    

print("Welcome To Parking System...!")

GPIO.add_event_detect(INTRUPT_PIN, GPIO.FALLING, callback=my_callback)

client.connect(broker_address)
client.on_message = on_message
client.loop_start()
client.subscribe("parking/edge/slot/return")
while True :
    radio.startListening()
    time.sleep(5)
    #print ("pi :",pi[0])
    #print sq, setreceivedata
    if  setreceivedata== 1:
        turnServo(sq)
        setreceivedata = 0   

    radio.stopListening()
client.loop_stop()
print("Main Exit")
