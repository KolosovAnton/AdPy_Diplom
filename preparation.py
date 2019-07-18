import os
import json
from pymongo import MongoClient


def new_search():
    if not os.path.isdir('log'):
        os.makedirs('log')
    if not os.path.isdir('json'):
        os.makedirs('json')
    with open('log/users_not_fit.txt', 'w', encoding='utf-8') as f_write:
        f_write.write('')
    with open('log/users_fit.txt', 'w', encoding='utf-8') as f_write:
        f_write.write('')
    with open('json/search_result.json', 'w', encoding='utf-8') as w_file:
        json.dump('search result:', w_file)
    client = MongoClient()
    diplom_db = client['diplom']
    result_collection = diplom_db['result']
    diplom_db.result.delete_many({})


if __name__ == '__main__':
    new_search()
