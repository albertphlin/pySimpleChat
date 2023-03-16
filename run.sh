#!/bin/bash
docker run -it -v "/home/linalbert/SW/pyChat/service/:/usr/pyChat/" -v "/home/linalbert/SW/pyChat/static/mosquitto/:/mosquitto/" --name pyChat -p 5000:5000 -p 1883:1883 -d pychat