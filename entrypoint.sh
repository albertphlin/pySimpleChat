#!/bin/bash
mosquitto -c /etc/mosquitto/mosquitto.conf &
/bin/python3 /usr/local/pyChat/main.py