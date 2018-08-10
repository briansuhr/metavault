#!/bin/bash

# Source this script via "source vagrant_setup.sh". Do not execute as "./vagrant_setup.sh". 

# Update system files
yes | sudo apt update
yes | sudo apt upgrade

# Set up Python
yes | sudo apt install python3-pip
yes | sudo apt install --upgrade pip

# Install py3exiv2 dependencies
yes | sudo apt install libboost-all-dev
yes | sudo apt install exiv2
yes | sudo apt install libexiv2-dev
yes | sudo apt install g++

# Install python3-exiv2
yes | sudo pip3 install py3exiv2

# Install xmltodict
yes | sudo pip3 install xmltodict
