"""
Chess board
Starting work on a ComputerPlayer!
Sucks in other ways too
"""

import json
import sys
import random

## response = '{"clock":{"w":300,"b":300},"pgn":"","fen":"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1","turn":"w","result":"*","color":"w"}'
## rr = json.loads(response)
## rr
#. {u'turn': u'w', u'pgn': u'', u'clock': {u'b': 300, u'w': 300}, u'fen': u'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', u'result': u'*', u'color': u'w'}
## rr['clock']
#. {u'b': 300, u'w': 300}
## rr['turn']
#. u'w'
## print str(parse_FEN(rr['fen']))
#. (True, True)
#. rnbqkbnr
#. pppppppp
#.         
#.         
#.         
#.         
#. PPPPPPPP
#. RNBQKBNR
#. (True, True)

## b = InitialChessBoard()
## b.mover
#. 'white'
## b.castling
#. ((True, True), (True, True))
## print str(b)
#. (True, True)
#. rnbqkbnr
#. pppppppp
#.         
#.         
#.         
#.         
#. PPPPPPPP
#. RNBQKBNR
#. (True, True)
## pw = HumanPlayer(white)
## pb = HumanPlayer(black)
## b.outcome
## ' '.join(sorted(map(str, b.get_moves())))
#. 'a2a3 a2a4 b1a3 b1c3 b2b3 b2b4 c2c3 c2c4 d2d3 d2d4 e2e3 e2e4 f2f3 f2f4 g1f3 g1h3 g2g3 g2g4 h2h3 h2h4 resign'
## m = b.parse_move('resign')
## b1 = m.update(b)
## b1.outcome
#. 'black'

## fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
## b2 = parse_FEN(fen)
## b2.mover
#. 'white'
## b2.castling
#. ((True, True), (True, True))
## print str(b2)
#. (True, True)
#. rnbqkbnr
#. pppppppp
#.         
#.         
#.         
#.         
#. PPPPPPPP
#. RNBQKBNR
#. (True, True)

def parse_FEN(fen):
    placement, to_move, castling, en_passant_target, halfmove_clock, fullmove_clock = fen.split()
    squares = []
    for row in placement.split('/'):
        s = ''
        for p in row:
            if p.isdigit():
                s += ' ' * int(p)
            else:
                s += p
        squares.append(s)
    mover = {'w': 'white', 'b': 'black'}[to_move]
    if castling == '-':
        castling = ((False, False), (False, False))
    else:
        castling = (('k' in castling, 'q' in castling),
                    ('K' in castling, 'Q' in castling))
    en_passant = None if en_passant_target == '-' else parse_coords(en_passant_target)
    return ChessBoard(mover, surround(squares), castling, en_passant, None)

def surround(rows):
    return ['----------'] + ['-%s-' % row for row in rows] + ['----------']

def main(argv):
    print "(Moves look like 'e2e3')"
    strategy_names = {'human': HumanPlayer, 'greedy': GreedyComputerPlayer, 'random': RandomComputerPlayer}
    play_chess(strategy_names[argv[1]], strategy_names[argv[2]])

def play_chess(white_strategy, black_strategy):
    return play(InitialChessBoard(), [white_strategy, black_strategy])

def play(board, strategies):
    players = [strategy(side)
               for strategy, side in zip(strategies, board.get_sides())]
    while board.get_outcome() is None:
        board = board.play_turn(players)
    for player in players:
        player.on_game_over(board)

class HumanPlayer:

    def __init__(self, side):
        self.side = side

    def pick_move(self, board):
        board.show()
        while True:
            string = raw_input('%s, your move? ' % self.side.capitalize())
            try:
                move = board.parse_move(string)
            except MoveIllegal:
                print 'Illegal move.'
            else:
                return move

    def on_game_over(self, board):
        board.show()
        if board.get_outcome() is None:
            pass
        elif board.get_outcome() == self.side:
            print '%s, you win!' % self.side.capitalize()
        elif board.get_outcome() == 'draw':
            print 'You draw.'
        else: print '%s, you lose!' % self.side.capitalize()

