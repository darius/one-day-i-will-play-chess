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

def parse_FEN(fen):
    placement, to_move, castling, en_passant_target, halfmove_clock, fullmove_clock = fen.split()
    print 'FEN from server:'
    print ' placement', placement
    print ' to_move', to_move
    print ' castling', castling
    print ' en_passant', en_passant_target
    print ' halfmove_clock', halfmove_clock
    print ' fullmove_clock', fullmove_clock

    squares = [''.join(' ' * int(p) if p.isdigit() else p
                       for p in row)
               for row in placement.split('/')]
    mover = {'w': 'white', 'b': 'black'}[to_move]
    castling = (('k' in castling, 'q' in castling),
                ('K' in castling, 'Q' in castling))
    en_passant = None if en_passant_target == '-' else parse_coords(en_passant_target)
    return ChessBoard(mover, surround(squares), castling, en_passant, None)

def surround(rows):
    return ['----------'] + ['-%s-' % row for row in rows] + ['----------']

def parse_coords(s):
    assert len(s) == 2
    c = 1 + 'abcdefgh'.index(s[0])
    r = int(s[1])
    assert 1 <= r <= 8
    return r, c

if __name__ == '__main__':
    main(sys.argv)
