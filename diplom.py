from preparation import new_search
from search import User
from pymongo import MongoClient
from pprint import pprint


def search():
    user_name = input('Введите имя пользователя или его id: ')
    TOKEN = '4e8238c2c57817994b48407e67bc2c15ded92e2e11331255b3a287f4b14835c4d1a6363c4f9b359403715'
    user = User(TOKEN, user_name)
    new_search()
    client = MongoClient()
    diplom_db = client['diplom']
    result_collection = diplom_db['result']
    list_user_fit = user.output_file()
    for item in list_user_fit:
        result_collection.insert_one(item)
    pprint(list(result_collection.find()))
    while True:
        try:
            user_command = int(input('Выберите вариант:\n\t1 - для продолжения поиска;'
                                     '\n\t2 - для окончания поиска;\n'))
        except ValueError:
            user_command = int(input('Введите число:\n\t1 - для продолжения поиска;'
                                     '\n\t2 - для окончания поиска;\n'))
        if user_command == 1:
            list_user_fit = user.output_file()
            for item in list_user_fit:
                result_collection.insert_one(item)
            pprint(list(result_collection.find()))
            print('1')
        elif user_command == 2:
            break
        elif user_command != 1 and user_command != 2:
            continue


if __name__ == '__main__':
    search()
