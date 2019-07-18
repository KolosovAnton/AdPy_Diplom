from preparation import new_search
from search import user
from pymongo import MongoClient
from pprint import pprint

new_search()


# тело программы с выбором варианта: новый поиск, продолжить поиск, выход
client = MongoClient()
diplom_db = client['diplom']
result_collection = diplom_db['result']
# удалить коллекцию

def search():
    list_user_fit = user.output_file()
    for item in list_user_fit:
        result_collection.insert_one(item)
    pprint(list(result_collection.find()))


if __name__ == '__main__':
    search()
