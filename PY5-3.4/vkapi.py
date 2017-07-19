from pprint import pprint

import requests
from urllib.parse import urlencode
import os

import time

APP_ID = 6119625
API_VERSION = '5.67'
URL = 'https://oauth.vk.com/authorize'
TOKEN_FILE = 'token.txt'  # Токен должен быть записан в этот файл


def get_friends_ids(params, user_id=None):
    if user_id is not None and isinstance(user_id, int):
        params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/friends.get', params)
    json_res = response.json()
    if 'response' in json_res and 'items' in json_res['response']:
        return json_res['response']['items']
    return False


def find_common_friend(friends_ids, common_friends_dict=None):
    if common_friends_dict is None:
        common_friends_dict = {}
    friends_set = set(friends_ids)
    for user_id in friends_ids:
        friend_friends_ids = get_friends_ids(params, user_id)
        if friend_friends_ids:
            common_friends_dict[user_id] = list(friends_set.intersection(friend_friends_ids))
    return common_friends_dict


request_params = {
    'client_id': APP_ID,
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'display': 'mobile',
    'scope': 'friends',
    'response_type': 'token',
    'v': API_VERSION
}

if not os.path.exists(TOKEN_FILE):
    print('?'.join((URL, urlencode(request_params))))
else:
    with open(TOKEN_FILE) as f:
        access_token = f.read()
        params = {
            'access_token': access_token,
            'v': API_VERSION
        }
        friends_ids = get_friends_ids(params)
        common_friends = find_common_friend(friends_ids)

pprint(common_friends)
