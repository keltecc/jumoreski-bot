import os
import sys
import vk_requests as vk
from time import sleep
from processor import MessageProcessor
from config import api_version, bot_timeout, dialogs_count

from tokens import community_token


class Message():
    
    def __init__(self, id, text, user_id):
        self.id = id
        self.text = text
        self.user_id = user_id
        

class Bot():
    
    def __init__(self):
        try:
            self._api = vk.create_api(service_token=community_token, api_version=api_version)
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit(1)
        self._processor = MessageProcessor()
        
    
    def answer(self):
        try:
            dialogs = self._api.messages.getDialogs(unread=True, count=dialogs_count)['items']
            for dialog in dialogs:
                info = dialog['message']
                message = Message(info['id'], info['body'], info['user_id'])
                self._api.messages.markAsRead(message_ids=message.id, peer_id=message.user_id)
                if message.text != '':
                    kwargs_ = self._processor.process(message.text)
                    self._api.messages.send(peer_id=message.user_id, **kwargs_)
        except Exception as e:
            print(e, file=sys.stderr)
            
            
if __name__ == '__main__':
    bot = Bot()
    while True:
        bot.answer()
        sleep(bot_timeout)
