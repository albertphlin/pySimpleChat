#!/bin/bash
CODEBASE=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
docker run -it -v "$CODEBASE/service/:/usr/pyChat/" -v "$CODEBASE/static/mosquitto/:/mosquitto/" --name pyChat -p 5000:5000 -p 1883:1883 -p 1884:1884 -d pychat