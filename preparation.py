import os


def new_search():
    if not os.path.isdir('log'):
        os.makedirs('log')
    if not os.path.isdir('json'):
        os.makedirs('json')
    with open('log/users_not_fit.txt', 'w', encoding='utf-8') as f_write:
        f_write.write('')
    with open('log/users_fit.txt', 'w', encoding='utf-8') as f_write:
        f_write.write('')


if __name__ == '__main__':
    new_search()
