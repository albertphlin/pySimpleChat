# FROM arm64v8/ubuntu:20.04
FROM ubuntu:20.04

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG en_US.UTF-8

RUN	apt-get update -y
RUN apt-get install -y wget git gcc curl adduser libfontconfig1 python3-dev python3-pip mosquitto
RUN python3 -m pip install pip --upgrade

#RUN mkdir "/temp/" && \
#	cd "/temp/" && \
#	wget http://s3.amazonaws.com/influxdb/influxdb_latest_amd64.deb && \
#	dpkg -i influxdb_latest_amd64.deb && \
#	service influxdb start && \
#	wget https://dl.influxdata.com/influxdb/releases/influxdb2-client-2.6.1-linux-amd64.tar.gz && \
#	tar xvzf path/to/influxdb2-client-2.6.1-linux-amd64.tar.gz && \
#	cp influxdb2-client-2.6.1-linux-amd64/influx /usr/local/bin/

WORKDIR /usr/local/pyChat
COPY ./service/. .
COPY ./static/mosquitto/config/mosquitto.conf /etc/mosquitto/
CMD mkdir /mosquitto/data && \
	mkdir /mosquitto/log
#COPY ./static/mosquitto/data /mosquitto/
#COPY ./static/mosquitto/log /mosquitto/
COPY ./requirements.txt .
COPY ./entrypoint.sh .

RUN python3 -m pip install -r ./requirements.txt

CMD ["./entrypoint.sh"]