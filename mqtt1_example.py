import json
import paho.mqtt.client as mqtt #import the client1
import time, datetime

clientID = "RPI_1"
topic = "parking/slotactivity"
broker_address="iot.eclipse.org"

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

print("creating new instance")
client = mqtt.Client(clientID) #create new instance

print("connecting to broker")
client.connect(broker_address) #connect to broker

client.loop_start() #start the loop
print("Subscribing to topic",topic)
publishSlotChanges("B1F1W11","B1","F1","W1","1","1",str(datetime.datetime.now()))
client.loop_stop() #stop the loop
