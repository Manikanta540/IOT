import time
import picamera
import paho.mqtt.client as mqtt

my_file = open('1.jpg', 'wb')
print "Picture 1"
camera = picamera.PiCamera()
camera.resolution = (800,600)
camera.start_preview()
time.sleep(2)
camera.capture(my_file)
print "Picture 2"
my_file.flush()
my_file.close()
camera.close() 

from PIL import Image
#import pytesseract
im =Image.open("image11.jpg")
#im.save("e.jpg",format="jpeg",quality=10)
bw = im.convert('L')
bw.save("e.jpg")
bw.save("e.jpg",format="jpeg",quality=40)
#text=pytesseract.image_to_string(im)

broker_address="iot.eclipse.org"

client = mqtt.Client("P1") #create new instance

print("connecting to broker")
client.connect(broker_address) #connect to broker

client.loop_start() #start the loop
print("Publishing message to topic","parking/entrance/camera")

#client.publish("house/main",payload=json.dumps(send_msg))
#time.sleep(4) # wait
fd = open("e.jpg",'rb')
print("Open Image")
fc = fd.read()
print("Read Image")
#bytearr = bytearray(fc)
client.publish("parking/entrance/camera",fc)
print("published")
client.loop_stop() #stop the loop
