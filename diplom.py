from preparation import new_search
from search import user
from pymongo import MongoClient
from pprint import pprint


def search():
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
        elif user_command == 2:
            break


if __name__ == '__main__':
    search()
