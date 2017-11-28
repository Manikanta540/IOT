import time
import pigpio 

LED_PIN = 18

#connect to pigpiod daemon
pi = pigpio.pi()

# setup pin as an output
pi.set_mode(LED_PIN, pigpio.OUTPUT)
 
while True:
  # enable LED
  pi.write(LED_PIN, 1)
 
  # wait 1 second
  time.sleep(1)  
 
  # disable LED
  pi.write(LED_PIN, 0)
  time.sleep(1)
  
#cleanup
pi.set_mode(LED_PIN, pigpio.INPUT)
#disconnect
pi.stop()