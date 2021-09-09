from bs4 import BeautifulSoup
import requests

from Model.Database import Database
from Model.Secret import *


class AllCategory:
    def __init__(self, header):
        self.connection = Database(SERVER, USERNAME, PASSWORD, DATABASE)
        self.db = self.connection.connect()
        self.header = header

    def get_all_category(self, category = []):
        page = requests.get('https://ww.mangakakalot.tv/', self.header)
        soup = BeautifulSoup(page.content, 'html.parser')


        categories = soup.find_all('tbody')
        categories = str(categories)
        categories = categories.replace('<td>', '').replace('</td>', '').replace('<tr>', '').replace('</tr>', '')
        categories = categories.replace('<tr class="bordertop">', '').replace('</tbody>', '').replace('<tbody>', '')
        categories = categories.replace('[', '').replace(']', '')
        categories = categories.split('\n')
        categories = categories[20:-2]
        categories = [categories[i] for i in range(len(categories)) if categories[i] != '']

        for categories in categories:
            if categories != '':
                categories = categories.replace('<a href="/manga_list?type=latest&amp;category=', '')
                cat = categories.find('&')
                categories = categories[:cat]
            category.append(categories)
        return category

    def set_all_category(self, cat):
        for i in cat:
            self.connection.set_category(self.db, i)


# cate = AllCategory('')
# category = cate.get_all_category()
# print(category)
# cate.set_all_category(category)