import requests
from urllib.parse import urlencode
import json
import time
import sys
from pprint import pprint
from datetime import datetime, date

# APP_ID = 7053235
# BASE_URL = 'https://oauth.vk.com/authorize'
# token = ''
# auth_data = {
#     'client_id': APP_ID,
#     'display': 'page',
#     'scope': 262222,
#     'response_type': 'token',
#     'v': '5.101'
# }
#
# print('?'.join((BASE_URL, urlencode(auth_data))))

TOKEN = '48e02f5c294c7b3fccb2a7188cc3ac0679ab135be99fa328d5da76ef1332428dd8845dc2a164c784a72c5'

user_name = input('Введите имя пользователя или его id: ')


class User:
    def __init__(self, TOKEN, user_name):
        self.token = TOKEN
        self.user_name = user_name
        try:
            self.user_id = int(user_name)
        except:
            params = {
                'access_token': self.token,
                'screen_name': self.user_name,
                'v': '5.95'
            }
            response = requests.get(
                'https://api.vk.com/method/utils.resolveScreenName',
                params
            )
            try:
                print('Получение id пользователя из его короткого имени')
                self.user_id = response.json()['response']['object_id']
            except KeyError:
                print(f'У пользователя {self.user_name} не получен id')
                sys.exit()

    def __str__(self):
        try:
            self.user_id = int(user_name)
            return f'https://vk.com/id{self.user_id}'
        except:
            return f'https://vk.com/{self.user_name}'

    def get_params(self):
        return dict(
            access_token=self.token,
            user_id=self.user_id,
            v='5.101'
        )

    def get_user(self):
        params = {
            'fields': 'bdate, city, interests, books, movies, music'
        }
        params.update(self.get_params())
        response = requests.get(
            'https://api.vk.com/method/users.get',
            params
        )
        user_result = response.json()['response']
        try:
            hometown = user_result[0]['city']['title']
            user_result[0]['hometown'] = hometown
        except KeyError:
            user_result[0]['hometown'] = input('Введите название своего города: ')
        try:
            bdate = user_result[0]['bdate'].split('.')
            now_date = datetime.now().date().strftime('%d.%m.%Y').split('.')
            age = int(now_date[2]) - int(bdate[2])
        except KeyError:
            age = int(input('Введите ваш возраст: '))
        user_result[0]['age'] = age
        try:
            if user_result[0]['interests'] == '':
                user_result[0]['interests'] = input('Введите ваши интересы: ')
        except KeyError:
            user_result[0]['interests'] = input('Введите ваши интересы: ')
        try:
            if user_result[0]['books'] == '':
                user_result[0]['books'] = input('Введите ваши любимые книги: ')
        except KeyError:
            user_result[0]['books'] = input('Введите ваши любимые книги: ')
        try:
            if user_result[0]['movies'] == '':
                user_result[0]['movies'] = input('Введите ваши любимые фильмы: ')
        except KeyError:
            user_result[0]['movies'] = input('Введите ваши любимые фильмы: ')
        try:
            if user_result[0]['music'] == '':
                user_result[0]['music'] = input('Введите вашу любимую музыку: ')
        except KeyError:
            user_result[0]['music'] = input('Введите вашу любимую музыку: ')
        return user_result

    def get_groups(self):
        params = self.get_params()
        response = requests.get(
            'https://api.vk.com/method/groups.get',
            params
        )
        try:
            user_groups = response.json()['response']['items']
            print(f'Получение списка групп пользователя https://vk.com/id{self.user_id}')
        except KeyError:
            print(f'Пользователь https://vk.com/id{self.user_id} ограничил доступ к своим'
                  f' группам, удален или заблокирован')
        else:
            return user_groups

    def search_users(self):
        user_result = self.get_user()
        sex = input('Введите пол для поиска:\n\t1 - женщина;\n\t2 - мужчина;\n\t0 - любой;\n')
        hometown = user_result[0]['hometown']
        age_from = user_result[0]['age'] - 1
        age_to = user_result[0]['age'] + 1
        params = {
            'count': 10,
            'hometown': hometown,
            'sex': sex,
            'status': 0 or 1 or 6,
            'age_from': age_from,
            'age_to': age_to,
            'has_photo': 1,
            'fields': 'screen_name, common_count, interests, books, movies, music'
        }
        params.update(self.get_params())
        response = requests.get(
            'https://api.vk.com/method/users.search',
            params
        )
        search_result = response.json()['response']['items']
        # print(response.json()['response']['count'])
        user_groups = set(self.get_groups())
        for result in search_result:
            try:
                if result['interests'] == '':
                    result['interests'] = 'Поле Интересы не заполнено'
            except KeyError:
                result['interests'] = 'Поле Интересы не заполнено'
            try:
                if result['books'] == '':
                    result['books'] = 'Поле Книги не заполнено'
            except KeyError:
                result['books'] = 'Поле Книги не заполнено'
            try:
                if result['movies'] == '':
                    result['movies'] = 'Поле Фильмы не заполнено'
            except KeyError:
                result['movies'] = 'Поле Фильмы не заполнено'
            try:
                if result['music'] == '':
                    result['music'] = 'Поле Музыка не заполнено'
            except KeyError:
                result['music'] = 'Поле Музыка не заполнено'
            time.sleep(0.34)
            self.user_id = result['id']
            try:
                groups_result = set(self.get_groups())
                common_group = user_groups.intersection(groups_result)
                result['common_group'] = len(common_group)
            except TypeError:
                result['common_group'] = 'Пользователь закрыл свои группы'
        return search_result


user = User(TOKEN, user_name)
print(user)
# pprint(user.get_user())
pprint(user.search_users())
