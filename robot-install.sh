#!/usr/bin/env bash

set -e

read -n1 -p "Press any key to confirm in virtual environment..."
echo
pip install robotpy-installer
robotpy-installer download-robotpy
robotpy-installer download-opkg python37-robotpy-cscore python37-robotpy-ctre
robotpy-installer download-pip coloredlogs
read -n1 -p "Press any key once connected to the robot..."
echo
robotpy-installer install-robotpy
robotpy-installer install-opkg python37-robotpy-cscore python37-robotpy-ctre
robotpy-installer install-pip coloredlogs
