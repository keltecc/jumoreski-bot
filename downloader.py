import sys
import vk_requests as vk
from time import time, sleep
from datetime import datetime
from config import api_version, posts_count

from tokens import service_token


class WallPost():

    def __init__(self, id, date, likes, reposts, views):
        self.id = id
        self.date = date
        self.likes = likes
        self.reposts = reposts
        self.views = views
        self.rating = 0
        if views > 0:
            self.rating += likes / views
        if likes > 0:
            self.rating += reposts / likes
        self.rating *= 100
        
        
    def combine(self):
        return self.id, self.date, self.likes, self.reposts, self.views, self.rating
        

class WallDownloader():

    def __init__(self, domain):
        try:
            self._api = vk.create_api(service_token=service_token, api_version=api_version)
            domain_info = self._api.utils.resolveScreenName(screen_name=domain)
            self._owner_id = domain_info['object_id']
            if domain_info['type'] == 'group':
                self._owner_id *= -1
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit(1)
        
        
    def _download(self, offset, count):
        posts = []
        try:
            response = self._api.wall.get(owner_id=self._owner_id, offset=offset, count=count)
            for post in response['items']:
                id = post['id']
                date = post['date']
                likes = post['likes']['count']
                reposts = post['reposts']['count']
                views = post['views']['count'] if 'views' in post else -1
                posts.append(WallPost(id, date, likes, reposts, views))
        except Exception as e:
            print(e, file=sys.stderr)
            
        return posts
            
            
    def download_all(self):
        offset = 0
        while True:
            posts = self._download(offset, posts_count)
            if len(posts) == 0:
                break
            for post in posts:
                yield post
            offset += len(posts)
             
             
    def update(self, timedelta):
        stamp = (datetime.utcnow() - timedelta).timestamp()
        for post in self.download_all():
            if post.date < stamp:
                break
            yield post
