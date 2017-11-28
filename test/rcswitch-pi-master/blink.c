/*
 * blink.c:
 *      blinks the first LED
 *      Gordon Henderson, projects@drogon.net
 */
 
#include <stdio.h>
#include <wiringPi.h>
 
int main (void)
{
  printf ("Raspberry Pi blink\n") ;
 
  if (wiringPiSetupGpio() == -1)
    return 1 ;
 
  pinMode (18, INPUT) ;         // aka BCM_GPIO pin 17
  int data ;
  for (;;)
  {
	 data =digitalRead (18) ;
    if(data==1)
    	printf("   we are recieving the data");       // On
    //delay (1) ;               // mS
    //digitalWrite (0, 0) ;       // Off
    //delay (500) ;
  }
  return 0 ;
}