from __future__ import print_function

import json
import os
import redis
import requests

AUTHORIZE_URL = os.environ['AUTHORIZE_URL']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']

r = redis.StrictRedis(host='redis-14072.c13.us-east-1-3.ec2.cloud.redislabs.com', port=14072, password=os.environ['REDIS_PASSWORD'])

def lambda_handler(event, context):
    data = {
        'code': event['code'],
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(AUTHORIZE_URL, data=data)
    return response.json()
