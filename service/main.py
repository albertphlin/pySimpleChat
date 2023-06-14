from flask import Flask, Response, jsonify, request, json, url_for, redirect,  render_template, send_from_directory
from flask_cors import CORS

import paho.mqtt.client as mqtt
import Control.DataHandler as DataHandler
import Model.CHATSQL as ModelCHATSQL
import time
import datetime

import os
import pathlib
from werkzeug.utils import secure_filename

VERSION = "0.0.3"
server = Flask(__name__)
CORS(server, resources=r'/*')
datahandler = DataHandler.DataHandler()

# 將會用到的model SQL產生實例
CHATSQL = ModelCHATSQL.SQL

# 透過module mqtt產生instance並設定為websockets模式
client = mqtt.Client(transport='websockets')
# 用mqtt instance連線到mosquitto的port 8083
client.connect("localhost", 8083)
# 讓mqtt連線持續運轉
client.loop_start()

# 取得目前檔案所在的資料夾
SRC_PATH =  pathlib.Path(__file__).parent.parent.absolute()
UPLOAD_FOLDER = os.path.join(SRC_PATH, 'static', 'uploads')
# 設定允許的副檔名
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx'])

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
		#print(f"[querymessages] resp: {resp}")
	else:
		resp = { 'Status': False }
	# 將webapi response payload 轉成json
	response = jsonify(resp)
	# 將webapi response 加上header
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response


# 確認上傳檔案是否為允許的副檔名function
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@server.route("/filesupload", methods=['POST'])
def filesupload():
	file = request.files['files']
	user = request.form['user']
	topic = request.form['topic']
	print(f"[filesupload] payload: {file}")
	#Content-Disposition: form-data; name="files"; filename="logo.png"
	#Content-Type: image/png
	#if file.filename != '':
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(UPLOAD_FOLDER, filename))
		datahandler.AddFile(User=user, Topic=topic, FileName=filename)
	# 宣告webapi response payload
	resp = { 'Status': True }
	# 將webapi response payload 轉成json
	response = jsonify(resp)
	# 將webapi response 加上header
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response


@server.route("/filesquery", methods=['POST'])
def filesquery():
	req_data = request.get_json(force=True)
	topic = req_data['topic']
	fileList = datahandler.QueryFilesByTopic(Topic=topic)
	filespayload = json.dumps({ 'files': [ob.to_dict() for ob in fileList]}, sort_keys=True, ensure_ascii=False)
	# 宣告webapi response payload
	resp = { 'Status': True, 'files': filespayload }
	# 將webapi response payload 轉成json
	response = jsonify(resp)
	# 將webapi response 加上header
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@server.route("/filesdownload", methods=['POST'])
def filesdownload():
	req_data = request.get_json(force=True)
	file = req_data['filename']
	#server.static_folder = '../static/uploads'
	return send_from_directory(directory=UPLOAD_FOLDER, filename=file, as_attachment=True)
	#return send_from_directory(server.static_folder, filename=file, as_attachment=True)


if __name__ == "__main__":
	print(VERSION)
	CORS(server)
	server.run(host='0.0.0.0', port=5000)