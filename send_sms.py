import sys
import os
import requests
import time
import json
import hashlib
import hmac
import base64

# import schedule
# import time
# import datetime


# POST https://sens.apigw.ntruss.com/sms/v2/services/{serviceId}/messages
# Content-Type: application/json; charset=utf-8
# x-ncp-apigw-timestamp: {Timestamp}
# x-ncp-iam-access-key: {Sub Account Access Key}
# x-ncp-apigw-signature-v2: {API Gateway Signature}

timestamp = int(time.time() * 1000)
timestamp = str(timestamp)

access_key = '{access_key}'				            # access key id (from portal or Sub Account)
uri = '/sms/v2/services/{service_id}/messages'
url = f'https://sens.apigw.ntruss.com{uri}'

def	make_signature():
	secret_key = bytes('{secret_key}', 'UTF-8')
	method = "POST"
	message = method + " " + uri + "\n" + timestamp + "\n" + access_key
	message = bytes(message, 'UTF-8')
	signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
	return signingKey

signature = make_signature()

header = {
    "Content-Type"             : "application/json; charset=utf-8",
    "x-ncp-apigw-timestamp"    : timestamp,
    "x-ncp-iam-access-key"     : access_key,
    "x-ncp-apigw-signature-v2" : signature
}

data = {
    'type':'SMS',
    'countryCode':'82',
    'from': '{phone_number}',
    'content':'월드보스 출현 10분전 준비하세요',
    'messages':[
        {
            # other's phone number
            'to': '123456789'
        }
    ]
}

response = requests.post(url, headers=header, data=json.dumps(data))
print(response.text)