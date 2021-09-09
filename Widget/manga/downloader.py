from bs4 import BeautifulSoup

import requests
import random
import os


class downloader:
    def __init__(self, link, header):
        self.link = link
        self.header = header

    def clear_link(self, src=[]):
        page = requests.get(self.link, self.header)
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

    def download(self, name):
        links = self.clear_link()
        os.mkdir(name)
        os.chdir(name)
        progress = ''
        for link in links:
            progress += '#'
            r = requests.get(link)
            with open(f"{random.randint(100000, 999999)}.jpg", "wb") as f:
                f.write(r.content)
            print(f'Download |{progress}| {len(links)} pages')

# for chapter in chapters:
#     down = downloader('https://ww.mangakakalot.tv/chapter/manga-mk952645/chapter-1', {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'})
#     down.download("Record Of Ragnarok Vol.1 Chapter 1")
    