
from bs4 import BeautifulSoup
import requests
from all_categories import AllCategory
from category_manga import Category

from Model.Database import Database
from Model.Secret import SERVER, USERNAME, PASSWORD, DATABASE



class InsertMangaCategory:



    def __init__(self, page):
        self.page = page
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
        
        self.connection = Database(SERVER, USERNAME, PASSWORD, DATABASE)
        self.db = self.connection.connect()
        
        
        self.manga = Category(self.page, self.header)
        self.category = AllCategory(self.header)

    def insert_manga_category(self):
        page = requests.get(self.page, self.header)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find('h1')
        category = self.manga.get_category()
        print(category)
        category_id = self.connection.get_all_category(self.db, category)
        print('Category id:', category_id)
        manga_id = self.connection.get_id_manga(self.db, title.get_text())
        print('Manga id:', manga_id)
        self.connection.insert_manga_category(self.db, manga_id, category_id)

    def insert_manga(self):

        page = requests.get(self.page, self.header)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find('h1')
        self.connection.set_manga(self.db, title.get_text())
        


manga = InsertMangaCategory('https://ww.mangakakalot.tv/manga/manga-mk952645')
# manga.insert_manga()
manga.insert_manga_category()

