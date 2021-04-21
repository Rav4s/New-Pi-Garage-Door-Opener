#!/bin/bash

echo "This script will install the Flask web server and allow you to control and monitor the state of your smart garage door opener."
sleep 0.5
read -r -p "Press y to acknowledge and continue running the script. [y/N] " response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    echo "Updating apt package data..."
    sudo apt-get update
    echo "Installing python3, rpi-gpio, and git..."
    sudo apt-get -y install python3 python3-dev python3-rpi.gpio git-all
    echo "Installing Flask..."
    pip3 install flask
    echo "Making directory..."
    mkdir garagedoor && cd garagedoor
    echo "Cloning repository..."
    git clone https://github.com/Rav4s/New-Pi-Garage-Door-Opener.git .
    echo "Copying systemd unit file..."
    sudo cp garage-door-controller.service /etc/systemd/system/garage-door-controller.service
    echo "Reloading systemd configuration..."
    sudo systemctl daemon-reload
    echo "Enabling and starting systemd service..."
    sudo systemctl enable --now garage-door-controller.service
    sleep 0.5
    echo "Successful install!"
    echo "Your web server is now accessible at localhost:1235"
else
    echo "Bye!"
    exit 1
fi

exit 0
