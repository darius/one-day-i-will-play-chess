"""
Interact with the NGW chess server.
https://community.recurse.com/t/ngw-chess-ai-tournament/1724
"""

import requests, sys, time

from chack import *

stem = 'http://52.200.188.234:3000/test/'

def main(argv):
    assert len(argv) == 4
    game = argv[1]
    strategy = argv[2]
    color = argv[3]
    url = stem + game

    while True:
        r = requests.get(url)
        if r.status_code != 200:
            print 'oh noes', r
            time.sleep(1)
            continue
        try:
            js = r.json()
        except ValueError as e:
            print 'oh the horror', e
            time.sleep(10)
            continue
        turn = js['turn']
        if turn != color:
            print 'waiting'
            time.sleep(1)
            continue
        board = parse_FEN(js['fen'])
        


def testme(argv):
    url = stem + '4'

    r = requests.get(url)
    print r.status_code
    print r.json()

    r = requests.post('%s?move=%s' % (url, 'e4'))
    print r.status_code
    print r.json()

if __name__ == '__main__':
    testme(sys.argv)