def greedy_evaluate(board, side):
    board_string = "".join(board.squares)
    white_count = sum(1 for piece in board_string if piece.isupper())
    black_count = sum(1 for piece in board_string if piece.islower())
    if side == "white":
        piece_count_score = white_count - black_count
    else:
        piece_count_score = black_count - white_count

    mobility_score = 0

    return piece_count_score + mobility_score

class ComputerPlayer:
    def __init__(self, side):
        self.side = side

    def on_game_over(self, board):
        board.show()
        if board.get_outcome() is None:
            pass
        elif board.get_outcome() == self.side:
            print '%s, you win!' % self.side.capitalize()
        elif board.get_outcome() == 'draw':
            print 'You draw.'
        else:
            print '%s, you lose!' % self.side.capitalize()

class GreedyComputerPlayer(ComputerPlayer):
    def pick_move(self, board):
        board.show()
        possible_moves = board.get_moves()
        possible_moves.remove(ResignMove())
        best_move = max(possible_moves, key=lambda move: greedy_evaluate(move.update(board), self.side))
        return best_move

class RandomComputerPlayer(ComputerPlayer):
    def pick_move(self, board):
        board.show()
        possible_moves = board.get_moves()
        possible_moves.remove(ResignMove())
        return random.choice(possible_moves)

def InitialChessBoard():
    squares = ['----------',
               '-rnbqkbnr-',
               '-pppppppp-',
               '-        -',
               '-        -',
               '-        -',
               '-        -',
               '-PPPPPPPP-',
               '-RNBQKBNR-',
               '----------',]
    return ChessBoard(white, squares, ((True, True), (True, True)), None, None)

class MoveIllegal(Exception):
    pass

