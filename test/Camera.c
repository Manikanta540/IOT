#include <signal.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>

#define TRIG 23
#define ECHO 18

static pid_t pid = 0;
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
void startVideo(char *filename, char *options) {
    if ((pid = fork()) == 0) {
        char **cmd;

        // count tokens in options string
        int count = 0;
        char *copy;
        copy = strdup(options);
        if (strtok(copy, " \t") != NULL) {
            count = 1;
            while (strtok(NULL, " \t") != NULL)
                count++;
        }

        cmd = malloc((count + 8) * sizeof(char **));
        free(copy);

        // if any tokens in options, 
        // copy them to cmd starting at positon[1]
        if (count) {
            int i;
            copy = strdup(options);
            cmd[1] = strtok(copy, " \t");
            for (i = 2; i <= count; i++)
                cmd[i] = strtok(NULL, " \t");
        }

        // add default options
        cmd[0] = "raspistill"; // executable name
        cmd[count + 1] = "-o"; // output file specifer
        cmd[count + 2] = filename;
        cmd[count + 3] = (char *)0;
        //cmd[count + 1] = "-n"; // no preview
        //cmd[count + 1] = "-t"; // default time (overridden by -s)
                               // but needed for clean exit
        //cmd[count + 2] = "10"; // 10 millisecond (minimum) time for -t
        //cmd[count + 3] = "-s"; // enable USR1 signal to stop recording
        //cmd[count + 4] = "-o"; // output file specifer
        //cmd[count + 5] = filename;
        //cmd[count + 6] = (char *)0; // terminator
        execv("/usr/bin/raspistill", cmd);
    }
}

void stopVideo(void) {
    if (pid) {
		
        kill(pid, 10); // seems to stop with two signals separated
                       // by 1 second if started with -t 10 parameter
        sleep(1);
        kill(pid, 10);
    }
}

int main(int argc, char **argv) {
	
	
	int sum,i;
        setup();
			while(1)
			{	sum=0;
				for(i=0;i<10;i++)
					{	sum=sum+getCM();
						delay(50);
					
					}
					sum=sum/10;
					if(sum<200)
					{
						
							printf("Recording video for 5 secs...");
							// example options give an upside-down black and white video
							startVideo("temp.jpeg", "-cfx 128:128 -rot 180"); 
							fflush(stdout);
							sleep(5);
							stopVideo();
							printf("\nVideo stopped - exiting in 2 secs.\n");
							sleep(2);
													
					}
				printf("Distance: %dcm\n", sum);
				delay(500);
				delay(2000);
			}
	
	
    
    return 0;
}
