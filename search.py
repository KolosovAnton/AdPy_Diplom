import requests
from urllib.parse import urlencode
import json
import time
import sys
from datetime import datetime

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

TOKEN = '9183c6520ce6eb31329c80d5979df4061cc6293894c3987819d2d4a3e3ece7c8f2be2a405157ea35b3f79'

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
                # print('Получение id пользователя из его короткого имени')
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
            # print(f'Получение списка групп пользователя https://vk.com/id{self.user_id}')
        except KeyError:
            user_groups = '0'
            # print(user_groups, f'Пользователь https://vk.com/id{self.user_id} ограничил доступ к своим группам')
        return user_groups

    def get_photos(self):
        params = {
            'owner_id': self.user_id,
            'album_id': -6,
            'extended': 1,
            'rev': 1,
            'photo_sizes': 1
        }
        params.update(self.get_params())
        response = requests.get(
            'https://api.vk.com/method/photos.get',
            params
        )
        try:
            user_photos = response.json()['response']['items']
            for photo in user_photos:
                photo['likes'] = photo['likes']['count']
        except KeyError:
            print(f'Пользователь https://vk.com/id{self.user_id} ограничил доступ к своим фотографиям')
        else:
            return user_photos

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
            'count': 1000,
            'hometown': hometown,
            'sex': sex,
            'age_from': age_from,
            'age_to': age_to,
            'has_photo': 1,
            'fields': 'bdate, screen_name, common_count, interests, books, music, relation'
        }
        params.update(self.get_params())
        response = requests.get(
            'https://api.vk.com/method/users.search',
            params
        )
        search_result = response.json()['response']['items']
        user_groups = set(self.get_groups())
        status = {0, 1, 6}
        search_result_after_relation = []
        for result in search_result:
            try:
                if result['relation'] in status:
                    search_result_after_relation.append(result)
            except KeyError:
                result['relation'] = 0
                search_result_after_relation.append(result)
        for result in search_result_after_relation:
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
                result['common_group'] = '0'
        return search_result_after_relation, user_result

    def result_search(self):
        search = self.search_users()
        search_result = search[0]
        user_result = search[1]
        result_after_closed = []
        for result in search_result:
            if result['is_closed'] == False:
                result_after_closed.append(result)
            else:
                with open('log/users_not_fit.txt', 'a', encoding='utf-8') as f_write:
                    f_write.write(f"{result['id']},")

        result_after_count = []
        users_fit = []
        result_after_closed = sorted(result_after_closed, key=lambda x: x['common_count'], reverse=True)
        for item in result_after_closed:
            if len(users_fit) == 10:
                break
            if item['common_count'] != 0:
                users_fit.append(item)
            else:
                result_after_count.append(item)

        result_bdate = []
        for result in result_after_count:
            try:
                bdate = result['bdate'].split('.')
                if len(bdate) == 3:
                    result_bdate.append(result)
                else:
                    with open('log/users_not_fit.txt', 'a', encoding='utf-8') as f_write:
                        f_write.write(f"{result['id']},")
            except KeyError:
                with open('log/users_not_fit.txt', 'a', encoding='utf-8') as f_write:
                    f_write.write(f"{result['id']},")
        result_bdate = sorted(result_bdate, key=lambda x: x['bdate'], reverse=True)
        result_after_bdate = []
        for item in result_bdate:
            if len(users_fit) == 10:
                break
            bdate = item['bdate'].split('.')
            now_date = datetime.now().date().strftime('%d.%m.%Y').split('.')
            item_age = int(now_date[2]) - int(bdate[2])
            if item_age == user_result[0]['age']:
                users_fit.append(item)
            else:
                result_after_bdate.append(item)

        result_after_bdate = sorted(result_after_bdate, key=lambda x: x['common_group'], reverse=True)
        result_after_group = []
        for item in result_after_bdate:
            if len(users_fit) == 10:
                break
            if item['common_count'] != 0:
                users_fit.append(item)
            else:
                result_after_group.append(item)

        result_common_interest = []
        for item in result_after_group:
            if len(users_fit) == 10:
                break
            if item['interests'] == 'Поле не заполнено' and item['music'] == 'Поле не заполнено' \
                    and item['books'] == 'Поле не заполнено':
                with open('log/users_not_fit.txt', 'a', encoding='utf-8') as f_write:
                    f_write.write(f"{item['id']},")
            else:
                result_common_interest.append(item)

        # поиск по интересам, музыке, книгам

        for item in users_fit:
            with open('log/users_fit.txt', 'a', encoding='utf-8') as f_write:
                f_write.write(f"{item['id']},")
            time.sleep(0.3)
            self.user_id = item['id']
            user_photos = self.get_photos()
            user_photos = sorted(user_photos, key=lambda x: x['likes'], reverse=True)
            top_3_url = []
            for photo in user_photos[:3]:
                for item_size in photo['sizes']:
                    if item_size['type'] == 'x':
                        top_3_url.append(item_size['url'])
            item['top_3'] = top_3_url
        return users_fit

    def output_file(self):
        user_fit = self.result_search()
        list_user_fit = []
        for item in user_fit:
            dict_item = {
                'account': f"https://vk.com/{item['screen_name']}",
                'top_3_photo': item['top_3']
            }
            list_user_fit.append(dict_item)
        with open('json/search_result.json', 'w', encoding='utf-8') as w_file:
            json.dump(list_user_fit, w_file)
        return list_user_fit


user = User(TOKEN, user_name)

if __name__ == '__main__':
    print(user)

# дополнить поиск на сравнение уже имеющихся id в логах с полученными id в ходе поиска
