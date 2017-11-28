#include "RCSwitch.h"
#include <stdlib.h>
#include <stdio.h>
 
int main(int argc, char *argv[]) {
 
    // This pin is not the first pin on the RPi GPIO header!
    // Consult https://projects.drogon.net/raspberry-pi/wiringpi/pins/
    // for more information.
    int PIN = 0;
 
    // Parse the firt parameter to this command as an integer
    int code = atoi(argv[1]);
 
    if (wiringPiSetup () == -1) return 1;
    printf("sending code[%i]\n", code);
    RCSwitch mySwitch = RCSwitch();
    mySwitch.enableTransmit(PIN);
 
    mySwitch.send(code, 24);
 
    return 0;
 
}
