#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>


#define TRIG 23
#define ECHO 18

void setup() 
{
        wiringPiSetupGpio();
        pinMode(TRIG, OUTPUT);
        pinMode(ECHO, INPUT);

        //TRIG pin must start LOW
        digitalWrite(TRIG, LOW);
        delay(30);
}

int getCM() 
{
        //Send trig pulse
        digitalWrite(TRIG, HIGH);
        delayMicroseconds(20);
        digitalWrite(TRIG, LOW);

        //Wait for echo start
        while(digitalRead(ECHO) == LOW);

        //Wait for echo end
        long startTime = micros();
        while(digitalRead(ECHO) == HIGH);
        long travelTime = micros() - startTime;

        //Get distance in cm
        int distance = travelTime / 58;

        return distance;
}

int main(void) 
{int sum,i;
        setup();
			while(1)
			{	sum=0;
				for(i=0;i<10;i++)
					{	sum=sum+getCM();
						delay(50);
					
					}
				printf("Distance: %dcm\n", sum/10);
			delay(500);
}
        return 0;
}
