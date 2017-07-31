import os
from pprint import pprint
from urllib.parse import urlencode, urljoin

import requests


class YaMetrikaBase:
    APP_ID = '83e073411b0f4b8b9528a2823140c224'
    APP_PASS = '23935641b4e84a86bacd0f722fd3afa9'
    TOKEN = None

    AUTHORIZE_URL = 'https://oauth.yandex.ru/authorize'

    AUTH_PARAMS = {
        'response_type': 'token',
        'client_id': APP_ID
    }

    def get_headers(self):
        return {
            'Authorization': 'OAuth {}'.format(self.TOKEN),
            'Content-Type': 'application/x-yametrika+json'
        }


class YaMetrikaAuth(YaMetrikaBase):
    def get_authorization_link(self):
        link = '?'.join([self.AUTHORIZE_URL, urlencode(self.AUTH_PARAMS)])
        print(link)


class YaMetrikaCounters(YaMetrikaAuth):
    MANAGMENT_URL = 'https://api-metrika.yandex.ru/management/v1/'

    def __init__(self, token=None):
        if token is not None:
            self.TOKEN = token
        elif os.path.exists('token.txt'):
            with open('token.txt') as f:
                self.TOKEN = f.read()

        if not self.TOKEN:
            print('Чтобы получить токен, перейдите по ссылке')
            self.get_authorization_link()

    def get_counters(self):
        headers = self.get_headers()
        response = requests.get(urljoin(self.MANAGMENT_URL, 'counters'), headers=headers)
        return response.json()


class YaMetrikaStat(YaMetrikaCounters):
    DATA_URL = 'https://api-metrika.yandex.ru/stat/v1/data'

    def print_all_stat(self):
        counters = self.get_counters()
        for counter in counters['counters']:
            stat = self.get_stat(counter['id'])
            if not stat['data']:
                continue

            print("\nСайт: {}".format(counter['site']))
            print('----------')
            print('Визитов: {:.0f}'.format(stat['data'][0]['metrics'][0]))
            print('Просмотров: {:.0f}'.format(stat['data'][0]['metrics'][1]))
            print('Посетителей: {:.0f}'.format(stat['data'][0]['metrics'][2]))

    def get_stat(self, counter_id):
        headers = self.get_headers()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:visits,ym:s:pageviews,ym:s:users'
        }
        response = requests.get(self.DATA_URL, params=params, headers=headers)
        return response.json()


# ya_metrika = YaMetrikaBase()
# ya_metrika.get_authorization_link()

yam_stat = YaMetrikaStat()
yam_stat.print_all_stat()
