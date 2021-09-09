from Model.Database import Database
from Model.Secret import DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE

from bs4 import BeautifulSoup

import requests
import random
import os


class manga:
    def __init__(self, header):
        self.header = header
        self.connection = Database(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
        self.db = self.connection.connect()
    
    def clear_link(self, page, src=[]):
        page = requests.get(page, self.header)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        images = soup.find_all('div', {'class': 'vung-doc'})
        images = str(images)
        images = images.split('\n')
        images = [images[i] for i in range(len(images)) if i % 2 == 1]
        images = images[0:-1]

        for i in images:
            test = i.split(' ')
            src.append(test[4][10:-1])
        return src
    
    def download_single_chapter(self, page, name, path):
        links = self.clear_link(page)
        path_manga = f'{path}\\{name}'
        os.mkdir(path_manga)
        os.chdir(path_manga)
        for link in links:
            r = requests.get(link)
            with open(f"{random.randint(100000, 999999)}.jpg", "wb") as f:
                f.write(r.content)
        print(name, 'complete!')
    
    def remove_dots(self, string):
        return string.replace(':', '')
    
    def download_all_manga_from_database(self, title_manga, path ):
        id_manga = self.connection.get_id_manga(self.db, title_manga)
        path_manga = f'{path}\\{title_manga}'
        print(path_manga)
        os.mkdir(path_manga)
        os.chdir(path_manga)
        names = self.connection.get_chapter_titles(self.db, id_manga)
        links = self.connection.get_chapter_urls(self.db, id_manga)
        for (name, link) in zip(names, links):
            self.download_single_chapter(link, self.remove_dots(name))
            os.chdir(path_manga)

    def get_category(self, page, cat=[]):
        page = requests.get(page, self.header)
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
    
    def clear_name(self, name):
        return name.replace(':', '') 
    
    def replace_path(self, path):
        return path.replace('/', '\\')

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
    
    def set_all_category(self, cat, id_torrent_category):
        for i in cat:
            self.connection.set_category(self.db, i, id_torrent_category)
    
    def insert_manga(self, page):
        page = requests.get(page, self.header)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find('h1')
        self.connection.set_manga(self.db, title.get_text())
    
    def insert_manga_category(self, page_link):
        page = requests.get(page_link, self.header)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find('h1')
        title = title.get_text()
        print(title)
        category = self.get_category(page_link)
        print('Category names: ', category)
        category_id = self.connection.get_id_category(self.db, category)
        print('Category id:', category_id)
        manga_id = self.connection.get_id_manga(self.db, title)
        print('Manga id:', manga_id)
        self.connection.insert_manga_category(self.db, manga_id, category_id)
    
    def clear_chapter(self, page, lists=[]):
        page = requests.get(page, self.header)
        soup = BeautifulSoup(page.content, 'html.parser')
        titles = soup.find_all('div', {'class':'chapter-list'})
        titles = str(titles)
        titles = titles.replace('<span>', '').replace('</span>', '')
        titles = titles.replace('<div class="row">', '').replace('</div>', '')
        titles = titles.replace('[<div class="chapter-list">', '').replace(']', '')
        titles = titles.split('\n')
        
        for title in titles:
            if title.startswith('<a'):
                title = title.replace('<a href=', '').replace('"', '').replace('>', '')
                title = title.strip()
                lists.append(title)
        return lists
    
    def get_url_request_chapter(self, page, link = []):
        urls = self.clear_chapter(page)
        for url in urls:
            url = str(url)
            url = url[:url.find('=')]
            url = url.replace(' title', '')
            url = f'https://ww.mangakakalot.tv{url}' 
            link.append(url)
        return link
    
    def get_title_request_chapter(self, page, name = []):
        titles = self.clear_chapter(page)
        for title in titles:
            title = str(title)
            title = title[title.find('='):]
            title = title.replace('= ','')
            name.append(title)
        return name
    
# manga = manga({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'})


# print(manga.replace_path('E:/manga'))

# print(manga.connection.get_id_torrent(manga.db, 'manga'))

# Adding chapters in manga table
# id_manga = manga.connection.get_id_manga(manga.db, 'Hellsing')
# urls = manga.get_url_request_chapter('https://ww.mangakakalot.tv/manga/manga-yv959004')
# titles = manga.get_title_request_chapter('https://ww.mangakakalot.tv/manga/manga-yv959004')
# manga.connection.set_manga_chapters(manga.db, titles, id_manga, urls)

# print(manga.connection.get_all_torrent_categories(manga.db))

# check the categories
# id_cattorrent = manga.connection.get_id_torrent(manga.db, 'manga')
# category = manga.get_all_category()
# print(category)
# # # insert categories of manga into database (m-to-m)
# print(manga.set_all_category(category, id_cattorrent))
# manga.insert_manga('https://ww.mangakakalot.tv/manga/manga-yv959004')
# manga.insert_manga_category('https://ww.mangakakalot.tv/manga/manga-yv959004')


# id_cattorrent = manga.connection.get_id_torrent(manga.db, 'manga')
# print(id_cattorrent)
# category = manga.get_all_category()
# print(category, id_cattorrent)
# manga.set_all_category(category, id_cattorrent)


# Download all chapters
# id_manga = manga.connection.get_id_manga(manga.db, 'Akame Ga Kill!')
# title = manga.connection.get_chapter_titles(manga.db, id_manga)
# url = manga.connection.get_chapter_urls(manga.db, id_manga)
# manga.download_all_manga_from_database('Akame Ga Kill!', 'E:\\manga')
# for i in url:
#     links = manga.clear_link(i)
#     print(links)


# Download entire chapter
# manga.download('https://ww.mangakakalot.tv/chapter/manga-mk952645/chapter-78.5', manga.clear_name('Akame Ga Kill! Chapter 78.5: Epilogue: Kill The Sorrow'))


# GET TITLEs AND URLS FROM CHAPTERS
# print(manga.get_url_request_chapter('https://ww.mangakakalot.tv/manga/manga-mk952645'))
# print(manga.get_title_request_chapter('https://ww.mangakakalot.tv/manga/manga-mk952645'))