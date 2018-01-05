import time, datetime
import json
import paho.mqtt.client as mqtt
import threading

clientID = "RPI_1"
topic = "parking/slotactivity"
topic2 = "parking/gate"
broker_address="iot.eclipse.org"

choices =  {'A1':("B1F1W11","B1","F1","W1","1"),
            'A2':("B1F1W11","B1","F1","W1","2"),
            'B1':("B1F1W11","B1","F1","W1","3"),
            'B2':("B1F1W11","B1","F1","W1","4"),
            'C1':("B1F1W11","B1","F1","W1","5"),
            'C2':("B1F1W11","B1","F1","W2","1"),
            'D1':("B1F1W11","B1","F1","W3","2"),
            'D2':("B1F1W11","B1","F1","W4","3"),
            'E1':("B1F1W11","B1","F1","W5","4"),
            'E2':("B1F1W11","B1","F1","W6","5")
           }


class SlotUpdate(threading.Thread):
    
    def __init__(self,data):
        threading.Thread.__init__(self)
        self.Data = data
        
    def run(self):
        print "SlotUpdate Class"
        print self.Data
        
        print("creating new instance")
        self.client = mqtt.Client(clientID) #create new instance
         
        print("connecting to broker")
        self.client.connect(broker_address) #connect to broker
        
        self.key = self.Data[0]+self.Data[1]
        print self.key
        self.status = self.Data[2]
        (self.SlotID,self.BID,self.FID,self.WID,self.SID) =  choices.get(self.key,('','','','',''))
        self.TS = str(datetime.datetime.now())    
        
        self.client.loop_start() #start the loop
        self.publishSlotChanges()
        self.client.loop_stop() #stop the loop
        
    def publishSlotChanges(self):
        self.send_msg = {
            "Slot_id" : self.SlotID,
            "Building": self.BID,
            "Floor": self.FID,
            "Wing": self.WID,
            "Slot": self.SID,
            "Status" : self.status,
            "Time" : self.TS
        }
        self.msg = json.dumps(self.send_msg)
        self.client.publish(topic,self.msg)
        print "Msg published : ",self.msg
