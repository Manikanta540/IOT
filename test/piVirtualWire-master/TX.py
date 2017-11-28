import piVirtualWire as piVirtualWire
import time
import pigpio

pi = pigpio.pi()
tx = piVirtualWire.tx(pi, 18, 1000) # Set pigpio instance, TX module GPIO pin and baud rate
while 1:
    k=tx.put("42111")
    print k
    tx.waitForReady()
    
    tx.put("hhsaERWERW")
    tx.waitForReady()

tx.cancel()
pi.stop()