from pprint import pprint

import requests
from urllib.parse import urlencode
import os
import json
import time

APP_ID = 6119625
API_VERSION = '5.67'
URL = 'https://oauth.vk.com/authorize'
TOKEN_FILE = 'token.txt'  # Токен должен быть записан в этот файл

user_id = 5030613 # ID юзера, за которым шпионим


def split_list(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def sleep_before_request(delay=0.4):
    """
    Добавляем задержку перед запросом к API и рисуем точку
    :param delay: 
    :return: 
    """
    time.sleep(delay)
    print('.')


def get_friends_ids(params, user_id=None):
    """
    Получаем список id друзей
    :param dict params: Параметры для запроса к API
    :param int user_id: ID пользователя, друзей которого хотим получить
    :return: 
    """
    sleep_before_request()
    req_params = dict(params)
    if user_id is not None and isinstance(user_id, int):
        req_params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/friends.get', req_params)
    json_res = response.json()
    if 'response' in json_res and 'items' in json_res['response']:
        return json_res['response']['items']
    return False


def get_user_groups(params, user_id=None):
    """
    Получаем список групп пользователя
    :param dict params: Параметры для запроса к API
    :param int user_id: ID пользователя
    :return: Список ID групп пользователя
    :rtype: list
    """
    sleep_before_request()
    req_params = dict(params)
    if user_id is not None and isinstance(user_id, int):
        req_params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/groups.get', req_params)
    json_res = response.json()
    if 'response' in json_res and 'items' in json_res['response']:
        return json_res['response']['items']
    return False


def check_users_is_member(params, group_id, user_ids):
    """
    Проверяем являются юзеры из user_ids членами группы group_id
    :param dict params: Параметры для запроса к API
    :param int group_id: ID группы для проверки
    :param list user_ids: Список ID юзеров для проверки
    :return: возвращает список словарей, в  которых есть флаг о том, является ли юзер членом группы
    :rtype: list
    """
    sleep_before_request()
    req_params = dict(params)
    req_params['group_id'] = group_id
    req_params['user_ids'] = ','.join(map(str, user_ids))
    response = requests.post('https://api.vk.com/method/groups.isMember', req_params)
    try:
        json_res = response.json()
        return json_res['response']
    except:
        print('В ответе, полученном от API, содержится не JSON строка')
        print(response.text)
        raise


def get_res_group_ids(user_group_ids, user_friend_ids):
    """
    Получаем список ID групп, в которых состоит пользователь, но не состоит никто из его друзей:
    :param user_group_ids: 
    :param user_friend_ids: 
    :rtype: list
    """
    # Полученный список друзей разбиваем на списке по 500 юзеров, т.к. метод groups.isMember может принять максимум 500 user_id
    splitted_list = split_list(user_friend_ids, 500)

    res_groups_ids = []

    for group_id in user_group_ids:
        print('Проверяем группу с ID {}'.format(group_id))

        for user_ids in splitted_list:
            # Получаем результат по каждому id из списка user_ids
            result = check_users_is_member(params, group_id, user_ids)
            # В полученном результате оставляем только тех, кто является участником группы group_id, если таковые имеются
            filtered_result = list(filter(lambda u: u['member'], result))
            # Если найдены друзья, которые состоят в той же группе, что и проверяемый юзер
            if len(filtered_result):
                add_group = False  # Помечаем, что эта группа нам не интересна
                # остальные user_ids для этой группы можно не проверять и прерываем цикл
                break
            # Иначе
            add_group = True

        if add_group:
            res_groups_ids.append(group_id)
    return res_groups_ids


def get_groups(params, group_ids):
    """
    :param dict params: Параметры для запроса к API
    :param list group_ids: Список id групп 
    :return: Получаем информацию для групп
    :rtype: list
    """
    sleep_before_request()
    req_params = dict(params)
    req_params['group_ids'] = ','.join(map(str, group_ids))
    req_params['fields'] = 'members_count'

    response = requests.get('https://api.vk.com/method/groups.getById', req_params)
    json_res = response.json()
    if 'response' in json_res:
        return json_res['response']
    return False


def save_groups(groups, filename='groups.json'):
    """
    Сохранаяем группы в filename с требуемыми полями gid, name, members_count
    :param list groups: список словарей с информацией о группах 
    :param str filename: имя файла для сохранения результата
    :rtype: None
    """
    res_groups = []
    for group in groups:
        res_groups.append({
            'gid': group['id'],
            'name': group['name'],
            'members_count': group['members_count']
        })
    with open(filename, 'w', encoding='utf8') as outfile:
        json.dump(res_groups, outfile, ensure_ascii=False)
        print('Groups were saved in {}'.format(filename))


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
    exit()
else:
    with open(TOKEN_FILE) as f:
        access_token = f.read()
        params = {
            'access_token': access_token,
            'v': API_VERSION
        }
        user_friend_ids = get_friends_ids(params, user_id)
        user_group_ids = get_user_groups(params, user_id)
        res_groups_ids = get_res_group_ids(user_group_ids, user_friend_ids)

print('ID групп, в которых состоит пользователь, но не состоит никто из его друзей:')
if res_groups_ids:
    print(res_groups_ids)
    groups = get_groups(params, res_groups_ids)
    save_groups(groups)
else:
    print('Во всех группах пользователя, состоит хотя бы один из его друзей')
