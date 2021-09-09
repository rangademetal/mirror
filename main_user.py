from os import path

from tabulate import tabulate

from Model.Database import Database
from Model.Secret import *
from Controller.manga import manga as download
from Controller.login import login
from Controller.ftp import ftp_ionos

connection = Database(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
ftp = ftp_ionos(FTP_HOSTNAME, FTP_USERNAME, FTP_PASSWORD)
download = download({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'})


db = connection.connect()  
head = ["Category"]
  
categories_torrent = connection.get_category_torrent(db)
categories_manga = connection.get_manga_categories(db)
manga = connection.get_name_manga(db)

username = input('Enter your email:')
password = input('Enter your password:')

MOVIE = connection.get_download_name_ftp(db, 3)
MUSIC = connection.get_download_name_ftp(db, 4)
PICTURE = connection.get_download_name_ftp(db, 5)
SOFTWARE = connection.get_download_name_ftp(db, 6)


login = login(username, password)
login.login()


while True:
    cmd = input('Enter your command: ')
    
    if cmd == 'categories':
        print(tabulate(categories_torrent, headers=head, tablefmt="grid"))
    elif cmd.capitalize() in categories_torrent[0]:
        head = [''.join(categories_torrent[0])]
        print(tabulate(manga, headers=head, tablefmt='grid'))
        cmd = input("Enter your manga's name: ")
        for i in manga:
            if cmd in i[0]:
                head = ['Chapter']
                id_manga = connection.get_id_manga(db, cmd)
                chapters = connection.get_chapter_title_immutable(db, id_manga)
                print(tabulate(chapters, headers=head, tablefmt='grid'))
    elif cmd.capitalize() in categories_torrent[1]:
        head = [''.join(categories_torrent[1])]
        print(tabulate(MOVIE, headers=head, tablefmt='grid'))
        
    
    elif cmd.capitalize() in categories_torrent[2]:
        head = [''.join(categories_torrent[2])]
        print(tabulate(MUSIC, headers=head, tablefmt='grid'))

    elif cmd.capitalize() in categories_torrent[3]:
        head = [''.join(categories_torrent[3])]
        print(tabulate(PICTURE, headers=head, tablefmt='grid'))

    elif cmd.capitalize() in categories_torrent[4]:
        head = [''.join(categories_torrent[4])]
        print(tabulate(SOFTWARE, headers=head, tablefmt='grid'))


    elif cmd == 'download':
        location_download_path
        category = input('Enter your category name:')
        id_category = connection.get_id_torrent(db, category)
        file = input('Enter your download name: ')
        path = connection.get_download_path_ftp(db, file)

        ftp.cwd_folder(path[0])
        ftp.download_ftp(file)

    elif cmd == 'download manga':
        print('Download manga')
        path = input('Enter your PATH: ')
        chapter = input("Enter your chapter's name: ")
        link_chapter = connection.get_chapter_url(db, chapter)
        download.download_single_chapter(link_chapter, download.remove_dots(chapter), path)
    