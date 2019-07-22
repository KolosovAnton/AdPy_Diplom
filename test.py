import unittest
from search import user
import json
from pprint import pprint

class TestSearch(unittest.TestCase):
    def test_1__str__(self):
        print('id: {}'.format(self.id()))
        self.assertIn('https://vk.com/', user.__str__())

    def test_2_get_user(self):
        print('id: {}'.format(self.id()))
        self.assertIsInstance(user.get_user(), list)

    def test_3_get_groups(self):
        print('id: {}'.format(self.id()))
        self.assertGreater(len(user.get_groups()), 0)

    def test_4_get_photos(self):
        print('id: {}'.format(self.id()))
        self.assertGreater(len(user.get_photos()), 0)

    def test_5_search_users(self):
        print('id: {}'.format(self.id()))
        self.assertGreater(len(user.search_users()[0]), 0)

    def test_6_result_search(self):
        print('id: {}'.format(self.id()))
        user.result_search()
        with open('log/users_not_fit.txt', encoding='utf-8') as f_read:
            not_fit = f_read.read()
        with open('log/users_fit.txt', encoding='utf-8') as f_read:
            fit = f_read.read()
        self.assertGreater(len(not_fit), 0)
        self.assertIsInstance(not_fit, str)
        self.assertGreater(len(fit), 0)
        self.assertIsInstance(fit, str)


if __name__ == '__main__':
    unittest.main()
