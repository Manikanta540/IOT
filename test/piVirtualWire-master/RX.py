import piVirtualWire as piVirtualWire
import time
import pigpio

msg = 1
pi = pigpio.pi()
rx = piVirtualWire.rx(pi, 18, 1000) # Set pigpio instance, TX module GPIO pin and baud rate
tx = piVirtualWire.tx(pi, 23, 1000) # Set pigpio instance, TX module GPIO pin and baud rate

def StartCommunication(k):
    Data="A"
    address=chr(k[0])
    Data=Data+address
    tx.put(Data)
    tx.waitForReady()
    print Data
    return 

print ('hello')
while True:
    t=rx.ready()
    #print(t)
    while t:
            k=rx.get()

            for i in k:
                print (i," ",chr(i))
            #rx.cancel()
            #rx.disable()
            StartCommunication(k)
            #rx.enable()
    time.sleep(0.05)



rx.cancel()
pi.stop()
