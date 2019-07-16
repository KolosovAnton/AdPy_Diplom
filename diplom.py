import requests
from urllib.parse import urlencode
import json
import time
import sys
from pprint import pprint
from datetime import datetime
import csv

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

TOKEN = '5bd9a1c37b7695f33d729c1adc8e0e656a58454f758b191d27b963579e562866c4817c38f44d1bbbda6a0'

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
                'v': '5.101'
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
            'fields': 'bdate, city, interests, books, music'
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
            try:
                age = int(input('Введите ваш возраст: '))
            except ValueError:
                age = int(input('Введите ваш возраст числом: '))
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
            print(f'Пользователь https://vk.com/id{self.user_id} ограничил доступ к своим группам')
        else:
            return user_groups

    def search_users(self):
        user_result = self.get_user()
        try:
            sex = int(input('Введите пол для поиска:\n\t1 - женщина;\n\t2 - мужчина;\n\t0 - любой;\n'))
        except ValueError:
            sex = int(input('Введите число 1, 2 или 0 для поиска женщины, мужчины или любой соответственно: '))
        hometown = user_result[0]['hometown']
        age_from = user_result[0]['age'] - 1
        age_to = user_result[0]['age'] + 1
        params = {
            'count': 31,
            'hometown': hometown,
            'sex': sex,
            'status': 0 or 1 or 6,
            'age_from': age_from,
            'age_to': age_to,
            'has_photo': 1,
            'fields': 'bdate, screen_name, common_count, interests, books, music'
        }
        params.update(self.get_params())
        response = requests.get(
            'https://api.vk.com/method/users.search',
            params
        )
        search_result = response.json()['response']['items']
        user_groups = set(self.get_groups())
        for result in search_result:
            try:
                if result['interests'] == '':
                    result['interests'] = 'Поле не заполнено'
            except KeyError:
                result['interests'] = 'Поле не заполнено'
            try:
                if result['books'] == '':
                    result['books'] = 'Поле не заполнено'
            except KeyError:
                result['books'] = 'Поле не заполнено'
            try:
                if result['music'] == '':
                    result['music'] = 'Поле не заполнено'
            except KeyError:
                result['music'] = 'Поле не заполнено'
            time.sleep(0.34)
            self.user_id = result['id']
            try:
                groups_result = set(self.get_groups())
                common_group = user_groups.intersection(groups_result)
                result['common_group'] = len(common_group)
            except TypeError:
                result['common_group'] = 'Пользователь закрыл свои группы'
        return search_result, user_result

    def result_search(self):
        search = self.search_users()
        search_result = search[0]
        user_result = search[1]
        for result in search_result:
            try:
                bdate = result['bdate'].split('.')
                if result['is_closed'] == True or len(bdate) != 3:
                    with open('users_not_fit.txt', 'w', encoding='utf-8') as f_write:
                        f_write.write(f"{result['id']}, ")
                    search_result.remove(result)
            except KeyError:
                with open('users_not_fit.txt', 'a', encoding='utf-8') as f_write:
                    f_write.write(f"{result['id']}, ")
                search_result.remove(result)
        users_fit = []
        search_result = sorted(search_result, key=lambda x: x['common_count'], reverse=True)
        for item in search_result:
            if len(users_fit) == 10:
                break
            if item['common_count'] != 0:
                users_fit.append(item)
                search_result.remove(item)
        search_result = sorted(search_result, key=lambda x: x['bdate'], reverse=True)
        for item in search_result:
            if len(users_fit) == 10:
                break
            bdate = item['bdate'].split('.')
            now_date = datetime.now().date().strftime('%d.%m.%Y').split('.')
            item_age = int(now_date[2]) - int(bdate[2])
            if item_age == user_result[0]['age']:
                users_fit.append(item)
                search_result.remove(item)
        search_result = sorted(search_result, key=lambda x: x['common_group'], reverse=True)
        for item in search_result:
            if len(users_fit) == 10:
                break
            if item['common_count'] != 0:
                users_fit.append(item)
                search_result.remove(item)
        for item in search_result:
            if item['interests'] == 'Поле не заполнено' and item['music'] == 'Поле не заполнено' \
                    and item['books'] == 'Поле не заполнено':
                with open('users_not_fit.txt', 'w', encoding='utf-8') as f_write:
                    f_write.write(f"{item['id']}, ")
                search_result.remove(item)
        # поиск по интересам, музыке, книгам
        return users_fit

    def new_search(self):
        with open('users_not_fit.txt', 'w', encoding='utf-8') as f_write:
            f_write.write('')
        with open('users_fit.txt', 'w', encoding='utf-8') as f_write:
            f_write.write('')


user = User(TOKEN, user_name)

if __name__ == '__main__':
    print(user)
    user.new_search()
    user.result_search()
