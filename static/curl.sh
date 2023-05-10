#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d '{"user" : "Albert", "message" : "你好", "topic": "msg/info"}' "localhost:5000/publish"
curl -X POST -H "Content-Type: application/json" -d '{"querytype": "TopN", "topic": "msg/info", "time": "2023/03/31 00:00:00", "n": "50"}' "localhost:5000/querymessages"