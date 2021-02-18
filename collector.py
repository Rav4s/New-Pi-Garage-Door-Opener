# Load libraries
import RPi.GPIO as GPIO #Import RPi GPIO library
import time
from time import localtime, strftime
import os

# Set up the GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
PIN_TRIG = 40
PIN_ECHO = 38

def collect_data():
    GPIO.setup(PIN_TRIG, GPIO.OUT) #Setup the gpio trigger pin as input
    GPIO.setup(PIN_ECHO, GPIO.IN) #Setup the gpio echo pin as output
    time.sleep(0.5) #Wait for 0.5 seconds for sensor to settle
    GPIO.output(PIN_TRIG, GPIO.LOW) #Set trigger to low
    GPIO.output(PIN_TRIG, GPIO.HIGH) #Set trigger to high
    time.sleep(0.00001) #Wait for 0.1 milliseconds before setting to low again
    GPIO.output(PIN_TRIG, GPIO.LOW) #Set trigger to low again
    while GPIO.input(PIN_ECHO)==0:
        pulse_start_time = time.time() #Set the start time of when the waves are emitted by the sensor
    while GPIO.input(PIN_ECHO)==1:
        pulse_end_time = time.time() #Record the time the waves traveled back to the sensor
        pulse_duration = pulse_end_time - pulse_start_time #Calculate how long it took for the round trip of the waves
        distance = round(pulse_duration * 17150, 2) #Convert the time it took to centimeters and round to 2 decimals
    date_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    if distance <= 80: #Check if the distance is greater than 80cm (This will depend on the garage)
        distance = str(distance)
        message = 'At ' + date_time + ', the garage was opened at a distance of ' + distance + ' centimeters!'
        command = '../telegram-bot-bash/bin/send_broadcast.sh --doit' + ' "' + message + '"' + '> /dev/null'
        os.system(command)

if __name__ == '__main__':
    while True:
        try:
            collect_data()
        except:
            print("quitting")
            quit()
        time.sleep(5)