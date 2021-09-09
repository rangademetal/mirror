from bs4 import BeautifulSoup
import requests

from Model.Database import Database
from Model.Secret import  SERVER, USERNAME, PASSWORD, DATABASE


class Category:
    def __init__(self, page, header):
        self.page = page
        self.header = header
        self.connection = Database(SERVER, USERNAME, PASSWORD, DATABASE)
        self.db = self.connection.connect()

    def get_category(self, cat=[]):
        page = requests.get(self.page, self.header)
        soup = BeautifulSoup(page.content, 'html.parser')
        categories = soup.find_all('li')[11]
        categories = str(categories)
        categories = categories.replace(' ', '')
        categories = categories.split('\n')
        for category in categories:
            if category.startswith('<a'):
                category = category.replace('<ahref="/manga_list?type=newest&amp;category=', '')
                remover = category.find('&')
                category = category[:remover]
            cat.append(category)
        cat = cat[1:-1]
        cat = [cat[i] for i in range(len(cat)) if i % 2 == 1]
        return cat


# category = Category('https://ww.mangakakalot.tv/manga/manga-kv952404', {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'})
# category_manga = category.get_category()
# print(category_manga)
