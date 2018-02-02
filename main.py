from bot import Bot
from os.path import exists
from time import time, sleep
from datetime import datetime
from update import make_update
from argparse import ArgumentParser
from config import bot_timeout, update_period


def build_parser():
    parser = ArgumentParser()
    parser.add_argument('-f', '--force', action='store_true', help='force update database')
    parser.add_argument('-v', '--verbose', action='store_true', help='be verbose')
    return parser
    
    
def verbose_update(all, verbose):
    type_ = 'DEEP' if all else 'FAST'
    if verbose:
        print('%s %s UPDATE STARTED' % (datetime.now(), type_))
    make_update(all)
    if verbose:
        print('%s %s UPDATE FINISHED' % (datetime.now(), type_))
    

def main():
    args = build_parser().parse_args()
    if args.force:
        verbose_update(True, args.verbose)
    bot = Bot(args.verbose)
    previous = time()
    while True:
        bot.answer()
        sleep(bot_timeout)
        if (time() - previous) / 60 > update_period:
            verbose_update(False, args.verbose)
            bot.update()
            previous = time()
        
        
if __name__ == '__main__':
    main()
