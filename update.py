import sys
import sqlite3
from downloader import WallDownloader
from config import db, table, domain, update_range


def _create_table(cursor):
    query = 'CREATE TABLE IF NOT EXISTS %s (' \
                'id integer PRIMARY KEY, ' \
                'date integer, ' \
                'likes integer, ' \
                'reposts integer, ' \
                'views integer, ' \
                'rating real' \
            ')' % table
    cursor.execute(query)
    
    
def _update_posts(cursor, posts, verbose=False):
    query = 'INSERT OR REPLACE ' \
            'INTO %s (id, date, likes, reposts, views, rating) ' \
            'VALUES (?, ?, ?, ?, ?, ?)' % table
    count = 0
    for post in posts:
        cursor.execute(query, post.combine())
        count += 1
        if verbose:
            print(count, post.combine())
    

def make_update(all, verbose=False):
    downloader = WallDownloader(domain)
    posts = downloader.download_all() if all else downloader.update(update_range)
    try:
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        
        _create_table(cursor)
        _update_posts(cursor, posts, verbose)
        
        connection.commit()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    
    
if __name__ == '__main__':
    make_update('-a' in sys.argv, True)
    