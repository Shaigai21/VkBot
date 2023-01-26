#!/usr/bin/python3
import http
import http.client
import json
import urllib
import urllib.parse
import sys
import time


apiVersion = '5.131'

apiConnection = http.client.HTTPSConnection('api.vk.com', http.client.HTTPS_PORT)

config = None

with open(sys.argv[1]) as f:
    config = json.load(f)

token = str(config['token'])

def sendAPIRequest(connection, token, method, **params):
    paramsString = ''

    for param in params.items():
        if param[1] is not None:
            paramsString += urllib.parse.quote(str(param[0]))
            paramsString += '='
            paramsString += urllib.parse.quote(str(param[1]))
            paramsString += '&'

    url = f'/method/{method}?{paramsString}access_token={token}&v={apiVersion}'
    print(url)
    connection.request('GET', url)
    resp = connection.getresponse().read()
    print(resp)
    res = json.loads(resp)
    print(res)
    return res


#botGroups = sendAPIRequest(apiConnection, token, 'groups.get')['response']["items"]


for group in config['groups']:
    #if group not in botGroups:
    #    sendAPIRequest(apiConnection, token, 'groups.join', group_id=group)
    for message in config['messages']:
        time.sleep(20)
        sendAPIRequest(apiConnection, token, 'wall.post', owner_id=(-int(group)), message=message['text'], attachments=message['attachments'])
