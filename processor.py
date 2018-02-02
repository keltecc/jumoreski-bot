import re


class MessageProcessor():

    def __init__(self):
        self._keyword = re.compile('^((йу|ю)м[оа]р+е[сз](ка|о[ч4]ка))\s+за\s+(\d+)$')
        
        
    def process(self, text):
        # echo
        return {'message': text}
        