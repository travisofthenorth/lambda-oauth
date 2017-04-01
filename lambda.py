from __future__ import print_function
from hashlib import sha1
from time import time

import json
import os
import redis
import requests

AUTHORIZE_URL = os.environ['AUTHORIZE_URL']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']

SESSION_REDIS = redis.StrictRedis(
    host= os.environ['REDIS_HOST'],
    port=14072,
    password=os.environ['REDIS_PASSWORD']
)


# Taken from werkzeug
def generate_key(salt=None):
    if salt is None:
        salt = repr(salt).encode('ascii')
    return sha1(b''.join([
        salt,
        str(time()).encode('ascii'),
        os.urandom(30)
    ])).hexdigest()


def authorize(code):
    data = {
        'code': code,
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(AUTHORIZE_URL, data=data)
    return response.json()


def lambda_handler(event, context):
    auth_data = authorize(event['code'])
    session_id = generate_key()

    SESSION_REDIS.set(session_id, auth_data)
    return { 'session_id': session_id }
