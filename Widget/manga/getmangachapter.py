from bs4 import BeautifulSoup
import requests


page = requests.get('https://ww.mangakakalot.tv/manga/manga-mk952645', {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'})
soup = BeautifulSoup(page.content, 'html.parser')
titles = soup.find_all('div', {'class':'chapter-list'})
titles = str(titles)
titles = titles.replace('<span>', '').replace('</span>', '')
titles = titles.replace('<div class="row">', '').replace('</div>', '')
titles = titles.replace('[<div class="chapter-list">', '').replace(']', '')
titles = titles.split('\n')
lists = []
for title in titles:
    if title.startswith('<a'):
        title = title.replace('<a href=', '').replace('"', '').replace('>', '')
        title = title.strip()
        lists.append(title)

urls = lists
titles = lists
item_i = []
for url in urls:
    url = str(url)
    url = url[:url.find('=')]
    url = url.replace(' title', '')
    url = f'https://ww.mangakakalot.tv{url}' 
    item_i.append(url)
    
item_j = []
for title in titles:
    # print(title)
    title = str(title)
    title = title[title.find('='):]
    title = title.replace('= ','' )
    item_j.append(title)

for (i,j) in zip(item_i, item_j):
    print(i+'   '+j)
    
    



