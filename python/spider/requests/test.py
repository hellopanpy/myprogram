#--*--coding:utf8--*--

import requests
import json


url = "http://www.baidu.com"
r = requests.get(url)

# 指定编码utf-8，避免中文乱码
r.encoding = 'utf-8'
print r.text
print r.cookies

## GET请求
payload = {'key1': 'value1', 'key2': 'value2'}
headers = {'content-type': 'application/json'}
r = requests.get("http://httpbin.org/get", params=payload, headers=headers)
print r.url

## POST请求
url = 'http://httpbin.org/post'
payload = {'some': 'data'}
r = requests.post(url, data=json.dumps(payload))
print r.text