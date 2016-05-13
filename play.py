"""
Interact with the NGW chess server.
https://community.recurse.com/t/ngw-chess-ai-tournament/1724
"""

import requests, sys, time

from chack import *

stem = 'http://52.200.188.234:3000/'

def main(argv):
    assert len(argv) == 3
    game = argv[1]
    strategy = argv[2]
    url = stem + game

    while True:
        print "it's", time.asctime()
        print 'GET', url
        r = requests.get(url)
        if r.status_code != 200:
            print 'oh noes', r
            time.sleep(10)
            continue
        print 'response:'
        print '  ', r.text
        try:
            js = r.json()
        except ValueError as e:
            print 'oh the horror', e
            time.sleep(10)
            continue

        color = js['color']
        side = {'w': 'white', 'b': 'black'}[color]
        player = strategy_names[strategy](side)

        turn = js['turn']
        if turn != color:
            print 'waiting'
            time.sleep(0.2)
            continue

        board = parse_FEN(js['fen'])
#        print board
        move = player.pick_move(board)
        print 'playing', move, 'yielding'
        print move.update(board)

        print 'POST', url + '?move=%s' % move
        r = requests.post(url + '?move=%s' % move)
        print 'response', r.status_code, r.text
        if r.status_code != 200:
            print 'OH NOES', r
            return
        
        time.sleep(0.2)

def testme(argv):
    url = stem + '4'

    r = requests.get(url)
    print r.status_code
    print r.json()

    r = requests.post('%s?move=%s' % (url, 'e4'))
    print r.status_code
    print r.json()

if __name__ == '__main__':
    main(sys.argv)
