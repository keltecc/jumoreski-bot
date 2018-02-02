import sys
import sqlite3
from downloader import WallDownloader

import config

    
def create_table(db, table):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    query = 'CREATE TABLE IF NOT EXISTS %s (' \
                'id integer PRIMARY KEY, ' \
                'date integer, ' \
                'likes integer, ' \
                'reposts integer, ' \
                'views integer' \
            ')'
    cursor.execute(query % table)
    connection.commit()
    connection.close()
    
    
def update_posts(db, table, posts, verbose=False):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    query = 'INSERT OR REPLACE INTO %s (id, date, likes, reposts, views) VALUES (?, ?, ?, ?, ?)' % table
    count = 0
    for post in posts:
        cursor.execute(query, post.combine())
        count += 1
        if verbose:
            print(count, post.combine())
    connection.commit()
    connection.close()
    

def make_update(all, verbose=False):
    create_table(config.db, config.table)
    downloader = WallDownloader(config.service_token, config.domain)
    posts = downloader.download_all() if all else downloader.update(config.update_time)
    update_posts(config.db, config.table, posts, verbose)
    
    
if __name__ == '__main__':
    make_update('-a' in sys.argv, True)
    