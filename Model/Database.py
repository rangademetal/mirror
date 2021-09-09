import mysql.connector
from mysql.connector import connection


class Database:
    def __init__(self, SERVER, USERNAME, PASSWORD, DATABASE):
        self.SERVER = SERVER
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.DATABASE = DATABASE

    def connect(self):
        self.database = mysql.connector.connect(
            host=self.SERVER,
            user=self.USERNAME,
            password=self.PASSWORD,
            database=self.DATABASE
        )
        return self.database

    def get_account(self, connection, email, password):
        cursor = connection.cursor()
        sql = 'SELECT * FROM account where email=%s AND password=%s'
        param = (email, password,)
        cursor.execute(sql, param)
        result = cursor.fetchone()
        return result

    def set_code(self, connection, email):
        cursor = connection.cursor()
        sql = 'UPDATE account SET verificatio_status=1 where email=%s'
        param = (email,)
        cursor.execute(sql, param)
        connection.commit()

    def set_register(self, connection, email, username, password, verification_code, verificatio_status=False):
        try:
            cursor = connection.cursor()
            sql = 'INSERT INTO account(email, username, password, verification_code, verificatio_status) values (%s, %s, %s, %s, %s)'
            param = (email, username, password, verification_code, verificatio_status,)
            cursor.execute(sql, param)
            connection.commit()
        except mysql.connector.IntegrityError as err:
            print(err)
        finally:
            connection.close()

    def set_manga(self, connection, link_name):
        try:
            cursor = connection.cursor()
            sql = 'INSERT INTO manga(name_manga) values(%s)'
            param = (link_name,)
            cursor.execute(sql, param)
            connection.commit()
        except mysql.connector.IntegrityError as err:
            print('ERROR #201:Manga Already exist')
        # finally:
        #     connection.close()

    def set_chapter(self, connection, chapter, id_manga):
        try:
            cursor = connection.cursor()
            sql = 'INSERT INTO chapter(name_chapter, id_manga) values(%s, %s)'
            param = (chapter, id_manga,)
            cursor.execute(sql, param)
            connection.commit()
        except mysql.connector.IntegrityError as err:
            print('ERROR #202:Chapter Already exist')
        finally:
            connection.close()

    def set_category(self, connection, category, id_torrent_category):
        try:
            cursor = connection.cursor()
            sql = 'INSERT INTO category(name_category, id_subcategory) values(%s, %s)'
            param = (category, id_torrent_category, )
            cursor.execute(sql, param)
            connection.commit()
        except mysql.connector.IntegrityError as err:
            print(err)

    def check_manga(self, connection, link_name):
        cursor = connection.cursor()
        sql = 'SELECT name_manga FROM manga WHERE name_manga=%s'
        param = (link_name, )
        cursor.execute(sql, param)
        result = cursor.fetchone()
        return result[0]


    def get_all_category(self, connection, category, list_id=[]):
        cursor = connection.cursor()
        sql = 'SELECT id FROM category WHERE name_category=%s'
        for i in category:
            param = (i, )
            cursor.execute(sql, param)
            result = cursor.fetchone()
            list_id.append(result[0])
        return list_id
    
    def get_id_category(self, connection, category, list_id = []):
        cursor = connection.cursor()
        sql = 'SELECT id FROM category WHERE name_category=%s'
        for i in category:
            param = (i, )
            cursor.execute(sql, param)
            result = cursor.fetchone()
            list_id.append(result[0])
        return list_id

    def get_id_manga(self, connection, manga):
        cursor = connection.cursor()
        sql = 'SELECT id FROM manga WHERE name_manga=%s'
        param = (manga, )
        cursor.execute(sql, param)
        result = cursor.fetchone()
        return result[0]

    def insert_manga_category(self, connection, manga, category):
        cursor = connection.cursor()
        sql = 'INSERT INTO category_manga(id_manga, id_category) values (%s, %s)'
        for i in category:
            param = (manga, i,)
            cursor.execute(sql, param)
            connection.commit()

    def set_manga_chapters(self, connection, chapter_name, id_manga, chapter_link):
        cursor = connection.cursor()
        sql = 'INSERT INTO chapter(name_chapter, id_manga, link_chapter) values (%s, %s, %s)'
        for (i, j) in zip (chapter_name, chapter_link):
            param = (i, id_manga, j,)
            cursor.execute(sql, param)
            connection.commit()
    
    def get_chapter_titles(self, connection, id_manga, titles = []):
        cursor = connection.cursor()
        sql = 'SELECT name_chapter FROM chapter where id_manga=%s'
        param = (id_manga,)
        cursor.execute(sql, param)
        results = cursor.fetchall()

        for result in results:
            titles.append(result[0])

        return titles
        
    
    def get_chapter_urls(self, connection, id_manga, urls = []):
        cursor = connection.cursor()
        sql = 'SELECT link_chapter FROM chapter where id_manga=%s'
        param = (id_manga,)
        cursor.execute(sql, param)
        results = cursor.fetchall()

        for result in results:
            urls.append(result[0])
        return urls
    
    def get_id_torrent(self, connection, torrent):
        cursor = connection.cursor()
        sql = 'select id from category_torrent where name_category=%s'
        param = (torrent,)
        cursor.execute(sql, param)
        result = cursor.fetchone()
        return result[0]
    
    def get_all_torrent_categories(self, connection, categories = []):
        cursor = connection.cursor()
        sql = 'select name_category from category_torrent'

        cursor.execute(sql)
        results = cursor.fetchall()

        for result in results:
            categories.append(result)
        
        return categories
    
    def get_category_torrent(self, connection, categories = []):
        cursor = connection.cursor()
        sql = 'select name_category from category_torrent'

        cursor.execute(sql)
        results = cursor.fetchall()

        for result in results:
            categories.append(result)
        
        return categories

    def get_manga_categories(self, connection, categories = []):
        cursor = connection.cursor()
        sql = 'select a.name_category from category a, category_torrent b WHERE a.id_subcategory = b.id'

        cursor.execute(sql)
        results = cursor.fetchall()

        for result in results:
            categories.append(result)
        
        return categories

    def get_chapter_title_immutable(self, connection, id_manga, chapters = []):
        cursor = connection.cursor()
        sql = 'SELECT name_chapter FROM chapter where id_manga=%s'
        param = (id_manga,)
        cursor.execute(sql, param)
        results = cursor.fetchall()

        for result in results:
            chapters.append(result)

        return chapters
    
    def get_name_manga(self, connection, manga=[]):
        cursor = connection.cursor()
        sql = 'SELECT name_manga FROM manga'
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            manga.append(result)
        
        return manga

    def get_chapter_url(self, connection, chapter):
        cursor = connection.cursor()
        sql = 'SELECT link_chapter FROM chapter WHERE name_chapter = %s'
        param = (chapter, )
        cursor.execute(sql, param)
        result = cursor.fetchone()
        return result[0]
        
    def get_download_name_ftp(self, connection, id_torrent):
        cursor = connection.cursor()
        sql =  'select torrent_name from  torrent_download where id_category_torrent = %s'
        param = (id_torrent, )
        cursor.execute(sql, param)
        results = cursor.fetchall()
        

        return results

    def get_download_path_ftp(self, connection, id_torrent):
        cursor = connection.cursor()
        sql =  'select path_torrent from torrent_download where torrent_name = %s'
        param = (id_torrent, )
        cursor.execute(sql, param)
        result = cursor.fetchone()


        return result