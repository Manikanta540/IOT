import piVirtualWire as piVirtualWire
import time
import pigpio
msg = 1
pi = pigpio.pi()
rx = piVirtualWire.rx(pi, 18, 1000) # Set pigpio instance, TX module GPIO pin and baud rate
print ('hello')
while True:
                t=rx.ready()
                print t
		while t:
			k=rx.get()
			msg = 0
			#s=b'hello'.decode(encoding)
			
			for i in k:
                            print (i)
                            print chr(i)
                            i=i-48
                            msg = msg*10 + i;    
                        print (msg)

		time.sleep(0.05)

rx.cancel()
pi.stop()