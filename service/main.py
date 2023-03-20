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

@server.route("/publish", methods=['POST'])
def publish():
	# 將payload轉型成json
	req_data = request.get_json(force=True)
	# 用key索引來取值
	user = req_data['user']
	message = req_data['message']
	# 宣告並定義回傳payload
	mqttpayload = { 
		'User': user,
		'Message': message
	}
	client.publish("msg/info", json.dumps(mqttpayload, ensure_ascii=False))
	resp = { 'Status': True }
	response = jsonify(resp)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

if __name__ == "__main__":
	CORS(server)
	server.run(host='0.0.0.0', port=5000)