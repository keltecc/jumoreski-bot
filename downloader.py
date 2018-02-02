import vk_requests as vk
from time import time, sleep
from datetime import datetime


API_VERSION = '5.71'


class WallPost():

    def __init__(self, id, date, likes, reposts, views):
        self.id = id
        self.date = date
        self.likes = likes
        self.reposts = reposts
        self.views = views
        
        
    def combine(self):
        return self.id, self.date, self.likes, self.reposts, self.views
        

class WallDownloader():

    def __init__(self, service_token, domain):
        self._api = vk.create_api(service_token=service_token, api_version=API_VERSION)
        domain_info = self._api.utils.resolveScreenName(screen_name=domain)
        self._owner_id = domain_info['object_id']
        if domain_info['type'] == 'group':
            self._owner_id *= -1
        
        
    def _download(self, offset, count):
        response = self._api.wall.get(owner_id=self._owner_id, offset=offset, count=count)
        posts = []
        for post in response['items']:
            id = post['id']
            date = post['date']
            likes = post['likes']['count']
            reposts = post['reposts']['count']
            views = post['views']['count'] if 'views' in post else -1
            posts.append(WallPost(id, date, likes, reposts, views))
        return posts
            
            
    def download_all(self):
        offset, count = 0, 100
        sleeping_time = 1/3
        while True:
            posts = self._download(offset, count)
            previous = time()
            if len(posts) == 0:
                break
            for post in posts:
                yield post
            offset += count
            delta = sleeping_time - (time() - previous)
            if delta > 0:
                sleep(delta)
             
             
    def update(self, timedelta):
        stamp = (datetime.utcnow() - timedelta).timestamp()
        for post in self.download_all():
            if post.date < stamp:
                break
            yield post
