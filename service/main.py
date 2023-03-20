from flask import Flask, Response, jsonify, request, json
from flask_cors import CORS

import paho.mqtt.client as mqtt
import time

server = Flask(__name__)
CORS(server, resources=r'/*')

client = mqtt.Client(transport='websockets')
#client.connect("test.mosquitto.org", 8081, 60)
#client.tls_set()
client.connect("localhost", 1884, 60)

@server.route("/")
def hello():
	return "Hello Flask"

@server.route("/publish", methods=['GET'])
def publish():
	mqttpayload = {'Message' : 'Test Message'}
	client.publish("msg/info", json.dumps(mqttpayload))
	resp = { 'Status': True }
	response = jsonify(resp)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

if __name__ == "__main__":
	CORS(server)
	server.run(host='0.0.0.0', port=5000)