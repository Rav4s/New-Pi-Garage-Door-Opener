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
    return render_template('index.html')

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
    app.run(host='0.0.0.0') #Run the webserver
