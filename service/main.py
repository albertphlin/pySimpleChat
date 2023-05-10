from flask import Flask, Response, jsonify, request, json
from flask_cors import CORS

import paho.mqtt.client as mqtt
import Control.DataHandler as DataHandler
import Model.CHATSQL as ModelCHATSQL
import time
import datetime

VERSION = "0.0.3"
server = Flask(__name__)
CORS(server, resources=r'/*')
datahandler = DataHandler.DataHandler()

# 將會用到的model SQL產生實例
CHATSQL = ModelCHATSQL.SQL

# 透過module mqtt產生instance並設定為websockets模式
client = mqtt.Client(transport='websockets')
# 用mqtt instance連線到mosquitto的port 8083
client.connect("10.0.0.19", 8083)
# 讓mqtt連線持續運轉
client.loop_start()

# Decorator(修飾): 將函式引入，至物件內未定義的函式
@server.route("/")
def hello():
	return "Hello Flask"

@server.route("/publish", methods=['POST'])
def publish():
	# 將payload轉型成json
	req_data = request.get_json(force=True)
	# 用key索引來取值
	# 預期payload: {"topic": "", "user": "", "message": ""}
	user = req_data['user']
	message = req_data['message']
	topic = req_data['topic']
	time = str(datetime.datetime.now())
	print(f"[publish] payload: {req_data}")
	# 宣告並定義要送mqtt的payload
	mqttpayload = { 
		'User': user,
		'Message': message,
		'Time': time
	}
	# mqtt publish
	client.publish(topic, json.dumps(mqttpayload, ensure_ascii=False))
	# 將這筆資料加入資料庫
	datahandler.AddMessage(Topic=topic, User=user, Message=message, IP=request.remote_addr, tDateTime=time)
	# 宣告webapi response payload
	resp = { 'Status': True }
	# 將webapi response payload 轉成json
	response = jsonify(resp)
	# 將webapi response 加上header
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@server.route("/querymessages", methods=['POST'])
def querymessages():
	# 將payload轉型成json
	req_data = request.get_json(force=True)
	# 用key索引來取值
	# 預期payload: {"querytype": "TopN", "topic": "", "n": "", "time"=""}
	querytype = req_data['querytype']
	print(f"[querymessages] payload: {req_data}")
	if "TopN" in querytype:
		topic = req_data['topic']
		n = req_data['n']
		time = req_data['time']
		# 去資料庫撈mqtt topic是topic、時間早於time、最後n筆
		messages = datahandler.QueryTopNMessagesByTime(Topic=topic, N=n, Time=time)
		# 宣告並定義撈回來的資料的json payload，將list中的MessageData物件轉型成json
		messagespayload = json.dumps({ 'messages': [ob.to_dict() for ob in messages]}, sort_keys=True, ensure_ascii=False)
		resp = { 'Status': True, 'rows': len(messages), 'messages': messagespayload }
		print(f"[querymessages] resp: {resp}")
	else:
		resp = { 'Status': False }
	# 將webapi response payload 轉成json
	response = jsonify(resp)
	# 將webapi response 加上header
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

if __name__ == "__main__":
	print(VERSION)
	CORS(server)
	server.run(host='0.0.0.0', port=5000)