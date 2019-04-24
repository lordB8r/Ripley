#!/bin/bash

# sets up fresh pi for Ripley

sudo apt --yes update
sudo apt --yes upgrade
sudo apt --yes install \
    vim git tree \
    python-dev python-pip \
    python3-dev python3-pip python3-venv \
    wiringpi

mkdir petrockblog; cd petrockblog
git clone https://github.com/petrockblog/RPi-MCP23S17.git
cd RPi-MCP23S17
python3 -m venv venv
. venv/bin/activate
python3 setup.py install
