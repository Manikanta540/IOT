import os, time
import threading
import paho.mqtt.client as mqtt
import picamera
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import spidev
import random
from mydef import SlotUpdate
from main_prog import on_message


broker_address="iot.eclipse.org"
client = mqtt.Client("P1") #create new instance

def on_log(client,userdata,level,buf):
    print ("Log:"+buf)

def on_connect(client,userdata,flags,rc):
    if rc == 0 :
        print ("Connected Ok")
    else :
        print ("Bad Coneection returned code =",rc)

def on_disconnect(client,userdata,flags,rc=0):
    print ("Disconnected: "+str(rc))

"""
def publish_image() :
    fd = open("img1.jpg",'rb')
    print("Open Image")
    fc = fd.read()
    print("Read Image")
    #bytearr = bytearray(fc)
    client.publish("parking/entrance/camera",fc,2)
    print("published")
"""

client.on_log = on_log()
client.on_connect = on_connect()
client.on_disconnect = on_disconnect()
client.on_message = on_message()

client.connect(broker_address)
client.loop_start()
client.subscribe("parking/edge/slot/return")
time.sleep(6000)
client.loop_stop()