class ChessBoard:

    def __init__(self, mover, squares, castling, en_passant_target, outcome):
        self.mover = mover
        self.squares = squares
        self.castling = castling
        self.en_passant_target = en_passant_target
        self.outcome = outcome

    def __str__(self):
        def addSpace(line):
            return " ".join(line)
        def addDots(line):
            return line.replace(" ", ".")

        return ('\n'.join(str(8-i)+"  "+addSpace(addDots(line[1:-1])) for i, line in enumerate(self.squares[1:-1]))
                + '\n\n' +  "   a b c d e f g h")

    def check(self, side):
        """ check if a particular player is in check """
        if side == 'white':
            king = 'K'
        else: king = 'k'
        
        possible_boards = [move.update(self) for move in self.get_piece_moves()]
        for board in possible_boards:
            if king not in "".join(board.squares):
                return True
        return False

    def checkmate(self):
        """ check if the person about to move is in checkmate """
        possible_boards = [move.update(self) for move in self.get_piece_moves()]
        for board in possible_boards:
            if not board.check(self.mover):
                return False
        return True

    def get_outcome(self):
        "Return None, 'draw', black, or white (meaning the winner)."
        if self.outcome == None:
            if self.checkmate():
                return opponent(self.mover)
            if len(self.get_piece_moves()) == 0:
                return 'draw'
        return self.outcome

    def resign(self):
        return ChessBoard(opponent(self.mover),
                          self.squares,
                          self.castling,
                          None,
                          opponent(self.mover))

    def move_piece(self, (r0, c0), (r1, c1), en_passant_target=None):
        squares = list(map(list, self.squares))
        piece = squares[r0][c0]
        squares[r0][c0] = ' '
        squares[r1][c1] = piece

        # Update castling status if necessary
        castling = self.castling
        if piece.upper() == 'K':
            castling = list(castling)
            castling[self.mover == white] = (False, False)
            castling = tuple(castling)
        elif piece.upper() == 'R':
            cm = castling[self.mover == white]
            if cm[0] or cm[1]:
                start_rank = 8 if self.mover == white else 1
                if r0 == start_rank:
                    queenside = (c0 == 1)
                    if cm[queenside]:
                        castling = list(map(list, castling))
                        castling[self.mover == white][queenside] = False
                        castling = tuple(map(tuple, castling))

        return ChessBoard(opponent(self.mover),
                          list(map(''.join, squares)),
                          castling,
                          en_passant_target,
                          None)

    def move_en_passant(self, (r0, c0), (r1, c1)):
        squares = list(map(list, self.squares))
        piece = squares[r0][c0]
        squares[r0][c0] = ' '   # moving from here...
        squares[r0][c1] = ' '   # (capturing this pawn)
        squares[r1][c1] = piece # ... to there.
        return ChessBoard(opponent(self.mover),
                          list(map(''.join, squares)),
                          self.castling,
                          None,
                          None)

    def move_promoting(self, (r0, c0), (r1, c1)):
        # XXX support promotions besides to queen 
        squares = list(map(list, self.squares))
        squares[r0][c0] = ' '
        squares[r1][c1] = 'Q' if self.mover == 'white' else 'q'
        return ChessBoard(opponent(self.mover),
                          list(map(''.join, squares)),
                          self.castling,
                          None,
                          None)

    def castle(self, (r0, c0), (r1, c1)):
        squares = list(map(list, self.squares))
        piece = squares[r0][c0]
        squares[r0][c0] = ' '
        squares[r1][c1] = piece
        rook_c = 8 if c1 == 7 else 1
        squares[r1][(c0+c1)//2] = squares[r1][rook_c]
        squares[r1][rook_c] = ' '

        castling = list(self.castling)
        castling[self.mover == white] = (False, False)
        castling = tuple(castling)

        return ChessBoard(opponent(self.mover),
                          list(map(''.join, squares)),
                          castling,
                          None,
                          None)

    def show(self):
        print self

    def get_sides(self):
        return (white, black)

    def play_turn(self, (white_player, black_player)):
        player = white_player if self.mover == white else black_player
        move = player.pick_move(self)
        if move in self.get_moves():
            return move.update(self)
        raise Exception("Bad move")

    def parse_move(self, string):
        for move in self.get_moves():
            if move.matches(string):
                return move
        raise MoveIllegal()

    def get_moves(self):
        return [ResignMove()] + self.get_piece_moves()

    def get_piece_moves(self):
        return sum(map(self.moves_from, self.army(self.mover)), [])

    def army(self, player):
        for r, row in enumerate(self.squares):
            for c, piece in enumerate(row):
                if piece.isalpha() and piece.isupper() == (player == white):
                    yield r, c

    def moves_from(self, pos):
        return list(self.gen_moves_from(pos))

    def gen_moves_from(self, (r, c)):
        piece = self.squares[r][c]
        piece, is_white = piece.upper(), piece.isupper()

        def is_takeable(r1, c1):
            return is_empty(r1, c1) or has_opponent(r1, c1)

        def is_empty(r1, c1):
            return self.squares[r1][c1] == ' '

        def has_opponent(r1, c1):
            there = self.squares[r1][c1]
            return there.isalpha() and there.isupper() != is_white

        def move_to(r1, c1):
            return PieceMove((r, c), (r1, c1))

        def pawn_move(r1, c1, en_passant_target=None):
            back_rank = 1 if is_white else 8
            if r1 == back_rank:
                return PawnPromotion((r, c), (r1, c1))
            else:
                return PieceMove((r, c), (r1, c1), en_passant_target)

        def move_freely(dirs):
            for dr, dc in dirs:
                for i in range(1, 9):
                    if is_empty(r+dr*i, c+dc*i):
                        yield pawn_move(r+dr*i, c+dc*i)
                    else:
                        if has_opponent(r+dr*i, c+dc*i):
                            yield pawn_move(r+dr*i, c+dc*i)
                        break

        if piece in ' -':
            pass
        elif piece == 'P':
            forward = -1 if is_white else 1
            if is_empty(r+forward, c):
                yield move_to(r+forward, c)
                if r == (7 if is_white else 2): # initial 2 steps
                    if is_empty(r+forward*2, c):
                        yield pawn_move(r+forward*2, c, en_passant_target=(r+forward, c))
            if has_opponent(r+forward, c-1): yield move_to(r+forward, c-1)
            if has_opponent(r+forward, c+1): yield move_to(r+forward, c+1)
            if self.en_passant_target:
                er, ec = self.en_passant_target
                if er == r+forward and abs(ec-c) == 1:
                    yield EnPassantCapture((r, c), (er, ec))
        elif piece == 'K':
            # TODO forbid moving into check
            # (and this can apply to moves of other pieces)
            for dr, dc in queen_dirs:
                if is_takeable(r+dr, c+dc):
                    yield move_to(r+dr, c+dc)
            if self.castling[is_white][0]: # King's side
                if self.squares[r][6:8].isspace():
                    yield CastlingMove((r, c), (r, 7))
            if self.castling[is_white][1]: # Queen's side
                if self.squares[r][2:5].isspace():
                    yield CastlingMove((r, c), (r, 3))
        elif piece == 'Q':
            for move in move_freely(queen_dirs):  yield move
        elif piece == 'R':
            for move in move_freely(rook_dirs):   yield move
        elif piece == 'B':
            for move in move_freely(bishop_dirs): yield move
        elif piece == 'N':
            for dr, dc in knight_jumps:
                if 1 <= r+dr <= 8 and 1 <= c+dc <= 8:
                    if is_takeable(r+dr, c+dc):
                        yield move_to(r+dr, c+dc)
        else:
            assert False

rook_dirs   = [( 0, 1), ( 0,-1), ( 1, 0), (-1, 0)]
bishop_dirs = [(-1,-1), (-1, 1), ( 1,-1), ( 1, 1)]
queen_dirs  = rook_dirs + bishop_dirs

knight_jumps = [( 2, 1), ( 2,-1), ( 1, 2), ( 1,-2),
                (-2, 1), (-2,-1), (-1, 2), (-1,-2)]

white, black = 'white', 'black'

def opponent(side):
    return black if side == white else white

class ResignMove:
    def __eq__(self, other):
        return isinstance(other, ResignMove)
    def update(self, board):
        return board.resign()
    def matches(self, string):
        return string.lower() == str(self)
    def __str__(self):
        return 'resign'

class PieceMove:
    def __init__(self, from_pos, to_pos, en_passant_target=None):
        self.from_pos = from_pos
        self.to_pos   = to_pos
        self.en_passant_target = en_passant_target
    def __eq__(self, other):
        return (isinstance(other, PieceMove)
                and self.from_pos == other.from_pos
                and self.to_pos == other.to_pos
                and self.en_passant_target == other.en_passant_target)
    def update(self, board):
        return board.move_piece(self.from_pos, self.to_pos, self.en_passant_target)
    def matches(self, string):
        return string.lower() == str(self)
    def __str__(self):
        fr, fc = self.from_pos
        tr, tc = self.to_pos
        return '%s%d%s%d' % ('abcdefgh'[fc-1], 9-fr,
                             'abcdefgh'[tc-1], 9-tr)

def parse_coords(s):
    assert len(s) == 2
    c = 1 + 'abcdefgh'.index(s[0])
    r = int(s[1])
    assert 1 <= r <= 8
    return r, c

class CastlingMove(PieceMove):
    def update(self, board):
        return board.castle(self.from_pos, self.to_pos)
    def __str__(self):
        if self.to_pos[1] == 3: return 'o-o-o'
        if self.to_pos[1] == 7: return 'o-o'
        assert False

class EnPassantCapture(PieceMove):
    # XXX might need special parsing/unparsing
    def update(self, board):
        return board.move_en_passant(self.from_pos, self.to_pos)

class PawnPromotion(PieceMove):
    # XXX might need special parsing/unparsing
    def update(self, board):
        return board.move_promoting(self.from_pos, self.to_pos)

if __name__ == '__main__':
    main(sys.argv)
