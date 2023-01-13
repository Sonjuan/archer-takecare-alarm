import sys
import os
import requests
import time
import json
import hashlib
import hmac
import base64

import schedule
import time
import datetime

# POST https://sens.apigw.ntruss.com/sms/v2/services/{serviceId}/messages
# Content-Type: application/json; charset=utf-8
# x-ncp-apigw-timestamp: {Timestamp}
# x-ncp-iam-access-key: {Sub Account Access Key}
# x-ncp-apigw-signature-v2: {API Gateway Signature}

dict = {}
with open(".env", "r") as fp :
    envs = [f.rstrip() for f in fp]

for env in envs :
    x, y = env.split("=")
    dict.update([(x, y)])   

secret_key = dict["secret_key"]
service_id = dict["service_id"]
to_num     = dict["to_num"]

dict["from_nums"] = [to_num]
with open(".numbers", "r") as fp :
    nums = [f.rstrip() for f in fp]

for num in nums :
    dict["from_nums"].append(num)

uri = f'/sms/v2/services/{service_id}/messages'
url = f'https://sens.apigw.ntruss.com{uri}'

def	make_signature():
    timestamp = str(int(time.time() * 1000))
	_secret_key = bytes(secret_key, 'UTF-8')
	method = "POST"
	message = method + " " + uri + "\n" + timestamp + "\n" + access_key
	message = bytes(message, 'UTF-8')
	signingKey = base64.b64encode(hmac.new(_secret_key, message, digestmod=hashlib.sha256).digest())
	return signingKey

def send_message() :
    header = {
        "Content-Type"             : "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp"    : timestamp,
        "x-ncp-iam-access-key"     : access_key,
        "x-ncp-apigw-signature-v2" : make_signature()
    }

    data = {
        'type':'SMS',
        'countryCode':'82',
        'from': to_num,
        'content':'아 잠시만요 월드보스 출현 7분전입니다 준비하세요ㅎㅎ',
        'messages':[]
    }
    for num in dict["from_nums"] :
        data['messages'].append({"to" : num})

    response = requests.post(url, headers=header, data=json.dumps(data))
    print(response.text)

def test_msg() :
    now = datetime.datetime.now()
    
    print(now)
    send_message()
    print("sending clear ======")
    return schedule.CancelJob

schedule.every().day.at("19:53").do(test_msg)

while True :
    schedule.run_pending()
    time.sleep(1)


