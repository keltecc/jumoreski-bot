import re
import sys
import sqlite3
from config import db, table, max_top_size


class MessageProcessor():

    def __init__(self):
        self._jumoreska_pattern = re.compile('^юм[0оа]рес([ао0][ч4])?ка(\s+за\s+(\d+))?$')
        self._top_pattern = re.compile('^топ\s+(\d+)\s+по\s+(лайкам|рейтингу)$')
        self._wall_post_mask = 'wall-92876084_%d'
        self._help = '\n'.join([
            'инструкция - написать это сообщение',
            'юмореска - прислать случайную (рандомную) юмореску',
            'юмореска за X - прислать юмореску, у которой не меньше X лайков',
            'топ X по лайкам - показать первые X юморесок, у которых больше всего лайков',
            'топ X по рейтингу - показать первые X юморесок с самым большим рейтингом (beta)',
            '',
            'P.S. Формула рейтинга: rating = (likes/views + 0.5*reposts/likes) * 100'
        ])
        self._recalculate()
        
        
    def _make_query(self, query):
        try:
            connection = sqlite3.connect(db)
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            connection.close()
            return result
        except Exception as e:
            print(e, file=sys.stderr)
            
            
    def _extract_top(self, type_):
        return self._make_query(
            'SELECT id, %s FROM %s ORDER BY %s DESC LIMIT %d' % (type_, table, type_, max_top_size)
        )
        
        
    def _recalculate(self):
        self._rating_top = self._extract_top('rating')
        self._likes_top = self._extract_top('likes')
        
        
    def _build_top(self, top, limit, header, title):
        text = [header % limit]
        number = 1
        for id, value in top[:limit]:
            text.append(title % (number, value))
            text.append('https://vk.com/' + self._wall_post_mask % id)
            text.append('')
            number += 1
        return {'message': '\n'.join(text)}
        
        
    def _get_likes_top(self, limit):
        return self._build_top(
            self._likes_top, 
            limit, 
            'Первые %d по лайкам:', 
            '%d: лайки = %d'
        )
        
        
    def _get_rating_top(self, limit):
        return self._build_top(
            self._rating_top, 
            limit, 
            'Первые %d по рейтингу:', 
            '%d: рейтинг = %.4f'
        )
        
        
    def _get_jumoreska(self, likes):
        id = self._make_query(
            'SELECT id FROM %s WHERE likes >= %d ORDER BY RANDOM() LIMIT 1' % (table, likes)
        )
        if len(id) > 0:
            return {'attachment': self._wall_post_mask % id[0][0]}
        return {'message': 'Нет такой юморески.'}
        
        
    def process(self, text):
        match_jumoreska = self._jumoreska_pattern.match(text)
        match_top = self._top_pattern.match(text)
        if match_jumoreska:
            likes = int(match_jumoreska.group(3) or 0)
            return self._get_jumoreska(likes)
        if match_top:
            count, type_ = int(match_top.group(1)), match_top.group(2)
            if not 0 < count <= max_top_size:
                return {'message': 'Я могу показать не больше %d.' % max_top_size}
            if type_ == 'рейтингу':
                return self._get_rating_top(count)
            if type_ == 'лайкам':
                return self._get_likes_top(count)
            return {'message': 'А нет такого топа!'}
        if text == 'инструкция':
            return {'message': self._help}
        return {'message': 'Я не знаю это. Да. Так что пиши "инструкция", чтобы узнать команды.'}
        
        
    def update(self):
        self._recalculate()
