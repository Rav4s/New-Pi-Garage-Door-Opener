# Python Script To Control Garage Door

# Load libraries
import RPi.GPIO as GPIO #Import RPi GPIO library
import time
import os
from flask import Flask, make_response, request, render_template, redirect, url_for, send_from_directory #Import flask web server and additional components
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

#Variables
correct_login = 0

# Route for the main page
@app.route('/')
def index():
    logged_in = request.cookies.get('logged_in')
    if logged_in == "yes":
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
        if distance >= 80: #Check if the distance is less than 80cm (This will depend on the garage)
            message = 'The garage is closed.'
            OpenOrClose = 'Open'
        else:
            message = 'The garage is open.'
            OpenOrClose = 'Close'
    else:
        return redirect(url_for('login'))
    return render_template('index.html', message=message, distance=distance, OpenOrClose=OpenOrClose)

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            global correct_login
            correct_login = 1
            return redirect(url_for('cookie'))
    return render_template('login.html', error=error)

# Route for the login page
@app.route('/set-cookie')
def cookie():
    if correct_login == 1:
        resp = make_response(redirect('/'))
        resp.set_cookie('logged_in', 'yes')
        return resp
    else:
        return 'Not logged in.'

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1235) #Run the webserver
