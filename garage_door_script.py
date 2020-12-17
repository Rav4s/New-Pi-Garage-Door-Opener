# Python Script To Control Garage Door

# Load libraries
import RPi.GPIO as GPIO #Import RPi GPIO library
import time #Import time
from flask import Flask, make_response, request, render_template, redirect, url_for #Import flask web server and additional components
app = Flask(__name__)

# Set up the GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
PIN_TRIG = 40
PIN_ECHO = 38
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.output(7, True)
GPIO.output(11, True)

#A variable
correct_login = 0

# Route for the main page
@app.route('/')
def index():
    GPIO.setup(PIN_TRIG, GPIO.OUT) #Setup the gpio trigger pin as input
    GPIO.setup(PIN_ECHO, GPIO.IN) #Setup the gpio echo pin as output
    time.sleep(2) #Wait for 2 seconds for sensor to settle
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
    if distance >= 80: #Check if the distance is less than 80cm (This will depend on the garage)
        return 'The garage is closed.'
    else:
        return 'The garage is open.'

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            correct_login = 1
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

# Route for the login page
@app.route('/set-cookie')
def cookie():
    if correct_login = 1:
        print("hello")
        resp = make_response()
        resp.set_cookie('logged_in', 'yes')
        return resp
    else:
        return 'Not logged in.'

if __name__ == '__main__':
    app.run(host='0.0.0.0') #Run the webserver
